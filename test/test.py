import os

from PIL import Image, ImageOps

import aalib

here = os.path.dirname(__file__)

if os.getenv('TERM') == 'linux':
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

# vim:ts=4 sw=4 et
