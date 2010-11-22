import sys
from dryopt.argdesc import ArgumentDescriptors
from dryopt.option import Option


class Command (object):
    """
    This decorates a commandline-oriented application function.
    """
    __slots__ = ['target', 'descriptors']

    def __init__(self, appfunc):
        self.target = appfunc
        self.descriptors = ArgumentDescriptors(appfunc)

    @property
    def name(self):
        return self.target.__name__

    def __call__(self, *a, **kw):
        '''
        Emulate python call.
        '''
        kwargs = {}

        # Positional non-vargs:
        for (name, value) in zip(self.descriptors.names, a):
            kwargs[name] = value

        # Key word vargs:
        for (name, value) in kw.items():
            if kwargs.has_key(name):
                raise TypeError(
                    '%s() got multiple values for keyword argument %r' % (
                        self.name, name))
            kwargs[name] = value

        # Defaults:
        for (name, opt) in self.descriptors.optmap.items():
            if (opt is not None) and not kwargs.has_key(name):
                d = opt.default
                if d is not Option.NoDefault:
                    kwargs[name] = d

        vargs = a[len(self.descriptors.names):]

        argsgiven = len(kwargs)
        argsneeded = len(self.descriptors.names)
        if argsgiven < argsneeded:
            plural = (argsneeded > 1) and 's' or ''
            if self.descriptors.varg is None:
                raise TypeError(
                    '%s() takes exactly %d argument%s (%d given)' % (
                        self.name, argsneeded, plural, argsgiven))
            else:
                raise TypeError(
                    '%s() takes at least %d argument%s (%d given)' % (
                        self.name, argsneeded, plural, argsgiven))

        return self.target(*vargs, **kwargs)

    def commandline_call(self, args = sys.argv[1:]):
        vargs, kwargs = self.descriptors.parse_commandline(args)
        return self(*vargs, **kwargs)

