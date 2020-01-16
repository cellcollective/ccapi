# imports - module imports
from ccapi.model.resource import Resource
from ccapi.core.mixins    import JupyterHTMLViewMixin

class Reaction(Resource, JupyterHTMLViewMixin):
    def __init__(self, lower_bound = None, upper_bound = None, *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)

        self.lower_bound    = lower_bound
        self.upper_bound    = upper_bound