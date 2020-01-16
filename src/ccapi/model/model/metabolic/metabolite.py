# imports - module imports
from ccapi.model.model.species import Species
from ccapi.core.mixins         import JupyterHTMLViewMixin

class Metabolite(Species, JupyterHTMLViewMixin):
    _REPR_ATTRIBUTES = [
        dict({
             "name": "compartment",
            "title": "Compartment"
        }),
        dict({
             "name": "charge",
            "title": "Charge"
        })
    ]

    def __init__(self, compartment = None, charge = None, *args, **kwargs):
        Species.__init__(self, *args, **kwargs)

        self.compartment    = compartment
        self.charge         = charge