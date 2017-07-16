#! /usr/bin/python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import pytest

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ
from dimensionalquantity import Translator


def test_SI_dimensions():
    T = Translator()
    # http://www.bipm.org/en/publications/si-brochure/section1-3.html
    assert( T.translate('m').dimensions==D({'L': 1}) )
    assert( T.translate('s').dimensions==D({'t': 1}) ) # 't' instead of suggested (by SI) 'T' because
    assert( T.translate('K').dimensions==D({'T': 1}) ) # the suggested \theta doesn't quite work, hence 'T' here.
    assert( T.translate('A').dimensions==D({'i': 1}) ) # lower case 'i' instead of upper 'I' to avoid confusion between (1, l, I) (one, lower L, upper i)
    assert( T.translate('mol').dimensions==D({'N': 1}) )
    assert( T.translate('cd').dimensions==D({'J': 1}) )
    assert( T.translate('kg').dimensions==D({'M': 1}) )

def test_SI_dimension_m_multiples():
    T = Translator()
    q0 = T.translate('m').dimensions
    d0 = D({'L': 1})
    assert( q0==d0 )
    q1 = T.translate('m2').dimensions
    d1 = D({'L': 2})
    assert( q1==d1 )
    q2 = T.translate('m-2').dimensions
    d2 = D({'L': -2})
    assert( q2==d2 )

def test_translating_complex_strings():
    T = Translator()
    string = '(kg.s)-2/((m3/K)-3/A2)'
    res = T.translate(string).dimensions
    _D = D({'M': -2.0, 't': -2.0, 'L': 9.0, 'T': -3.0, 'i': 2.0})
    assert( res==_D )
    string = '(kg.s)2/((m3/K)-3/A2)'
    res = T.translate(string).dimensions
    _D = D({'M': 2.0, 't': 2.0, 'L': 9.0, 'T': -3.0, 'i': 2.0})
    assert( res==_D )
    string = '(kg.s)2/(m3/K)-3/A2'
    res = T.translate(string).dimensions
    _D = D({'M': 2.0, 't': 2.0, 'L': 9.0, 'T': -3.0, 'i': -2.0})
    assert( res==_D )
    string = '(kg.s)2/(m3/K)-3/A-2'
    res = T.translate(string).dimensions
    _D = D({'M': 2.0, 't': 2.0, 'L': 9.0, 'T': -3.0, 'i': 2.0})
    assert( res==_D )
    string = '(kg.s)2/(m3/K)3/A-2'
    res = T.translate(string).dimensions
    _D = D({'M': 2.0, 't': 2.0, 'L': -9.0, 'T': 3.0, 'i': 2.0})
    assert( res==_D )
