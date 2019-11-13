# imports - standard imports
from cc.util.string     import ellipsis
from cc._compat         import iteritems
from cc.util.datetime   import now
from cc.model.util      import get_temporary_id

class Resource:
    """
    Defines common behaviour of all objects in the CC API
    """

    def __init__(self, id=None, name="", autosave=False, client=None):
        """
        A resource object with an identifier and/or name.

        :param id: An integer or None. An identifier associated with the resource.
        :param name: A string or None. A name associated with the resource.
        :param client: A :class:`cc.Client` object. A reference to the client
            object used to fetch this resource.
        """
        
        self._id      = id
        self._name    = name
        self.autosave = autosave 
        self._client  = client

        self.created  = now()
        self.updated  = now()

    @property
    def id(self):
        _id = getattr(self, "_id", get_temporary_id())
        return _id

    @id.setter
    def id(self, value):
        if self.id == value:
            pass
        elif not isinstance(value, int):
            raise TypeError("ID must be an integer.")
        else:
            self._id = value

    @property
    def name(self):
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value):
        if self.name == value:
            pass
        elif not isinstance(value, str):
            raise TypeError("ID must be a string.")
        else:
            self._name = value

    @property
    def client(self):
        client = getattr(self, "_client", None)
        if not client:
            raise ValueError("%s has no client instance." % 
                self.__class__.__name__
            )
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
        name    = " name='%s'" % (ellipsis(self.name, threshold = 30)) \
            if self.name else ""

        repr_   = "<%s %s%s>" % (klass, id_, name)

        return repr_

    def __eq__(self, other):
        equals = False

        if self.id and other.id:
            equals = self.id == other.id
            
        return equals

    def _prepare_save_data(self, resource):
        """
        Prepares the data to be dispatched to save this resource object.
        """
        
        name   = resource.__class__.__name__
        fields = resource.FIELDS
        
        data       = dict()

        for attr, info in iteritems(fields):
            value = getattr(resource, attr, None)
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

    def _before_save(self):
        self.client.raise_for_authentication()

    def save(self):
        self._before_save()
        raise NotImplementedError

    def _before_delete(self):
        self.client.raise_for_authentication()

    def delete(self):
        self._before_delete()
        raise NotImplementedError