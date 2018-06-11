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

from buildok.statements.chdir import ChangeDir
from buildok.statements.mkdir import MakeDir
from buildok.statements.symlink import MakeSymlink
from buildok.statements.web import ViewWeb
from buildok.statements.google import GoogleSearch
from buildok.statements.shell import ShellExec
from buildok.statements.chmod import ChangeMod
from buildok.statements.chown import ChangeOwner
from buildok.statements.kill import KillProcess
from buildok.statements.copy import Copy
from buildok.statements.move import Move
from buildok.statements.remove import Remove


class Statement(object):
    """Statement parser and launcher.

    Attributes:
        __actions (frozen set): Set of all known statements and actions.
        statements (list): List of all statements.
    """

    __actions = {
        ChangeDir,    # Change current working directory.
        MakeDir,      # Make a directory or make recursive directories.
        MakeSymlink,  # Make a symlink for a target source
        ViewWeb,      # Open a link in default browser.
        GoogleSearch, # Perform a Google search and open default browser.
        ShellExec,    # Run a command in shell.
        ChangeMod,    # Change permissions on file or directory.
        ChangeOwner,  # Change owner and group on file or directory.
        Copy,         # Copy files from a given source to a given destination.
        Move,         # Move files from a given source to a given destination.
        Remove,       # Remove files from a given source.
        KillProcess,  # Send SIGTERM signal to a process.
    }

    statements = {}

    @classmethod
    def prepare(cls):
        """Statement initialization.

        Loops through all supported actions, validates and maps statements with
        actions.

        Returns:
            bool: True if statements are mapped successful.
        """
        for action in cls.__actions:
            if not callable(action):
                raise SystemExit("Expected action to be callable")
            for line in action.parse_statements():
                exp = re.compile(line.strip(), re.I)
                cls.statements.update({exp: action})
        if len(cls.statements) < len(cls.__actions):
            raise SystemExit("Unable to map statements to action")

    @classmethod
    def find_statement(cls, stmt):
        """Lookup a statement.

        Returns:
            mixt: Statement if found, otherwise None.
        """
        return cls.statements.get(stmt)

    @classmethod
    def has_statement(cls, stmt):
        """Check whetever a statement exists.

        Returns:
            bool: True if statement is found.
        """
        return cls.find_statement(stmt) is not None

    @classmethod
    def get_statements(cls):
        """Statetements getter.

        Returns:
            iterator: A key-value itertator of all statements.
        """
        return cls.statements.iteritems()

    @classmethod
    def get_actions(cls):
        """Actions getter.

        Returns:
            list: All supported actions.
        """
        return cls.__actions
