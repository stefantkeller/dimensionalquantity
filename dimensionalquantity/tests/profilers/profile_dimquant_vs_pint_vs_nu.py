#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" This script is supposed to be run with line_profiler or memory_profiler:
    $ pip3 install line_profiler
    $ pip3 install memory_profiler psutil
    To run the profiling:
    $ kernprof -v -l this_script.py
    or
    $ python3 -m memory_profiler this_script.py
    respectively.
    The @profile decorators used below is used by line_profiler and memory_profiler.
    If this script is run with regular python
    $ python3 this_script.py
    instead of the specified ways above, those decorators will cause problems."""

import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

import numericalunits as nu
nu.reset_units()

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ

@profile
def multiplying_Q_many_times():
    dq_1m = DQ(1, D({'L':1}))
    pint_1m = 1*ureg.meter
    nu_1m = 1*nu.m
    normal_int = 1
    for i in range(1000):
        dq_1m *= dq_1m
        pint_1m *= pint_1m
        nu_1m *= nu_1m
        normal_int *= normal_int

@profile
def create_many_instances():
    bigN = 1000
    for j in range(bigN): pint_m = Q_('{} m'.format(j))
    for j in range(bigN): pint_kg = Q_('{} kg'.format(j))
    for j in range(bigN): nu_m = j*nu.m
    for j in range(bigN): nu_kg = j*nu.kg
    for j in range(bigN): dq_m = DQ('{} m'.format(j))
    for j in range(bigN): dq_kg = DQ('{} kg'.format(j))
    for j in range(bigN): normal_int = int(j)
    for j in range(bigN): normal_string = '{} m'.format(j)
    for j in range(bigN): normal_dict = dict(j=j)

if __name__=="__main__":
    multiplying_Q_many_times()
    create_many_instances()
