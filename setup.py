# encoding=UTF-8

# Copyright © 2009-2015 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
*python-aalib* is an interface to
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
with f:
    version = f.readline().split()[1].strip('()')

distutils.core.setup(
    name='python-aalib',
    version=version,
    license='MIT',
    description='interface to AAlib',
    long_description=__doc__.strip(),
    classifiers=classifiers,
    url='http://jwilk.net/software/python-aalib',
    author='Jakub Wilk',
    author_email='jwilk@jwilk.net',
    py_modules=['aalib'],
    cmdclass=dict(build_py=build_py),
)

# vim:ts=4 sts=4 sw=4 et
