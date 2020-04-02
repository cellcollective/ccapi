# imports - module imports
from ccapi.core.querylist import QueryList
from ccapi.model.resource import Resource

class Regulator(Resource):
    _REPR_ATTRIBUTES = [
        dict({
             "name": "number_of_conditions",
            "title": "Number of Conditions",
              "key": lambda x: len(x.conditions)
        })
    ]

    def __init__(self, species, type, conditions = [ ], *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)

        self.type       = type
        self.species    = species

        self.conditions = QueryList(conditions)

class PositiveRegulator(Regulator):
    def __init__(self, species, conditions = [ ], *args, **kwargs):
        Regulator.__init__(self, species, 'positive',
            conditions = conditions, *args, **kwargs)

class NegativeRegulator(Regulator):
    def __init__(self, species, conditions = [ ], *args, **kwargs):
        Regulator.__init__(self, species, 'negative',
            conditions = conditions, *args, **kwargs)