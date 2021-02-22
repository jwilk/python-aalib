/* Copyright © 2021 Jakub Wilk <jwilk@jwilk.net>
 * SPDX-License-Identifier: MIT
 */

#include <stddef.h>
#include <stdio.h>

#include <aalib.h>

#define PRINT_SIZE() do { \
    printf("=%zu\n", sizeof(struct STRUCT)); \
} while (0)

#define PRINT_OFS(fld) do { \
    printf("%zu\n", offsetof(struct STRUCT, fld)); \
} while (0)

int main(int argc, char **argv)
{
#define STRUCT aa_hardware_params
    PRINT_OFS(font);
    PRINT_OFS(supported);
    PRINT_OFS(minwidth);
    PRINT_OFS(minheight);
    PRINT_OFS(maxwidth);
    PRINT_OFS(maxheight);
    PRINT_OFS(recwidth);
    PRINT_OFS(recheight);
    PRINT_OFS(mmwidth);
    PRINT_OFS(mmheight);
    PRINT_OFS(width);
    PRINT_OFS(height);
    PRINT_OFS(dimmul);
    PRINT_OFS(boldmul);
    PRINT_SIZE();
#undef STRUCT
#define STRUCT aa_renderparams
    PRINT_OFS(bright);
    PRINT_OFS(contrast);
    PRINT_OFS(gamma);
    PRINT_OFS(dither);
    PRINT_OFS(inversion);
    PRINT_OFS(randomval);
    PRINT_SIZE();
    return 0;
}

/* vim:set ts=4 sts=4 sw=4 et: */
