# imports - module imports
from ccapi.model.resource       import Resource
from ccapi.core.mixins          import JupyterHTMLViewMixin
from ccapi._compat              import iterkeys, iteritems
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
        super_                  = super(Reaction, self)
        super_.__init__(name = name, *args, **kwargs)
        
        self.subsystem              = subsystem
        self.lower_bound            = lower_bound
        self.upper_bound            = upper_bound

        self._coefficient_map       = { }

    @property
    def metabolites(self):
        metabolites = list(iterkeys(self._coefficient_map))
        return metabolites

    def add_metabolites(self, metabolites):
        for metabolite, coefficient in iteritems(metabolites):
            self._coefficient_map[metabolite] = coefficient

    def to_json(self):
        super_                      = super(Reaction, self)
        data                        = super_.to_json()

        data["subsystem"]           = self.subsystem
        
        data["lowerBound"]          = float(self.lower_bound)
        data["upperBound"]          = float(self.upper_bound)

        if self._coefficient_map:
            data["metabolites"]     = { }

            for metabolite, coefficient in iteritems(self._coefficient_map):
                data["metabolites"][metabolite.id] = coefficient

        return data