class Option (object):
    NoDefault = object() # immutable sentinel

    def __init__(self, default=NoDefault, kind=None, help=None):
        self.default = default
        if kind is None:
            assert default is not self.NoDefault, 'Either default or kind must be supplied.'
            kind = type(default)
        self.kind = kind
        self.help = help
        
