# imports - module imports
from ccpaw.model.model.version import ModelVersion
from ccpaw.core.querylist      import QueryList
from ccpaw.core.mixins         import JupyterHTMLViewMixin

# imports - constraint-based model imports
from ccpaw.model.model.cbm.metabolite  import Metabolite
from ccpaw.model.model.cbm.gene        import Gene
from ccpaw.model.model.cbm.reaction    import Reaction

class ConstraintBasedModel(ModelVersion, JupyterHTMLViewMixin):
    def _repr_html_(self):
        pass