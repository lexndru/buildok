CWD=$(shell pwd)
BUILD_VER=$(shell git log -1 --format="%h")
SRCDIR=buildok
APPNAME=buildok
TESTDIR=test

.PHONY: all clean build release update test

all: clean update build

build: update
	cd /tmp && virtualenv $(SRCDIR) && cd $(SRCDIR)
	cp -R $(CWD) /tmp/$(SRCDIR)
	ls -l

clean:
	find $(SRCDIR) -regextype posix-extended -regex ".*.pyc" -type f -delete
	find $(TESTDIR) -regextype posix-extended -regex ".*.pyc" -type f -delete

release: build
	cd /tmp/$(SRCDIR)/buildok && python setup.py sdist
	ls -l

update:
	echo "__build__ = \""$(BUILD_VER)"\"" > $(SRCDIR)/__init__.py

docker:
	docker build -t $(APPNAME) .

test:
	docker run -it --rm --name $(APPNAME) -v `pwd`:/opt/src/app -w /opt/src/app $(APPNAME) python test.py
