# imports - module imports
from cc.core.querylist import QueryList
from cc.model.resource import Resource

class Regulator(Resource):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id")
        self.type       = kwargs.get("type")
        self.species    = kwargs.get("species")
        self.of         = kwargs.get("of")
        self.conditions = kwargs.get("conditions", QueryList())

    def __repr__(self):
        repr_ = "<Regulator id=%s type='%s'>" % (self.id, self.type)
        return repr_