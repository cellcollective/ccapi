# imports - module imports
from cc.core.querylist import QueryList
from cc.model.resource import Resource

class Regulator(Resource):
    def __init__(self, species, type, id=None, client = None):
        Resource.__init__(self, id = id, client = client)

        self.type       = type
        self.species    = species

        # self.of         = kwargs.get("of")
        # self.conditions = kwargs.get("conditions", QueryList())

    def __repr__(self):
        repr_ = "<Regulator id=%s type='%s'>" % (self.id, self.type)
        return repr_

class PositiveRegulator(Regulator):
    def __init__(self, species, *args, **kwargs):
        Regulator.__init__(self, species, 'positive', *args, **kwargs)

class NegativeRegulator(Regulator):
    def __init__(self, species, *args, **kwargs):
        Regulator.__init__(self, species, 'negative', *args, **kwargs)