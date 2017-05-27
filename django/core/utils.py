# coding: utf8
"""Utilities module."""
from __future__ import unicode_literals

from inspect import isroutine

from six import string_types


def getprop(obj, name):
    """Get property."""
    result = ''
    for prop in name.split('.'):
        obj = getattr(obj, prop)
        if isroutine(obj):
            obj = obj()
        result = obj if isinstance(obj, string_types) else str(obj)
    return result


def tostr(obj, *fields):
    """Get obj representation."""
    return '{0}: {1}'.format(
        type(obj).__name__,
        '|'.join(
            ['{0}={1}'.format(field, getprop(obj, field)) for field in fields]
        )
    )
