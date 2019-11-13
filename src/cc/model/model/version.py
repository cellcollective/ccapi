# imports - module imports
from cc.model.resource import Resource
from cc.model.util     import get_temporary_id

class ModelVersion(Resource):
    def __init__(self, id=None, name="", version=None
    ):
        Resource.__init__(self, id = id, name = name)

        self._version = version or get_temporary_id()
        
    @property
    def version(self):
        return getattr(self, "_version", get_temporary_id())

    @version.setter
    def version(self, value):
        if self.version == value:
            pass
        elif not isinstance(version, int):
            raise TypeError("Version number must be an integer.")
        else:
            self._version = value

    def export(self):
        raise NotImplementedError