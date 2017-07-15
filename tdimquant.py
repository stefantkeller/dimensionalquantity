#! /usr/bin/python3
# -*- coding: utf-8 -*-

from . import Dimensional as D
from . import DimQuant
from . import Translator

class TDimQuant(DimQuant):
    _T = Translator()

    def __init__(self, *args, **kwargs):
        dq_string = args[0]
        if len(args)==1 and isinstance(dq_string, str):
            _q, _d = dq_string.split(' ')
            _DQ = self._T.translate(_d)
            self.numeric = _DQ.numeric * float(_q)
            self.dimensions = _DQ.dimensions
        else:
            super(TDimQuant, self).__init__(*args, **kwargs)

    @classmethod
    def register_translator(cls, translator):
        cls._T = translator
