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

@pytest.mark.parametrize('expected_str,dq',(
                         ('1 m.s-1',DQ(1, D({'L': 1, 't': -1}))),
                         ('2 m.s-1',DQ(2, D({'L': 1, 't': -1}))),
                         ('1 m2.s-1',DQ(1, D({'L': 2, 't': -1}))),
                        ))
def test_dimquant_str_out(expected_str,dq):
    assert( str(dq)==expected_str )

@pytest.mark.parametrize('expected_repr,dq',(
                         ('DimQuant(1, Dimensional({\'L\': 1, \'t\': -1}))',
                             DQ(1, D({'L': 1, 't': -1}))),
                         ('DimQuant(2, Dimensional({\'L\': 1, \'t\': -1}))',
                             DQ(2, D({'L': 1, 't': -1}))),
                         ('DimQuant(1, Dimensional({\'L\': 2, \'t\': -1}))',
                             DQ(1, D({'L': 2, 't': -1}))),
                        ))
def test_dimquant_repr_out(expected_repr,dq):
    assert( repr(dq)==expected_repr )

