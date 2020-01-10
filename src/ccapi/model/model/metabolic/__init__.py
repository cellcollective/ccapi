# imports - module imports
from ccapi.model.model.version import ModelVersion
from ccapi.core.querylist      import QueryList
from ccapi.core.mixins         import JupyterHTMLViewMixin

# imports - constraint-based model imports
from ccapi.model.model.metabolic.metabolite  import Metabolite
from ccapi.model.model.metabolic.gene        import Gene
from ccapi.model.model.metabolic.reaction    import Reaction

class ConstraintBasedModel(ModelVersion, JupyterHTMLViewMixin):
    def write(self):
        pass