#! /usr/bin/python3
# -*- coding: utf-8 -*-

# wrapper for Dimensional operations (such as __add__, __sub__) to
# i.   make code more readable by putting reoccuring stuff here,
# ii.  make behavior more intuitive (Dimensional looks like a dict,
#      so it should at least run silently for dicts),
# iii. report sensible error messages
def compatible_with_operation(operation='<undefined>'):
    def decorate_specified_operation(method):
        def decorated(self, other, **kwargs):
            try:
                return method(self, other)
            except (KeyError, AttributeError):
                # while technically an error, for the user there is no real difference
                # between a Dimensional and a dict or ordered_dict or default_dict, etc.
                # hence KeyError is easy to fix:
                # input 'other' has to be converted into Dimensional
                # (if compatible with dict)
                # otherwise the 'KeyError' is actually a TypeError
                # note: isinstance(other, dict) is True also derived instances
                # such as defaultdict or OrderedDict
                if isinstance(other, dict):
                    return method(self, Dimensional(other))
                else:
                    raise TypeError(''.join(['unsupported operand type(s) for {}:'.format(operation),
                                             ' \'{}\' and \'{}\''.format(type(self).__name__,
                                                                         type(other).__name__)]))
        return decorated
    return decorate_specified_operation

class Dimensional(dict):
    def __getitem__(self, key):
        return super(Dimensional, self).get(key,0)
    
    @compatible_with_operation('+')
    def __add__(self, other):
        return Dimensional({key:self[key]+other[key] for key in set(self.keys()).union(other.keys())})

    @compatible_with_operation('+')
    def __radd__(self, other):
        return self.__add__(other)
        
    @compatible_with_operation('-')
    def __sub__(self, other):
        return Dimensional({key:self[key]-other[key] for key in set(self.keys()).union(other.keys())})
    
    @compatible_with_operation('-')
    def __rsub__(self, other):
        return Dimensional({key:other[key]-self[key] for key in set(self.keys()).union(other.keys())})
        


