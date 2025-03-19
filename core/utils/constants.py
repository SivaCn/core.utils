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
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.helpers.frozenobj import frozen
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
    'const_dates',
    'const_states',
]


class HTTPStatusCodes(object):
    #
    # HTTP Status codes

    #
    # Success 2XX
    HTTP_200 = 200  # Ok
    HTTP_201 = 201  # Created
    HTTP_202 = 202  # Accepted
    HTTP_204 = 204  # No Content
    HTTP_206 = 206  # Partial Content

    #
    # 3XX Redirection
    HTTP_300 = 300  # Multiple Choices
    HTTP_301 = 301  # Moved Permanently
    HTTP_302 = 302  # Found
    HTTP_303 = 303  # See Other
    HTTP_304 = 304  # Not Modified
    HTTP_307 = 307  # Temporary Redirect
    HTTP_308 = 308  # Permanent Redirect

    #
    # 4XX Client Errors
    HTTP_400 = 400  # Bad Request
    HTTP_401 = 401  # Unauthorized
    HTTP_403 = 403  # Forbidden
    HTTP_404 = 404  # Not Found
    HTTP_405 = 405  # Method Not Allowed
    HTTP_406 = 406  # Not Acceptable
    HTTP_408 = 408  # Request Timeout
    HTTP_409 = 409  # Conflict
    HTTP_410 = 410  # Gone
    HTTP_415 = 415  # Unsupported Media Type
    HTTP_422 = 422  # Unprocessable Entity
    HTTP_429 = 429  # Too Many Requests

    #
    # 5XX Server Errors
    HTTP_500 = 500  # Internal Server Error
    HTTP_501 = 501  # Not Implemented
    HTTP_502 = 502  # Bad Gateway
    HTTP_503 = 503  # Service Unavailable
    HTTP_504 = 504  # Gateway Timeout
    HTTP_505 = 505  # HTTP Version Not Supported

http_status = frozen(HTTPStatusCodes())


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


class AuthorizationConstants(object):

    #
    # Authorization Related
    JWT_SECRECT_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_TOKEN_EXPIRE_AFTER_MINUTES = int(os.getenv('JWT_TOKEN_EXPIRE_AFTER_MINUTES') or 30)

    if not JWT_SECRECT_KEY or not JWT_ALGORITHM or not JWT_TOKEN_EXPIRE_AFTER_MINUTES:
        raise Exception("CRITICAL: Unable to read JWT related details")


const_auth = frozen(AuthorizationConstants())


class RegexConstants(object):
    #
    # All regex patterns
    MOBILE_NUMBER = r"(?P<country_code>\+\d{1,3})[\-](?P<number>\d{7,15})"
    '''Supports:
            +91-9876543210      # India
            +1-4155552671       # USA
            +81-9012345678      # Japan
            etc.,
    '''

    STRICT_6_DIGITS = r"^\d{6}$"

    USER_NAME = r"^[A-Za-z]+([ '-][A-Za-z]+)*$"
    '''Valid names are: John Doe, Mary-Jane, O'Connor, Anne Marie, Jean-Luc'''


const_regex = frozen(RegexConstants())


class BusinessConstants(object):
    #
    # All Business Related
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


const_business = frozen(BusinessConstants())

