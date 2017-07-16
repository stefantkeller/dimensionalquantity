#! /usr/bin/python3
# -*- coding: utf-8 -*-

import re # https://docs.python.org/3/library/re.html#writing-a-tokenizer
from collections import namedtuple

from . import Dimensional as D
from . import BaseDimQuant as DQ


# https://docs.python.org/3/library/re.html#writing-a-tokenizer
Token = namedtuple('Token', ['typ', 'value'])

SI_unit_LUT = {'m': DQ(1, {'L':1}),
               's': DQ(1, {'t':1}),
               'K': DQ(1, {'T':1}),
               'A': DQ(1, {'i':1}),
               'mol': DQ(1, {'N':1}),
               'cd': DQ(1, {'J':1}),
               # SI uses 'kg' as base unit, i.e. '1e3 g',
               # but instead of creating a special case,
               # initalizing 'g' as basic seems to be cleaner.
               'g': DQ(1e-3, {'M':1}), 
               }

SI_prefix_LUT = {'Y': 1e24,
                 'Z': 1e21,
                 'E': 1e18,
                 'P': 1e15,
                 'T': 1e12,
                 'G': 1e9,
                 'M': 1e6,
                 'k': 1e3,
                 'h': 1e2,
                 #'da': 1e1, # TBD: this is the only prefix needing more than one character
                 '': 1e0,
                 'd': 1e-1,
                 'c': 1e-2,
                 'm': 1e-3,
                 'u': 1e-6,
                 'n': 1e-9,
                 'p': 1e-12,
                 'f': 1e-15,
                 'a': 1e-18,
                 'z': 1e-21,
                 'y': 1e-24,
                 }

class BasicTranslator(object):
    # the following protected entries are available (and identical)
    # for all instances of Translator()
    # https://docs.python.org/3/library/re.html#writing-a-tokenizer
    _token_specification = [
        ('UNIT',  r'[A-Za-z]+'), # any collection of letters...
        ('HOWOFTEN', r'(\-)?(\d+(\.\d+)?)'), # a (possibly negative) (float) number
        ('SEP',r'\.'),            # '.' is a separator, has no real functionality except to help understand from where to where a unit goes
        ('NEGSEP',r'\/'),            # m/s should be the same as m.s-1; NEGSEP makes sure we don't miss the '-1'
        ('GROUPOPEN', r'\('), # stuff between (...) should both apply to '/' inverting the sign of the exponents as well as exponents overall
        ('GROUPCLOSE', r'\)'),
        ]
    _token_grammar = '|'.join('(?P<%s>%s)' % pair for pair in _token_specification)
    _token_program = re.compile(_token_grammar)

    def __init__(self):
        self._unit_LUT = {}
        self._prefix_LUT = {}

    @classmethod
    def _tokenize(cls, string):
        yield Token('GROUPOPEN','^')
        for match in cls._token_program.finditer(string):
            kind = match.lastgroup
            value = match.group(kind)
            if kind=='UNIT':
                yield Token('GROUPOPEN','(')
                yield Token('UNIT', value)
                yield Token('GROUPCLOSE', ')')
            else:
                yield Token(kind, value)
        yield Token('GROUPCLOSE','$')

    def _process_tokens(self, tokens, sign=1, parens_ineq=-1):
        # parens_ineq starts at -1 because tokenizer wraps everything within ^...$,
        # so that an equal parens has still one left (from ^);
        # hence either weassume equal==1 (which looks unintuitive)
        # or we start with a -1 offset
        _collection = []
        _D = D()
        conversion_factor = 1
        for token in tokens:
            if token.typ=='GROUPCLOSE':
                _collection.append( _D )
                parens_ineq -= 1
                return _collection, conversion_factor, parens_ineq # this return will be seen only by recursive call from GROUPOPEN
            if token.typ=='NEGSEP':
                if parens_ineq==0:
                    sign = -1
                else:
                    sign *= -1
            if token.typ=='GROUPOPEN':
                parens_ineq += 1
                lower_coll, _cf, parens_ineq = self._process_tokens(tokens, sign, parens_ineq)
                conversion_factor *= _cf
                lower_coll[-1] *= sign
                _lower = D() 
                for _d in lower_coll:
                    _lower += _d
                _collection.append( _lower )
            if token.typ=='UNIT':
                _DQ = self._process_unit(token.value)
                _D += _DQ.dimensions
                conversion_factor *= _DQ.numeric
            if token.typ=='SEP':
                if parens_ineq==0:
                    sign = (-1)**parens_ineq
                else:
                    pass
            if token.typ=='HOWOFTEN':
                _collection[-1] *= float(token.value)
        return DQ(conversion_factor, _collection[-1])

    def _process_unit(self, unit_value):
        if unit_value in self._unit_LUT.keys():
            return self._unit_LUT[unit_value]
        if len(unit_value)>=2:
            prefix = unit_value[0]
            unit_value = unit_value[1:]
            if unit_value not in self._unit_LUT.keys(): 
                raise KeyError(' '.join(['{} doesn\'t recognize'.format(type(self).__name__),
                                         'symbol {}'.format(unit_value),
                                         'and can thus not translate it into a DimQuant.']))
            if prefix not in self._prefix_LUT.keys():
                raise KeyError(' '.join(['{} doesn\'t recognize'.format(type(self).__name__),
                                         'prefix \'{}\''.format(prefix),
                                         'of unit \'{}\'.'.format(unit_value)]))
            return self._unit_LUT[unit_value]*self._prefix_LUT[prefix]
        else:
            raise ValueError(' '.join(['Cannot recognize a registered unit pattern',
                                        'in \'{}\'.'.format(unit_value),
                                        'to translate into a DimQuant']))

    def translate(self, string):
        tokens = self._tokenize(string)
        return self._process_tokens(tokens)

    def register_unit_LUT(self, unit_LUT, overwrite=False):
        if overwrite:
            self._unit_LUT = dict(unit_LUT) #copy to have different pointer to avoid spooky action from a distance
        else:
            for (symbol, dimension) in unit_LUT.items():
                if symbol in self._unit_LUT.keys():
                    raise ValueError(' '.join(['Cannot register rule to translate',
                                               'symbol \'{}\' into dimension \'{}\''.format(symbol, dimension),
                                               'because this symbol is already registered with',
                                               'dimension \'{}\'.'.format(symbol)]))
                else:
                    self._unit_LUT[symbol] = dimension

    def register_prefix_LUT(self, prefix_LUT, overwrite=False):
        if overwrite:
            self._prefix_LUT = dict(prefix_LUT) #copy to have different pointer to avoid spooky action from a distance
        else:
            for (symbol, value) in prefix_LUT.items():
                if symbol in self._prefix_LUT.keys():
                    raise ValueError(' '.join(['Cannot register prefix \'{}\''.format(symbol),
                                               'because this symbol is already used.']))
                else:
                    self._prefix_LUT[symbol] = value

class Translator(BasicTranslator):
    def __init__(self):
        super(Translator, self).__init__()
        self.register_unit_LUT(SI_unit_LUT)
        self.register_prefix_LUT(SI_prefix_LUT)


