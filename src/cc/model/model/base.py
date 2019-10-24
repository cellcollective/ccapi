from cc.model.resource import Resource

class Model(Resource):
    def __init__(self):
        self.id = None
        
    def __repr__(self):
        repr_ = "<Model id=%s>" % (self.id)
        return repr_