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

import timeit

from buildok.statement import Statement
from buildok.converter import Converter
from buildok.matcher import Matcher
from buildok.reader import Reader
from buildok.report import Report

from buildok.readers.read_me import ReadmeReader

from buildok.structures.topic import Topic


class Script(object):
    """Automated script wrapper.

    Args:
        args         (list): List of shell arguments.
        topic         (str): Topic as a text string.
        steps        (list): List of topic steps.
        last_step     (int): Last step index.
        guide_topics (list): List of guide topics.
        convert      (bool): Convertion flag.
    """

    def __init__(self, args):
        self.args = args
        self.topic = None
        self.steps = None
        self.last_step = 0
        self.guide_topics = None
        self.convert = False

    def setup(self):
        """Setup project path, topic and topic pattern, convertion type.
        """

        # Look for a specific topic
        if self.args.topic is not None:
            Topic.set_project_topic(self.args.topic)

        # Set topic pattern
        if self.args.topic_pattern is not None:
            Topic.set_project_topic_pattern(self.args.topic_pattern)

        # Change project path from current working directory to choosen path
        if self.args.guide is not None:
            Reader.set_project_path(self.args.guide)

        # Convert build steps to script before exit
        if self.args.convert is not None:
            Converter.prepare(self.args.convert)
            self.convert = True

    def run(self):
        """Run all steps for the current selected topic.

        Args:
            convert (bool): Whether to convert steps before exist or not.
        """

        failed = False
        selected_topic = self.topic.get_title()
        alert_text = "Preparing to run:"
        title_len = len(alert_text) + len(selected_topic)
        print("")
        print("-" * (title_len + 1))
        print(u"%s \033[92m%s\033[0m" % (alert_text, selected_topic))
        print("-" * (title_len + 1))
        print("")

        # Loop steps and run each one
        start_time = timeit.default_timer()
        for self.last_step, step in enumerate(self.steps):
            print("Running step #%d" % (self.last_step+1))
            print("---> \033[93m%s\033[0m" % step.get_step())
            print("     \033[95m%s\033[0m" % step.get_description())
            try:
                success, output = step.run()
                if success:
                    print(u"   \033[92m\u2713 (OK) %s\033[0m" % output)
                else:
                    print(u"   \033[91m? (Failed) %s\033[0m" % output)
                Report.inc_step(1)
            except Exception as e:
                failed = True
                Report.set_error(e)
                print(u"   \033[91m? (Error) %s\033[0m" % str(e))
                break
            print("")
        stop_time = timeit.default_timer()

        # Save runtime
        Report.set_runtime(stop_time - start_time)

        # Wrap up...
        print("\nDone running steps...")
        if failed:
            print("An error occured while topic '%s' was running" % self.topic.get_title())
            Report.set_status("Failed")
        else:
            print("Topic '%s' has ran all steps with no errors" % self.topic.get_title())
            Report.set_status("OK")
        if self.convert:
            print("Converting...")
            Converter.check() and Converter.save(self.steps)
            print("Conversion done!")
        print("Closing...")

    def parse(self):
        """Parse guide and extract topics.

        User prompter asks to choose a topic from the selection in order to know
        what steps are queued.
        """

        rr = ReadmeReader(validate=True)
        rr.read()
        rr.parse()

        # Preview scanned guide
        if self.args.preview:
            rr.preview(150)

        # Scan guide for topics
        guide = rr.get_guide() if self.args.topic is None else rr.get_guide_by_topic()
        if guide is None:
            raise ValueError("Guide has no such topic")

        # Scan topics
        topic, steps = None, []
        topics = [t.get_title() for t in guide.get_topics()]
        topics_len = len(topics)

        # Handle no topics
        if topics_len == 0:
            raise ValueError("No topics found")

        # Handle topics
        print("Found the following topics:")
        for pos, name in enumerate(topics):
            print(("%" + str(len(str(topics_len))+1) + "d) %s") % (pos+1, name))
        print("\nChoose a topic to run, either by it's ID or by name.")
        print("Exit with ^C or leave field blank and press return.\n--\n")

        # Save topic and topic's steps
        self.guide_topics = guide.get_topics()
        self.topic = self.get_user_input()
        self.steps = self.topic.get_steps()

        # Pair each step with appropriate statement
        Matcher.pair_all(self.steps)

        # Prepare report
        Report.set_total_steps(len(self.steps))
        Report.set_topic(self.topic.get_title())
        return self

    def get_user_input(self):
        """Prompt user to choose a topic from a list.

        Exists if user leaves blank input or hits C^, otherwise continues until
        it receives a valid topic.
        """

        # Prompt for input
        try:
            user_input = raw_input("> ")

        # Exit on C^
        except KeyboardInterrupt:
            Report.set_status("Exit")
            raise Exception

        # Exit on blank input
        if len(user_input) == 0:
            Report.set_status("Exit")
            raise Exception

        # Validate index or start over
        try:
            pos = int(user_input)
            if pos <= 0 or pos > len(self.guide_topics):
                raise IndexError
            return self.guide_topics[pos-1]
        except IndexError:
            return self.get_user_input()
        except Exception:
            pass

        # Validate full or partial topic name or start over
        try:
            topic = unicode(user_input)
            partial_match = None
            drop_partial = False
            for each in self.guide_topics:
                if each.get_title().strip() == topic.strip():
                    return each
                if partial_match is not None and each.get_title().startswith(topic) and not drop_partial:
                    drop_partial = True
                if partial_match is None and each.get_title().startswith(topic):
                    partial_match = each
            if not drop_partial and partial_match is not None:
                return partial_match
        except Exception:
            pass

        # No valid topic found, start over
        return self.get_user_input()

    def print_report(self):
        """Dumps a report of the script outcome.
        """
        print("\nPreparing to print report...\n")
        Report.output()
        print("\n")
