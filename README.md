Test benchmark for:
* https://pypi.python.org/pypi/numericalunits
* https://pypi.python.org/pypi/Pint/0.7.2

posible implementation:

D = namedtuple('D', 'L M T I ...') # complete SI quantities
a=D(1,2,3,4)
b=D(0,0,0,1)
c=D(*zip(np.sum([a,b],axis=0)))
