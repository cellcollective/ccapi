# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.core.querylist  import QueryList
from ccapi.model.resource  import Resource
from ccapi.core.mixins     import JupyterHTMLViewMixin
from ccapi.template        import render_template
from bpyutils.util.array      import sequencify

from ccapi.model.model.boolean.condition.state     import State
from ccapi.model.model.boolean.condition.type      import Type
from ccapi.model.model.boolean.condition.relation  import Relation

class BaseCondition(Resource, JupyterHTMLViewMixin):
    def __init__(self, type = Type.IF, state = State.ON,
        relation = Relation.INDEPENDENT, components = [ ],
        *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)

        self.type                   = type
        self.state                  = state
        self.relation               = relation
        self.components             = QueryList(sequencify(components))

class Condition(BaseCondition):
    def __init__(self, sub_condition_relation = Relation.INDEPENDENT,
        sub_conditions = [ ], *args, **kwargs):
        BaseCondition.__init__(self, *args, **kwargs)

        self.sub_condition_relation = sub_condition_relation
        self.sub_conditions         = QueryList(sequencify(sub_conditions))