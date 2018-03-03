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
    return {
        key: value.split(',')
        for key, value in environments_ini.section_as_dict('queue_details').items()
    }


def get_amqp_connection_str():
    """."""

    rmq = get_rabbitmq_details()

    if rmq['vhost'] == '/':
        return AMQP_CONNECTION_STRING % rmq

    return AMQP_CONNECTION_STRING % rmq + '/' + rmq['vhost']
