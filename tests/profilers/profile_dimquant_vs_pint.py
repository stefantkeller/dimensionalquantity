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

from dimensionalquantity import Dimensional as D
from dimensionalquantity import DimQuant as DQ

@profile
def multiplying_Q_many_times():
    dq_1m = DQ(1, D({'L':1}))
    pint_1m = 1*ureg.meter
    for i in range(1000):
        dq_1m *= dq_1m
        pint_1m *= pint_1m

if __name__=="__main__": multiplying_Q_many_times()
