# encoding=UTF-8

# Copyright © 2009-2021 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
interface to AAlib, an ASCII art library
'''

import ctypes
import sys

type(b'')  # Python >= 2.6 is required

if sys.version_info < (3,):
    import __builtin__ as builtins  # pylint: disable=import-error
    range = builtins.xrange  # pylint: disable=redefined-builtin

libaa = ctypes.CDLL('libaa.so.1')

class Font(ctypes.Structure):
    pass

FontPtr = ctypes.POINTER(Font)

class Structure(ctypes.Structure):
    def clone(self):
        clone = type(self)()
        ctypes.pointer(clone)[0] = self
        return clone

class HardwareSettings(Structure):
    _fields_ = [
        ('font', FontPtr),
        ('options', ctypes.c_int),
        ('min_width', ctypes.c_int),
        ('min_height', ctypes.c_int),
        ('max_width', ctypes.c_int),
        ('max_height', ctypes.c_int),
        ('recommended_width', ctypes.c_int),
        ('recommended_height', ctypes.c_int),
        ('physical_width', ctypes.c_int),
        ('physical_height', ctypes.c_int),
        ('width', ctypes.c_int),
        ('height', ctypes.c_int),
        ('dim_value', ctypes.c_double),
        ('bold_value', ctypes.c_double),
    ]

HardwareSettingsPtr = ctypes.POINTER(HardwareSettings)

OPTION_NORMAL_MASK = 1
OPTION_DIM_MASK = 2
OPTION_BRIGHT_MASK = 4
OPTION_BOLD_MASK = 8
OPTION_REVERSE_MASK = 16
OPTION_ALL_MASKS = 128
OPTION_8BITS = 256

ATTRIBUTE_NORMAL = 0
ATTRIBUTE_DIM = 1
ATTRIBUTE_BRIGHT = 2
ATTRIBUTE_BOLD = 3
ATTRIBUTE_REVERSE = 4

DEFAULT_HARDWARE_SETTINGS = HardwareSettings.in_dll(libaa, 'aa_defparams')

class RenderSettings(Structure):
    _fields_ = [
        ('brightness', ctypes.c_int),
        ('contrast', ctypes.c_int),
        ('gamma', ctypes.c_float),
        ('dithering_mode', ctypes.c_int),
        ('inversion', ctypes.c_int),
        ('random', ctypes.c_int),
    ]

RenderSettingsPtr = ctypes.POINTER(RenderSettings)

DEFAULT_RENDER_SETTINGS = RenderSettings.in_dll(libaa, 'aa_defrenderparams')

DITHER_NONE = 0
DITHER_ERROR_DISTRIBUTION = 1
DITHER_FLOYD_STEINBERG = 2

class Driver(Structure):
    pass

DriverPtr = ctypes.POINTER(Driver)

class Context(Structure):
    pass

ContextPtr = ctypes.POINTER(Context)

aa_init = libaa.aa_init
aa_init.argtypes = [DriverPtr, HardwareSettingsPtr, ctypes.c_void_p]
aa_init.restype = ContextPtr

aa_close = libaa.aa_close
aa_close.argtypes = [ContextPtr]

aa_image = libaa.aa_image
aa_image.argtypes = [ContextPtr]
aa_image.restype = ctypes.POINTER(ctypes.c_ubyte)

aa_text = libaa.aa_text
aa_text.argtypes = [ContextPtr]
aa_text.restype = ctypes.POINTER(ctypes.c_ubyte)

aa_attrs = libaa.aa_attrs
aa_attrs.argtypes = [ContextPtr]
aa_attrs.restype = ctypes.POINTER(ctypes.c_ubyte)

aa_imgwidth = libaa.aa_imgwidth
aa_imgwidth.argtypes = [ContextPtr]
aa_imgwidth.restype = ctypes.c_int

aa_imgheight = libaa.aa_imgheight
aa_imgheight.argtypes = [ContextPtr]
aa_imgheight.restype = ctypes.c_int

aa_scrwidth = libaa.aa_scrwidth
aa_scrwidth.argtypes = [ContextPtr]
aa_scrwidth.restype = ctypes.c_int

aa_scrheight = libaa.aa_scrheight
aa_scrheight.argtypes = [ContextPtr]
aa_scrheight.restype = ctypes.c_int

aa_render = libaa.aa_render
aa_render.argtypes = [ContextPtr, RenderSettingsPtr] + 4 * [ctypes.c_int]

aa_mem_d = Driver.in_dll(libaa, 'mem_d')

class ScreenInitializationFailed(Exception):
    pass

class NoImageBuffer(Exception):
    pass

class Screen(object):

    def _get_default_settings(self):
        return DEFAULT_HARDWARE_SETTINGS.clone()

    def __init__(self, **kwargs):
        '''Initialize the virtual screen.

        Possible keyword arguments:
        - `font`,
        - `options`,
        - `min_width`, `min_height` (in pixels),
        - `max_width`, `max_height` (in pixels),
        - `recommended_width`, `recommended_height` (in pixels),
        - `width`, `height` (in pixels),
        - `physical_width`, `physical_height` (in mm),
        - `dim_value`,
        - `bold_value`.
        '''
        settings = self._get_default_settings()
        for k, v in kwargs.items():
            setattr(settings, k, v)
        context = self._context = aa_init(ctypes.pointer(aa_mem_d), ctypes.pointer(settings), None)
        if context is None:
            raise ScreenInitializationFailed
        self._render_width = aa_scrwidth(context)
        self._render_height = aa_scrheight(context)
        self._virtual_width = aa_imgwidth(context)
        self._virtual_height = aa_imgheight(context)
        self._framebuffer = aa_image(context)

    def close(self):
        try:
            context = self._context
        except AttributeError:
            return
        aa_close(context)
        del self._context

    @property
    def render_width(self):
        '''Width of rendered image, in pixels.'''
        return self._render_width

    @property
    def render_height(self):
        '''Height of rendered image, in pixels.'''
        return self._render_height

    @property
    def render_size(self):
        '''Size of rendered image, in pixels.'''
        return self._render_width, self._render_height

    @property
    def virtual_width(self):
        '''Height of the virtual screen, in pixels.'''
        return self._virtual_width

    @property
    def virtual_height(self):
        '''Height of the virtual screen, in pixels.'''
        return self._virtual_height

    @property
    def virtual_size(self):
        '''Size of the virtual screen, in pixels.'''
        return self._virtual_width, self._virtual_height

    def __setitem__(self, xy, value):
        '''Put a pixel on the virtual screen.'''
        (x, y) = xy
        self._framebuffer[y * self._virtual_width + x] = value

    def put_image(self, xy, image):
        virtual_width = self._virtual_width
        virtual_height = self._virtual_height
        (x0, y0) = xy
        (image_width, image_height) = image.size
        for y in range(max(y0, 0), min(y0 + image_height, virtual_height)):
            p = y * virtual_width
            for x in range(max(x0, 0), min(x0 + image_width, virtual_width)):
                self._framebuffer[p + x] = image.getpixel((x - x0, y - y0))

    def __getitem__(self, xy):
        '''Get a pixel from the virtual screen.'''
        (x, y) = xy
        return self._framebuffer[y * self._virtual_width + x]

    def render(self, **kwargs):
        '''Render the image.

        Possible keyword arguments:
        - `brightness`,
        - `contrast`,
        - `gamma`,
        - `dithering_mode` (see `DITHER_*` constants),
        - `inversion`,
        - `random`.
        '''
        settings = DEFAULT_RENDER_SETTINGS.clone()
        for k, v in kwargs.items():
            setattr(settings, k, v)
        context = self._context
        buffer = aa_image(context)
        if buffer is None:
            raise NoImageBuffer
        width, height = self._render_width, self._render_height
        aa_render(context, settings, 0, 0, width, height)
        text = aa_text(context)
        attrs = aa_attrs(context)
        return [
            [
                (chr(text[y * width + x]), attrs[y * width + x])
                for x in range(width)
            ]
            for y in range(height)
        ]

    def __del__(self):
        self.close()

class AsciiScreen(Screen):

    '''Pure ASCII screen.'''

    _formats = {ATTRIBUTE_NORMAL: '{s}'}

    def _get_default_settings(self):
        settings = Screen._get_default_settings(self)
        settings.options = OPTION_NORMAL_MASK
        return settings

    def render(self, **kwargs):
        raw = Screen.render(self, **kwargs)
        return '\n'.join(
            ''.join(self._formats[attr].format(s=ch) for (ch, attr) in line)
            for line in raw
        )
    render.__doc__ = Screen.render.__doc__

class AnsiScreen(AsciiScreen):

    '''Screen that uses ANSI escape sequences.'''

    _formats = {
        ATTRIBUTE_NORMAL: '{s}',
        ATTRIBUTE_BRIGHT: '\x1B[1m{s}\x1B[0m',
    }

    def _get_default_settings(self):
        settings = Screen._get_default_settings(self)
        settings.options = OPTION_NORMAL_MASK | OPTION_BRIGHT_MASK
        return settings

class LinuxScreen(AsciiScreen):

    '''Screen that uses Linux console escape sequences.'''

    _formats = {
        ATTRIBUTE_NORMAL: '{s}',
        ATTRIBUTE_BOLD: '\x1B[1m{s}\x1B[0m',
        ATTRIBUTE_DIM: '\x1B[30;1m{s}\x1B[0m',
        ATTRIBUTE_REVERSE: '\x1B[7m{s}\x1B[0m',
    }

    def _get_default_settings(self):
        settings = Screen._get_default_settings(self)
        settings.options = OPTION_NORMAL_MASK | OPTION_BOLD_MASK | OPTION_DIM_MASK | OPTION_REVERSE_MASK
        return settings

__all__ = (
    'AsciiScreen', 'AnsiScreen', 'LinuxScreen', 'ScreenInitializationFailed',
    'DITHER_NONE', 'DITHER_ERROR_DISTRIBUTION', 'DITHER_FLOYD_STEINBERG',
)

# vim:ts=4 sts=4 sw=4 et
