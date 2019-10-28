from cc.model.resource import Resource

class Species(Resource):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id_")
        self.name       = kwargs.get("name")
        self.type       = kwargs.get("type")
        self.created    = kwargs.get("created")
        self.updated    = kwargs.get("updated")
        self.regulators = kwargs.get("regulators", [ ])

    def __repr__(self):
        repr_ = "<Species id=%s name='%s'>" % (self.id, self.name)
        return repr_

    def __eq__(self, other):
        return self.id == other.id