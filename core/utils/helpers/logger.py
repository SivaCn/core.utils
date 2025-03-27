# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import os
import time

from collections import defaultdict

from typing import List, Optional

from logging import (
    getLogger,
    handlers,
    Formatter,

    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    WARN,
    WARNING,

    StreamHandler,
)
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import (
    const_dates,
    const_logging,
)

from core.utils.helpers.environ import get_build_config
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


# Create a defaultdict that returns logging.ERROR for missing keys
log_levels = defaultdict(
    lambda: ERROR,
    {
        'info': INFO,
        'warn': WARN,
        'debug': DEBUG,
        'error': ERROR,
        'fatal': FATAL,
        'warning': WARNING,
        'critical': CRITICAL,
    }
)

file_name_mapper = {
    'consumer-script': 'consumer_script.log'
}


logger_config = get_build_config(section='logger-config')


def create_logger(
        logger_name: str,
        file_name: Optional[str] = None,
        set_handlers: List[str] = ['file', 'stream'],
        max_file_size: int = 5,
        file_backup_count: int = 10
    ):

    if not file_name:
        #
        # Try auto resolving the file name for logging
        if logger_name not in file_name_mapper:
            raise Exception(f"Unable to resolve log file name, for logger_name: {logger_name}")

        file_name = file_name_mapper[logger_name]

    log_file_name = os.path.join(
        os.environ['BUILD_HOME'], '../..', 'var', 'log', file_name
    )

    _logger = getLogger(logger_name)
    _logger.setLevel(
        log_levels[logger_config.loglevel]
    )

    formatter = Formatter(fmt=const_logging.LOG_FORMAT, datefmt=const_dates.ISO_DATETIME_FORMAT)
    formatter.converter = time.gmtime

    #
    # Fail safe, when configurations are not available
    max_bytes = logger_config.max_file_size or max_file_size
    max_backup_count = logger_config.file_backup_count or file_backup_count

    for handler_to_set in set_handlers:

        handler_to_set = handler_to_set.strip()

        if handler_to_set == 'file':
            handler = handlers.RotatingFileHandler(
                log_file_name,
                maxBytes=max_bytes * 1024,
                backupCount=max_backup_count
            )
            handler.setFormatter(formatter)
            _logger.addHandler(handler)

        if handler_to_set == 'stream':
            stream_handler = StreamHandler()
            stream_handler.setFormatter(formatter)
            _logger.addHandler(stream_handler)

    return _logger


consumer_script_logger = create_logger(logger_name='consumer-script')

