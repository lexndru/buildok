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

from buildok import __build__


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
        os_version = "N/A"

        # Basic support for windows systems
        if system().lower() == "windows":
            os_version = u"WINDOWS"
            cls.OS_NAME = "win"

        # Extended support for macos systems
        elif system().lower() == "darwin":
            os_version = u"MACINTOSH"
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
            os_version = u"%s (%s)" % (os_name.upper(), pretty_name.strip())
            cls.OS_NAME = os_name

        # Extended or full support for bsd systems
        elif "bsd" in system().lower():
            os_version =  "BSD"
            cls.OS_NAME = "bsd"

        # Print version
        print("Buildok {} [build {}] {}\n".format(version, __build__, os_version))

        # Print disclaimer
        print('THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR')
        print("IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,")
        print("FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE")
        print("AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER")
        print("LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,")
        print("OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE")
        print("SOFTWARE.\n")

        # Support
        print("Please report bugs at https://github.com/lexndru/buildok")
        print("Use --help to see a list of all options\n")
