# imports - standard imports
from cc.util.string import ellipsis

class Resource:
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
        name    = " name='%s'" % (ellipsis(self.name, threshold = 30)) \
            if self.name else ""

        repr_   = "<%s %s%s>" % (klass, id_, name)

        return repr_

    def __eq__(self, other):
        return self.id == other.id

class ResourceAttribute:
    """
    An attribute of a resource.
    """

    def __init__(self, key, value):
        self.key   = key
        self.value = value

    def __repr__(self):
        repr_ = self.value
        return repr_

    def __eq__(self, other):
        equal = False
        
        if isinstance(other, ResourceAttribute):
            equal = self.key == other.key and self.value == other.value
        else:
            equal = self.value = other
        
        return equal