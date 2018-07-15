# Buildok
[![Build Status](https://travis-ci.org/lexndru/buildok.svg?branch=master)](https://travis-ci.org/lexndru/buildok)

A tool to automate build steps from README files.

## Introduction

## Getting started
There are two possible ways to make use of this tool. You either create a file named `.build` and write each step on a line;
or write a new section in your `README.md` file starting with one of the following statements: "how to build ok" or "build ok steps".
Each step you write has to respect the following pattern: `n) build step <punctuation>` where `n` is a number and `<punctuation>` is one of the following: `.`, `!` or `?`.

## Install system requirements (Debian)
```
$ apt-get install python python-pip
```

## Install from PyPi
```
$ pip install buildok
```

## Install from sources
```
$ python setup.py install
```

## Supported statements

|   | Run a command in shell.                                                    |
|---|----------------------------------------------------------------------------|
| ✓ | ^run `(?P<cmd>.+)`$                                                        |


|   | Open a link in default browser.                                            |
|---|----------------------------------------------------------------------------|
| ✓ | ^open in browser `(?P<url>.+)`$                                            |
| ✓ | ^open (?:link\|url) `(?P<url>.+)`$                                          |


|   | Remove files from a given source.                                          |
|---|----------------------------------------------------------------------------|
| ✓ | ^remove from `(?P<src>.+)`$                                                |
| ✓ | ^remove `(?P<src>.+)` files$                                               |
| ✓ | ^remove (?:file\|folder\|directory) `(?P<src>.+)`$                           |


|   | Make a symlink for a target source.                                        |
|---|----------------------------------------------------------------------------|
| ✓ | ^create symlink from `(?P<src>.+)` to `(?P<dst>.+)`$                       |
| ✓ | ^make symlink `(?P<dst>.+)` from `(?P<src>.+)`$                            |
| ✓ | ^make symlink `(?P<dst>.+)`$                                               |


|   | Open a Google search results in default browser.                           |
|---|----------------------------------------------------------------------------|
| ✓ | ^google (?:for )?`(?P<search>.+)`$                                         |


|   | Change owner and group on file or directory.                               |
|---|----------------------------------------------------------------------------|
| ✓ | ^change file owner to `(?P<owner>.+)` on `(?P<path>.+)`$                   |
| ✓ | ^change owner to `(?P<owner>.+)` on `(?P<path>.+)`$                        |
| ✓ | ^change user to `(?P<owner>.+)` on `(?P<path>.+)`$                         |
| ✓ | ^change user and group to `(?P<owner>.+):(?P<group>.+)`$                   |
| ✓ | ^set owner and group `(?P<owner>.+):(?P<group>.+)` for `(?P<path>.+)`$     |


|   | Make a directory or make recursive directories.                            |
|---|----------------------------------------------------------------------------|
| ✓ | ^create (?:folder\|directory) `(?P<path>.+)`$                               |
| ✓ | ^make new (?:folder\|directory) `(?P<path>.+)`$                             |


|   | Change current working directory.                                          |
|---|----------------------------------------------------------------------------|
| ✓ | ^go to `(?P<path>.+)`$                                                     |
| ✓ | ^change (?:dir\|directory\|folder) to `(?P<path>.+)`$                        |


|   | Copy files from a given source to a given destination.                     |
|---|----------------------------------------------------------------------------|
| ✓ | ^copy from `(?P<src>.+)` to `(?P<dst>.+)`$                                 |
| ✓ | ^copy `(?P<src>.+)` files to `(?P<dst>.+)`$                                |
| ✓ | ^copy `(?P<src>.+)` to `(?P<dst>.+)`$                                      |


|   | No operation; nothing to do.                                               |
|---|----------------------------------------------------------------------------|
| ✓ | ^nothing (?:else \|more )?to do$                                            |
| ✓ | ^done$                                                                     |
| ✓ | ^that's all folks$                                                         |


|   | Open a DuckDuckGo search in default browser.                               |
|---|----------------------------------------------------------------------------|
| ✓ | ^lookup `(?P<search>.+)` online$                                           |


|   | Change permissions on file or directory.                                   |
|---|----------------------------------------------------------------------------|
| ✓ | ^change permissions to `(?P<mode>.+)`$                                     |
| ✓ | ^change permissions to `(?P<mode>.+)` for `(?P<path>.+)`$                  |
| ✓ | ^change permissions `(?P<mode>.+)` for `(?P<path>.+)`$                     |
| ✓ | ^set permissions to `(?P<mode>.+)` for `(?P<path>.+)`$                     |


|   | Edit content of an existing file.                                          |
|---|----------------------------------------------------------------------------|
| ✓ | ^add the following content to file `(?P<filepath>[\w\.]+)`$                |


|   | Open a GitHub search in default browser.                                   |
|---|----------------------------------------------------------------------------|
| ✓ | ^lookup `(?P<search>.+)` on github$                                        |


|   | Create a new file.                                                         |
|---|----------------------------------------------------------------------------|
| ✓ | ^create file `(?P<filepath>[\w\.]+)`$                                      |


|   | Move files from a given source to a given destination.                     |
|---|----------------------------------------------------------------------------|
| ✓ | ^move from `(?P<src>.+)` to `(?P<dst>.+)`$                                 |
| ✓ | ^move `(?P<src>.+)` files to `(?P<dst>.+)`$                                |
| ✓ | ^rename `(?P<src>.+)` to `(?P<dst>.+)`$                                    |


|   | Open a Wikipedia search in default browser.                                |
|---|----------------------------------------------------------------------------|
| ✓ | ^wiki(?:pedia)? `(?P<search>.+)`$                                          |


|   | Invoke another topic from guide.                                           |
|---|----------------------------------------------------------------------------|
| ✓ | ^read (?:steps from )?topic `(?P<topic>.+)`$                               |
| ✓ | ^continue reading topic `(?P<topic>.+)`$                                   |
| ✓ | ^follow steps from `(?P<topic>.+)`$                                        |


|   | Send SIGTERM signal to a process.                                          |
|---|----------------------------------------------------------------------------|
| ✓ | ^(?:kill\|stop) process `(?P<pname>.+)`$                                    |
| ✓ | ^(?:kill\|stop) pid `(?P<pid>.+)`$                                          |


|   | Install new software package(s).                                           |
|---|----------------------------------------------------------------------------|
| ✓ | ^install `(?P<pkgs>.+)`$                                                   |


## How to build OK
1) Create folder `/tmp/_buildok`.
2) Go to `/tmp/_buildok`!
3) Run `pwd`!
4) Open link `https://github.com/lexndru/buildok`.
5) Run `echo Hello, friendly world`.

## License
Copyright 2018 Alexandru Catrina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
