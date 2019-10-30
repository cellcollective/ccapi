# imports - module imports
from cc.model.resource import Resource

class User(Resource):
    """
    A User resource object.
    """

    def __init__(self,
        id          = None,
        first_name  = None,
        last_name   = None,
    ):
        self.super.__init__(self, id)
        self.first_name = first_name
        self.last_name  = last_name

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