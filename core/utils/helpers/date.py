# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import pendulum

from datetime import datetime, timedelta
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import const_dates
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def seconds_to_hms(seconds, elongate=False):

    """An utility to convert seconds into HH:MM:SS format.

    Usage:
        >>> seconds_to_hms(10800)
        '3:00:00'
        >>> seconds_to_hms(10800, elongate=True)
        '3h 00m 00s'
    """

    if not isinstance(seconds, int):
        raise TypeError(f"Argument seconds must be of type int, Got: {type(seconds)}")

    time_data = timedelta(seconds=seconds).__str__()

    if elongate:
        time_data = ' '.join(
            [x + y for x, y in zip(time_data.split(':'), ('h', 'm', 's'))]
        )

    return time_data


def is_valid_unix_timestamp(unix_timestamp: int) -> bool:
    """Validates and returns boolean result for a given unix timestamp."""
    # Check the range for 32-bit Unix timestamps
    return 0 <= unix_timestamp <= 2147483647


def datetime_from_unix_timestamp(unix_timestamp: int) -> datetime:
    """Computes python datetime from unix timestamp."""

    if not is_valid_unix_timestamp(unix_timestamp):
        raise TypeError(f"Not a valid Unix Timestamp: '{unix_timestamp}'")

    return datetime.fromtimestamp(unix_timestamp)


def parse_date_from_iso(data, as_iso=True):

    """Parses any datetime string and returns the data part from it.

    Usage:
        >>> parse_date_from_iso("2021-10-30T13:30:04.944880")
        '2021-10-30'
        >>> parse_date_from_iso("2021-10-30T13:30:04+05:30")
        '2021-10-30'
        >>> parse_date_from_iso("2021-10-30T13:30")
        '2021-10-30'
        >>> parse_date_from_iso("2021-10-30T13")
        '2021-10-30'
        >>> parse_date_from_iso("2021-10-30")
        '2021-10-30'
        >>> parse_date_from_iso("2021-10-30T13:30:04.944880", as_iso=False)
        datetime.datetime(2021, 10, 30, 0, 0)
    """

    fmt = const_dates.DATE_FORMAT

    #
    # ``strftime(fmt)`` is being invoked to discard any date part other than date and time
    result = pendulum.parse(data).strftime(fmt)
    if as_iso:
        return result

    return datetime.strptime(result, fmt)


def parse_datetime_from_iso(data, fmt=None, tz=False, as_iso=True):

    """Parses any datetime string and returns the data part from it.

    Usage:
        >>> parse_datetime_from_iso("2021-10-30T13:30:04.944880")
        '2021-10-30T13:30:04'
        >>> parse_datetime_from_iso("2021-10-30T13:30:04+05:30")
        '2021-10-30T13:30:04'
        >>> parse_datetime_from_iso("2021-10-30T13:30")
        '2021-10-30T13:30:00'
        >>> parse_datetime_from_iso("2021-10-30T13")
        '2021-10-30T13:00:00'
        >>> parse_datetime_from_iso("2021-10-30")
        '2021-10-30T00:00:00'
        >>> parse_datetime_from_iso("2021-10-30", as_iso=False)
        datetime.datetime(2021, 10, 30, 0, 0)
    """
    fmt = fmt or const_dates.ISO_DATETIME_FORMAT
    if tz:
        fmt = const_dates.ISO_DATETIME_FORMAT_TZ
    #
    # ``strftime(fmt)`` is being invoked to discard any date part other than date and time
    result = pendulum.parse(data).strftime(fmt)
    if as_iso:
        return result
    return datetime.strptime(result, fmt)

