# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import string
import secrets

from hashlib import sha256
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def generate_secret_key(length: int = 32) -> str:
    """Generates secret key.

    Usage:
        >>> generate_secret_key()
        'xueiTge6k9Rr-FMFfu9PfnYyrjRiNKKr'
    """

    # Characters to choose from (letters, digits, hypen(five times))
    alphabet = string.ascii_letters + string.digits + '-' * 5

    # Generate a random string with cryptographic safety
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_token(category: str='invite') -> str:

    return f"{category}_{generate_secret_key()}"


def generate_otp(length: int=6) -> str:
    """For OTP codes"""

    return ''.join(
        secrets.choice(string.digits) for _ in range(length)
    )

