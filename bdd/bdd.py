"""Behavior driven development module

.. :moduleauthor:: Jared Patrick <jared.patrick@gmail.com>

"""

import re
import pdb
import time
import inspect
import termcolor
import collections


_bdd_context = collections.OrderedDict()


class Expect(object):
    """The expect, BDD style assertion handler"""
    
    pdb = False

    def __init__(self, expr):
        """Expect constructor

        :param expr: the expression to run assertions against
        :type expr: any valid python expression

        :note:: set the Expect.pdb attribute to True for tracing
        """

        if self.pdb is True:
            pdb.set_trace()

        stack = inspect.stack()
        self.caller = {
            'file': stack[1][1],
            'line': stack[1][2],
            'func': stack[1][3],
            'repr': stack[1][4][0].strip().replace('\n', ''),
            'ctxt': stack[3][4][0].strip().replace('\n', '')
        }
        self.expr = expr

    def to_equal(self, value):
        """Expect boolean equal assertion

        :param value: the value to compare the instance.expr to

        :note:: thie method calls final for post assert reporting
        """

        self.caller['result'] = (self.expr == value)
        self.final()

    def to_not_equal(self, value):
        """Expect boolean not equal assertion

        :param value: the value to compare the instance.expr to

        :note:: thie method calls final for post assert reporting
        """

        self.caller['result'] = (self.expr != value)
        self.final()

    def to_be_true(self):
        """Expect boolean True assertion

        :param value: the value to compare the instance.expr to

        :note:: thie method calls final for post assert reporting
        """

        self.caller['result'] = (self.expr is True)
        self.final()

    def to_be_false(self):
        """Expect boolean false assertion

        :param value: the value to compare the instance.expr to

        :note:: thie method calls final for post assert reporting
        """

        self.caller['result'] = (self.expr is False)
        self.final()

    def to_raise(self, exc):
        """Expect exception assertion

        :param exc: the exception to attempt to capture
        :type exc: class Exception
        :return: the current Expect instance for next assertion phase
        :rtype: class Expect
        """

        self.raise_exc = exc
        return self

    def when_passed(self, *args):
        """Except exception argument processor

        :param args: the arguments to pass to the instance.expr
        :type args: list or tuple

        :note:: this method is the final assertion phase of a the
            raises assertion.

        :note:: thie method calls final for post assert reporting
        """

        try:
            self.expr(*args)
        except Exception as e:
            result = (type(e) == self.raise_exc)
        else:
            result = False

        self.caller['result'] = result
        self.final()

    def final(self):
        """BDD context setter"""

        _bdd_context[self.caller['ctxt']].append(self.caller)


def describe(desc):
    """The BDD describe decorator

    :param desc: the test description
    :type desc: str or type
    :return: the decorator wrapper function
    :rtype: function

    :note:: this method sets the bdd context for output reporting
    """

    module = inspect.stack()[1][4][0].strip().replace('\n', '')
    _bdd_context.setdefault(module, [])

    def wrapper(fn):
        """The BDD describe decoratr wrapper function

        :param fn: the decorated function
        :type fn: function
        :return: the decorated function with injected Expect arg
        :rtype: function
        """
        
        return fn(Expect)
    return wrapper


def output_report(start_time):
    """Output the test report for sucess and debug analysis

    :param start_time: the start timer for TTC rendering
    :type start_time: float
    """

    failure_data = []
    passed_tests = 0
    failed_tests = 0

    for desc, data in _bdd_context.items():
        patt = re.compile(r'@(.*\.)?describe\((\'|\")(?P<module>.*)(\'|\")\)')
        module = re.match(patt, desc).groupdict()['module']

        print '\n {}:'.format(module)
        for d in data:
            output_str = '   ' + ' '.join(d['func'].split('_'))

            if d['result'] is True:
                passed_tests += 1
                print termcolor.colored(output_str, 'green')
            else:
                failed_tests += 1
                failure_data.append((d['file'], d['line'], d['repr']))
                print termcolor.colored(output_str, 'red')

    if failed_tests > 0:
        for fd, line, reprd in failure_data:
            output = '\n File "{}", line {}, \n     {}'.format(fd, line, reprd)
            print termcolor.colored(output, 'yellow')

        status = termcolor.colored('FAILED', 'red')
    else:
        status = termcolor.colored('PASSED', 'green')

    amount_tests = (passed_tests + failed_tests)
    complete_time = time.clock() - start_time

    print '\n{} - {} total tests in {:.03f}s, {} passed, {} failed'.format(
        '{}'.format(status),
        amount_tests,
        complete_time,
        passed_tests,
        failed_tests
    )


def main():
    """The main method that triggers the test run process"""

    start_time = time.clock()
    output_report(start_time)
