__author__ = "Stefan T. Keller"
__version__ = '0.3'
# https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
#from pkg_resources import get_distribution
#__version__ = get_distribtion('dimensionalquantity').version
#__author__ =  get_distribtion('dimensionalquantity').author

from . dimensional import *
from . basedimquant import *
from . translator import *
from . dimquant import *
