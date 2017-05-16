#! /usr/bin/python3
# -*- coding: utf-8 -*-

from . dimensional import Dimensional as D

# like compatible_with_operation() for Dimensional but expl. only for __add__ and __sub__
def compatible_with_linear_operation(operation='<undefined>'):
    def decorate_specified_operation(method):
        def decorated(self, other, **kwargs):
            if not isinstance(other, DimQuant):
                raise TypeError(''.join(['unsupported operand type(s) for {}:'.format(operation),
                                         ' \'{}\' and \'{}\''.format(type(self).__name__,
                                                                     type(other).__name__)]))
            elif self.dimensions!=other.dimensions:
                raise ValueError(''.join(['Operation {} requires'.format(operation),
                                          'the two operands to have equal dimensions.']))
            else:
                return method(self, other)
        return decorated
    return decorate_specified_operation


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
            raise TypeError('Numeric value isn\'t a numeric type but of \'{}\' instead.'.format(type(value).__name__))

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
            raise TypeError('Dimensions aren\'t of type \'Dimensional\' but of \'{}\' instead.'.format(type(dims).__name__))
    
    @compatible_with_linear_operation('+')
    def __add__(self, other):
        return DimQuant(numeric = self.numeric+other.numeric,\
                        dimensions = D(self.dimensions))
    # the __radd__ isn't actually necessary
    # because the compatible_with_linear_operation decorator
    # anyway only accepts other's of DimQuant type
    # hence, the only time __radd__ would come into play would be
    # to throw a TypeError; which we can easily leave for other to throw.
    #@compatible_with_linear_operation('+')
    #def __radd__(self, other):
    #    self.__add__(other)

    @compatible_with_linear_operation('-')
    def __sub__(self, other):
        return DimQuant(numeric = self.numeric-other.numeric,\
                        dimensions = D(self.dimensions))
    # not implementing __rsub__ for same reason as __radd__
    #@compatible_with_linear_operation('-')
    #def __rsub__(self, other):
    #    return -self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, DimQuant):
            return DimQuant(numeric = self.numeric*other.numeric,\
                            dimensions = self.dimensions+other.dimensions)
        else:
            return DimQuant(numeric = self.numeric*other,\
                            dimensions = D(self.dimensions))
    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        if isinstance(other, DimQuant): 
            return DimQuant(numeric = self.numeric/other.numeric,\
                            dimensions = self.dimensions-other.dimensions)
        else:
            return DimQuant(numeric = self.numeric/other,\
                            dimensions = D(self.dimensions))

    def __rtruediv__(self, other):
        # if isinstance(other, DimQuant): this case is covered by __truediv__
        return DimQuant(numeric = other/self.numeric,\
                        dimensions = -1*D(self.dimensions))

    # __pow__ makes sense only if the exponent is either not an instance of DimQuant
    # or if all entries of DimQuant.dimensions are 0
    def __pow__(self, other):
        if not isinstance(other, DimQuant):
            return DimQuant(numeric = self.numeric**other,\
                            dimensions = self.dimensions*other)
        else:
            if any(other.dimensions.values()):
                raise NotImplementedError(' '.join(['The exponent cannot be a dimensional quantity,',\
                                                    'it has to be a purely numerical value!']))
            else:
                if any(self.dimensions.values()):
                    return self**other.numeric
                else:
                    return self.numeric**other.numeric
    def __rpow__(self, other):
        return DimQuant(other)**self

    def __eq__(self, other):
        if not isinstance(other, DimQuant):
            return False
        else:
            return (self.numeric == other.numeric \
                    and self.dimensions == other.dimensions)
