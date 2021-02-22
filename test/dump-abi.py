# encoding=UTF-8

# Copyright © 2021 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

from __future__ import print_function

import ctypes

import aalib

type(b'')  # Python >= 2.6 is required

def main():
    for struct in aalib.HardwareSettings, aalib.RenderSettings:
        for fldname, _ in struct._fields_:
            field = getattr(struct, fldname)
            print(field.offset)
        print('=', ctypes.sizeof(struct), sep='')

if __name__ == '__main__':
    main()

# vim:ts=4 sts=4 sw=4 et
