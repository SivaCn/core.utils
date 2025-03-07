# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to to avoid the overwriting of the constants and any
    objects that needs to be restricted.

    This module was borrowed from the frozenobj from pypi.org,
    Refer: https://pypi.org/project/frozenobj/
    Note: this module has a dependency of `lazy-object-proxy`

    The frozenobj module is copied here, since it's single module and to avoid
    any accidental loses or changes from the maintainers

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import types

from weakref import WeakValueDictionary
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from lazy_object_proxy import Proxy
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #

# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class ImmutableError(Exception):
    """ Attempted to change an immutable object. """


def is_mutable(obj):
    """
    Test whether `obj` is in a list of known immutables. May misclassify immutable objects as mutable.
    (Of course someone could do `function.bla = 42`; this just protects against accidental changes, not hackers.)
    """
    if obj is None:
        return False
    if isinstance(obj, (int, float, bool, str, tuple, types.MethodType, types.FunctionType, ImmutableProxy)):
        return False
    return True


class ImmutableProxy(Proxy):
    """Immutable proxy; any attempted changes raise an exception
    (underlying object can still be changed by those that have a reference).
    """
    def __setattr__(self, name, value, __setattr__=object.__setattr__):
        raise ImmutableError('frozenobj, attributes cannot be assigned')

    def __delattr__(self, name, __delattr__=object.__delattr__):
        raise ImmutableError('frozenobj, attributes cannot be deleted')

    def __getattr__(self, name):
        obj = super(ImmutableProxy, self).__getattr__(name)
        return frozen(obj)

    def __setitem__(self, key, value):
        raise ImmutableError('frozenobj, items cannot be assigned')

    def __delitem__(self, key):
        raise ImmutableError('frozenobj, items cannot be deleted')

    def __getitem__(self, key):
        obj = super(ImmutableProxy, self).__getitem__(key)
        return frozen(obj)

    def __setslice__(self, i, j, value):
        raise ImmutableError('frozenobj, slices cannot be assigned')

    def __delslice__(self, i, j):
        raise ImmutableError('frozenobj, slices cannot be deleted')

    def __getslice__(self, i, j):
        obj = super(ImmutableProxy, self).__getslice__(i, j)
        return frozen(obj)

    def __iadd__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __isub__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __imul__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __idiv__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __itruediv__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __ifloordiv__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __imod__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __ipow__(self, other, *args):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __ilshift__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __irshift__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __iand__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __ixor__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')

    def __ior__(self, other):
        raise ImmutableError('frozenobj, it cannot be changed in place')


class ListProxy(ImmutableProxy):

    def report_error(self):
        raise ImmutableError('frozenobj, it cannot be changed')

    def append(self, p_object):
        self.report_error()

    def clear(self):
        self.report_error()

    def extend(self, iterable):
        self.report_error()

    def insert(self, index, p_object):
        self.report_error()

    def pop(self, index=None):
        self.report_error()

    def remove(self, value):
        self.report_error()

    def reverse(self):
        self.report_error()

    def sort(self, key=None, reverse=False):
        self.report_error()


class DictProxy(ImmutableProxy):

    def report_error(self):
        raise ImmutableError('frozenobj, it cannot be changed')

    def clear(self):
        self.report_error()

    def pop(self, k, d=None):
        self.report_error()

    def popitem(self):
        self.report_error()

    def setdefault(self, k, d=None):
        self.report_error()

    def update(self, E=None, **F):
        self.report_error()


class SetProxy(ImmutableProxy):

    def report_error(self):
        raise ImmutableError('set "{0:}" is frozenobj; it cannot be changed'.format(self))

    def add(self, *args, **kwargs):
        self.report_error()

    def clear(self, *args, **kwargs):
        self.report_error()

    def difference_update(self, *args, **kwargs):
        self.report_error()

    def discard(self, *args, **kwargs):
        self.report_error()

    def intersection_update(self, *args, **kwargs):
        self.report_error()

    def pop(self, *args, **kwargs):
        self.report_error()

    def remove(self, *args, **kwargs):
        self.report_error()

    def symmetric_difference_update(self, *args, **kwargs):
        self.report_error()

    def update(self, *args, **kwargs):
        self.report_error()


_IMMUTABLES_CACHE = WeakValueDictionary()


def frozen(obj):
    if is_mutable(obj):
        if not _IMMUTABLES_CACHE.get(id(obj), None):
            # print('cache miss for',id(obj))
            proxy = ImmutableProxy
            if isinstance(obj, list):
                proxy = ListProxy
            if isinstance(obj, dict):
                proxy = DictProxy
            if isinstance(obj, set):
                proxy = SetProxy
            imobj = proxy(lambda: obj)
            # print('created', imobj, 'for', obj)
            _IMMUTABLES_CACHE[id(obj)] = imobj
        return _IMMUTABLES_CACHE[id(obj)]
    return obj

