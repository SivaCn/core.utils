# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from core.utils.utils import CustomConfigParser
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.constants import AMQP_CONNECTION_STRING
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


def get_build_path():
    """."""

    _dir, _file = os.path.split(os.path.abspath(__file__))
    _drive, _path = os.path.splitdrive(_dir)

    return os.path.join(os.sep, *_path.split(os.sep)[:-4])

def get_log_dir_path():

    return os.path.join(
        get_build_path(), 'var', 'log'
    )


def parse_environmets_ini():
    """."""

    build_path = get_build_path()

    env_file_path = os.path.join(build_path, 'ini', 'environments.ini')

    return CustomConfigParser(env_file_path)


def get_user_session_details():
    """."""

    def normalize(value):

        value = value.strip()

        if value.isdigit():
            value = int(value)

        return value

    return {
        key: normalize(value)
        for key, value in parse_environmets_ini().section_as_dict('user-session').items()
    }


def get_rabbitmq_details():
    """."""

    def normalize(key, value):
        _trans = {
            #         (requested as, default map)
            'vhost': ('default', '/')
        }

        if key in _trans:
            if value == _trans[key][0]:
                return _trans[key][1]
        return value

    environments_ini = parse_environmets_ini()
    return {
        key: normalize(key, value)
        for key, value in environments_ini.section_as_dict('rabbitmq_details').items()
    }


def get_normalized_rmq_credentials():

    rmq_details = get_rabbitmq_details()

    return {
        key: value
        for key, value in rmq_details.items()
        if key in ('username', 'password', )
    }

def get_normalized_rmq_env_details():

    rmq_details = get_rabbitmq_details()

    normalized_mapper = {
        'host': 'host',
        'port': 'port',
        'vhost': 'virtual_host',
    }

    def normalize_key(key):
        return normalized_mapper[key]

    return {
        normalize_key(key): value
        for key, value in rmq_details.items()
        if key in normalized_mapper
    }


def get_main_db_details():
    """."""
    environments_ini = parse_environmets_ini()
    _config = {
        key: value
        for key, value in environments_ini.section_as_dict('main-db').items()
    }

    _config.update({'path': os.path.join(get_build_path(), 'parts', _config['name'])})

    return _config


def get_jobs_db_details():
    """."""
    environments_ini = parse_environmets_ini()
    _config = {
        key: value
        for key, value in environments_ini.section_as_dict('jobs-db').items()
    }

    _config.update({'path': os.path.join(get_build_path(), 'parts', _config['name'])})

    return _config


def get_queue_details():
    """."""

    environments_ini = parse_environmets_ini()

    def adjust_durable_prop(value):
        _queue_name, _durable = value.split(',')
        return _queue_name.strip(), True if _durable == 'durable_true' else False

    return {
        key: adjust_durable_prop(value)
        for key, value in environments_ini.section_as_dict('queue_details').items()
    }

def get_log_file_details():
    """."""

    return parse_environmets_ini().section_as_dict('log-files')


def get_amqp_connection_str():
    """."""

    rmq = get_rabbitmq_details()

    if rmq['vhost'] == '/':
        return AMQP_CONNECTION_STRING % rmq

    return AMQP_CONNECTION_STRING % rmq + '/' + rmq['vhost']
