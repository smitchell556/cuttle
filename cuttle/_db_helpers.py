# -*- coding: utf-8 -*-
"""

This module contains functions to assist sql methods.

"""


def _nested_subclasses(cls):
    """
    Creates a list of all nested subclasses.
    """
    return cls.__subclasses__() + [s for sc in cls.__subclasses__()
                                   for s in _nested_subclasses(sc)]
