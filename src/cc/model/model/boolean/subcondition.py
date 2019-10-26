from cc.model.resource import Resource

class SubCondition(Resource):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id")

    def __repr__(self):
        repr_ = "<SubCondition id=%s>" % (self.id)
        return repr_