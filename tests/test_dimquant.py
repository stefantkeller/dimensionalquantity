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

def test_add_create_new_instance_dimensions():
    q0 = DQ(dimensions=D({'a':-1}))
    q1 = DQ(dimensions=D({'a':-1}))
    q2 = q0+q1

    assert(q0.dimensions == q2.dimensions \
            and q1.dimensions == q2.dimensions)

    assert(id(q0.dimensions)!=id(q2.dimensions) \
            and id(q1.dimensions)!=id(q2.dimensions))

def test_add_basics():
    q0 = DQ(1, D({'a':1, 'b':0, 'c':0}))
    q1 = DQ(2, D({'a':1, 'b':0, 'c':0}))
    q2_exp = DQ(3, D({'a':1, 'b':0, 'c':0}))

    q2_real = q0 + q1

    assert(q2_exp.numeric == q2_real.numeric)
    assert(q2_exp.dimensions == q2_real.dimensions)

def test_eq():
    q0 = DQ(1, D({'a':1, 'b':0, 'c':0}))
    q1 = DQ(1, D({'a':1, 'b':0, 'c':0}))

    assert(q0 == q1)

def test_eq_fail_type():
    q0 = DQ(1)

    assert( not (q0 == 1) )

def test_sub_wrong_dimensions():
    q0 = DQ(1,{'a':2})
    q1 = DQ(1,{'a':1})
    q2 = DQ(1,{'b':1})
    with pytest.raises(ValueError):
        q3 = q0-q1
    with pytest.raises(ValueError):
        q3 = q0-q2

def test_sub_wrong_type():
    q0 = DQ()
    with pytest.raises(TypeError):
        q1 = 1-q0
    with pytest.raises(TypeError):
        q1 = q0-1

def test_sub_create_new_instances():
    q0 = DQ()
    q1 = DQ()
    q2 = q0-q1

    assert(id(q0)!=id(q2) and id(q1)!=id(q2))

def test_sub_create_new_instance_dimensions():
    q0 = DQ(dimensions=D({'a':-1}))
    q1 = DQ(dimensions=D({'a':-1}))
    q2 = q0-q1

    assert(q0.dimensions == q2.dimensions \
            and q1.dimensions == q2.dimensions)

    assert(id(q0.dimensions)!=id(q2.dimensions) \
            and id(q1.dimensions)!=id(q2.dimensions))

def test_sub_basics():
    q0 = DQ(1, D({'a':1, 'b':0, 'c':0}))
    q1 = DQ(2, D({'a':1, 'b':0, 'c':0}))
    q2_exp = DQ(-1, D({'a':1, 'b':0, 'c':0}))

    q2_real = q0 - q1

    assert(q2_exp.numeric == q2_real.numeric)
    assert(q2_exp.dimensions == q2_real.dimensions)


def test_mul_create_new_instances():
    q0 = DQ()
    q1 = DQ()
    q2 = q0*q1

    assert(id(q0)!=id(q2) and id(q1)!=id(q2))

def test_mul_create_new_instance_dimensions():
    q0 = DQ(2, dimensions=D({'a':-1}))
    q1 = DQ(3, dimensions=D({'a':-1}))
    q2_exp = DQ(6, D({'a':-2}))
    q2_real = q0*q1

    assert(q2_exp.dimensions == q2_real.dimensions)

    assert(id(q0.dimensions)!=id(q2_real.dimensions) \
            and id(q1.dimensions)!=id(q2_real.dimensions))

def test_mul_basics():
    q0 = DQ(2, D({'a':1, 'b':-1}))
    q1 = DQ(3, D({'b':1, 'c':1}))
    q2 = DQ(5, D({'c':2}))
    q01_exp = DQ(6, D({'a':1, 'b':0, 'c':1}))
    q02_exp = DQ(10, D({'a':1, 'b':-1, 'c':2}))

    q01_real = q0 * q1
    q02_real = q0 * q2

    assert(q01_exp.numeric == q01_real.numeric)
    assert(q01_exp.dimensions == q01_real.dimensions)
    assert(q02_exp.numeric == q02_real.numeric)
    assert(q02_exp.dimensions == q02_real.dimensions)

def test_mul_other_types():
    q0 = DQ(1)
    q1 = q0*2
    q1_ = 2*q0
    assert( q1==q1_ )
    assert( q1.numeric==2 )

def test_mul_other_incompat_types():
    q0 = DQ(1)
    with pytest.raises(TypeError):
        q1 = q0*[1]
    with pytest.raises(TypeError):
        q1 = (1,2)*q0
    with pytest.raises(TypeError):
        q1 = q0*{'a':1}

def test_div_create_new_instances():
    q0 = DQ(1)
    q1 = DQ(1)
    q2 = q0/q1

    assert(id(q0)!=id(q2) and id(q1)!=id(q2))

def test_div_ZeroDiv_with_default():
    q0 = DQ(1)
    q1 = DQ() # default value is 0
    with pytest.raises(ZeroDivisionError):
        q2 = q0/q1

def test_div_create_new_instance_dimensions():
    q0 = DQ(1, dimensions=D({'a':-1}))
    q1 = DQ(2, dimensions=D({'a':-1}))
    q2_exp = DQ(0.5, D({'a':0}))
    q2_real = q0/q1

    assert(q2_exp.dimensions == q2_real.dimensions)

    assert(id(q0.dimensions)!=id(q2_real.dimensions) \
            and id(q1.dimensions)!=id(q2_real.dimensions))

def test_div_basics():
    q0 = DQ(2, D({'a':1, 'b':-1}))
    q1 = DQ(8, D({'b':1, 'c':1}))
    q2 = DQ(0.5, D({'c':2}))
    q01_exp = DQ(0.25, D({'a':1, 'b':-2, 'c':-1}))
    q02_exp = DQ(4, D({'a':1, 'b':-1, 'c':-2}))

    q01_real = q0 / q1
    q02_real = q0 / q2

    assert(q01_exp.numeric == q01_real.numeric)
    assert(q01_exp.dimensions == q01_real.dimensions)
    assert(q02_exp.numeric == q02_real.numeric)
    assert(q02_exp.dimensions == q02_real.dimensions)

def test_div_other_types():
    q0 = DQ(1)
    q1 = q0/2
    assert( q1.numeric==0.5 )
    q2 = DQ(4)
    q3 = 1/q2
    q3_ = DQ(1/4)
    assert( q3.numeric==0.25 )
    assert( q3==q3_ )
    q4 = DQ(1, {'a':2})
    q5 = 1/q4
    q5_ = DQ(1, {'a':-2})
    assert( q5==q5_ )

def test_div_other_incompat_types():
    q0 = DQ(1)
    with pytest.raises(TypeError):
        q1 = q0/[1]
    with pytest.raises(TypeError):
        q1 = (1,2)/q0
    with pytest.raises(TypeError):
        q1 = q0/{'a':1}
