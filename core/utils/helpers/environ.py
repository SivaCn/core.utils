# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import os
import sys

from pathlib import Path
from copy import deepcopy
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from dotenv import load_dotenv
from configparser import ConfigParser
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import (
    const_general,
)

from core.utils.helpers.utils import (
    DotDict,
    py_datatype_from_str,
)
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def load_config_from_dotenv():
    """Load the build's .env configurations."""

    cwd = os.getcwd()
    env_file_path = os.path.join(cwd, '.env')

    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"Unable to find the environment file under '{cwd}' Directory")

    load_dotenv(env_file_path)


load_config_from_dotenv()


class ConsoleScript:

    def __init__(self, func):
        self.func = func

    def validate_env(self):

        if not os.environ['BUILD_HOME']:
            print('\nERROR: Unable to find Build Home')
            sys.exit()

        if not os.environ['INSTANCE_TYPE']:
            print('\nERROR: Unable to find Instance Type')
            sys.exit()

    def __call__(self, *args, **kwargs):

        self.validate_env()
        return self.func(*args, **kwargs)


def get_build_path() -> str:
    """A utility method to get the build path.
    """
    return os.environ['BUILD_HOME']


def get_build_name() -> str:
    """Get the buildname from the current file path.
    """

    path_parts = [str(node) for node in Path(get_build_path()).parts]

    from_services = path_parts[path_parts.index('services'):]  # Consider the nodes from services

    buildname = None
    for node in from_services:
        if node in ('services', 'src', ):
            #
            # Ignore the specifc directories
            continue
        buildname = node
        break

    if not buildname:
        raise Exception(f"Unable to Resolve the buildname. Please report this incident to Site Admin.")

    return buildname


def load_build_config():
    """Load the build configurations to the local cache.

    NOTE: Any Change in the config file, the Instance needs to be restarted to get loaded again.
    """

    filename = os.path.join(
      get_build_path(), 'parts', 'config', 'config.ini'
    )

    config = ConfigParser(interpolation=None)
    config.read(filename)

    data = dict()
    for section in config.sections():
        data[section] = {
            key: py_datatype_from_str(value) for key, value in config.items(section)
        }

    return data


_V_BUILD_CONFIG_CACHE = dict()
"""Local Cache to hold all the build configurations."""


def get_build_config(section: str | None=None) -> dict:
    """Get the build configurations for a given section.

    Usage:
        >>> get_build_config(section='database')
        <DotDict(database: postgres, host: 127.0.0.1, port: 5432, ...)>
        >>>
        >>>
        >>> get_build_config(section='database').as_dict()
        {'database': 'postgres',
         'db_name': 'mydb',
         'host': '127.0.0.1',
         'password': 'admin',
         'port': 5432,
         'username': 'admin'}
    """

    def get_database_config(section):

        database_name = _V_BUILD_CONFIG_CACHE[section]['database']
        verbose = _V_BUILD_CONFIG_CACHE[section]['verbose']
        return {
            'database': database_name,
            'verbose': verbose,
            'master': _V_BUILD_CONFIG_CACHE['db-master'],
            'replica': _V_BUILD_CONFIG_CACHE['db-replica'],
        }

    global _V_BUILD_CONFIG_CACHE

    if not _V_BUILD_CONFIG_CACHE:
        #
        # Populate the build config cache
        _V_BUILD_CONFIG_CACHE = load_build_config()

    build_config_data = deepcopy(_V_BUILD_CONFIG_CACHE)
    for each_section in _V_BUILD_CONFIG_CACHE:

        if each_section == 'database':
            build_config_data[each_section].update(get_database_config(each_section))

    if section:
        return DotDict(build_config_data[section])

    return DotDict(build_config_data)


def get_amqp_connection_str() -> str:
    """."""

    rmq = get_build_config(section='rabbitmq')

    return const_general.AMQP_CONNECTION_STRING % rmq.as_dict()


def get_celery_result_backend():

    """Compute the celery result backend."""

    consumer_config = get_build_config(section='consumer-config')

    result_backend = 'rpc://'

    celery_result_backend = consumer_config.celery_result_backend.strip()

    if celery_result_backend == 'rpc':
        #
        # if rpc is chosen or any invalid option is given fallback to rpc
        result_backend = 'rpc://'

    elif celery_result_backend == 'redis':
        #
        # Complpute the result backend for redis
        redis = get_build_config(section='redis')

        template = const_general.REDIS_URL_WITHOUT_CREDENTIALS
        if redis.username and redis.password:
            #
            # use credentials if configured
            template = const_general.REDIS_URL_WITH_CREDENTIALS

        result_backend = template % redis.as_dict()

    else:
        #
        # Anythinf apart from rpc ot redis, falling back to rpc
        result_backend = 'rpc://'

    return result_backend
