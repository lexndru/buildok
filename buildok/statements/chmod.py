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

from os import chmod, getcwd

def change_mod(mode="400", path=None):
    r"""Change permissions on file or directory.

    Args:
        mode (str): Octal integer permissions.
        path (str): Path to file or directory.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `path` is provided.
        TypeError: If an invalid `mode` is provided.

    Accepted statements:
        ^change permissions to `(?P<mode>.+)`[\.\?\!]$
        ^change permissions `(?P<mode>.+)` for `(?P<path>.+)`[\.\?\!]$
        ^set permissions to `(?P<mode>.+)` for `(?P<path>.+)`[\.\?\!]$
    """
    try:
        mode = oct(int("0%s" % mode, 8))
        if path is None:
            path = getcwd()
        chmod(path, mode)
        return "Changed permissions %s => %s" % (mode, path)
    except OSError as e:
        raise e
    except TypeError as e:
        raise e
    return "Nothing to do"


def change_mod_test(*args, **kwargs):
    """Test if it's possible to change permissions.

    Build steps:
        1) Run `touch /tmp/buildok_test.txt`.
        2) Change permissions to `400` for `/tmp/buildok_test.txt`.

    Expected:
        Changed permissions 400 => /tmp/buildok_test.txt
    """
    return change_mod(*args, **kwargs)
