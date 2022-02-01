# imports - standard imports
from bpyutils.util.string     import ellipsis
from ccapi._compat         import iteritems
from bpyutils.util.datetime   import now
from ccapi.model.util      import get_temporary_id

class Resource:
    _REPR_ATTRIBUTES = [
        dict({
             "name": "id",
            "title": "ID"
        }),
        dict({
             "name": "name",
            "title": "Name"
        })
    ]
    
    """
    Defines a common behaviour of all objects within the CC API
    """
    def __init__(self, id = None, name = "", client = None):
        """
        A resource object with an identifier and/or name.

        :param id: An integer or None. An identifier associated with the resource.
        :param name: A string or None. A name associated with the resource.
        :param client: A :class:`ccapi.Client` object. A reference to the client
            object used to fetch this resource.
        """
        self.created    = now()
        self.updated    = now()

        self._id        = id or get_temporary_id()
        self._name      = name

        self._client    = client

    @property
    def id(self):
        _id = getattr(self, "_id", None) or get_temporary_id()
        return _id

    @id.setter
    def id(self, value):
        if self.id == value:
            pass
        elif not isinstance(value, int):
            raise TypeError("ID must be an integer.")
        else:
            self._id = value or get_temporary_id()

    @property
    def name(self):
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value):
        if self.name == value:
            pass
        elif not isinstance(value, str):
            raise TypeError("Name must be a string.")
        else:
            self._name = value

    @property
    def client(self):
        client = getattr(self, "_client", None)
        
        if not client:
            raise ValueError("%s has no client instance." % 
                self.__class__.__name__)
        
        return client

    @client.setter
    def client(self, value):
        if self.client == value:
            pass
        else:
            self._client = value

    def __repr__(self):
        klass   = self.__class__.__name__
        id_     = self.id
        memory  = "0x0%x" % id(self)
        name    = " name='%s'" % (ellipsis(self.name, threshold = 30)) \
            if self.name else ""

        repr_   = "<%s %s at %s%s>" % (klass, id_, memory, name)

        return repr_

    def __eq__(self, other):
        equals = False

        if other and isinstance(other, Resource):
            if self.id and other.id:
                equals = self.id == other.id

        return equals

    def _prepare_save_data(self):
        """
        Prepares the data to be dispatched to save this resource object.
        """
        name   = self.__class__.__name__
        fields = self.FIELDS
        
        data   = dict()

        for attr, info in iteritems(fields):
            value = getattr(self, attr, None)
            if value == None and not fields["none"]:
                raise ValueError("%s cannot be None for resource %s." % 
                    (attr, name)
                )
            elif not isinstance(value, info["type"]):
                raise ValueError("%s cannot be of type %s for resource %s." %
                    (attr, type(value), name)
                )
            else:
                target       = info["target"]
                data[target] = value

        return data

    def _before_crud(self):
        """
        Hook to perform before Create, Read, Update and Delete Operations.
        """
        self.client.raise_for_authentication()
    
    def _before_save(self):
        self._before_crud()

    def save(self):
        self._before_crud()
        raise NotImplementedError

    def _before_delete(self):
        self._before_crud()

    def delete(self):
        self._before_crud()
        raise NotImplementedError

    def __hash__(self):
        return id(self)

    def to_json(self):
        data            = dict()

        data["id"]      = str(self.id)
        data["name"]    = self.name

        return data

    @property
    def dirty(self):
        return self.id < 0