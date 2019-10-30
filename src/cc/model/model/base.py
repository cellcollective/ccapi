from cc.model.resource import Resource
from cc.util.string    import ellipsis

class Model(Resource):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id")
        self.name       = kwargs.get("name", "")
        self.versions   = kwargs.get("versions",  [ ])
        self.documents  = kwargs.get("documents", [ ])
        
    def __repr__(self):
        name  = ellipsis(self.name, threshold = 10)
        repr_ = "<Model id=%s name='%s'>" % (self.id, name)
        return repr_