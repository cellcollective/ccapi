# imports - standard imports
from os.path import join, abspath
import re

# imports - module imports
from ccapi.core.config              import Configuration
from ccapi.core.querylist           import QueryList
from ccapi.core.mixins              import JupyterHTMLViewMixin
from ccapi.model.model.version      import ModelVersion
from ccapi.model.model.education    import Module
from bpyutils.util.system              import read
from bpyutils.table                    import Table
from ccapi.template                 import render_template
from ccapi.constant                 import BOOLEAN_MODEL_EXPORT_TYPE
from bpyutils.util.system              import makepath
from bpyutils.util.imports             import import_handler
from bpyutils.util.request             import download_file

# imports - boolean-model imports
from ccapi.model.resource                import Resource
from ccapi.model.util                    import slugify_name
from ccapi.model.model.boolean.component import (
    Component,
    InternalComponent, ExternalComponent
)
from ccapi.model.model.boolean.regulator    import (
    Regulator, PositiveRegulator, NegativeRegulator
)
from ccapi.model.model.boolean.condition    import (
    Condition,
    State    as ConditionState,
    Type     as ConditionType,
    Relation as ConditionRelation
)

_ACCEPTED_COMPONENT_CLASSES = tuple([InternalComponent, ExternalComponent])

config = Configuration()

class BooleanModel(ModelVersion, Module, JupyterHTMLViewMixin):
    """
    A Boolean Model.

    Usage::

        >>> from ccapi.model import Model, BooleanModel, InternalComponent
        >>> model    = Model('Cortical Area Development')
        >>> bool_    = BooleanModel()

        >>> Coup_fti = InternalComponent('Coup_fti')
        >>> Sp8      = InternalComponent('Sp8')
        >>> Pax6     = InternalComponent('Pax6')
        >>> Fgf8     = InternalComponent('Fgf8')
        >>> Emx2     = InternalComponent('Emx2')
        >>> bool_.add_components(Coup_fti, Sp8, Pax6, Fgf8, Emx2)
        
        >>> model.add_version(bool_)
        >>> model.save()
    """
    def __init__(self, *args, **kwargs):
        ModelVersion.__init__(self, *args, **kwargs)

        self._components = QueryList()

    @property
    def components(self):
        components = getattr(self, "_components", QueryList())
        return components

    @components.setter
    def components(self, value):
        if self.components == value:
            pass
        elif not isinstance(value, (list, tuple, QueryList)):
            raise TypeError("ID must be an integer.")
        else:
            self._components = value
        
        if not isinstance(value, QueryList):
            raise TypeError("Components must be of type (list, tuple, QueryList).")
        else:
            for component in value:
                if not isinstance(component, Component):
                    raise TypeError("Element must be of type Component, \
                        InternalComponent or ExternalComponent.")

            self._components = value

    @property
    def internal_components(self):
        return self.components.query(lambda c: isinstance(c, InternalComponent))

    @property
    def external_components(self):
        return self.components.query(lambda c: isinstance(c, ExternalComponent))

    def add_component(self, component):
        if not isinstance(component, _ACCEPTED_COMPONENT_CLASSES):
            raise TypeError("Component must be of type %s, found %s." % 
                (_ACCEPTED_COMPONENT_CLASSES, type(component))
            )
        else:
            if component in self.components:
                raise ValueError("Component already exists.")
            else:
                self.components.append(component)

    def add_components(self, *components):
        for component in components:
            if not isinstance(component, _ACCEPTED_COMPONENT_CLASSES):
                raise TypeError("Component must be of type %s, found %s." % 
                    (_ACCEPTED_COMPONENT_CLASSES, type(component))
                )

        for component in components:
            self.add_component(component)

    def _repr_html_(self):
        repr_ = render_template(join("boolean", "model.html"), context = dict({
            "id":                   self.id,
            "version":              self.version,
            "name":                 self.name,
            "memory_address":       "0x0%x" % id(self),
            "number_of_components": len(self.components),
            "components":           ", ".join([s.name for s in self.components])
        }))
        return repr_

    def draw(self, type_ = "networkx", **kwargs):
        if type_ == "networkx":
            error_string    = "Unable to draw using networkx. Please install networkx \
                https://networkx.github.io/documentation/stable/install.html"
            nx              = import_handler("networkx",
                err_str = error_string
            )
            graphviz_layout = import_handler("networkx.drawing.nx_agraph.graphviz_layout",
                err_str = error_string
            )

            # https://github.com/miguelgrinberg/Flask-SocketIO/issues/65#issuecomment-60697013
            patch  = import_handler("bpyutils.util.gevent.patch")
            patch()

            graph  = nx.DiGraph()
            graph.add_nodes_from([c.name for c in self.components])

            layout = graphviz_layout(graph)

            nx.draw_networkx_nodes(graph, layout,
                nodelist    = [c.name for c in self.internal_components],
                node_color  = 'b',
                alpha       = 0.8
            )
            nx.draw_networkx_nodes(graph, layout,
                nodelist    = [c.name for c in self.external_components],
                node_color  = 'r',
                alpha       = 0.8
            )

            def get_edges(type_):
                edges      = [ ]

                for component in self.internal_components:
                    for regulator in component.regulators:
                        if regulator.type == type_:
                            edges.append([
                                component.name,
                                regulator.component.name
                            ])
                
                return edges

            edges = get_edges("positive")
            nx.draw_networkx_edges(graph, layout,
                edgelist    = edges,
                alpha       = 0.5,
                edge_color  = 'g'
            )

            edges = get_edges("negative")
            nx.draw_networkx_edges(graph, layout,
                edgelist    = edges,
                alpha       = 0.5,
                edge_color  = 'r'
            )

            labels = dict((c.name, c.name) for c in self.components)
            nx.draw_networkx_labels(graph, layout, labels)
        # elif type_ == "ccnetviz":
        #     HTML     = import_handler("IPython.core.display.HTML")
        # elif type_ == "d3":
        #     HTML     = import_handler("IPython.core.display.HTML")
        #     display  = import_handler("IPython.display.display")
        #     template = render_template("draw/d3.html")

        #     display(HTML(template))
        else:
            raise TypeError("No drawing type %s found." % type_)

    def summary(self):
        table    = Table(header = ["Internal Components (+, -)", "External Components"])

        internal = self.internal_components
        external = self.external_components

        maximum  = max(len(internal), len(external))

        for _ in range(maximum):
            row = [ ]

            if len(internal):
                component   = internal.pop(0)
                value       = "%s (%s,%s)" % (
                    component.name,
                    len(component.positive_regulators),
                    len(component.negative_regulators)
                )
                row.append(value)

            if len(external):
                component = external.pop(0)
                row.append(component.name)

            table.insert(row)

        string = table.render()

        print(string)

    def write(self, path = None, type = "sbml", **kwargs):
        self.save()

        type_           = BOOLEAN_MODEL_EXPORT_TYPE[type]["value_api"]
        params          = { "version": self.version, "type": type_ }

        response        = self.client.request("GET", "_api/model/export/%s" % self.id,
            params = params)

        nchunk      = kwargs.get("nchunk", config.max_chunk_download_bytes)

        path        = download_file(response, path, chunk_size = nchunk)

        return path