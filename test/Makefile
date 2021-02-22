# Copyright © 2021 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

PYTHON = python

CFLAGS ?= -O2 -g
CFLAGS += -Wall

.PHONY: all
all: smoke-test

.PHONY: smoke-test
smoke-test:
	$(PYTHON) test.py

.PHONY: abi-test
abi-test: dump-abi
	./dump-abi > abi.c.txt
	$(PYTHON) dump-abi.py > abi.py.txt
	diff -U999 abi.c.txt abi.py.txt

.PHONY: clean
clean:
	rm -f dump-abi abi.*.txt

# vim:ts=4 sts=4 sw=4 noet
