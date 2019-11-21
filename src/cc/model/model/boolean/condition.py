# imports - module imports
from cc.core.querylist  import QueryList
from cc.model.resource  import Resource
from cc.core.mixins     import JupyterHTMLViewMixin
from cc.template        import render_template

class Condition(Resource, JupyterHTMLViewMixin):
    def __init__(self, id = None, type = None, state = None,
        operator = None, autosave = False, client = None):
        Resource.__init__(self, id = id, autosave = autosave, client = client)

        self.type       = type
        self.state      = state
        self.operator   = operator

        self.sub_condition_operator = kwargs.get("sub_condition_operator")
        self.sub_conditions         = kwargs.get("sub_conditions", QueryList())
        self.species                = kwargs.get("species", QueryList())

    def __repr__(self):
        repr_ = "<Condition id=%s>" % self.id
        return repr_

    def _repr_html_(self):
        repr_ = render_template("condition.html")
        return repr_

class ConditionType:
    IF_WHEN = 1

class ConditionState:
    ON  = 1
    OFF = 2