class DryOptError (Exception):
    def __init__(self, *values):
        self.values = values
        Exception.__init__(self, (self.Template, values))

    def __str__(self):
        return self.Template % self.values

class MissingPositionalArgs (DryOptError):
    Template = 'Not enough positional arguments supplied; expecting %d, received: %r'

class TooManyPositionalArgs (DryOptError):
    Template = 'Too many positional arguments supplied; expecting %d, received: %r'
            
class MissingOption (DryOptError):
    Template = 'Required option %r not supplied.'

class BadOptionType (DryOptError):
    Template = 'Could not convert %r to type %r for option %r.'


