# imports - module imports
from cc.core.querylist  import QueryList
from cc.model.resource  import Resource
from cc.core.mixins     import JupyterHTMLViewMixin
from cc.template        import render_template
from cc.util.string     import capitalize

class Species(Resource, JupyterHTMLViewMixin):
    """
    A species is a class for holding information regarding a chemical species.

    :param id: An integer or None. An identifier associated with the resource.
    :param name: A string or None. A name associated with the resource.
    :param client: A :class:`cc.Client` object. A reference to the client
        object used to fetch this resource.
    """

    def __init__(self, id=None, name="", autosave=False, client=None):
        Resource.__init__(self, id = id, name = name, autosave = autosave,
            client = client)

    def _repr_html_(self):
        repr_ = render_template("species.html", dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address":   "0x0%x" % id(self)
        }))
        return repr_