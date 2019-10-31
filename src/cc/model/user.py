# imports - module imports
from cc.model.resource import Resource, ResourceAttribute as RAttr

class User(Resource):
    """
    A User resource object.
    """

    def __init__(self,
        id         = None,
        first_name = None,
        last_name  = None,
    ):
        self._first_name = RAttr("firstName", first_name)
        self._last_name  = RAttr("lastName",  last_name)

        Resource.__init__(self, id, self.name)

    @property
    def first_name(self):
        first_name = getattr(self, "_first_name", None)
        return first_name
    
    @first_name.setter
    def first_name(self, value):
        if self.first_name == value:
            pass
        elif not isinstance(value, RAttr):
            self._first_name = RAttr("firstName", value)

    @property
    def last_name(self):
        last_name = getattr(self, "_last_name", None)
        return last_name
    
    @last_name.setter
    def last_name(self, value):
        if self.last_name == value:
            pass
        elif not isinstance(value, RAttr):
            self._last_name = RAttr("lastName", value)

    @property
    def name(self):
        _name = None

        if self.first_name:
            _name = self.first_name

            if self.last_name:
                _name += " " + self.last_name

        return _name

    def save(self):
        pass