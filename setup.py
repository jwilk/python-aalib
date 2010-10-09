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
Topic :: Multimedia :: Graphics
'''.strip().split('\n')

import os
import distutils.core

os.putenv('TAR_OPTIONS', '--owner root --group root --mode a+rX')

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
    py_modules = ['aalib']
)

# vim:ts=4 sw=4 et
