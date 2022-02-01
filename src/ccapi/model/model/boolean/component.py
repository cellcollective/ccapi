# imports - standard imports
from os.path import join

# imports - module imports
from ccapi.core.querylist                  import QueryList
from ccapi.model.resource                  import Resource
from ccapi.model.model.species             import Species
from ccapi.model.model.boolean.regulator   import Regulator
from ccapi.core.mixins                     import JupyterHTMLViewMixin
from ccapi.template                        import render_template
from bpyutils.util.string                     import capitalize

class Component(Species, JupyterHTMLViewMixin):
    """
    A species is a class for holding information regarding a chemical species.

    :param id: An integer or None. An identifier associated with the resource.
    :param name: A string or None. A name associated with the resource.
    :param client: A :class:`ccapi.Client` object. A reference to the client
        object used to fetch this resource.
    """

    def __init__(self, *args, **kwargs):
        Species.__init__(self, *args, **kwargs)

        self._model = None

class InternalComponent(Component):
    _REPR_ATTRIBUTES = [
        dict({
             "name": "number_of_positive_regulators",
            "title": "Number of Positive Regulators",
              "key": lambda x: len(x.positive_regulators)
        }),
        dict({
             "name": "number_of_negative_regulators",
            "title": "Number of Negative Regulators",
              "key": lambda x: len(x.negative_regulators)
        })
    ]

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
        return self.regulators.query(lambda r: r.type == "positive")

    @property
    def negative_regulators(self):
        return self.regulators.query(lambda r: r.type == "negative")

    def _repr_html_(self):
        repr_ = render_template(join("boolean", "component", "internal.html"), 
            context = dict({
                "id":   self.id,
                "name": self.name,
                "memory_address": "0x0%x" % id(self),
                "number_of_positive_regulators": len(self.positive_regulators),
                "number_of_negative_regulators": len(self.negative_regulators)
            })
        )
        return repr_

class ExternalComponent(Component):
    pass