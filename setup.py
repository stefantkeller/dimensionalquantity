"""Following
Ninad Sathaye, ``Learning Python Application Development,'' by PacktPub, 2016,
https://www.packtpub.com/application-development/learning-python-application-development
"""
from distutils.core import setup

with open('README.md') as file_:
    readme = file_.read()

setup(
    name='dimensionalquantity',
    version='0.4.4',
    packages=['dimensionalquantity','dimensionalquantity/tests'],
    url='https://testpypi.python.org/pypi/dimensionalquantity/',
    license='LICENSE',
    description='Conveniently attach units to numbers.',
    long_description=readme,
    author='Stefan T. Keller',
    author_email='stefantkeller@gmail.com'
)
