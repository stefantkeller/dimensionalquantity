#! /usr/bin/python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

import pytest

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ

def test_dimquant_with_str_init():
    q0 = DQ('1 m')
    q1 = DQ('1 s')
    q2 = DQ('1 m/s')
    assert( q2==(q0/q1) )
    q2_ = DQ('1 m.s-1')
    assert( q2==q2_ )

def test_dimquant_str_out():
    q0 = DQ(1, D({'L': 1, 't': -1}))
    assert( str(q0)=='1 m.s-1' )

def test_dimquant_repr_out():
    q0 = DQ(1, D({'L': 1, 't': -1}))
    assert( repr(q0)=='DimQuant(1, Dimensional({\'L\': 1, \'t\': -1}))' )

