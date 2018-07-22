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
```
|--------------------------------------------------------------------------------|
| Open a GitHub search in default browser.                                       |
|--------------------------------------------------------------------------------|
|   | ^lookup `(?P<search>.+)` on github$                                        |
|--------------------------------------------------------------------------------|
|   | - Lookup `buildok` on GitHub.                                              |
|--------------------------------------------------------------------------------|
| Open a link in default browser.                                                |
|--------------------------------------------------------------------------------|
|   | ^open in browser `(?P<url>.+)`$                                            |
|   | ^open (?:link|url) `(?P<url>.+)`$                                          |
|--------------------------------------------------------------------------------|
|   | - Open link `https://github.com/lexndru/buildok`.                          |
|--------------------------------------------------------------------------------|
| Reinstall software package(s).                                                 |
|--------------------------------------------------------------------------------|
|   | ^reinstall `(?P<pkgs>.+)`$                                                 |
|--------------------------------------------------------------------------------|
|   | - Reinstall `vim curl`.                                                    |
|--------------------------------------------------------------------------------|
| Install new software package(s).                                               |
|--------------------------------------------------------------------------------|
|   | ^install `(?P<pkgs>.+)`$                                                   |
|--------------------------------------------------------------------------------|
|   | - Install `vim curl`.                                                      |
|--------------------------------------------------------------------------------|
| Remove files from a given source.                                              |
|--------------------------------------------------------------------------------|
|   | ^remove from `(?P<src>.+)`$                                                |
|   | ^remove `(?P<src>.+)` files$                                               |
|   | ^remove (?:file|folder|directory) `(?P<src>.+)`$                           |
|--------------------------------------------------------------------------------|
|   | - Go to `/tmp`.                                                            |
|   | - Run `touch buildok_test_tmp.txt`.                                        |
|   | - Remove file `buildok_test_tmp.txt`.                                      |
|--------------------------------------------------------------------------------|
| Change owner and group on file or directory.                                   |
|--------------------------------------------------------------------------------|
|   | ^change file owner to `(?P<owner>.+)` on `(?P<path>.+)`$                   |
|   | ^change owner to `(?P<owner>.+)` on `(?P<path>.+)`$                        |
|   | ^change user to `(?P<owner>.+)` on `(?P<path>.+)`$                         |
|   | ^change user and group to `(?P<owner>.+):(?P<group>.+)`$                   |
|   | ^set owner and group `(?P<owner>.+):(?P<group>.+)` for `(?P<path>.+)`$     |
|--------------------------------------------------------------------------------|
|   | - Run `touch /tmp/buildok_test.txt`.                                       |
|   | - Change owner to `nobody` on `/tmp/buildok_test.txt`.                     |
|--------------------------------------------------------------------------------|
| Send SIGTERM signal to a process.                                              |
|--------------------------------------------------------------------------------|
|   | ^(?:kill|stop) process `(?P<pname>.+)`$                                    |
|   | ^(?:kill|stop) pid `(?P<pid>.+)`$                                          |
|--------------------------------------------------------------------------------|
|   | - Stop process `someProcessName`.                                          |
|--------------------------------------------------------------------------------|
| No operation; nothing to do.                                                   |
|--------------------------------------------------------------------------------|
|   | ^nothing (?:else |more )?to do$                                            |
|   | ^done$                                                                     |
|   | ^that's all folks$                                                         |
|--------------------------------------------------------------------------------|
|   | - Nothing to do.                                                           |
|--------------------------------------------------------------------------------|
| Start new service.                                                             |
|--------------------------------------------------------------------------------|
|   | ^start service `(?P<srv>.+)`$                                              |
|--------------------------------------------------------------------------------|
|   | - Start service `urandom`.                                                 |
|--------------------------------------------------------------------------------|
| Open a Wikipedia search in default browser.                                    |
|--------------------------------------------------------------------------------|
|   | ^wiki(?:pedia)? `(?P<search>.+)`$                                          |
|--------------------------------------------------------------------------------|
|   | - Wikipedia `buildok`.                                                     |
|--------------------------------------------------------------------------------|
| Disable service at boot time.                                                  |
|--------------------------------------------------------------------------------|
|   | ^disable service `(?P<srv>.+)`$                                            |
|--------------------------------------------------------------------------------|
|   | - Disable service `urandom`.                                               |
|--------------------------------------------------------------------------------|
| Open a Google search results in default browser.                               |
|--------------------------------------------------------------------------------|
|   | ^google (?:for )?`(?P<search>.+)`$                                         |
|--------------------------------------------------------------------------------|
|   | - Google `buildok`.                                                        |
|--------------------------------------------------------------------------------|
| Make a symlink for a target source.                                            |
|--------------------------------------------------------------------------------|
|   | ^create symlink from `(?P<src>.+)` to `(?P<dst>.+)`$                       |
|   | ^make symlink `(?P<dst>.+)` from `(?P<src>.+)`$                            |
|   | ^make symlink `(?P<dst>.+)`$                                               |
|--------------------------------------------------------------------------------|
|   | - Run `touch buildok_test_symlink`.                                        |
|   | - Make symlink `buildok_test_symlink_ok` from `buildok_test_symlink`.      |
|--------------------------------------------------------------------------------|
| Install software package(s) with Node.js's package manager (npm).              |
|--------------------------------------------------------------------------------|
|   | ^install node\.?js packages? `(?P<pkgs>.+)`$                               |
|--------------------------------------------------------------------------------|
|   | - Install Node.js package `npm bower`.                                     |
|--------------------------------------------------------------------------------|
| Change current working directory.                                              |
|--------------------------------------------------------------------------------|
|   | ^go to `(?P<path>.+)`$                                                     |
|   | ^change (?:dir|directory|folder) to `(?P<path>.+)`$                        |
|--------------------------------------------------------------------------------|
|   | - Go to `/tmp`.                                                            |
|--------------------------------------------------------------------------------|
| Copy files from a given source to a given destination.                         |
|--------------------------------------------------------------------------------|
|   | ^copy from `(?P<src>.+)` to `(?P<dst>.+)`$                                 |
|   | ^copy `(?P<src>.+)` files to `(?P<dst>.+)`$                                |
|   | ^copy `(?P<src>.+)` to `(?P<dst>.+)`$                                      |
|--------------------------------------------------------------------------------|
|   | - Run `touch /tmp/buildok_test_copy.txt`.                                  |
|   | - Copy `/tmp/buildok_test_copy.txt` to `/tmp/buildok_test_copy2.txt`.      |
|--------------------------------------------------------------------------------|
| Invoke another topic from guide.                                               |
|--------------------------------------------------------------------------------|
|   | ^read (?:steps from )?topic `(?P<topic>.+)`$                               |
|   | ^continue reading topic `(?P<topic>.+)`$                                   |
|   | ^follow steps from `(?P<topic>.+)`$                                        |
|--------------------------------------------------------------------------------|
|   | - Follow steps from `do something else`.                                   |
|--------------------------------------------------------------------------------|
| List files in directory.                                                       |
|--------------------------------------------------------------------------------|
|   | ^list (?:files|folders) (?:in|from|of) `(?P<path>.+)`$                     |
|   | ^list everything$                                                          |
|--------------------------------------------------------------------------------|
|   | - List files in `/tmp`.                                                    |
|--------------------------------------------------------------------------------|
| Reload service configuration.                                                  |
|--------------------------------------------------------------------------------|
|   | ^reload service (?:config(?:uration)? )?`(?P<srv>.+)`$                     |
|--------------------------------------------------------------------------------|
|   | - Reload service config `urandom`.                                         |
|--------------------------------------------------------------------------------|
| Move files from a given source to a given destination.                         |
|--------------------------------------------------------------------------------|
|   | ^move from `(?P<src>.+)` to `(?P<dst>.+)`$                                 |
|   | ^move `(?P<src>.+)` files to `(?P<dst>.+)`$                                |
|   | ^rename `(?P<src>.+)` to `(?P<dst>.+)`$                                    |
|--------------------------------------------------------------------------------|
|   | - Go to `/tmp`.                                                            |
|   | - Create folder `buildok_test_folder_move`.                                |
|   | - Rename `buildok_test_folder_move` to `buildok_test_folder_moved`.        |
|--------------------------------------------------------------------------------|
| Get status of service.                                                         |
|--------------------------------------------------------------------------------|
|   | ^get status (?:for|of) service `(?P<srv>.+)`$                              |
|   | ^Print `(?P<srv>.+)` service status$                                       |
|--------------------------------------------------------------------------------|
|   | - Get status of service `urandom`.                                         |
|--------------------------------------------------------------------------------|
| Edit content of an existing file.                                              |
|--------------------------------------------------------------------------------|
|   | ^add the following content to file `(?P<filepath>[\w\.]+)`$                |
|--------------------------------------------------------------------------------|
|   | - Go to `/tmp`;                                                            |
|   | - Add the following content to file `buildok.txt`:                         |
|   | ```                                                                        |
|   | Lorem ipsum dolor sit amet, consectetur adipisicing elit...                |
|   | ```                                                                        |
|--------------------------------------------------------------------------------|
| Make a directory or make recursive directories.                                |
|--------------------------------------------------------------------------------|
|   | ^create (?:folder|directory) `(?P<path>.+)`$                               |
|   | ^make new (?:folder|directory) `(?P<path>.+)`$                             |
|--------------------------------------------------------------------------------|
|   | - Go to `/tmp`.                                                            |
|   | - Create folder `buildok_test_folder`.                                     |
|--------------------------------------------------------------------------------|
| Enable service at boot time.                                                   |
|--------------------------------------------------------------------------------|
|   | ^enable service `(?P<srv>.+)`$                                             |
|--------------------------------------------------------------------------------|
|   | - Enable service `urandom`.                                                |
|--------------------------------------------------------------------------------|
| Restart running service.                                                       |
|--------------------------------------------------------------------------------|
|   | ^restart service `(?P<srv>.+)`$                                            |
|--------------------------------------------------------------------------------|
|   | - Restart service `urandom`.                                               |
|--------------------------------------------------------------------------------|
| Change permissions on file or directory.                                       |
|--------------------------------------------------------------------------------|
|   | ^change permissions to `(?P<mode>.+)`$                                     |
|   | ^change permissions to `(?P<mode>.+)` for `(?P<path>.+)`$                  |
|   | ^change permissions `(?P<mode>.+)` for `(?P<path>.+)`$                     |
|   | ^set permissions (?:to )?`(?P<mode>.+)` (?:for|to|on) `(?P<path>.+)`$      |
|--------------------------------------------------------------------------------|
|   | - Run `touch /tmp/buildok_test.txt`.                                       |
|   | - Set permissions to `400` for `/tmp/buildok_test.txt`.                    |
|--------------------------------------------------------------------------------|
| Create a new file.                                                             |
|--------------------------------------------------------------------------------|
|   | ^create(?: new)? file `(?P<filepath>[\w\.]+)`$                             |
|--------------------------------------------------------------------------------|
|   | - Create file `/tmp/buildok.txt`.                                          |
|--------------------------------------------------------------------------------|
| Stop running service.                                                          |
|--------------------------------------------------------------------------------|
|   | ^stop service `(?P<srv>.+)`$                                               |
|--------------------------------------------------------------------------------|
|   | - Stop service `urandom`.                                                  |
|--------------------------------------------------------------------------------|
| Open a DuckDuckGo search in default browser.                                   |
|--------------------------------------------------------------------------------|
|   | ^lookup `(?P<search>.+)` online$                                           |
|--------------------------------------------------------------------------------|
|   | - Lookup `buildok` online.                                                 |
|--------------------------------------------------------------------------------|
| Uninstall software package(s).                                                 |
|--------------------------------------------------------------------------------|
|   | ^uninstall `(?P<pkgs>.+)`$                                                 |
|--------------------------------------------------------------------------------|
|   | - Uninstall `vim curl`.                                                    |
|--------------------------------------------------------------------------------|
| Run a command in shell.                                                        |
|--------------------------------------------------------------------------------|
|   | ^run `(?P<cmd>.+)`$                                                        |
|--------------------------------------------------------------------------------|
|   | - Run `echo hello friend how are you`.                                     |
|--------------------------------------------------------------------------------|
| Install software package(s) with Python's PIP package manager.                 |
|--------------------------------------------------------------------------------|
|   | ^install python packages? `(?P<pkgs>.+)`$                                  |
|   | ^install python dependencies(?: from `(?P<deps>.+)`)?$                     |
|--------------------------------------------------------------------------------|
|   | - Install Python package `buildok`.                                        |
|--------------------------------------------------------------------------------|
```

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
