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

from subprocess import call

from buildok.action import Action


class InstallPackage(Action):
    r"""Install new software package(s).

    Args:
        pkgs (str): Packages to install.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        Exception: If any of `pkgs` are not found in repositories.

    Accepted statements:
        ^install `(?P<pkgs>.+)`$

    Sample input:
        1) Install `vim curl`.

    Expected:
        Installed 2 new packages
    """

    def run(self, pkgs=None, *args, **kwargs):
        packages = pkgs.split()
        if len(packages) == 0:
            return self.fail("No packages to install...")
        try:
            installed_pkgs = 0
            if self.env.OS_NAME == "debian":
                installed_pkgs = self.install_debian(packages)
            if installed_pkgs > 0:
                self.success("Installed %d new packages" % installed_pkgs)
            else:
                self.fail("Failed to install packages...")
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def _convert_bash(cls, pkgs=None, *args, **kwargs):
        if pkgs is None:
            return "echo nothing to install"
        return "apt-get install -y %s" % pkgs

    def install_debian(self, packages):
        installed = 0
        for pkg in packages:
            if 0 == call(["apt-get", "install", "-y", pkg]):
                installed += 1
        return installed
