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

from buildok.statement import Statement
from buildok.converter import Converter
from buildok.matcher import Matcher
from buildok.reader import Reader

from buildok.readers.read_me import ReadmeReader

from buildok.structures.topic import Topic

from buildok.util.console import Console, timeit_log
from buildok.util.shell import Shell
from buildok.util.analyze import self_analyze, analyze, crash
from buildok.util.locker import lock, unlock



def setup(args):
    """Setup project path and verbose level.

    Args:
        args (object): Shell arguments.

    Return:
        bool: True if setup is done, otherwise False.
    """

    # Set verbose level
    Console.verbose = args.verbose

    # Look for a specific topic
    if args.topic is not None:
        Topic.set_project_topic(args.topic)

    # Set topic pattern
    if args.topic_pattern is not None:
        Topic.set_project_topic_pattern(args.topic_pattern)

    # Change project path from current working directory to choosen path
    if args.guide is not None:
        Reader.set_project_path(args.guide)

    # Convert build steps to script before exit
    if args.convert is not None:
        Converter.prepare(args.convert, Statement)

    return True


# def read():
#     """Read README.md file.
#
#     Return:
#         tuple: Returns build steps.
#     """
#     rr = ReadmeReader(validate=True)
#     rr.parse()
#     raise SystemExit
#     # steps = rr.get_steps()
#     # for s in steps:
#     #     print s
#         # if Parser.is_valid(s):
#         #     Console.info("  %s" % s)
#         # else:
#         #     Console.warn("  %s <--- bad grammar" % s)
#     return steps


# def run(steps, last_step="n/a"):
#     """Parse steps and build.
#
#     Args:
#         steps (tuple): Ordonated list of build steps.
#         last_step (str): Last known step.
#
#     Raises:
#         SystemExit: If build steps are invalid.
#         IOError: If build steps link to invalid I/O operations.
#     """
#     pr = Parser(steps)
#     pr.prepare(validate=True)
#     while pr.has_step():
#         step = pr.get_step()
#         if step is None:
#             raise Console.fatal("Unexpected step found after: %s" % last_step)
#         Console.info(step)
#         stmt = Statement(step)
#         results = stmt.run()
#         Console.eval(results)
#         last_step = step
#     Converter.check() and Converter.save()


@timeit_log
def main(error=None):
    """
    Launch buildok.

    Create a lock file and make sure no other build process is being launched
    until the lock file is removed.
    """

    # Parse command line args
    args = Shell.parse()

    # Prepare all statements
    Statement.prepare()

    # Run analysis and exit
    if args.analyze:
        return analyze(Statement)

    # Self-analyze buildok and continue or crash
    self_analyze(None, Statement) or crash("Run an analyze and correct problems")

    # Prepare reader and side-setup
    if not setup(args):
        raise SystemExit("Setup not ready. If problem persist try to reinstall")

    # Create a lock file
    lock()
    try:

        # Read guide and fetch all steps to run
        steps, topic = parse_guide(args)
        if topic is None or len(steps) == 0:
            raise Exception("Nothing to build")

        # Run all build steps
        run_topic(steps, topic)

    except Exception as e:
        error = e

    # Free lock file
    unlock()

    # Throw any errors found...
    if error is not None:
        raise Console.fatal(error)

def run_topic(steps, topic):
    print("\nPreparing to run steps for topic:")
    print("\033[92m%s\033[0m\n" % topic.get_title().upper())
    for i, step in enumerate(steps):
        print("Running step #%d\n---> \033[93m%s\033[0m" % (i+1, step.get_step()))
        print("     \033[95m%s\033[0m\n" % step.get_description())

def parse_guide(args):
    rr = ReadmeReader(validate=True)
    rr.read()
    rr.parse()

    # Preview scanned guide
    if args.preview:
        rr.preview(150)

    # Scan guide for topics
    if args.topic is None:
        guide = rr.get_guide()
    else:
        guide = rr.get_guide_by_topic()
    if guide is None:
        raise ValueError("Guide has no such topic")

    # Scan topics
    topic = None
    topics = [t.get_title() for t in guide.get_topics()]
    topics_len = len(topics)
    steps = []

    # Handle topics
    if topics_len == 0:
        print("No topics found!")
    else:
        print("Found the following topics:")
        for pos, name in enumerate(topics):
            print(("%" + str(len(str(topics_len))+1) + "d) %s") % (pos+1, name))
        print("\nChoose a topic to run, either by it's ID or by name.")
        print("Exit with ^C or leave field blank and press return.\n--\n")
        topic = get_topic(guide.get_topics())
        steps = topic.get_steps()
        Matcher.pair_all(steps)

    # Returns steps
    return steps, topic

def get_topic(topics):
    try:
        user_input = raw_input("> ")
    except KeyboardInterrupt:
        raise Exception("Program exits...")
    if len(user_input) == 0:
        raise Exception("Nothing to do...")
    try:
        pos = int(user_input)
        if pos <= 0 or pos > len(topics):
            raise IndexError
        return topics[pos-1]
    except IndexError:
        return get_topic(topics)
    except Exception:
        pass
    try:
        topic = unicode(user_input)
        partial_match = None
        drop_partial = False
        for each in topics:
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
    return get_topic(topics)
