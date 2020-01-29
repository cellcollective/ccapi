# imports - module imports
from ccapi.model.resource  import Resource
from ccapi.core.mixins     import JupyterHTMLViewMixin

class Compartment(Resource, JupyterHTMLViewMixin):
    def __init__(self, name="", id=None, client=None, compartment_id=None):
        Resource.__init__(self, id = id, name = name, client = client)

        self.compartment_id = compartment_id

    def to_json(self):
        super_ = super(Compartment, self)
        data   = super_.to_json()

        if self.compartment_id:
            data["compartmentId"] = self.compartment_id

        return data