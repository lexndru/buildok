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

from statement import Statement
from parser import Parser
from reader import Reader

from readers.file import FileReader
from readers.readme import ReadmeReader

from util.console import Console, timeit_log


def read(first=True):
    """Read all posible sources.

    Args:
        first (bool): Return steps from first source only.

    Return:
        tuple: Returns build steps.
    """
    rr = ReadmeReader()
    if not rr.exists():
        fr = FileReader()
        if not fr.exists():
            raise Console.fatal("Nothing to build from...")
    return Reader.get_first() if first else Reader.get_all()


def run(steps, last_step="n/a"):
    """Parse steps and build.

    Args:
        steps (tuple): Ordonated list of build steps.
        last_step (str): Last known step.

    Raises:
        SystemExit: If build steps are invalid.
        IOError: If build steps link to invalid I/O operations.
    """
    pr = Parser(steps)
    pr.prepare(validate=True)
    while pr.has_step():
        step = pr.get_step()
        if step is None:
            raise Console.fatal("Unexpected step found after: %s" % last_step)
        Console.info(step)
        results = Statement.parse(step)
        Console.eval(results)
        last_step = step

@timeit_log
def main():
    steps = read()
    if len(steps) == 0:
        raise Console.fatal("Nothing to build")
    run(steps)

if __name__ == "__main__":
    main()
