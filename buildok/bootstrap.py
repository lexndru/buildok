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

    # # Statement.find():
    # for k, v in Statement.get_statements():
    #     print(k, v)
    # # print Statement.get_actions()

    # Create a lock file
    # lock()
    try:

        # Prepare reader and side-setup
        if not setup(args):
            raise Exception("Setup not ready")

        # Read build steps and validate-parse through
        rr = ReadmeReader(validate=True)
        rr.read()
        rr.parse()

        # Preview scanned guide
        if args.preview:
            rr.preview(150)

        raise SystemExit("WIP...")

        # Scan guide for topics
        if args.topic is None:
            guide = rr.get_guide()
        else:
            guide = rr.get_guide_by_topic()
        if guide is None:
            raise ValueError("Guide has no such topic")

        # Scan topics
        topics = [t.get_title() for t in guide.get_topics()]
        topics_len = len(topics)

        if topics_len > 0:
            print("Found the following topics:")
            for pos, name in enumerate(topics):
                print(("%" + str(len(str(topics_len))+1) + "d) %s") % (pos+1, name))
            steps = read_steps(guide.get_topics())

            for step in steps:
                print(step)
                if lookup_statements(step):
                    print(step.run())
                else:
                    print("nothing to do...")
                # fun = Statement.lookup(step.get_step())
                # step.set_statement(fun)
            #     for exp, fun in Statement.get_statements():

            print("total steps =",len(steps))

        # for s in t.get_steps():
        #     print s

        raise SystemExit
        # steps = read()
        # if len(steps) == 0:
        #     raise Exception("Nothing to build")

        # Run all build steps
        # run(steps)

    except Exception as e:
        error = e

    # Free lock file
    # unlock()

    # Throw any errors found...
    if error is not None:
        raise Console.fatal(error)

def lookup_statements(step):
    for exp, fun in Statement.get_statements():
        args = exp.match(step.get_step())
        if args is not None:
            step.set_statement(fun)
            step.set_arguments(args.groups())
            return True
    return False

def read_steps(topics):
    user_input = raw_input("Run by id or by topic name: ")
    try:
        pos = int(user_input)
        if pos <= 0 or pos > len(topics):
            raise Exception
        return topics[pos-1].get_steps()
    except Exception as e:
        pass
    try:
        topic = unicode(user_input)
        for each in topics:
            if each.get_title() == topic:
                return each.get_steps()
    except Exception as e:
        pass
    return []
