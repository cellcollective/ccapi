# imports - module imports
from cc.model.resource      import Resource
from cc.model.util          import get_temporary_id

class ModelVersion(Resource):
    def __init__(self, name="", version=None, model = None, *args, **kwargs):
        Resource.__init__(self, name = name, *args, **kwargs)
        
        self._version = version or get_temporary_id()
        self._model   = model
        
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
            self._model = model

    def save(self):
        if self.model:
            self.model.save()

    def draw(self):
        raise NotImplementedError

    def export(self):
        raise NotImplementedError
