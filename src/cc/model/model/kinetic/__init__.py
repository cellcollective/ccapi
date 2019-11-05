# imports - module imports
from cc.model.model.version import ModelVersion
from cc.core.querylist      import QueryList
from cc.core.mixins         import JupyterHTMLViewMixin

# imports - kinetic-based imports

class KineticModel(ModelVersion, JupyterHTMLViewMixin):
    pass