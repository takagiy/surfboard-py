# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

PKGVER := $(shell cat setup.py | grep "version" | sed -e 's/^ *version="//;s/",//')
SRC := $(shell find surfboard -type f -name "*.py")
TARDIST := dist/surfboard-$(PKGVER).tar.gz
WHEEL := dist/surfboard-$(PKGVER)-py3-none-any.whl
DIST := $(TARDIST) $(WHEEL)

.PHONY: all clean bdist publish.test publish.pypi licensenote genimports

all: licensenote bdist

clean:
	rm -rf dist
	rm -rf build
	rm -rf surfboard.egg-info

bdist: $(DIST)

$(SRC): genimports licensenote

$(DIST): $(SRC) setup.py
	python setup.py sdist bdist_wheel

publish.test: $(DIST)
	twine upload --repository testpypi dist/*

publish.pypi: $(DIST)
	twine upload --repository pypi dist/*

publish.github: $(SRC)
	git tag -a v$(PKGVER) -m "update to v$(PKGVER)"
	git push --follow-tags

licensenote:
	python script/notelicense.py

genimports:
#	python script/genimports.py
