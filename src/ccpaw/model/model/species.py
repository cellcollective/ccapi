# imports - module imports
from ccpaw.core.querylist  import QueryList
from ccpaw.model.resource  import Resource
from ccpaw.core.mixins     import JupyterHTMLViewMixin
from ccpaw.template        import render_template
from ccpaw.util.string     import capitalize

class Species(Resource, JupyterHTMLViewMixin):
    """
    A species is a class for holding information regarding a chemical species.

    :param id: An integer or None. An identifier associated with the resource.
    :param name: A string or None. A name associated with the resource.
    :param client: A :class:`ccpaw.Client` object. A reference to the client
        object used to fetch this resource.
    """

    def __init__(self, id=None, name="", client=None):
        Resource.__init__(self, id = id, name = name, client = client)

    def _repr_html_(self):
        repr_ = render_template("species.html", dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address":   "0x0%x" % id(self)
        }))
        return repr_