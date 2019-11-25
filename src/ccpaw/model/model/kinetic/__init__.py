# imports - module imports
from ccpaw.model.model.version import ModelVersion
from ccpaw.core.querylist      import QueryList
from ccpaw.core.mixins         import JupyterHTMLViewMixin

# imports - kinetic-based imports

class KineticModel(ModelVersion, JupyterHTMLViewMixin):
    pass