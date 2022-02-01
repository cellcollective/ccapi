# imports - module imports
from ccapi.model.resource       import Resource
from ccapi.model.util           import get_temporary_id
from bpyutils.util.string          import ellipsis
from ccapi.model.util           import slugify_name

class ModelVersion(Resource):
    def __init__(self, name="", version=None, model = None, *args, **kwargs):
        Resource.__init__(self, name = name, *args, **kwargs)
        
        self._version = version or get_temporary_id()
        self._model   = model

    def __repr__(self):
        klass   = self.__class__.__name__
        
        id_     = self.id
        version = self.version

        memory  = "0x0%x" % id(self)
        name    = " name='%s'" % (ellipsis(self.name, threshold = 30)) \
            if self.name else ""

        repr_   = "<%s %s version %s at %s%s>" % (klass, id_, version, memory, name)

        return repr_
        
    @property
    def version(self):
        return getattr(self, "_version", get_temporary_id())

    @version.setter
    def version(self, value):
        if self.version == value:
            pass
        elif not isinstance(value, int):
            raise TypeError("Version number must be an integer.")
        else:
            self._version = value

    @property
    def model(self):
        return getattr(self, "_model", None)

    @model.setter
    def model(self, value):
        if self.model == value:
            pass
        else:
            self._model = value

    def save(self):
        self.model.save()

    def draw(self):
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    @property
    def url(self):
        url = "/".join([
            self.model.url,
            slugify_name(self.name or "")
        ])

        return url