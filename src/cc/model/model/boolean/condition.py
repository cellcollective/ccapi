# imports - module imports
from cc.core.querylist  import QueryList
from cc.model.resource  import Resource
from cc.core.mixins     import JupyterViewMixin

class Condition(Resource, JupyterViewMixin):
    def __init__(self, *args, **kwargs):
        self.id                     = kwargs.get("id")
        self.state                  = kwargs.get("state")
        self.type                   = kwargs.get("type")
        self.operator               = kwargs.get("operator")
        self.sub_condition_operator = kwargs.get("sub_condition_operator")
        self.sub_conditions         = kwargs.get("sub_conditions", QueryList())
        self.species                = kwargs.get("species", QueryList())

    def __repr__(self):
        repr_ = "<Condition id=%s>" % self.id
        return repr_

    def _repr_html(self):
        repr_ = render_template