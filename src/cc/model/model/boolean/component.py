# imports - standard imports
from os.path import join

# imports - module imports
from cc.core.querylist      import QueryList
from cc.model.resource      import Resource
from cc.model.model         import Species
from cc.core.mixins         import JupyterHTMLViewMixin
from cc.template            import render_template
from cc.util.string         import capitalize

class Component(Species, JupyterHTMLViewMixin):
    """
    A species is a class for holding information regarding a chemical species.

    :param id: An integer or None. An identifier associated with the resource.
    :param name: A string or None. A name associated with the resource.
    :param client: A :class:`cc.Client` object. A reference to the client
        object used to fetch this resource.
    """

    def __init__(self, name="", id=None, autosave=False, client=None):
        Species.__init__(self, id = id, name = name, autosave = autosave,
            client = client)

    def _repr_html_(self):
        repr_ = render_template(join("boolean", "component.html"), dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address": "0x0%x" % id(self)
        }))
        return repr_

class InternalComponent(Component):
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

class ExternalComponent(Component):
    pass