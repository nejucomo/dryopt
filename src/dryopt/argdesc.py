from dryopt.inspection import inspect_appfunc


class ArgumentDescriptors (object):
    __slots__ = ['names', 'optmap', 'varg']

    def __init__(self, appfunc):
        opts, varg = inspect_appfunc(appfunc)
        self.names = [k for (k,_) in opts]
        self.optmap = dict(opts)
        self.varg = varg
