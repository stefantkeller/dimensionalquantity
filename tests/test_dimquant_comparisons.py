#! /usr/bin/python3
# -*- coding: utf-8 -*-

import pytest

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ

def test_eq():
    q0 = DQ(1, D({'a':1, 'b':0, 'c':0}))
    q1 = DQ(1, D({'a':1, 'b':0, 'c':0}))

    assert(q0 == q1)

def test_eq_non_dimensional_DQ():
    q0 = DQ(1)
    assert( q0 == 1 )
    q1 = DQ(1, {'a':0})
    assert( q1==1 )
    q2 = DQ(1, {'a':1})
    with pytest.raises(TypeError):
        a = (q2==1)
    with pytest.raises(NotImplementedError):
        a = (q1==q2)

def test_gt():
    q0 = DQ(2)
    q1 = DQ(1)
    assert(q0>q1)
    assert(q0>1)
    q2 = DQ(1, {'a':1})
    with pytest.raises(TypeError):
        a = (q2>0)
    with pytest.raises(NotImplementedError):
        a = (q0>q2)
    q0.dimensions = D({'a':1})
    assert(q0>q2)

def test_lt():
    q0 = DQ(2)
    q1 = DQ(1)
    assert(q1<q0)
    q2 = DQ(1, {'a':1})
    with pytest.raises(TypeError):
        q0<=q2
