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
