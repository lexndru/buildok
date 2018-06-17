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

from buildok.reader import Reader
from buildok.matcher import Matcher

from buildok.structures.instruction import Instruction
from buildok.structures.guide import Guide
from buildok.structures.topic import Topic

from buildok.util.console import Console
from buildok.util.readerr import ReadError


class ReadmeReader(Reader):
    """File class helper to detect and read a README file.

    Class arguments:
        last_guide      (Guide): Last Guide instance.
        last_topic      (Topic): Last Topic instance.
        last_step (Instruction): Last Instruction instance.
        delimiter         (str): Payload delimiter.
        recent_topic      (str): Holder for recent topic.
    """

    READER = r"README.md"

    class NoPayloadError(ReadError):

        error = r"Instruction payload missing for step: %s"

    class UnclosedPayloadError(ReadError):

        error = r"Unclosed instruction payload for step: %s"

    class BadFormatError(ReadError):

        error = r"Missing instruction payload for step: %s"

    last_guide = None
    last_topic = None
    last_step = None

    recent_topic = "n/a"

    delimiter = r"```"
    __topicre = Topic.prepare(r"## how to (?P<topic>[\s\w\-]+)")

    def parse(self):
        """Parse build steps file.

        Loop through all steps and check for topics and instructions.
        """
        self.last_guide = Guide()
        while self.has_next():
            line = self.get_line()
            self.check_topic(line)
            self.check_instruction(line).check_payload(self.next_content())
            self.next_line()

    def get_guide(self):
        """Get latest guide.

        Returns:
            mixt: Guide instance if is set, otherwise None.
        """
        return self.last_guide

    def get_guide_by_topic(self):
        """Get new guide filtered by topic.

        Returns:
            mixt: Guide instance if is set, otherwise None.
        """
        for topic in self.last_guide.get_topics():
            if Topic.TOPIC == topic.get_title():
                guide = Guide()
                guide.add_topic(topic)
                return guide
        return None

    def check_topic(self, line):
        """Check line from build steps if it's a topic.

        Args:
            line (str): Build step line as string.

        Returns:
            self: Self instance.
        """
        scan = Topic.PATTERN.match(line)
        if scan is not None:
            title = scan.group("topic")
            self.last_topic = Topic(self.get_line_number(), title)
            self.last_guide.add_topic(self.last_topic)
        return self

    def check_instruction(self, line):
        """Check line from build steps if it's an instruction.

        Args:
            line (str): Build step line as string.

        Raises:
            Exception: If last topic is missing and step is found.

        Returns:
            self: Self instance.
        """
        scan = Instruction.PATTERN.match(line)
        if scan is not None:
            step = scan.group("step")
            punct = scan.group("punct")
            self.last_step = Instruction(self.get_line_number(), step, punct)
            if self.last_topic is None:
                raise Exception("Unaccepted instruction: missing topic in guide")
            self.last_topic.add_step(self.last_step)
        return self

    def check_payload(self, content):
        """Check line from build steps if it's an instruction payload.

        Args:
            content (list): Build step lines ahead of current cursor.

        Returns:
            self: Self instance.
        """
        if self.last_step is None or self.last_step.punct != Instruction.RunType.ARGS:
            return self
        newlines, borders = 0, []
        for i, next_line in enumerate(content):
            if len(borders) == 0 and newlines > 1:
                raise self.NoPayloadError(self.last_step)
            if next_line.strip() == "":
                newlines += 1
                continue
            if next_line.strip() == self.delimiter:
                borders.append(i)
            if len(borders) == 2:
                break
        if len(borders) == 1:
            raise self.UnclosedPayloadError(self.last_step)
        try:
            a, z = borders
            self.last_step.set_payload(content[1+a:z])
            self.skip_line(lines=z+1)
            self.last_step = None
        except Exception as e:
            raise self.BadFormatError(self.last_step)
        return self

    def preview_line(self, line, preview_line):
        """Preview line from build file.

        Useful to customize the display row of a line.
        """
        line_topic = Topic.PATTERN.match(line)
        if line_topic is not None:
            self.recent_topic = line_topic.group("topic")
            line_desc = "topic (%s)" % self.recent_topic
            return Console.green(preview_line, "<--- %s" % line_desc)
        line_step = Instruction.PATTERN.match(line)
        if line_step is not None:
            step = line_step.group("step")
            if Matcher.is_valid(step):
                line_desc = "instruction (%s)" % self.recent_topic
                method = "yellow"
            else:
                line_desc = "unsupported instruction (%s)" % self.recent_topic
                method = "red"
            return getattr(Console, method)(preview_line, "<--- %s" % line_desc)
        return Console.darkgray(preview_line)
