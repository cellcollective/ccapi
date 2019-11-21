# imports - standard imports
import os.path as osp

# imports - module imports
from cc.core.querylist  import QueryList
from cc.model.resource  import Resource
from cc.core.mixins     import JupyterHTMLViewMixin
from cc.template        import render_template

from cc.model.model.boolean.condition.state import ConditionState
from cc.model.model.boolean.condition.type  import ConditionType

class Condition(Resource, JupyterHTMLViewMixin):
    def __init__(self, id = None, type = None, state = None,
        operator = None, autosave = False, client = None):
        Resource.__init__(self, id = id, autosave = autosave, client = client)

        self.type       = type
        self.state      = state
        self.operator   = operator

        # self.sub_condition_operator = kwargs.get("sub_condition_operator")
        # self.sub_conditions         = kwargs.get("sub_conditions", QueryList())
        # self.species                = kwargs.get("species", QueryList())

    def __repr__(self):
        repr_ = render_template(join("boolean", "condition.html"))
        return repr_