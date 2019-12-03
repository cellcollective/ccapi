# imports - module imports
from ccapi.model.model.version import ModelVersion
from ccapi.core.querylist      import QueryList
from ccapi.core.mixins         import JupyterHTMLViewMixin

# imports - kinetic-based imports

class KineticModel(ModelVersion, JupyterHTMLViewMixin):
    pass