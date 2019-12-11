# imports - module imports
from ccapi.model.resource import Resource
from ccapi.core.mixins    import JupyterHTMLViewMixin

class Reaction(Resource, JupyterHTMLViewMixin):
    def _repr_html_(self):
        pass