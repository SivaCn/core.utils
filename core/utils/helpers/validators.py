# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import re

from uuid import UUID
from datetime import datetime
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from email_validator import validate_email, EmailNotValidError
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import (
    const_regex,
    const_business,
)
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def validate_is_active(is_active: str) -> bool:

    allowed_values = (
        const_business.IS_ACTIVE_YES,
        const_business.IS_ACTIVE_NO,
        const_business.IS_ACTIVE_DELETED,
    )

    return is_active in allowed_values


def is_valid_email(email):
    """Validates and normailzed a given Email-Id."""

    try:
        validate_email(email)  # Validate and normalize
        return True

    except EmailNotValidError:
        return False


def is_valid_website(url: str) -> bool:
    """Validates a given website address.

    Usage:
        >>> is_valid_website("https://www.example.com")
        True
        >>> is_valid_website("http://sub.example.com/path")
        True
        >>> is_valid_website("example.com")
        True
        >>> is_valid_website("www.example.org")
        True
        >>> is_valid_website("invalid.url")
        False
        >>> is_valid_website("http://example")
        False
    """

    pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// or https:// (optional)
        r'([a-zA-Z0-9-]+\.)+'  # subdomains
        r'[a-zA-Z]{2,}'  # top level domain (at least 2 chars)
        r'(\/[a-zA-Z0-9-._~:\/?#\[\]@!$&\'()*+,;=]*)?'  # path/query params
        r'$'
    )
    return bool(pattern.match(url))


def is_valid_mobile_number(mobile_number: str) -> bool:
    """Validates a mobile numer."""

    pattern = re.compile(const_regex.MOBILE_NUMBER)

    return bool(pattern.fullmatch(mobile_number))


def is_valid_otp(otp: str) -> bool:
    """Validates a given OTP number."""

    pattern = re.compile(const_regex.OTP_6)

    return bool(pattern.fullmatch(otp))


def is_valid_uuid4(uuid_str):
    """validates a given uuid4 string."""

    try:
        val = UUID(uuid_str, version=4)
        return str(val) == uuid_str  # Ensure it's properly formatted

    except ValueError:
        return False


def is_valid_user_slug(user_slug: str) -> bool:
    """Validates a given user slug."""

    return is_valid_uuid4(user_slug)


def is_valid_user_name(name: str) -> bool:
    """Validates a given user Name."""

    pattern = re.compile(const_regex.USER_NAME)

    return bool(pattern.fullmatch(name))


def is_valid_iso_date(date_str):
    """Validates a given ISO date."""

    try:
        datetime.fromisoformat(date_str)  # Validates ISO 8601 format (YYYY-MM-DD)
        return True

    except ValueError:
        return False


def is_valid_plan_name(name: str) -> bool:
    """Validates a given Plan Name."""

    pattern = re.compile(const_regex.UPPER_CASE_LETTERS_N_NUMBERS_N_HYPENS)
    return bool(re.fullmatch(pattern, name))


def is_valid_coupon_code(code: str) -> bool:
    """Validates a given coupon Code."""

    pattern = re.compile(const_regex.UPPER_CASE_LETTERS_N_NUMBERS_N_HYPENS)
    return bool(re.fullmatch(pattern, code))


def is_strong_password(
        password: str,
        min_length: int = 8,
        require_upper: bool = True,
        require_lower: bool = True,
        require_number: bool = True,
        require_special: bool = True,
) -> bool:

    # Check minimum length
    if len(password) < min_length:
        return False

    # Check for uppercase letters
    if require_upper and not re.search(r'[A-Z]', password):
        return False

    # Check for lowercase letters
    if require_lower and not re.search(r'[a-z]', password):
        return False

    # Check for numbers
    if require_number and not re.search(r'[0-9]', password):
        return False

    # Check for special characters
    if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True
