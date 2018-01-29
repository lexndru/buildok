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

import re

from statements.shell import exec_shell
from statements.chdir import change_dir
from statements.copy import copy_files
from statements.move import move_files
from statements.remove import remove_files

class Statement(object):
    """Statement parser.

    Attributes:
        statement_header (str): Lookup string before build steps.
        known_actions (frozen set): Set of all known statements and actions.
    """
    statement_header = r"accepted statements"
    known_actions = {
        exec_shell,
        change_dir,
        copy_files,
        move_files,
        remove_files,
    }

    @classmethod
    def parse(cls, step):
        """Translate a step into a statement.

        Args:
            step (str): Raw build step to lookup.

        Return:
            NoneType: If no statement was found, otherwise mixt.
        """
        for func in cls.known_actions:
            for stmt in cls.parse_func(func):
                result = re.match(stmt, step, re.I)
                if result is not None:
                    return func(*result.groups())
        return None

    @classmethod
    def parse_func(cls, func):
        """Extract "accepted statements" from function doc string.

        Args:
            func (function): Statement function equivalent.

        Raises:
            SystemExit: If `func` is not a function.

        Returns:
            list: List of possible statements.
        """
        if not callable(func):
            raise SystemExit("Expected callable function")
        lines = func.__doc__.split("\n")
        start_line = -1
        newlines = []
        for idx, line in enumerate(lines):
            line = line.rstrip()
            if cls.statement_header in line.lower():
                start_line = idx
                break
            if len(line) == 0:
                newlines.append(idx)
        if len(newlines) > 0 and newlines[-1] > start_line:
            rows = lines[1 + start_line:newlines[-1]]
        else:
            rows = lines[1 + start_line:]
        return [l.strip() for l in rows if l.strip()]
