import os

try:
    # Python 2.X
    from urllib2 import urlopen
except ImportError:
    # Python 3.X
    from urllib.request import urlopen

try:
    # Python 2.X
    from cStringIO import StringIO as BytesIO
except ImportError:
    # Python 3.X
    from io import BytesIO

from PIL import Image
import aalib

if os.getenv('TERM') == 'linux':
    screen = aalib.LinuxScreen
else:
    screen = aalib.AnsiScreen
screen = screen(width=60, height=30)
fp = BytesIO(urlopen('http://python.org/favicon.ico').read())
image = Image.open(fp).convert('L').resize(screen.virtual_size)
screen.put_image((0, 0), image)
print(screen.render())

# vim:ts=4 sw=4 et
