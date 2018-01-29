CWD=$(shell pwd)
BUILDDIR=build
BUILDPATH=$(CWD)/$(BUILDDIR)
PYTHON=$(shell which python)
SHEBANG=$(shell echo '\#!$(PYTHON) -O')
BUILDOKAPP=buildok_app

.PHONY: all clean build

all: clean build

build:
	mkdir -p $(BUILDDIR)
	cp -R src/* $(BUILDDIR)
	python -m compileall $(BUILDDIR)
	find $(BUILDDIR) -regextype posix-extended ! -regex ".*__.+__.py|.+.pyc" -type f -delete
	cd $(BUILDPATH) && zip -r build.zip .
	cd $(BUILDPATH) && echo "$(SHEBANG)" | cat - build.zip > $(BUILDOKAPP)
	mv $(BUILDPATH)/$(BUILDOKAPP) $(CWD)/$(BUILDOKAPP) && chmod +x $(BUILDOKAPP)

clean:
	rm -f $(BUILDOKAPP) 2> /dev/null
	rm -rf $(BUILDDIR) 2> /dev/null
	find src -regextype posix-extended -regex ".*.pyc" -type f -delete
