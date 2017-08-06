#! /usr/bin/python3
# -*- coding: utf-8 -*-

import inspect

import pytest

from dimensionalquantity import Dimensional as D
from dimensionalquantity import BaseDimQuant as BDQ
from dimensionalquantity import DimQuant as DQ
from dimensionalquantity import BasicTranslator as BT
from dimensionalquantity import Translator as T
import dimensionalquantity

"""
Purpose of the following test(s):
    Verify whether all "public" methods are documented.
    These tests cannot assure that said documentation is any good;
    the tests pass as soon as the "public" elements have a non-None __doc__.
    With "public" I refer to any method not starting with a "_".
    The underscore methods aren't supposed to be used by 3rd parties anyway,
    hence no need for a doc-string.
"""

def inspect_selected_members(of_what):
    """This function shortens the inspect.getmembers(...) call;
    in an attempt to make the pytest.mark.parametrize() more readable."""
    return inspect.getmembers(of_what,
                              predicate=lambda x: (
                                  hasattr(x, '__doc__') and \
                                  hasattr(x, '__name__') and \
                                  not x.__name__.startswith('_') )
                             )

@pytest.mark.parametrize('name,documentable',
                         inspect_selected_members(dimensionalquantity) )
def test_doc_string_coverage(name,documentable):
    """Note: `name` isn't used explicitly,
    but (i) since pytest prints the input arguments of a failing test,
    having `name` available makes it simpler to trace back where the test failed;
    and (ii) the unpacked response of inspect.getmembers() *is* two values."""
    if documentable.__doc__ is None:
        raise NotImplementedError('Doc-string missing for {}!'.format(
                                    documentable.__name__))
