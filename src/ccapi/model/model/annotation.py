# imports - module imports
from ccapi.model.resource  import Resource
from ccapi.core.mixins     import JupyterHTMLViewMixin

class Annotation(Resource, JupyterHTMLViewMixin):
    def __init__(self, name="", id=None, client=None):
        Resource.__init__(self, id = id, name = name, client = client)