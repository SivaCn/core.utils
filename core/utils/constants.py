# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.helpers.frozenobj import frozen
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
    'const_dates',
    'const_states',
]


class StateConstants(object):
    #
    # Task Status
    CREATED = 'CREATED'            # The task has been created but not yet queued or processed.
    QUEUED = 'QUEUED'              # The task is in the queue waiting to be processed.
    PENDING = 'PENDING'            # The task is about to be processed but hasn't started yet.
    IN_PROGRESS = 'IN_PROGRESS'    # The task is currently being processed.
    PAUSED = 'PAUSED'              # The task has been temporarily halted.
    RESUMED = 'RESUMED'            # The task has been resumed after being paused.
    COMPLETED = 'COMPLETED'        # The task has finished successfully.
    FAILED = 'FAILED'              # The task encountered an error and couldn't complete.
    RETRYING = 'RETRYING'          # The task failed but is being attempted again.
    CANCELLED = 'CANCELLED'        # The task was manually cancelled before completion.
    TIMEOUT = 'TIMEOUT'            # The task exceeded its allocated time limit.
    BLOCKED = 'BLOCKED'            # The task is waiting for a resource or condition to be met.
    SCHEDULED = 'SCHEDULED'        # The task is set to run at a future time.
    VALIDATING = 'VALIDATING'      # The task's results are being checked for correctness.
    ARCHIVED = 'ARCHIVED'          # The task has been moved to long-term storage.
    DELETED = 'DELETED'            # The task has been removed from the system.
    UNKNOWN = 'UNKNOWN'            # The state of the task cannot be determined.


const_states = frozen(StateConstants())


class DatabaseConstants(object):
    #
    #
    MIGRATION_DB_URL_DIALECT = 'postgresql+psycopg2'
    READ_WRITE_DB_URL_DIALECT = 'postgresql+asyncpg'


const_db = frozen(DatabaseConstants())


class DateConstants(object):
    #
    # Date and Time Related
    TIME_FORMAT = '%H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'
    ISO_DATETIME_FORMAT = f'{DATE_FORMAT}T{TIME_FORMAT}'
    ISO_DATETIME_FORMAT_TZ = f'{DATE_FORMAT}T{TIME_FORMAT}Z'


const_dates = frozen(DateConstants())

