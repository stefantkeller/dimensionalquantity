#! /usr/bin/python3
# -*- coding: utf-8 -*-

from . dimensional import Dimensional as D

class DimQuant(object):
    def __init__(self, numeric=0, dimensions=D({})):
        self.numeric=numeric
        self.dimensions=dimensions

    @property
    def numeric(self):
        return self.__numeric
    @numeric.setter
    def numeric(self, value):
        if isinstance(value, (int, float, complex)) \
                and not isinstance(value, bool): # note: bool is instance of int but that doesn't make sense here!
            self.__numeric = value
        else:
            raise TypeError('Numeric value isn\'t a numeric type but of \'{}\' instead.'.format(type(value)))

    @property
    def dimensions(self):
        return self.__dimensions
    @dimensions.setter
    def dimensions(self, dims):
        if isinstance(dims, D):
            self.__dimensions = dims
        elif isinstance(dims, dict):
            self.__dimensions = D(dims)
        else:
            raise TypeError('Dimensions aren\'t of type \'Dimensional\' but of \'{}\' instead.'.format(type(dims)))
    
    @compatible_with_linear_operation('+')
    def __add__(self, other):
        pass
    @compatible_with_linear_operation('+')
    def __radd__(self, other):
        self.__add__(other)

    @compatible_with_linear_operation('-')
    def __sub__(self, other):
        pass
    @compatible_with_linear_operation('-')
    def __rsub__(self, other):
        pass

    def __mul__(self, other):
        pass
    def __rmul__(self, other):
        pass

    def __div__(self, other):
        pass
    def __rdiv__(self, other):
        pass

    def __pow__(self, other):
        pass
    def __rpow__(self, other):
        raise NotImplementedError(' '.join(['The exponent cannot be a dimensional quantity,',\
                                            'it has to be a purely numerical value!']))
