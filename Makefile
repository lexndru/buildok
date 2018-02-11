CWD=$(shell pwd)
SRCDIR=buildok
TESTDIR=test

.PHONY: all clean build

all: clean build

build:
	cd /tmp && virtualenv $(SRCDIR) && cd $(SRCDIR)
	cp -R $(CWD) /tmp/$(SRCDIR)
	ls -l

clean:
	find $(SRCDIR) -regextype posix-extended -regex ".*.pyc" -type f -delete
	find $(TESTDIR) -regextype posix-extended -regex ".*.pyc" -type f -delete
