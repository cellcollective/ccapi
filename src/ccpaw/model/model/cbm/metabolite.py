# imports - module imports
from ccpaw.model.model.species import Species
from ccpaw.core.mixins         import JupyterHTMLViewMixin

class Metabolite(Species, JupyterHTMLViewMixin):
    pass