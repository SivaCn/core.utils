# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

"""


# ----------- START: Native Imports ---------- #
import time
import traceback
import simplejson as json

from typing import Optional
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import pika
# ----------- END: Third Party Imports ---------- #

# ----------- START: in App Imports ---------- #
from core.utils.constants import (
    const_consumer,
    const_scheduler,
)

from core.utils.helpers.utils import (
    json_serialize
)

from core.utils.helpers.environ import (
    get_build_config,
)
# ----------- END: in App Imports ---------- #


__all__ = [
    # Public Symbols
]


class RabbitMQ:

    RMQ_DETAILS = get_build_config(section='rabbitmq')

    def __init__(self,
                 timeout: Optional[int] = 0,
                 reconnect_time: Optional[int] = const_consumer.RECONNECT_TIME_SECS,
                 reconnect_attempt: Optional[int] = const_consumer.RECONNECT_ATTEMPT):

        """Rabbit MQ's RPC technique wherein we will wait for a response on a
        dedicated queue.

        Args:
            timeout (int): a positive integer represented in seconds,
                           0 is defaulted to specify the endless wait.
            reconnect_time (int): waiting time in secs between retry attempts
            reconnect_attempt (int): number of retry attempts

        """

        if not isinstance(timeout, int):
            _msg = "argument timeout should be of type int, Got {}"
            raise Exception(_msg.format(type(timeout)))

        if timeout < 0:
            _msg = "argument timeout should be greater than or equal to zero, Got {}"
            raise Exception(_msg.format(timeout))

        self.host = self.RMQ_DETAILS.host
        self.port = self.RMQ_DETAILS.port
        self.virtual_host = self.RMQ_DETAILS.virtual_host
        self.username = self.RMQ_DETAILS.username
        self.password = self.RMQ_DETAILS.password

        self.timeout = timeout
        self.reconnect_time = reconnect_time
        self.reconnect_attempt = reconnect_attempt

        self.is_reconnected = None

        self.connection = None
        self.channel = None

    def create_connection(self):
        """
        Private method to establish connection to rabbit mq and enable timeout
        """
        pika_connection_params = {
            'host': self.host,
            'port': self.port,
            'virtual_host': self.virtual_host,
            'socket_timeout': const_consumer.PIKA_SOCKET_CONNECTION_TIMEOUT
        }

        # passing credentials as one of the parameter to pika
        # in-order to establish the MQ connection
        if self.username and self.password:
            pika_connection_params.update({'credentials': pika.PlainCredentials(self.username, self.password)})

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(**pika_connection_params)
        )

        if self.timeout > 0:
            #
            # INFO: the ``self.on_timeout`` method will be defined in the childern class,
            #       which extends class ``RabbitMQ``
            self.connection.call_later(self.timeout, self.on_timeout)

    def create_channel(self):

        if not self.connection:
            self.create_connection()

        if not self.channel:
            self.channel = self.connection.channel()


class RabbitMQPublisher(RabbitMQ):

    """
    """

    def __init__(self, timeout: Optional[int] = 0):
        super().__init__(timeout=timeout)

    def publish(self,
                payload: dict | str,
                routing_key: str,
                fail_try_attempts: Optional[int] = 3,
                **properties):

        properties = {
            'content_type': 'application/json',
            'delivery_mode': pika.DeliveryMode.Transient,
            **properties
        }

        self.create_channel()
        self.channel.confirm_delivery()

        message_body = payload if isinstance(payload, str) else json_serialize(payload)

        error_msg = None
        for fail_try in range(fail_try_attempts):

            try:
                self.channel.basic_publish(
                    exchange=const_consumer.YELLOW_EXCHAMGE,
                    routing_key=routing_key,
                    body=message_body,
                    properties=pika.BasicProperties(**properties),
                    mandatory=True,
                )

                break

            except pika.exceptions.UnroutableError as error:
                error_msg = str(error)

        else:
            raise Exception(
                f"Unable to publish to RabbitMQ, with routing_key: '{routing_key}'. Encountered Error: {error_msg}"
            )

        return True


class RabbitMQRemoteProcedure(RabbitMQ):

    """
    RabbitMQ's RPC will work like this:

        When the Client starts up, it creates an anonymous exclusive callback queue.

        For an RPC request, the Client sends a message with two properties:
        reply_to, which is set to the callback queue and correlation_id, which is set
        to a unique value for every request.  The request is sent to an rpc_queue
        queue.

        The RPC worker (aka: server) is waiting for requests on that queue. When a
        request appears, it does the job and sends a message with the result back to
        the Client, using the queue from the reply_to field.

        The client waits for data on the callback queue. When a message appears, it
        checks the correlation_id property. If it matches the value from the request it
        returns the response to the application.

    """

    def __init__(self, timeout=const_consumer.RPC_DEFAULT_TIMEOUT_SECS):

        self.response = dict()
        self.got_response = False

        super().__init__(timeout=timeout)

    def create_rpc_channel(self, reconnect=False):
        """
        Method to create channel and bind the queue to newly created channel

        Args:
            reconnect (bool): Flag specifying wheater the request is from reconnect or not

        """
        if reconnect:

            #
            # Attempt to close the persistent Connection and channel.
            # This is required to avoid creating the unused TCP/IP connections on every reconnect.

            #
            # Queue should be retained
            self.close(queue_delete=False)

        self.create_channel()

        if not getattr(self, 'callback_queue', None):

            self.callback_queue = self.channel.queue_declare(
                queue='', durable=True
            ).method.queue

        self.channel.queue_bind(exchange=const_consumer.YELLOW_EXCHAMGE, queue=self.callback_queue)

        #
        # No Auto acknowdgement to be done here, while waiting on the reply_to queue.
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            #
            # Do not allow more than one consumer to this callback queue
            exclusive=True
        )

    def reconnect(self):
        """
        Method to reconnect to rabbit mq
        """
        for trial in range(int(self.reconnect_attempt)):

            time.sleep(int(self.reconnect_time))

            try:
                self.create_rpc_channel(reconnect=True)
            except (pika.exceptions.AMQPConnectionError,
                    pika.exceptions.ConnectionClosed,
                    pika.exceptions.ChannelClosed):

                continue

            else:
                self.is_reconnected = True
                break
        else:
            self.is_reconnected = False

    def consume(self):

        while not self.got_response:

            try:
                self.channel.connection.process_data_events(time_limit=const_consumer.DATA_EVENTS_TIME_LIMIT)

            except (pika.exceptions.AMQPConnectionError,
                    pika.exceptions.ConnectionClosed,
                    pika.exceptions.ChannelClosed) as error:

                self.reconnect()

                # break the loop if reconnect fails
                if not self.is_reconnected:

                    break

        self.close()

        return self.response

    def on_response(self, ch, method, props, body):
        """
        A call back method.
        """
        response = json.loads(body)

        #
        # Acknowdge the message on successful consumption
        ch.basic_ack(delivery_tag=method.delivery_tag)

        if getattr(self, 'consume', None):
            self.got_response = True

        self.response = {
            'code': 200,
            'message': 'Successfully completed the RabbitMQ RPC',
            **response
        }

    def on_timeout(self):
        """
        Method triggering timeout response
        """

        if getattr(self, 'consume', None):
            self.got_response = True

        self.response = {
            'code': 320,
            'message': 'Encountered timeout, while waiting for the response',
        }

    def close(self, queue_delete=True):
        """
        Method uses to close the connection and channel.

        Args:
            queue_delete (bool): Boolean flag inform wheater to delete the queue or not.

        """

        try:
            if queue_delete:
                self.channel.queue_delete(queue=self.callback_queue)

            self.channel.close()
            self.connection.close()

        except Exception as error:
            pass


def communicate_scheduler(payload):
    """
    Enables Rabbit MQ RPC by starting consumer with given timeout

    """

    rpc_obj = RabbitMQRemoteProcedure()

    rpc_obj.create_rpc_channel()

    try:

        publisher = RabbitMQPublisher()

        _ = publisher.publish(
            payload,
            routing_key=const_scheduler.SCHEDULER_QUEUE_NAME,
            reply_to=rpc_obj.callback_queue,
            correlation_id='request_id'  # TODO
        )

    except Exception:

        #
        # Close the RPC channel as it's not going to be used
        rpc_obj.close(queue_delete=True)

        raise

    result = None
    try:
        result = rpc_obj.consume()

    finally:
        rpc_obj.close(queue_delete=True)

    return result

