# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import re

from string import Template
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def string_substitute(string: str, substitutes: dict) -> str:
    """Substitue the given string with substitutes dictionary.

    Usage:
        >>> string_substitute(string='The value is: $value', substitutes={'value': 1000}
        'The value is: 1000'
    """

    return Template(string).safe_substitute(substitutes)


def apply_title_case(text: str) -> str:
    """Replaces non-alphanumeric and non-whitespace and underscore characters, then converts to title case.
    """
    # Replace underscore, hypens, colon and dot with whitespace
    text = re.sub(r'[_\-\:\.]', ' ', text)

    return text.title()


def apply_pascal_case(text: str):
    """Convert the given string into pascal case.

    Usage:
        >>> apply_pascal_case(text='api_request_otp')
        'ApiRequestOtp'
    """

    return ''.join(
        word.capitalize() for word in text.split('_')
    )


def extract_name_from_email(email: str) -> str:
    """Extracts name from given email.

    Usage:
        >>> extract_name_from_email(email='john.doe_123@example.com')
        'John Doe'

    """
    # Get the name for fallback
    name, *_ = email.split('@')

    # Extract the part before @
    match = re.match(r"([^@]+)", email)

    if match:
        try:
            #
            # Try getting a nicer name
            name = match.group(1)
            # Replace non-alphabetic characters with space
            name = re.sub(r"[\W\d_]+", " ", name).strip().title()

        except Exception:
            pass

    return apply_title_case(name)

