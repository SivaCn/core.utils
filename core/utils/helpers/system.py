# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry
    level.

"""

# ----------- START: Native Imports ---------- #
import os
import time
import shlex
import psutil
import shutil

from subprocess import (
    Popen, PIPE
)
# ----------- END: Native Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.error import (
    DirectoryNotFoundError,
)
# ----------- END: In-App Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #


__all__ = [
    # All public symbols go here.
]


def remove_file(file_name):

    if os.path.exists(file_name):
        os.remove(file_name)


def remove_dir(dir_name, recursive=False):

    if not os.path.exists(dir_name):
        return

    if not os.path.isdir(dir_name):
        raise DirectoryNotFoundError("Supplied path is not a directory")

    if recursive:
        shutil.rmtree(dir_name)
    else:
        os.rmdir(dir_name)


def fork(command):

    if isinstance(command, str):
        command = shlex.split(command)

    return Popen(command, stdout=PIPE, stderr=PIPE)


def process_info(pid):

    try:
        #
        # ``process_iter.as_dict`` raises ``psutil.NoSuchProcess`` error when the process is not available
        info = [proc.as_dict()for proc in psutil.process_iter() if proc.pid == pid]

    except Exception:
        info = None

    return info[0] if info else None


def get_process_handler(pid):

    return psutil.Process(pid)


def terminate_process(pid):

    status = False
    for _ in range(3):
        try:
            get_process_handler(pid).kill()
        except psutil.NoSuchProcess:
            pass

        if not process_info(pid):
            status = True
            break

        time.sleep(0.1)

    return status

