# imports - module imports
from cc.core.querylist  import QueryList
from cc.model.resource  import Resource
from cc.config          import DEFAULT
from cc.util.string     import ellipsis

class Model(Resource):
    """
    The Base Model class.

    Usage::

        >>> from cc.model import Model
        >>> model = Model()
    """
    
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id")
        self.name       = kwargs.get("name", DEFAULT["MODEL_NAME"])
        self.versions   = kwargs.get("versions",  QueryList())
        self.documents  = kwargs.get("documents", QueryList())
        self._client    = kwargs.get("_client")
        
    def __repr__(self):
        name    = ellipsis(self.name, threshold = 15)
        repr_   = "<Model id=%s name='%s'>" % (self.id, name)
        return repr_

    def remove(self):
        data = dict(("%s/%s" % (self.id, model.version), None)
            for model in self.versions
        )
        self._client.post("_api/model/save", json = data)