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

    def __init__(self, name = "", formula = None,
        compartment = None, charge = None, *args, **kwargs):
        Species.__init__(self, name = name, *args, **kwargs)

        self.formula        = formula
        self.compartment    = compartment
        self.charge         = charge

    def to_json(self):
        data                    = dict()

        data["id"]              = self.id
        data["name"]            = self.name
        
        data["compartment"]     = self.compartment

        data["formula"]         = self.formula
        data["charge"]          = self.charge

        return data