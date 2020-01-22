# imports - module imports
from ccapi.model.resource       import Resource
from ccapi.core.mixins          import JupyterHTMLViewMixin
from ccapi._compat              import iteritems
from ccapi.model.model.boolean  import InternalComponent

class Reaction(InternalComponent, JupyterHTMLViewMixin):
    _REPR_ATTRIBUTES = [
        dict({
             "name": "subsystem",
            "title": "Subsystem"
        }),
        dict({
             "name": "lower_bound",
            "title": "Lower Bound"
        }),
        dict({
             "name": "upper_bound",
            "title": "Upper Bound"
        })
    ]

    def __init__(self, name = "", subsystem = None, lower_bound = None,
        upper_bound = None, *args, **kwargs):
        self.super                  = super(Reaction, self)
        self.super.__init__(name = name, *args, **kwargs)
        
        self.subsystem              = subsystem
        self.lower_bound            = lower_bound
        self.upper_bound            = upper_bound

        self._coefficient_map       = { }

    def add_metabolites(self, metabolites):
        for metabolite, coefficient in iteritems(metabolites):
            self._coefficient_map[metabolite] = coefficient

    def to_json(self):
        data                        = self.super.to_json()

        data["subsystem"]           = self.subsystem
        
        data["lower_bound"]         = float(self.lower_bound)
        data["upper_bound"]         = float(self.upper_bound)

        if self._coefficient_map:
            data["metabolites"]     = { }

            for metabolite, coefficient in iteritems(self._coefficient_map):
                data["metabolites"][metabolite.id] = coefficient

        return data