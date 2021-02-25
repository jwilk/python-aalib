# encoding=UTF-8

# Copyright © 2009-2019 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
*python-aalib* is an interface to
`AAlib <http://aa-project.sourceforge.net/aalib/>`_,
an ASCII art library.
'''

import io
import os

import distutils.core
import distutils.command.build_py

from distutils.command.sdist import sdist as distutils_sdist

try:
    import distutils644
except ImportError:
    pass
else:
    distutils644.install()

type(b'')  # Python >= 2.6 is required

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

def get_version():
    path = os.path.join('doc/changelog')
    with io.open(path, encoding='UTF-8') as file:
        line = file.readline()
    return line.split()[1].strip('()')

class cmd_sdist(distutils_sdist):

    def maybe_move_file(self, base_dir, src, dst):
        src = os.path.join(base_dir, src)
        dst = os.path.join(base_dir, dst)
        if os.path.exists(src):
            self.move_file(src, dst)

    def make_release_tree(self, base_dir, files):
        distutils_sdist.make_release_tree(self, base_dir, files)
        self.maybe_move_file(base_dir, 'LICENSE', 'doc/LICENSE')

distutils.core.setup(
    name='python-aalib',
    version=get_version(),
    license='MIT',
    description='interface to AAlib',
    long_description=__doc__.strip(),
    classifiers=classifiers,
    url='http://jwilk.net/software/python-aalib',
    author='Jakub Wilk',
    author_email='jwilk@jwilk.net',
    py_modules=['aalib'],
    cmdclass=dict(
        sdist=cmd_sdist,
    ),
)

# vim:ts=4 sts=4 sw=4 et
