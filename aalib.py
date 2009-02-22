#!/usr/bin/python
# encoding=UTF-8

# Copyright © 2009 Jakub Wilk <ubanus@users.sf.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

'''
bindings for AAlib, an ASCII art library
'''

import ctypes as _ct
from itertools import imap as _map

libaa = _ct.CDLL('libaa.so.1')

class Font(_ct.Structure):
    pass

FontPtr = _ct.POINTER(Font)

class Structure(_ct.Structure):
    def clone(self):
        clone = type(self)()
        size = min(_ct.sizeof(self), _ct.sizeof(clone))
        bytes = buffer(self)[:]
        _ct.memmove(_ct.addressof(clone), bytes, size)
        return clone

class HardwareSettings(Structure):
    _pack_ = 4
    _fields_ = [
        ('font', FontPtr),
        ('options', _ct.c_int),
        ('min_width', _ct.c_int),
        ('min_height', _ct.c_int),
        ('max_width', _ct.c_int),
        ('max_height', _ct.c_int),
        ('recommended_width', _ct.c_int),
        ('recommended_height', _ct.c_int),
        ('physical_width', _ct.c_int),
        ('physical_height', _ct.c_int),
        ('width', _ct.c_int),
        ('height', _ct.c_int),
        ('dim_value', _ct.c_double),
        ('bold_value', _ct.c_double),
    ]

HardwareSettingsPtr = _ct.POINTER(HardwareSettings)

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
    _pack_ = 4
    _fields_ = [
        ('brightness', _ct.c_int),
        ('contrast', _ct.c_int),
        ('gamma', _ct.c_float),
        ('dithering_mode', _ct.c_int),
        ('inversion', _ct.c_int),
        ('random', _ct.c_int),
    ]

RenderSettingsPtr = _ct.POINTER(RenderSettings)

DEFAULT_RENDER_SETTINGS = RenderSettings.in_dll(libaa, 'aa_defrenderparams')

DITHER_NONE = 0
DITHER_ERROR_DISTRIBUTION = 1
DITHER_FLOYD_STEINBERG = 2

class Driver(Structure):
    pass

DriverPtr = _ct.POINTER(Driver)

class Context(Structure):
    pass

ContextPtr = _ct.POINTER(Context)

aa_init = libaa.aa_init
aa_init.argtypes = [DriverPtr, HardwareSettingsPtr, _ct.c_void_p]
aa_init.restype = ContextPtr

aa_close = libaa.aa_close
aa_close.argtypes = [ContextPtr]

aa_image = libaa.aa_image
aa_image.argtypes = [ContextPtr]
aa_image.restype = _ct.POINTER(_ct.c_ubyte)

aa_text = libaa.aa_text
aa_text.argtypes = [ContextPtr]
aa_text.restype = _ct.POINTER(_ct.c_ubyte)

aa_attrs = libaa.aa_attrs
aa_attrs.argtypes = [ContextPtr]
aa_attrs.restype = _ct.POINTER(_ct.c_ubyte)

aa_imgwidth = libaa.aa_imgwidth
aa_imgwidth.argtypes = [ContextPtr]
aa_imgwidth.restype = _ct.c_int

aa_imgheight = libaa.aa_imgheight
aa_imgheight.argtypes = [ContextPtr]
aa_imgheight.restype = _ct.c_int

aa_scrwidth = libaa.aa_scrwidth
aa_scrwidth.argtypes = [ContextPtr]
aa_scrwidth.restype = _ct.c_int

aa_scrheight = libaa.aa_scrheight
aa_scrheight.argtypes = [ContextPtr]
aa_scrheight.restype = _ct.c_int

aa_render = libaa.aa_render
aa_render.argtypes = [ContextPtr, RenderSettingsPtr] + 4 * [_ct.c_int]

aa_mem_d = Driver.in_dll(libaa, 'mem_d')

class ScreenInitializationFailed(Exception):
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
        for k, v in kwargs.iteritems():
            setattr(settings, k, v)
        context = self._context = aa_init(_ct.pointer(aa_mem_d), _ct.pointer(settings), None)
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
        aa_close(self._context)
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
        x0 = max(x0, 0)
        y0 = max(y0, 0)
        (image_width, image_height) = image.size
        x1 = min(x0 + image_width, virtual_width)
        y1 = min(x0 + image_height, virtual_height)
        for iy in xrange(image_height):
            y = iy + x0
            if y < 0:
                continue
            if y >= virtual_height:
                continue
            p = y * virtual_width
            for ix in xrange(image_width):
                x = ix + y0
                if x < 0:
                    continue
                if x >= virtual_width:
                    continue
                self._framebuffer[p + x] = image.getpixel((ix, iy))

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
        for k, v in kwargs.iteritems():
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
                for x in xrange(width)
            ]
            for y in xrange(height)
        ]

    def __del__(self):
        self.close()

class AsciiScreen(Screen):

    '''Pure ASCII screen.'''

    _formats = {ATTRIBUTE_NORMAL: '%s'}

    def _get_default_settings(self):
        settings = Screen._get_default_settings(self)
        settings.options = OPTION_NORMAL_MASK
        return settings

    def render(self, **kwargs):
        raw = Screen.render(self, **kwargs)
        return '\n'.join(
            ''.join(self._formats[attr] % ch for (ch, attr) in line)
            for line in raw
        )
    render.__doc__ = Screen.render.__doc__

class AnsiScreen(AsciiScreen):

    '''Screen that uses ANSI escape sequences.'''

    _formats = {
        ATTRIBUTE_NORMAL: '%s',
        ATTRIBUTE_BRIGHT: '\x1b[1m%s\x1b[0m',
    }

    def _get_default_settings(self):
        settings = Screen._get_default_settings(self)
        settings.options = OPTION_NORMAL_MASK | OPTION_BRIGHT_MASK
        return settings

class LinuxScreen(AsciiScreen):

    '''Screen that uses Linux console escape sequences.'''

    _formats = {
        ATTRIBUTE_NORMAL: '%s',
        ATTRIBUTE_BOLD: '\x1b[1m%s\x1b[0m',
        ATTRIBUTE_DIM: '\x1b[30;1m%s\x1b[0m',
        ATTRIBUTE_REVERSE: '\x1b[7m%s\x1b[0m',
    }

    def _get_default_settings(self):
        settings = Screen._get_default_settings(self)
        settings.options = OPTION_NORMAL_MASK | OPTION_BOLD_MASK | OPTION_DIM_MASK | OPTION_REVERSE_MASK
        return settings

__all__ = (
    'AsciiScreen', 'AnsiScreen', 'LinuxScreen', 'ScreenInitializationFailed',
    'DITHER_NONE', 'DITHER_ERROR_DISTRIBUTION', 'DITHER_FLOYD_STEINBERG',
)

# vim:ts=4 sw=4 et
