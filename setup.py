'''
*python-aalib* is a set of bindings for
`AAlib <http://aa-project.sourceforge.net/aalib/>`_,
an ASCII art library.
'''

classifiers = '''
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: POSIX
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Multimedia :: Graphics
'''.strip().splitlines()

import sys

import distutils.core
import distutils.command.build_py

try:
    # Python 3.X
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # Python 2.X
    from distutils.command.build_py import build_py

try:
    f = open('doc/changelog', encoding='UTF-8')
except TypeError:
    f = open('doc/changelog')

try:
    version = f.readline().split()[1].strip('()')
finally:
    f.close()

distutils.core.setup(
    name = 'python-aalib',
    version = version,
    license = 'MIT',
    description = 'Bindings for AAlib',
    long_description = __doc__.strip(),
    classifiers = classifiers,
    url = 'http://jwilk.net/software/python-aalib',
    author = 'Jakub Wilk',
    author_email = 'jwilk@jwilk.net',
    py_modules = ['aalib'],
    cmdclass = dict(build_py=build_py),
)

# vim:ts=4 sw=4 et
