from cc.model.resource import Resource

class Condition(Resource):
    def __init__(self, *args, **kwargs):
        self.id             = kwargs.get("id")
        self.sub_conditions = kwargs.get("sub_conditions") 

    def __repr__(self):
        repr_ = "<Condition id=%s>" % self.id
        return repr_