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
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


def get_build_path():
    """."""

    _dir, _file = os.path.split(os.path.abspath(__file__))
    _drive, _path = os.path.splitdrive(_dir)

    return os.path.join(os.sep, *_path.split(os.sep)[:-4])
