# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class APIError(Exception):
    def __init__(self,
                 code: str,
                 message: str,
                 status_code: int,
                 details: dict = dict()):

        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class AuthError(APIError):
    def __init__(self, message: str):

        super(
            self.__class__, self
        ).__init__(
            code='AUTH-ERROR',
            message=f"{self.__class__.__name__}: {message}",
            status_code=401,
        )


class MissingWorkspaceError(APIError):
    def __init__(self, message: str):

        super(
            self.__class__, self
        ).__init__(
            code='INPUT-MISSING',
            message=f"{self.__class__.__name__}: {message}",
            status_code=400,
        )


class MissingContextError(APIError):
    def __init__(self, message: str):

        super(
            self.__class__, self
        ).__init__(
            code='CONTEXT-MISSING',
            message=f"{self.__class__.__name__}: {message}",
            status_code=400,
        )


class coreException(Exception):
    def __init__(self, message):
        if not getattr(self, 'code', None):
            self.code = 400

        self.message = message
        super().__init__(self.message)

    def __repr__(self):
        return f'{self.message}'

    def __str__(self):
        return self.__repr__()


class TimedOutError(coreException):
    def __init__(self, message):
        self.code = 408
        super().__init__(message or 'Process Timed Out')


class ProcessSkippedError(coreException):
    def __init__(self, message):
        self.code = 409
        super().__init__(message)


class BadArgumentError(coreException):
    pass


class NotAllowedError(coreException):
    pass


class UnSupportedError(coreException):
    pass


class DirectoryNotFoundError(coreException):
    pass
