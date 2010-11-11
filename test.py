import urllib2
from cStringIO import StringIO

import Image
import aalib

screen = aalib.AnsiScreen(width=60, height=30)
fp = StringIO(urllib2.urlopen('http://python.org/favicon.ico').read())
image = Image.open(fp).convert('L').resize(screen.virtual_size)
screen.put_image((0, 0), image)
print screen.render()

# vim:ts=4 sw=4 et
