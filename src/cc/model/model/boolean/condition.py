from cc.model.resource import Resource

class Condition(Resource):
    def __init__(self, *args, **kwargs):
        self.id                     = kwargs.get("id")
        self.state                  = kwargs.get("state")
        self.type                   = kwargs.get("type")
        self.operator               = kwargs.get("operator")
        self.sub_condition_operator = kwargs.get("sub_condition_operator")
        self.sub_conditions         = kwargs.get("sub_conditions")
        self.species                = kwargs.get("species", [ ])

    def __repr__(self):
        repr_ = "<Condition id=%s>" % self.id
        return repr_