# imports - module imports
from ccapi.model.model.version import ModelVersion
from ccapi.core.querylist      import QueryList
from ccapi.core.mixins         import JupyterHTMLViewMixin

# imports - constraint-based model imports
from ccapi.model.model.cbm.metabolite  import Metabolite
from ccapi.model.model.cbm.gene        import Gene
from ccapi.model.model.cbm.reaction    import Reaction

class ConstraintBasedModel(ModelVersion, JupyterHTMLViewMixin):
    def _repr_html_(self):
        pass