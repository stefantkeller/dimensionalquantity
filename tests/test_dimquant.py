#! /usr/bin/python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import pytest

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ

def test_DQ_default_init():
    default = DQ()
    assert( default.numeric==0 )
    assert( default.dimensions==D() )

def test_numeric_value_settings():
    with pytest.raises(TypeError):
        test = DQ(numeric='1',dimensions=D())
    with pytest.raises(TypeError):
        test = DQ(numeric=(1,1),dimensions=D())
    with pytest.raises(TypeError):
        test = DQ(numeric=True,dimensions=D())
    valid = DQ(numeric=1)
    valid = DQ(numeric=1.0)
    valid = DQ(numeric=1+2j)

def test_dimensions_settings():
    valid = DQ(dimensions={'a':1})
    valid = DQ(dimensions=OrderedDict({'a':1}))
    valid = DQ(dimensions=D({'a':1}))
    with pytest.raises(TypeError):
        test = DQ(dimensions=1)
    with pytest.raises(TypeError):
        test = DQ(dimensions='1')
    with pytest.raises(TypeError):
        test = DQ(dimensions=(1,2))
    with pytest.raises(TypeError):
        test = DQ(dimensions=[1,2])

def test_add_wrong_dimensions():
    q0 = DQ(1,{'a':2})
    q1 = DQ(1,{'a':1})
    q2 = DQ(1,{'b':1})
    with pytest.raises(ValueError):
        q3 = q0+q1
    with pytest.raises(ValueError):
        q3 = q0+q2

def test_add_wrong_type():
    q0 = DQ()
    with pytest.raises(TypeError):
        q1 = 1+q0
    with pytest.raises(TypeError):
        q1 = q0+1

def test_add_create_new_instances():
    q0 = DQ()
    q1 = DQ()
    q2 = q0+q1

    assert(id(q0)!=id(q2) and id(q1)!=id(q2))

