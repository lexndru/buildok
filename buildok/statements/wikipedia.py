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

import webbrowser as wb

from buildok.action import Action


class WikipediaSearch(Action):
    r"""Open a Wikipedia search in default browser.

    Args:
        search (str): Search string to lookup.

    Retuns:
        str: Output as string.

    Raises:
        TypeError: If an invalid `search` is provided.

    Accepted statements:
        ^wiki(?:pedia)? `(?P<search>.+)`$

    Sample (input):
        1) Wikipedia `buildok`.

    Expected:
        Wikipedia results => https://duckduckgo.com/?q=buildok
    """

    def run(self, search=None, *args, **kwargs):
        url = r"https://wikipedia.org/wiki/{}".format(search)
        try:
            wb.get().open(url, new=2)
            self.success("Wikipedia results => %s" % url)
        except TypeError as e:
            self.fail(str(e))
        except Exception as e:
            self.fail("Cannot open \"%s\"" % url)

    @classmethod
    def _convert_bash(cls, search=None, *args, **kwargs):
        if search is None:
            return "echo Nothing to lookup"
        return "echo Cannot lookup on wikipedia \"%s\"" % search
