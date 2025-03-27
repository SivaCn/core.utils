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


class NotAllowedError(coreException):
    pass


class UnSupportedError(coreException):
    pass


class DirectoryNotFoundError(coreException):
    pass
