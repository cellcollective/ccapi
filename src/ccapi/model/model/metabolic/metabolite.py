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
             "name": "formula",
            "title": "Formula"
        }),
        dict({
             "name": "charge",
            "title": "Charge"
        })
    ]

    def __init__(self, name = "", formula = None,
        compartment = None, charge = None, *args, **kwargs):
        self.super  = super(Metabolite, self)
        self.super.__init__(name = name, *args, **kwargs)

        self.formula        = formula
        self.compartment    = compartment
        self.charge         = charge

    def to_json(self):
        data                    = self.super.to_json()
        
        data["compartment"]     = self.compartment

        data["formula"]         = self.formula
        data["charge"]          = self.charge

        return data