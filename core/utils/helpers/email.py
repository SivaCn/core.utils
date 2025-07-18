# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os
import time
import traceback

from typing import Optional, List, Any
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import mandrill
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.error import BadArgumentError

from core.utils.helpers.environ import (
    get_build_config,
)
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


email_config = get_build_config(section='email-config')
yellow_config = get_build_config(section='yellow-config')


class EmailRecipientType:
    email: str
    name: Optional[str] = None


class Mandrill:

    def __init__(self):
        """Initialize the Mandrill client with rate limit tracking"""

        self.pause_time = 0.25
        self.retry_after = 0.25

        # Initialize Mandrill client
        self.client = mandrill.Mandrill(os.getenv('MANDRILL_API_KEY'))

    def send_email(
            self,
            recipients: List[EmailRecipientType],
            subject: str,
            html_content: Optional[str] = None,
            text_content: Optional[str] = None,
            tags: Optional[List[str]] = None) -> dict[str, Any]:

        if not html_content and not text_content:
            raise BadArgumentError(
                'Argument either html_content or text_content should be supplied, Got None'
            )

        recipients_detail = [
            {
                'type': 'to',
                'email': recipient['email'],
                'name': recipient['name'] or '',
            }
            for recipient in recipients
        ]

        result = {
            'log': list(),
            'response': None,
            'status': False
        }

        for attempt in range(int(email_config.fail_try_attempts)):

            # Send email through Mandrill
            message = {
                'html': html_content,
                'text': text_content,
                'subject': subject,
                'from_email': email_config.sender_email_id,
                'from_name': yellow_config.org_name,
                'to': recipients_detail,
                'important': True,
                'track_opens': True,
                'track_clicks': True,
                'tags': tags or list(),
                'metadata': {
                    'website': yellow_config.org_website
                }
            }

            try:
                # Send the message
                response = self.client.messages.send(message=message)
                '''
                >>> self.client.messages.send(message=message)
                [{'email': 'siva@getyellow.in',
                  'status': 'sent',
                  '_id': '8e5b579530c84724997119f8296a1bd8',
                  'reject_reason': None,
                  'queued_reason': None}]
                '''

                result['response'] = response

                time.sleep(self.pause_time)

                # #
                # # Get message status
                # result['info'] = self.client.messages.info(id=response[0]['_id'])

                result['status'] = True

                #
                # Skip re-attempt when succeeded
                break

            except Exception as error:

                result['status'] = False

                error_class = error.__class__.__name__

                result['log'].append(f"Attempt: {attempt}, failed. {error_class}: {error}")

                if error_class == 'InvalidKeyError':
                    return result

                if attempt < int(email_config.fail_try_attempts):
                    time.sleep(self.retry_after)

                    #
                    # Set exponential wait time before the next attempt
                    self.retry_after = self.retry_after * 2

                    continue

        return result


def get_email_client():

    EmailClient = {
        'mandrill': Mandrill,
    }['mandrill']

    return EmailClient()

