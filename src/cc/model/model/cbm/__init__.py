# imports - module imports
from cc.model.model.version import ModelVersion
from cc.core.querylist      import QueryList
from cc.core.mixins         import JupyterHTMLViewMixin

# imports - constraint-based model imports
from cc.model.model.cbm.metabolite  import Metabolite
from cc.model.model.cbm.gene        import Gene
from cc.model.model.cbm.reaction    import Reaction

class ConstraintBasedModel(ModelVersion, JupyterHTMLViewMixin):
    def _repr_html_(self):
        pass