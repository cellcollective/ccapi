# imports - module imports
from cc.core.querylist import QueryList
from cc.model.resource import Resource

class Regulator(Resource):
    def __init__(self, component, type, id=None, conditions=[], client = None):
        Resource.__init__(self, id = id, client = client)

        self.type       = type
        self.component  = component

        self.conditions = QueryList(conditions)

class PositiveRegulator(Regulator):
    def __init__(self, component, *args, **kwargs):
        Regulator.__init__(self, component, 'positive', *args, **kwargs)

class NegativeRegulator(Regulator):
    def __init__(self, component, *args, **kwargs):
        Regulator.__init__(self, component, 'negative', *args, **kwargs)