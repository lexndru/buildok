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

from reader import Reader

class ReadmeReader(Reader):
    """File class helper to detect and read a README file.

    Attributes:
        filename (string): Path to README filename.
        context (string): Original context of `filename`.
        build_section (tuple): Build section accepted titles.
    """
    READ_MODE = "rb"
    filename = "README.md"
    context = []
    build_section = ("how to build ok", "build ok steps")

    def read(self):
        """Read README file content.

        Returns:
            str: Returns build steps from `filename` content on success.
            NoneType: Returns None on failure.

        Raises:
            IOError: If `filename` does not exist or does not have permissions.
        """
        with open(self.filename, self.READ_MODE) as file_:
            ctx = file_.readlines()
            self.parse_build(ctx)
            return self.context
        return None

    def parse_build(self, ctx=[]):
        """Parse README file and look for build steps.

        Args:
            ctx (list): Original `filename` content as lines.

        Returns:
            list: Non-empty list if build steps are found.
        """
        steps_start, steps_stop = -1, -1
        steps, newlines = [], []
        for idx, line_ in enumerate(ctx):
            line = line_.rstrip()
            if steps_start > -1:
                if len(newlines) > 0 and newlines[-1] > steps_start + 1:
                    break
                steps.append(line)
            if len(line) == 0:
                newlines.append(idx)
            for section in self.build_section:
                if section in line.lower():
                    steps_start = idx
                    break
            if len(newlines) > 2:
                a, b = newlines[:-3:-1]
                if a == b + 1:
                    steps_stop = idx
                    break
        self.context = [s for s in steps if s]
