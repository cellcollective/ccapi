# imports - module imports
from ccapi.core.querylist  import QueryList
from ccapi.model.resource  import Resource
from ccapi.core.mixins     import JupyterHTMLViewMixin
from ccapi.template        import render_template
from bpyutils.util.string     import capitalize

class Species(Resource, JupyterHTMLViewMixin):
    """
    A species is a class for holding information regarding a chemical species.

    :param id: An integer or None. An identifier associated with the resource.
    :param name: A string or None. A name associated with the resource.
    :param client: A :class:`ccapi.Client` object. A reference to the client
        object used to fetch this resource.
    """
    def __init__(self, name="", id=None, client=None):
        Resource.__init__(self, id = id, name = name, client = client)

    def _repr_html_(self):
        repr_ = render_template("species.html", dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address":   "0x0%x" % id(self)
        }))
        return repr_