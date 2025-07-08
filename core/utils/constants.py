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


class GeneralConstants(object):
    #
    # All General Constants

    #
    # Environments
    SANDBOX = 'sandbox'
    DEV = 'dev'
    STAGE = 'stage'
    PROD = 'prod'

    LINE_BREAK = r'\n'

    AMQP_CONNECTION_STRING = 'pyamqp://%(username)s:%(password)s@%(host)s:%(port)s/%(virtual_host)s'
    REDIS_URL_WITHOUT_CREDENTIALS = 'redis://%(host)s:%(port)s/%(db_number)s'
    REDIS_URL_WITH_CREDENTIALS = 'redis://%(username)s:%(password)s@%(host)s:%(port)s/%(db_number)s'


const_general = frozen(GeneralConstants())


class OperatorConstants(object):
    #
    # Numeric Operators Related
    EQUAL = '='
    NOT_EQUAL = '!='
    LESS_THAN = '<'
    LESS_THAN_OR_EQUAL = '<='
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='

    ANY = 'in'
    NOT_ANY = 'not in'

    CONTAINS = 'contains'


const_operators = frozen(OperatorConstants())


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
    ERROR = 'ERROR'                # The task encountered an error and couldn't complete
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

    LOGGED_IN = 'LOGGED-IN'
    LOGGED_OUT = 'LOGGED-OUT'
    FORCE_LOGGED_OUT = 'FORCE-LOGGED-OUT'


const_states = frozen(StateConstants())


class DatabaseConstants(object):
    #
    #
    DATABASE_URL = '{dialect}://{username}:{password}@{host}:{port}/{db_name}'
    MIGRATION_DB_URL_DIALECT = 'postgresql+psycopg2'
    READ_WRITE_DB_URL_DIALECT = 'postgresql+asyncpg'


const_db = frozen(DatabaseConstants())


class DateConstants(object):
    #
    # Date and Time Related
    TIME_FORMAT = '%H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
    COMPACT_DATETIME_FORMAT = '%Y%m%dT%H%M%S'
    DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'
    ISO_DATETIME_FORMAT = f'{DATE_FORMAT}T{TIME_FORMAT}'
    ISO_DATETIME_FORMAT_TZ = f'{DATE_FORMAT}T{TIME_FORMAT}Z'


const_dates = frozen(DateConstants())


class SecretConstants(object):

    #
    # Authorization Related
    JWT_TOKEN_TYPE = 'Bearer'
    JWT_SECRECT_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_TOKEN_EXPIRE_AFTER_MINUTES = int(os.getenv('JWT_TOKEN_EXPIRE_AFTER_MINUTES') or 30)

    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
    RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')


const_secrets = frozen(SecretConstants())


class RegexConstants(object):
    #
    # All regex patterns
    MOBILE_NUMBER = r"(?P<country_code>\+\d{1,3})[\-](?P<number>\d{10})"
    '''Supports:
            +91-9876543210      # India
    '''

    OTP_6 = r"^[A-Z0-9]{6}$"
    STRICT_6_DIGITS = r"^\d{6}$"

    WORKSPACE = r"^[a-z0-9]+$"
    '''strings containing only lowercase letters and numbers'''

    USER_NAME = r"^[A-Za-z]+([ '-][A-Za-z]+)*$"
    '''Valid names are: John Doe, Mary-Jane, O'Connor, Anne Marie, Jean-Luc'''

    UPPER_CASE_LETTERS_N_NUMBERS_N_HYPENS = r'^[A-Z0-9]+(?:-[A-Z0-9]+)*$'
    '''uppercase letters, numbers, and hyphens, where hyphens are not allowed at the start or end
    '''

    DB_HOST = (
        r'^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'
        r'|localhost'
        r'|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        r'|\[?[0-9a-fA-F:]+\]?)(?::\d+)?$'
    )
    '''
    Valid:
       localhost
       postgres.example.com
       192.168.1.1
       mysql.internal:5432

    Invalid:
        http://example.com (protocol not allowed)
        example..com (double dots)
        256.1.1.1 (invalid IPv4)
        hostname/ (special chars)
    '''

    DB_PORT = r"^\d{4,}$"

    DB_NAME = r"^[a-zA-Z_][a-zA-Z0-9_-]{0,63}$"
    '''
    Valid Names:
        mydb
        app_db1
        analytics_prod
        user_data_2024

    Invalid Names:
        1database (starts with a number)
        my-db! (contains special characters)
        this_name_is_way_too_long_for_most_database_engines_and_will_be_rejected (>64 chars)
    '''

    #
    # Matches the pattern 'YYYY-MM-DDTHH:MM:SS'
    # Example string: '2023-05-23T12:00:36'
    DATETIME_PATTERN = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'


const_regex = frozen(RegexConstants())


class BusinessConstants(object):
    #
    # All Business Related

    NA = 'NA'

    ADMIN_PROD_EMAIL = 'admin.eng@getyellow.in'

    OPEN_API_RATE_LIMIT = "2/minute"
    CHANGE_ADMIN_PASSWORD_AFTER_DAYS = 7
    ADMIN_INVITE_EXPIRES_AFTER_DAYS = 1

    DEFAULT_ITEMS_PER_PAGE = 10
    DEFAULT_CURRENT_PAGE = 1

    IS_ACTIVE_YES = 'Y'
    IS_ACTIVE_NO = 'N'
    IS_ACTIVE_DELETED = 'D'
    IS_ACTIVE_ARCHIVED = 'A'

    #
    # Tag Categories
    TARIFF = 'TARIFF'

    #
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY'

    #
    # Plan Features
    WILL_DOWNLOAD = 'WILL-DOWNLOAD'
    WILL_PRINT_AND_SHIP = 'WILL-PRINT-AND-SHIP'

    #
    # Tariff Related
    PLAN = 'PLAN'
    SUBSCRIPTION = 'SUBSCRIPTION'
    ADD_ON = 'ADD_ON'

    #
    # Duration Periods
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'

    #
    # Address Entity Types
    ADDRESS_PERMANENT = 'PERMANENT'
    ADDRESS_MAILING = 'MAILING'

    #
    # Print and Ship Status Related
    PRINT_REQUEST_RECEIVED = 'RECEIVED'
    PRINT_REQUEST_REVIEWED = 'REVIEWED'
    PRINT_REQUEST_DELIVERED = 'DELIVERED'
    PRINT_REQUEST_SHIPPED = 'SHIPPED'
    PRINT_REQUEST_INPROGRESS = 'INPROGRESS'
    PRINT_REQUEST_CANCELLED = 'CANCELLED'
    PRINT_REQUEST_REJECTED = 'REJECTED'
    PRINT_REQUEST_PRINTED = 'PRINTED'

    #
    # User Roles
    ROLE_SUPER_ADMIN = 'SUPER-ADMIN'
    ROLE_ADMIN = 'ADMIN'
    ROLE_CONTENT = 'CONTENT'
    ROLE_SUPPORT = 'SUPPORT'
    ROLE_OPERATIONS = 'OPERATIONS'

    EMAIL = 'EMAIL'
    PHONE = 'PHONE'

    PERSON = 'PERSON'
    CHARITY = 'CHARITY'

    INVITED = 'INVITED'
    RE_INVITED = 'RE_INVITED'
    ACCEPTED = 'ACCEPTED'
    EXPIRED = 'EXPIRED'
    REVOKED = 'REVOKED'
    FORGOT_PASSWORD = 'FORGOT_PASSWORD'

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

    #
    # Will Progress Stages
    NOT_INITIATED = 'NOT-INITIATED'
    MY_PEOPLE = 'MY-PEOPLE'
    MY_ASSETS = 'MY-ASSETS'
    ASSET_DISTRIBUTION = 'ASSET-DISTRIBUTION'
    COMPLETED = 'COMPLETED'

    WILL_PROGRESS_ORDER = [
        NOT_INITIATED,
        MY_PEOPLE,
        MY_ASSETS,
        ASSET_DISTRIBUTION,
        COMPLETED,
    ]

    #
    # Immovable Asset Types
    RESIDENTIAL = 'RESIDENTIAL'
    COMMERCIAL = 'COMMERCIAL'
    AGRICULTURAL = 'AGRICULTURAL'

    #
    # Immovable Asset Sub Types
    PLOT = 'PLOT'
    VILLA = 'VILLA'
    APARTMENT = 'APARTMENT'
    BUILDING = 'BUILDING'

    NOT_APPLICABLE = 'NA'

    #
    # Holding Types
    SINGLE = 'SINGLE'
    JOINT = 'JOINT'

    #
    # Dropdown Enums
    RELIGION = 'RELIGION'
    RELATIONSHIP = 'RELATIONSHIP'
    ID_PROOF = 'ID_PROOF'
    INVITE_ROLES = 'INVITE_ROLES'


    #
    # Religions
    HINDU = 'HINDU'
    CHRISTIAN = 'CHRISTIAN'
    MUSLIM = 'MUSLIM'
    SIKH = 'SIKH'
    PARSI = 'PARSI'
    JAIN = 'JAIN'
    OTHER = 'OTHER'

    #
    # Relationships
    CHILD = 'CHILD'
    PARENT = 'PARENT'
    SPOUSE = 'SPOUSE'
    SIBLING = 'SIBLING'
    FRIEND = 'FRIEND'
    RELATIVE = 'RELATIVE'
    OTHER = 'OTHER'

    #
    # Relationship Associations
    SON = 'SON'
    DAUGHTER = 'DAUGHTER'
    FATHER = 'FATHER'
    MOTHER = 'MOTHER'
    HUSBAND = 'HUSBAND'
    WIFE = 'WIFE'
    BROTHER = 'BROTHER'
    SISTER = 'SISTER'

    #
    # ID Proofs
    PAN = 'PAN'
    PASSPORT = 'PASSPORT'
    DRIVING_LICENSE = 'DRIVING-LICENCE'
    VOTER_ID = 'VOTER-ID'


const_business = frozen(BusinessConstants())


class CouponConstants(object):
    #
    # Coupons Related
    DISCOUNT_TYPE_PERCENT = 'PERCENT'
    DISCOUNT_TYPE_FLAT = 'FLAT'

    RESTRICTION_TYPE_USER = 'USER'


const_coupon = frozen(CouponConstants())


class EmailConstants(object):
    #
    # Email Template Bindings
    EMAIL_VERIFICATION_LINK = 'email-verification-link'
    EMAIL_ADMIN_INVITE = 'email-admin-invite'
    EMAIL_ADMIN_LOGIN_OTP = 'email-admin-login-otp'
    EMAIL_ADMIN_WELCOME = 'email-admin-welcome'
    EMAIL_ADMIN_FORGOT_PASSWORD = 'email-admin-forgot-password'
    EMAIL_ADMIN_CHANGED_PASSWORD = 'email-admin-changed-password'

    EMAIL_SUBJECT_DEFAULT = 'Greetings from Yellow organisation'
    EMAIL_SUBJECT_VERIFICATION_LINK = ''
    EMAIL_SUBJECT_ADMIN_INVITE = 'You are invited to join Yellow organisation'
    EMAIL_SUBJECT_ADMIN_LOGIN_OTP = 'Complete your Login'
    EMAIL_SUBJECT_ADMIN_WELCOME = 'Welcome to the team'
    EMAIL_SUBJECT_ADMIN_FORGOT_PASSWORD = 'Reset Password'
    EMAIL_SUBJECT_ADMIN_CHANGED_PASSWORD = 'Your Password Has Been Reset'

    USER_VERIFY_EMAIL_VIA_OTP = 'verify_email_via_otp'
    SUBJECT_USER_VERIFY_EMAIL_VIA_OTP = 'Verify your Email'


const_email = frozen(EmailConstants())


class StoreConstants(object):
    #
    # Store Related
    DEFAULT_EXPIRE_AFTER_SECONDS = 600
    OTP_EXPIRES_AFTER_SECONDS = 600

    PREFIX_VERIFIED_EMAIL = 'VERIFIED-EMAIL'
    PREFIX_EMAIL_VERIFY_OTP = 'EMAIL-VERIFY-OTP'
    PREFIX_EMAIL_LOGIN_OTP = 'EMAIL-LOGIN-OTP'
    PREFIX_SMS_LOGIN_OTP = 'SMS-LOGIN-OTP'


const_store = frozen(StoreConstants())


class CloudConstants(object):
    #
    # Store Related
    PROVIDER_GCP = 'GCP'
    SERVICE_ACCOUNT_KEY_FILE_NAME = 'service-account-key.json'


const_cloud = frozen(CloudConstants())


class FileConstants(object):
    #
    # File related constants
    PHOTO = 'PHOTO'
    VIDEO = 'VIDEO'
    DOCUMENT = 'DOCUMENT'

    THUMBNAIL_SQUARE_SIZE = (128, 128)
    THUMBNAIL_A4_SIZE = (595, 842)  # A4 at 72dpi, Texts can be best viewed

    PHOTO_FILE_MAX_SIZE = 1024 * 1024 * 2  # 2MB
    DOCUMENT_FILE_MAX_SIZE = 1024 * 1024 * 10  # 10MB


const_file = frozen(FileConstants())


class LoggingConstants(object):
    #
    # Logging Related
    LOG_FORMAT = '[%(asctime)s] %(levelname)-10s - %(message)s'


const_logging = frozen(LoggingConstants())


class CurrencyConstants(object):
    #
    # Logging Related
    INR = ('INR', 'Indian Rupees', )


const_currency = frozen(CurrencyConstants())


class ConsumerConstants(object):
    #
    # Consumer Related
    PACKAGE_NAME = 'core.consumers'
    YELLOW_EXCHAMGE = 'yellow-exchange'
    YELLOW_EXCHAMGE_TYPE = 'direct'

    PIKA_SOCKET_CONNECTION_TIMEOUT = 5
    RECONNECT_TIME_SECS = 10
    RECONNECT_ATTEMPT = 5
    RPC_DEFAULT_TIMEOUT_SECS = 20

    # Check for the response for process data events after (in seconds)
    DATA_EVENTS_TIME_LIMIT = 3


const_consumer = frozen(ConsumerConstants())


class SchedulerConstants(object):
    #
    # Scheduler Related

    #
    # Job Action
    ADD = 'add'
    UPDATE = 'update'
    REMOVE = 'remove'

    SCHEDULE_ACTION = [ADD, UPDATE, REMOVE]

    #
    # Schedule Type
    ONETIME = 'onetime'
    MINUTES = 'minutes'
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    SCHEDULE_TYPES = [
        ONETIME,
        MINUTES,
        HOURLY,
        DAILY,
        WEEKLY,
        MONTHLY,
    ]

    MISFIRE_GRACE_TIME = 180

    SCHEDULER_COALESCE = False
    SCHEDULER_MAX_INSTANCES = 3
    SCHEDULER_THREAD_POOL_EXECUTOR_COUNT = 20
    SCHEDULER_PROCESS_POOL_EXECUTOR_COUNT = 5
    SCHEDULER_MISFIRE_GRACE_TIME_IN_SECS = 60
    SCHEDULER_DEFAULT_SCHEDULE_DELAY_BY_SECS = 10

    SCHEDULER_QUEUE_NAME = 'scheduler-queue'
    SCHEDULER_QUEUE_DURABLE = True

    SCHEDULER_TABLE_NAME = 'scheduler_job'
    SCHEDULER_LOG_TABLE_NAME = 'scheduler_job_log'

    #
    # Scheduler Job Status
    STAGED = 'STAGED'
    ADDED = 'ADDED'
    UPDATED = 'UPDATED'
    EXECUTED = 'EXECUTED'
    ERROR = 'ERROR'
    MISSED = 'MISSED'
    REMOVED = 'REMOVED'


const_scheduler = frozen(SchedulerConstants())

