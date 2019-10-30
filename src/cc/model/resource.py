# imports - standard imports
from cc.util.string import ellipsis

class BaseResource:
    """
    Defines common behaviour of all objects in the CC API
    """

    def __init__(self, id=None, name=""):
        self._id    = id
        self.name   = name

    @property
    def id(self):
        _id = getattr(self, "_id", None)
        return _id
    
    @id.setter
    def id(self, value):
        if self.id == value:
            pass
        elif not isinstance(value, int):
            raise TypeError("ID must be an integer.")
        else:
            self._id = value

    def __repr__(self):
        klass   = self.__class__.__name__
        id_     = self.id
        memory  = id(self)
        name    = " name='%s'" % (ellipsis(self.name, threshold = 30))
            if self.name else ""
        
        repr_   = "<%s %s%s>" % (klass, id_, name)

        return repr_
        
    def __eq__(self, other):
        return self.id == other.id

class Resource(BaseResource):
    """
    An intermediate between :class:`BaseResource` and cc objects.
    """

    def __init__(self, *args, **kwargs):
        self.super = super(BaseResource, self)
        self.super.__init__(*args, **kwargs)