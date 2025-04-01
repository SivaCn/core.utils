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


def generate_token(category: str='invite') -> str:

    token = f"{category}_{secrets.token_urlsafe(32)}"
    return sha256(token.encode()).hexdigest()


def generate_otp(length: int=6) -> str:
    """For OTP codes"""

    return ''.join(
        secrets.choice(string.digits) for _ in range(length)
    )

