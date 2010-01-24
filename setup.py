'''
*python-aalib* is a set of bindings for
`AAlib <http://aa-project.sourceforge.net/aalib/>`_,
an ASCII art library.
'''

classifiers = '''\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Topic :: Multimedia :: Graphics\
'''.split('\n')

import os
from distutils.core import setup

os.putenv('TAR_OPTIONS', '--owner root --group root --mode a+rX')

setup(
    name = 'python-aalib',
    version = '0.1.1',
    license = 'GNU GPL 2',
    description = 'Bindings for AAlib',
    long_description = __doc__.strip(),
    classifiers = classifiers,
    url = 'http://jwilk.net/software/python-aalib.html',
    author = 'Jakub Wilk',
    author_email = 'ubanus@users.sf.net',
    py_modules = ['aalib']
)

# vim:ts=4 sw=4 et
