# imports - module imports
from cc.core.querylist import QueryList
from cc.model.resource import Resource

class SubCondition(Resource):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id")
        self.type       = kwargs.get("type")
        self.operator   = kwargs.get("operator")
        self.state      = kwargs.get("state")
        self.species    = kwargs.get("species", QueryList())