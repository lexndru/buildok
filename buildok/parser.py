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

class Parser(object):
    """Build steps parser.

    Attributes:
        steps (tuple): Ordonated list of build steps.
        build (list): List of ready-to-run instructions.

    Raises:
        TypeError: If provided `steps` are not a tuple.
    """
    PATTERN = re.compile(r"^\d+(?:\.\d+)?\)\s*(?P<step>.+)[^\!\.\?][\!\.\?]{1}$", re.U)

    def __init__(self, steps):
        if not isinstance(steps, tuple):
            raise TypeError("Unexpected steps datatype")
        self.steps, self.build = steps, [None] * len(steps)

    def is_valid(self, step):
        """Test if a step is valid.

        Args:
            step (str): Raw step to test.

        Returns:
            bool: True if `step` has a valid pattern, otherwise False.
        """
        result = self.PATTERN.match(step)
        try:
            step = result.group("step")
            return len(step) > 1
        except:
            return False

    def prepare(self, validate=False):
        """Prepare, parse and sort build steps.

        Args:
            validate (bool): Stop on first error if True.

        Returns:
            self: Parser
        """
        for s in self.steps:
            if not self.is_valid(s):
                self.build.pop()
                continue
            sep = s.find(")")
            pos = int(s[:sep])
            self.build[pos-1] = s[sep+1:].lstrip()
        self.build.reverse()
        return self

    def has_step(self):
        """Check if there is a next step available.

        Returns:
            bool: True if steps are in queue, otherwise False.
        """
        return len(self.build) > 0

    def get_step(self):
        """Return step as string.

        Raises:
            IndexError: If no more steps are in queue.

        Returns:
            str: Raw step string.
        """
        return self.build.pop()