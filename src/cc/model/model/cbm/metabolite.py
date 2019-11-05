# imports - module imports
from cc.model.model.species import Species
from cc.core.mixins         import JupyterHTMLViewMixin

class Metabolite(Species, JupyterHTMLViewMixin):
    pass