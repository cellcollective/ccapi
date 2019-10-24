# imports - module imports
from cc.model.resource import Resource

class User(Resource):
    def __init__(self):
        self.id         = None
        self.first_name = None
        self.last_name  = None

    @property
    def name(self):
        _name = None

        if self.first_name:
            _name = self.first_name

            if self.last_name:
                _name += " " + self.last_name

        return _name

    def __repr__(self):
        repr_ = "<User id=%s name='%s'>" % (self.id, self.name)
        return repr_