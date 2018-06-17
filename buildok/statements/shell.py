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

from subprocess import check_output, CalledProcessError, STDOUT

from buildok.action import Action


class ShellExec(Action):
    r"""Run a command in shell.

    Args:
        cmd (str): Raw shell command.

    Retuns:
        str: Output as string.

    Raises:
        OSError: If an invalid `cmd` is provided.

    Accepted statements:
        ^run `(?P<cmd>.+)`$

    Sample input:
        1) Run `echo hello friend how are you`.

    Expected:
        hello friend how are you
    """

    def run(self, cmd=None, *args, **kwargs):
        try:
            output = check_output(cmd.split(), stderr=STDOUT)
        except CalledProcessError as e:
            self.fail(e.output)
        if output is None:
            self.success("no error")
        else:
            self.success(output.decode('utf-8').strip())
