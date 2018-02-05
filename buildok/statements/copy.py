# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from os import path
from glob import glob
from shutil import copy
from distutils.dir_util import copy_tree

def copy_files(src=None, dst=None):
    r"""Copy files from a given source to a given destination.

    Args:
        src (str): Source of files.
        dst (str): Target destination of files.

    Retuns:
        str: Status of copy.

    Raises:
        OSError: If an invalid `src` or `dst` is provided.

    Accepted statements:
        ^copy from `(?P<src>.+)` to `(?P<dst>.+)`[\.\?\!]$
        ^copy `(?P<src>.+)` files to `(?P<dst>.+)`[\.\?\!]$
    """
    files, folders = 0, 0
    for item in glob(src):
        if path.isfile(item):
            copy(item, dst)
            files += 1
        elif path.isdir(item):
            copy_tree(item, dst)
            folders += 1
    return "Copied %d files and %d folders" % (files, folders)
