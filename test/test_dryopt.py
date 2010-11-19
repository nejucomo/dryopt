#! /usr/bin/env python

# Tweak sys.path:
import sys, os
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'src'))

import unittest
from dryopt import Command, Option
from dryopt.errors import BadOptionType


class TestBase (unittest.TestCase):
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
        self.assertEqual(3, self.f(arg=3))

    def test_pycall_type_error(self):
        self.assertCallRaises(BadOptionType, self.f, 'banana')

    def test_cmdcall_no_args(self):
        self.assertEqual(0, self.f.commandline_call([]))

    def test_cmdcall_opt(self):
        self.assertEqual(7, self.f.commandline_call(['--arg', '7']))

    def test_cmdcall_type_error(self):
        self.assertCallRaises(SystemExit, self.f.commandline_call, ['--arg', 'banana'])


class NoDefaultOptTests (TestBase):
    def makeTarget(self):
        def f(arg = Option(type=int)):
            return arg
        return f

    def test_pycall_no_args(self):
        self.assertCallRaises(TypeError, self.f)

    def test_pycall_kwarg(self):
        self.assertEqual(3, self.f(arg=3))

    def test_cmdcall_no_args(self):
        self.assertCallRaises(SystemExit, self.f.commandline_call, [])

    def test_cmdcall_opt(self):
        self.assertEqual(7, self.f.commandline_call(['--arg', '7']))


class NoDefaultOptTests (TestBase):
    def makeTarget(self):
        def f(posarg):
            return posarg
        return f

    def test_pycall_no_args(self):
        self.assertCallRaises(TypeError, self.f)

    def test_pycall_posarg(self):
        self.assertEqual(3, self.f(3))

    def test_cmdcall_no_args(self):
        self.assertCallRaises(SystemExit, self.f.commandline_call, [])

    def test_cmdcall_posarg(self):
        self.assertEqual(7, self.f.commandline_call(['7']))


if __name__ == '__main__':
    unittest.main()

