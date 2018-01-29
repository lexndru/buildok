# Buildok
A tool to automate build steps from README files.

## Getting started
There are two possible ways to make use of this tool. You either create a file named `.build` and write each step on a line;
or write a new section in your `README.md` file starting with one of the following statements: "how to build ok" or "build ok steps".
Each step you write has to respect the following pattern: `n) build step <punctuation>` where `n` is a number and `<punctuation>` is one of the following: `.`, `!` or `?`.

## How to build OK
1) Run `pwd`!
2) Copy `src/` files to `/tmp/_buildok`.
3) Go to `/tmp/_buildok`!
4) Run `python -m compileall .`.
5) Remove `*.py` files.
6) Run `ls -l`.
7) Run `zip -r build.zip .`.
8) Rename `build.zip` to `build`.

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
