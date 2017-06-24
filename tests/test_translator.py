#! /usr/bin/python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import pytest

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ
from dimensionalquantity import BaseTranslator as BT

def test_SI_dimensions():
    # http://www.bipm.org/en/publications/si-brochure/section1-3.html
    assert( BT('m')==D({'L': 1}) )
    assert( BT('s')==D({'t': 1}) ) # 't' instead of suggested (by SI) 'T' because
    assert( BT('K')==D({'T': 1}) ) # the suggested \theta doesn't quite work, hence 'T' here.
    assert( BT('A')==D({'i': 1}) ) # lower case 'i' instead of upper 'I' to avoid confusion between (1, l, I) (one, lower L, upper i)
    assert( BT('mol')==D({'N': 1}) )
    assert( BT('cd')==D({'J': 1}) )
    assert( BT('kg')==D({'M': 1}) )

def test_SI_dimension_m_multiples():
    q0 = BT('m')
    d0 = D({'L': 1})
    assert( q0==d0 )
    q1 = BT('m2')
    d1 = D({'L': 2})
    assert( q1==d1 )
    q2 = BT('m-2')
    d2 = D({'L': -2})
    assert( q2==d2 )

