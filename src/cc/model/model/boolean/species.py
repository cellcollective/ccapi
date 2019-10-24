from cc.model.resource import Resource

class Species(Resource):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id_")
        self.name       = kwargs.get("name")
        self.created    = kwargs.get("created")
        self.updated    = kwargs.get("updated")

    def __repr__(self):
        repr_ = "<Species id=%s name='%s'>" % (self.id, self.name)
        return repr_