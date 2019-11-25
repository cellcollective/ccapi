# imports - module imports
from ccpaw.core.querylist import QueryList
from ccpaw.model.resource import Resource

class Regulator(Resource):
    def __init__(self, component, type, conditions = [ ], *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)

        self.type       = type
        self.component  = component

        self.conditions = QueryList(conditions)

class PositiveRegulator(Regulator):
    def __init__(self, component, conditions = [ ], *args, **kwargs):
        Regulator.__init__(self, component, 'positive',
            conditions = conditions, *args, **kwargs)

class NegativeRegulator(Regulator):
    def __init__(self, component, conditions = [ ], *args, **kwargs):
        Regulator.__init__(self, component, 'negative',
            conditions = conditions, *args, **kwargs)