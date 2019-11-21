# imports - standard imports
from os.path import join

# imports - module imports
from cc.core.querylist                  import QueryList
from cc.model.resource                  import Resource
from cc.model.model.species             import Species
from cc.model.model.boolean.regulator   import Regulator
from cc.core.mixins                     import JupyterHTMLViewMixin
from cc.template                        import render_template
from cc.util.string                     import capitalize

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

        self._model = None

    def _repr_html_(self):
        repr_ = render_template(join("boolean", "component.html"), dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address":   "0x0%x" % id(self)
        }))
        return repr_

class InternalComponent(Component):
    def __init__(self, *args, **kwargs):
        self.super = super(InternalComponent, self)
        self.super.__init__(*args, **kwargs)

        self._regulators = QueryList()

    @property
    def regulators(self):
        regulators = getattr(self, "_regulators", QueryList())
        return regulators

    @regulators.setter
    def regulators(self, value):
        if self.regulators == value:
            pass
        elif not isinstance(value, (list, tuple, QueryList)):
            raise TypeError("ID must be an integer.")
        else:
            self._regulators = value
        
        if not isinstance(value, QueryList):
            raise TypeError("Components must be of type (list, tuple, QueryList).")
        else:
            for regulator in value:
                if not isinstance(regulator, Regulator):
                    raise TypeError("Element must be of type Regulator.")

            self._regulators = value

    def add_regulator(self, regulator):
        self.regulators.append(regulator)

    def add_regulators(self, *regulators):
        for regulator in regulators:
            self.regulators.append(regulator)

    @property
    def positive_regulators(self):
        for regulator in self.regulators:
            if regulator.type == "positive":
                yield regulator

    @property
    def negative_regulators(self):
        for regulator in self.regulators:
            if regulator.type == "negative":
                yield regulator


class ExternalComponent(Component):
    pass