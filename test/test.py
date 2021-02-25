# encoding=UTF-8

# Copyright © 2010-2019 Jakub Wilk <jwilk@jwilk.net>
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

import os
import sys

from PIL import Image, ImageOps

import aalib

type(b'')  # Python >= 2.6 is required

here = os.path.dirname(__file__)

if not sys.stdout.isatty():
    screen = aalib.AsciiScreen
elif os.getenv('TERM') == 'linux':
    screen = aalib.LinuxScreen
else:
    screen = aalib.AnsiScreen
screen = screen(width=76, height=24)
with open(os.path.join(here, 'python.jpeg'), 'rb') as fp:
    image = Image.open(fp).convert('L')
    image = ImageOps.invert(image)
    image = image.resize(screen.virtual_size)
    screen.put_image((0, 0), image)
    print(screen.render())

# vim:ts=4 sts=4 sw=4 et
