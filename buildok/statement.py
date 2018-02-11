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

from buildok.statements.web import exec_web
from buildok.statements.shell import exec_shell
from buildok.statements.chdir import change_dir
from buildok.statements.chmod import change_mod
from buildok.statements.chown import change_own
from buildok.statements.mkdir import make_dir
from buildok.statements.kill import kill_proc
from buildok.statements.copy import copy_files
from buildok.statements.move import move_files
from buildok.statements.remove import remove_files
from buildok.statements.symlink import make_symlink

class Statement(object):
    """Statement parser.

    Attributes:
        statement_header (str): Lookup string before build steps.
        known_actions (frozen set): Set of all known statements and actions.
    """
    statement_header = r"accepted statements"
    known_actions = {
        exec_web,
        exec_shell,
        change_dir,
        change_mod,
        change_own,
        copy_files,
        move_files,
        remove_files,
        make_symlink,
        make_dir,
        kill_proc,
    }

    @classmethod
    def analyze(cls):
        """Analyze all statements.

        Returns:
            list: List of all statements including duplicated.
        """
        results, stmts = [], set([])
        for idx1, func in enumerate(cls.known_actions):
            class_ = func.__name__
            funcs = cls.parse_func(func)
            for idx2, stmt in enumerate(funcs):
                status = "duplicated" if stmt in stmts else "ok"
                line = ("%d.%d" % (idx1+1, idx2+1), class_, stmt, status)
                results.append(line)
                stmts.add(stmt)
        set_max = lambda o, s: len(s) if len(s) > o else o
        ids_max_len, grp_max_len, stmt_max_len, status_max_len = 0, 0, 0, 0
        for ids, grp, stmt, status in results:
            ids_max_len, grp_max_len = set_max(ids_max_len, ids), set_max(grp_max_len, grp)
            stmt_max_len, status_max_len = set_max(stmt_max_len, stmt), set_max(status_max_len, status)
        line = "| %-" + str(ids_max_len) + "s | %-" + str(grp_max_len) + "s | "
        line += "%-" + str(stmt_max_len) + "s | %-" + str(status_max_len) + "s |"
        header = line % ("", "Group", "Statement", "")
        sep = "-" * len(header)
        lines = [header, sep]
        for r in results:
            color = "\033[101m" if r[-1] == "duplicated" else "\033[94m"
            lines.append((color + line + "\033[0m") % r)
        lines.append(sep)
        return lines

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
                    return func(**result.groupdict())
        return None

    @classmethod
    def parse_func(cls, func, statement_header=None):
        """Extract "accepted statements" from function doc string.

        Args:
            func (function): Statement function equivalent.
            statement_header (str): Headline to look up (default None).

        Raises:
            SystemExit: If `func` is not a function.

        Returns:
            list: List of possible statements.
        """
        if not callable(func):
            raise SystemExit("Expected callable function")
        if statement_header is None:
            statement_header = cls.statement_header
        lines = func.__doc__.split("\n")
        start_line = -1
        newlines = []
        for idx, line in enumerate(lines):
            line = line.rstrip()
            if len(line.strip()) == 0:
                newlines.append(idx)
            if start_line == -1 and statement_header in line.lower():
                start_line = idx
        if len(newlines) > 0:
            stop = -1
            for i in newlines:
                if i > start_line:
                    stop = i
                    break
            if stop > start_line:
                rows = lines[1 + start_line:stop]
            else:
                rows = lines[1 + start_line:]
        else:
            rows = lines[1 + start_line:]
        return [l.strip() for l in rows if l.strip()]
