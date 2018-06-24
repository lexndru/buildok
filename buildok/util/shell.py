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

from argparse import ArgumentParser


class Shell(object):
    """Shell argument parser.

    Attributes:
        parser (ArgumentParser): Argument parser.
        args (dict): Dictionary of arguments.
    """

    parser = ArgumentParser(description="A tool to automate build steps from README files")
    args = {
        ("-g", "--guide"): {
            "action": "store",
            "dest": "guide",
            "help": "path to guide"
        },
        ("-v", "--verbose"): {
            "action": "store_true",
            "dest": "verbose",
            "help": "verbose output"
        },
        ("-c", "--convert"): {
            "action": "store",
            "dest": "convert",
            "help": "create automated build scripts from build steps"
        },
        ("-a", "--analyze"): {
            "action": "store_true",
            "dest": "analyze",
            "help": "scan all known statements"
        },
        ("-t", "--topic"): {
            "action": "store",
            "dest": "topic",
            "help": "set topic to build"
        },
        (None, "--topic-pattern"): {
            "action": "store",
            "dest": "topic_pattern",
            "help": "set topic pattern"
        },
        ("-p", "--preview"): {
            "action": "store_true",
            "dest": "preview",
            "help": "visual preview of scanned guide"
        },
        (None, "--install-policy"): {
            "action": "store",
            "dest": "install_policy",
            "help": "set or install a system utility policy"
        },
    }

    @classmethod
    def parse(cls):
        """Ceate parser listener.

        Return:
            Namespace: Namespace of parser arguments from shell.
        """
        for keys, vals in cls.args.iteritems():
            short, long_ = keys
            if short is None:
                cls.parser.add_argument(long_, **vals)
            else:
                cls.parser.add_argument(short, long_, **vals)
        return cls.parser.parse_args()
