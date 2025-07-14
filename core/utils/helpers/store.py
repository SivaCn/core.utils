# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
from io import BytesIO

from typing import Any, Optional
from abc import ABC, ABCMeta, abstractmethod
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import redis

import simplejson as json

from pandas import read_csv, DataFrame
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import (
    const_cloud,
    const_general,
)

from core.utils.helpers.utils import (
    encoded_uuid,
    json_custom_serializer
)

from core.utils.helpers.environ import (
    get_build_config,
)
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class IntermediateInterface(metaclass=ABCMeta):

    """An Abstract Base class for the Intermediate Store Interface.

    Any class which extends ``IntermediateInterface`` should implement the below methods
        * connect
        * set
        * get
        * __enter__
        * __exit__

    Where __enter__ and __exit__ are used as context managers

    """

    def __init__(self):
        self.conn = None
        self.is_connected = False

    def serialize(self, py_data):
        return json.dumps(py_data, default=json_custom_serializer)

    def deserialize(self, data_buff):
        return json.loads(data_buff)

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def set(self, key, data):
        raise NotImplementedError()

    @abstractmethod
    def get(self, key):
        raise NotImplementedError()

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abstractmethod
    def __exit__(self, *args, **kwargs):
        raise NotImplementedError()


class RedisStore(IntermediateInterface):

    """A derived class from ``IntermediateInterface`` for the Redis Server
    """

    def connect(self):

        """A method which establishes the connection to the Redis Server
        """

        if self.is_connected:
            #
            # Reuse the exisitng connection if exists
            return

        redis_details = get_build_config(section='redis')

        #
        # Create a new Physical connection, which needs to be closed on the exit
        self.conn = redis.Redis(
            connection_pool=redis.ConnectionPool(
                host=redis_details.host,
                port=redis_details.port,
                db=redis_details.db_number,
            )
        )

        try:
            #
            # Test the Server Reachability
            self.conn.get('test-key')
            self.is_connected = True

        except ConnectionError:
            self.is_connected = False
            raise

    def set(self, key, data, expires_after=300):

        """A method to store the data to the Redis Server.
        """

        self.connect()

        if key in self.conn.keys():
            #
            # Delete the data if the key exist
            self.conn.delete(key)

        #
        # Store the data into the Redis Store
        response = bool(self.conn.set(key, self.serialize(data)))
        #
        # Set item Expiry time
        self.conn.expire(key, expires_after)

        return response

    def get(self, key):

        """A method to retrieve the data from the Redis Store.
        """

        self.connect()
        #
        # Retrieve the stored data, retrieves ``None`` when Expired
        data = self.conn.get(key)
        return self.deserialize(data) if data else None

    def remove(self, key):

        """A method to remove data from the Redis Server.
        """

        self.connect()
        return self.conn.delete(key)

    def flush_cache(self, pattern):

        """A method to flush the entire cache for the given tenant from the Redis Server.
        """

        self.connect()

        keys_removed = list()
        for key in self.conn.scan_iter(pattern):
            keys_removed.append(key)
            self.conn.delete(key)

        return keys_removed

    def __enter__(self):

        """The Context Manager.
        """
        return self

    def __exit__(self, *args, **kwargs):

        """The Context Manager.
        """
        #
        # Explicit connection closure is not required when used with the connection pool
        pass


#
# TODO:
# The interfaces to be extended to the other possible intermediate stores as well such as MongoDB, etc.,
#
# class MongoDBStore(IntermediateInterface):
#     pass


class IntermediateStore(object):

    """A Switchable Interface class for the various Intermediate Stores.
    The Intermediate switch can be controlled from the basebuild configuration

        ``general:intermediate_store``
    Which gives the actual Intermediate Store configured form the basebuild
    """

    MAPPER = {
        'redis': RedisStore,
        # 'Mongodb': MongoDBStore,  # TODO:
    }

    def _get_store(self):

        intermediate_store = get_build_config(section='general').intermediate_store

        if intermediate_store not in self.MAPPER:
            raise Exception(
                f'Specified Intermediate Store: {intermediate_store} is not Supported.'
            )

        return intermediate_store, self.MAPPER[intermediate_store]

    def set(
            self,
            data: Any,
            key: Optional[str] = None,
            prefix: Optional[str] = None,
            expires_after: Optional[int] = None
    ) -> str | bool:

        """Store the data to the any available Intermediate Store.

        Usage:
            >>> store = IntermediateStore()
            >>> store.set(1000)
            redis:774f3590-8520-44c6-b91e-60083729a42a
            >>> set(data=2000, key='my_key')
            1
        """

        _key_generated = False
        _, store_class = self._get_store()

        if not key:
            _key_generated = True
            key = encoded_uuid()

        key = f"{prefix}:{key}" if prefix else key

        with store_class() as istore:
            istore.set(key, data, expires_after=expires_after or 300)

        return key

    def get(self, key: str, prefix: Optional[str] = None):

        """Retrives the data from the any available Intermediate Store for the given Identifier named key.

        Usage:
            >>> intermediate_store = IntermediateStore()
            >>> intermediate_store.get('redis:774f3590-8520-44c6-b91e-60083729a42a')
            1000
            >>> intermediate_store.get('my_key')
            2000
        """

        _, store_class = self._get_store()

        key = f"{prefix}:{key}" if prefix else key

        with store_class() as istore:
            return istore.get(key)

    def remove(self, key: str):

        _, store_class = self._get_store()

        with store_class() as istore:
            return istore.remove(key)

    def flush_cache(self, pattern: str):

        _, store_class = self._get_store()

        with store_class() as istore:
            return istore.flush_cache(pattern=pattern)


def set_to_store(data, key=None, prefix=None, expires_after=None):
    return IntermediateStore().set(
        data=data, key=key, prefix=prefix, expires_after=expires_after
    )


def fetch_from_store(key: str, prefix=None):
    return IntermediateStore().get(key=key, prefix=prefix)



import os
from fastapi import UploadFile
from google.cloud import storage
from google.api_core.exceptions import NotFound, Conflict
from google.auth.exceptions import DefaultCredentialsError

from core.utils.helpers.environ import get_build_config, get_build_path
general_build_config = get_build_config('general')
cloud_build_config = get_build_config('cloud')


class BucketStorageService(ABC):

    @abstractmethod
    async def upload_file(self,
                          file: UploadFile,
                          destination_path: str,
                          content_type: str) -> bool:
        """Upload a file to cloud storage"""
        pass


class GCPBucketStorageService(BucketStorageService):

    def __init__(self, bucket_name: str):

        try:
            if general_build_config.environment.lower() == const_general.SANDBOX.lower():

                service_account_key_file_path = os.path.join(
                    get_build_path(), '../..', const_cloud.SERVICE_ACCOUNT_KEY_FILE_NAME
                )
                if not os.path.exists(service_account_key_file_path):
                    raise Exception("Unable to locate the service key file in basebuild directory")

                self.client = storage.Client.from_service_account_json(
                    service_account_key_file_path
                )

            else:
                #
                # Production: Uses attached service account
                self.client = storage.Client()

        except DefaultCredentialsError:
            raise Exception("Unable to access cloud Storage")

        self.bucket_name = bucket_name
        self.bucket = self.client.get_bucket(bucket_name)

    async def upload_file(self,
                          file,
                          destination_path: str,
                          content_type: str) -> bool:

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_path)
        blob.upload_from_file(file, content_type=content_type)

        return True

    async def download_file(self, file_path: str) -> BytesIO:

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_path)

        if not blob.exists():
            raise Exception(f"File does not exist: {file_path}")

        file_stream = BytesIO()
        blob.download_to_file(file_stream)
        file_stream.seek(0)

        return file_stream

    async def download_as_dataframe(self, file_path: str) -> DataFrame:

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_path)

        if not blob.exists():
            raise Exception(f"File does not exist: {file_path}")

        data = blob.download_as_bytes()

        return read_csv(BytesIO(data))

def get_bucket_store(bucket_name: str) -> BucketStorageService:

    if cloud_build_config.provider == const_cloud.PROVIDER_GCP:
        return GCPBucketStorageService(bucket_name=bucket_name)

    else:
        raise ValueError(f"Unsupported cloud provider: {cloud_build_config.provider}")

