# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os
import random
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from ConfigParser import SafeConfigParser
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class CustomConfigParser(object):

    def __init__(self, filename):
        self.filename = filename

        self.config = SafeConfigParser()
        self.config.read(filename)

    def section_as_dict(self, section):
        """."""
        if not self.config.has_section(section):
            return dict()

        return {
            _option: self.config.get(section, _option)
            for _option in self.config.options(section)
        }


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


def get_ordinal(num):

    if not num:
        return num

    if isinstance(num, str) and not num.isdigit():
        return num

    num = int(num)
    return "{}{}".format(
        num,
        "th" if 4<=num%100<=20 else {1:"st", 2:"nd", 3:"rd"}.get(num%10, "th")
    )


def generate_otp():

    from core.utils.environ import get_general_configs

    return int(
        ''.join(
            [str(random.randint(1, 9))
             for _ in range(get_general_configs()['otp_code_digits'])
             ]
        )
    )
