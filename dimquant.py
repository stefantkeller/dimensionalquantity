#! /usr/bin/python3
# -*- coding: utf-8 -*-

from . import Dimensional as D
from . import BaseDimQuant
from . import Translator

class DimQuant(BaseDimQuant):
    _T = Translator()

    def __init__(self, *args, **kwargs):
        if len(args)==1 and isinstance(args[0], str):
            dq_string = args[0]
            _q, _d = dq_string.split(' ')
            _DQ = self._T.translate(_d)
            self.numeric = _DQ.numeric * float(_q)
            self.dimensions = _DQ.dimensions
        else:
            super(DimQuant, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'DimQuant({}, {})'.format(self.numeric,self.dimensions)

    def __str__(self):
        unit_string = self._T.reverse_unit_lookup(self.dimensions)
        return ' '.join([str(self.numeric), unit_string])

    @classmethod
    def register_translator(cls, translator):
        cls._T = translator
