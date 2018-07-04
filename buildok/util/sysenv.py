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

from os import environ, listdir
from platform import system


class Sysenv(object):
    """System environment wrapper.

    Used in various files as a bash ENV-like to determine OS-related calls.
    """

    OS_NAME = ""

    @classmethod
    def check(cls, version):
        """Check system OS.

        Determine support and print CLI headers.
        """

        # Exit if version is missing
        if not version:
            raise SystemExit("Invalid launch")

        # Buildok version header
        header = "buildok v%s @ " % version

        # Basic support for windows systems
        if system().lower() == "windows":
            header += u"\033[92mwindows\033[0m system"
            cls.OS_NAME = "win"

        # Extended support for macos systems
        elif system().lower() == "darwin":
            header += u"\033[92mmacintosh\033[0m system"
            cls.OS_NAME = "mac"

        # Full support for linux systems
        elif system().lower() == "linux":
            files = [f for f in listdir("/etc") if f.endswith("-release")]
            distro, pretty_name = "", ""
            for each_file in files:
                data = []
                with open("/etc/%s" % each_file, "r") as fd:
                    data = fd.readlines()
                for line in data:
                    if line.lower().startswith("id") and distro == "":
                        _, distro = line.split("=", 1)
                    if line.lower().startswith("pretty_name") and pretty_name == "":
                        _, pretty_name = line.split("=", 1)
            os_name = distro.strip()
            header += u"\033[92m%s\033[0m system (%s)" % (os_name, pretty_name.strip())
            cls.OS_NAME = os_name

        # Extended or full support for bsd systems
        elif "bsd" in system().lower():
            header +=  u"\033[92mbsd\033[0m system"
            cls.OS_NAME = "bsd"

        print("%s\n--" % header)
