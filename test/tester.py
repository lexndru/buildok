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

from __future__ import print_function

from re import compile
from importlib import import_module

from buildok.statement import Statement
from buildok.parser import Parser

class Tester(object):

    IMPORT_PATTERN = compile(r"^from\s+(?P<mod>buildok\.statements\.\w+)\s+import\s+(?P<stmt>\w+)$")
    STATEMENT_PY = "buildok/statement.py"
    STATEMENTS_MOD = "buildok.statements"
    TEST_INPUT_OUTPUT = ("build steps", "expected")

    @classmethod
    def scan(cls):
        imports = []
        with open(cls.STATEMENT_PY) as file_:
            for line in file_.readlines():
                if not line.startswith("from"):
                    continue
                result = cls.IMPORT_PATTERN.match(line)
                statement = result.group("stmt").strip()
                module = result.group("mod").strip()
                imports.append((module, "%s_test" % statement))
        return imports

    @classmethod
    def run_test(cls, imports, *args):
        module, func = imports
        tin, tout = cls.TEST_INPUT_OUTPUT
        try:
            mod = import_module(module)
            if not hasattr(mod, func):
                raise ImportError
            test = getattr(mod, func)
            steps = Statement.parse_func(test, tin)
            pr = Parser(tuple(steps))
            pr.prepare()
            step = pr.get_step()
            expected = Statement.parse_func(test, tout)
            output = Statement.parse(step)
            if len(expected) != 1:
                raise Exception("Incomplete or invalid test: no expectations")
            else:
                expected = expected[0]
            assert output == expected, "Expected '%s' got '%s'" % (expected, output)
            print(u"[Test] \033[92mPassed OK %s\033[0m" % module)
        except ImportError:
            print(u"[Test] \033[93mMissing test: %s\033[0m" % module)
        except AssertionError as e:
            print(u"[Test] \033[101mFailed %s: %s\033[0m" % (module, e))
        except Exception as e:
            print(u"[Test] \033[91mError %s: %s\033[0m" % (module, e))

def main():
    for t in Tester.scan():
        try:
            Tester.run_test(t)
        except Exception as e:
            raise
