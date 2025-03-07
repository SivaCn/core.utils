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
from string import Template
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
# ----------- END: In-App Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def string_substitute(string, substitutes):

    if not isinstance(string, str):
        raise TypeError(
            f"Argument string is expected as string type, Got {type(string).__name__}"
        )

    return Template(string).safe_substitute(substitutes)

