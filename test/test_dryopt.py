#! /usr/bin/env python

# Tweak sys.path:
import sys, os
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'src'))

import unittest
from dryopt import Command, Option
from dryopt import usage


class TestBase (unittest.TestCase):
    def __str__(self):
        c = self.__class__
        return '%s.%s.%s' % (c.__module__, c.__name__, self._testMethodName)

    def setUp(self):
        self.f = Command(self.makeTarget())

    def assertCallRaises(self, ExcClass, f, *args, **kw):
        try:
            x = f(*args, **kw)
        except Exception, e:
            if isinstance(e, ExcClass):
                return # pass.  We saw the expected exception.
            else:
                raise
        self.fail('Expected exception %r, but returned value %r.' % (ExcClass, x))


class MinimalOptTests (TestBase):
    def makeTarget(self):
        def f(arg = Option(0)):
            return arg
        return f

    def test_pycall_no_args(self):
        self.assertEqual(0, self.f())

    def test_pycall_kwarg(self):
        for v in [3, 'banana']:
            self.assertEqual(v, self.f(arg=v))

    def test_pycall_posarg(self):
        for v in [3, 'banana']:
            self.assertEqual(v, self.f(v))

    def test_cmdcall_no_args(self):
        self.assertEqual(0, self.f.commandline_call([]))

    def test_cmdcall_opt(self):
        self.assertEqual(7, self.f.commandline_call(['--arg', '7']))

    def test_cmdcall_type_error(self):
        self.assertCallRaises(SystemExit, self.f.commandline_call, ['--arg', 'banana'])


class NoDefaultOptTests (TestBase):
    def makeTarget(self):
        def f(arg = Option(parse=int)):
            return arg
        return f

    def test_pycall_no_args(self):
        self.assertCallRaises(usage.TooFewArgs, self.f)

    def test_pycall_kwarg(self):
        self.assertEqual(3, self.f(arg=3))

    def test_cmdcall_no_args(self):
        self.assertCallRaises(SystemExit, self.f.commandline_call, [])

    def test_cmdcall_opt(self):
        self.assertEqual(7, self.f.commandline_call(['--arg', '7']))


class OnlyPosArgTests (TestBase):
    def makeTarget(self):
        def f(posarg):
            return posarg
        return f

    def test_pycall_no_args(self):
        self.assertCallRaises(usage.TooFewArgs, self.f)

    def test_pycall_posarg(self):
        self.assertEqual(3, self.f(3))

    def test_cmdcall_no_args(self):
        self.assertCallRaises(SystemExit, self.f.commandline_call, [])

    def test_cmdcall_posarg(self):
        self.assertEqual('7', self.f.commandline_call(['7']))


class OnlyVarArgsTests (TestBase):
    Vectors = [(), (1,), ('apple', 'banana')]

    def makeTarget(self):
        def f(*a):
            return a
        return f

    def test_pycall(self):
        for args in self.Vectors:
            self.assertEqual(args, self.f(*args))

    def test_cmdcall(self):
        for args in self.Vectors:
            args = tuple(map(str, args))
            self.assertEqual(args, self.f.commandline_call(args))


if __name__ == '__main__':
    unittest.main()

