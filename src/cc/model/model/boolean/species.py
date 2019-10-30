# imports - module imports
from cc.core.querylist  import QueryList
from cc.model.resource  import Resource
from cc.core.mixins     import JupyterHTMLViewMixin
from cc.template        import render_template
from cc.util.string     import capitalize

class Species(Resource, JupyterHTMLViewMixin):
    def __init__(self, *args, **kwargs):
        self.id         = kwargs.get("id_")
        self.name       = kwargs.get("name")
        self.type       = kwargs.get("type")
        self.created    = kwargs.get("created")
        self.updated    = kwargs.get("updated")
        self.regulators = kwargs.get("regulators", QueryList())

    @property
    def positive_regulators(self):
        regulators = [regulator
            for regulator in self.regulators
                if regulator.type == "positive"
        ]

        return regulators

    @property
    def negative_regulators(self):
        regulators = [regulator
            for regulator in self.regulators
                if regulator.type == "negative"
        ]

        return regulators

    def __repr__(self):
        repr_ = "<Species id=%s name='%s'>" % (self.id, self.name)
        return repr_

    def _repr_html_(self):
        repr_ = render_template("species.html", dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address":   "0x0%x" % id(self),
            "type":             capitalize(self.type),
            "number_of_positive_regulators": len(self.positive_regulators),
            "number_of_negative_regulators": len(self.negative_regulators) 
        }))
        return repr_