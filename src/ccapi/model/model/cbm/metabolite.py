# imports - module imports
from ccapi.model.model.species import Species
from ccapi.core.mixins         import JupyterHTMLViewMixin

class Metabolite(Species, JupyterHTMLViewMixin):
    pass