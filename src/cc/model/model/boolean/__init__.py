# imports - standard imports
from os.path import join, abspath
import re

# imports - module imports
from cc.core.querylist      import QueryList
from cc.core.mixins         import JupyterHTMLViewMixin
from cc.model.model.version import ModelVersion
from cc.util.system         import read
from cc.table               import Table
from cc.template            import render_template
from cc.constant            import MODEL_EXPORT_TYPE_MAP

class BooleanModel(ModelVersion, JupyterHTMLViewMixin):
    """
    A Boolean Model.

    Usage::

        >>> from cc.model import Model, BooleanModel, Component
        >>> model    = Model('Cortical Area Development')
        >>> bool     = BooleanModel()
        >>> Coup_fti = Component('Coup_fti')
        >>> Sp8      = Component('Sp8')
        >>> Pax6     = Component('Pax6')
        >>> Fgf8     = Component('Fgf8')
        >>> Emx2     = Component('Emx2')
        >>> bool.add_components(Coup_fti, Sp8, Pax6, Fgf8, Emx2)
        >>> model.add_version(bool)
        >>> model.save()
    """
    def __init__(self, id=None, name="", version=None, base_model=None):
        ModelVersion.__init__(self, id = id, name = name,
            version = version
        )

        self._base_model = base_model

        self.components  = QueryList()

    def _repr_html_(self):
        repr_ = render_template(join("boolean", "model.html"), args = dict({
            "id":                   self.id,
            "version":              self.version,
            "name":                 self.name,
            "memory_address":       "0x0%x" % id(self),
            "number_of_components": len(self.components),
            "components":           ", ".join([s.name for s in self.components])
        }))
        return repr_

    def draw(self, *args, **kwargs):
        engine = kwargs.get("engine", "networkx")
        labels = kwargs.get("labels", True)

        if engine == "networkx":
            try:
                import networkx as nx
                
                graph = nx.Graph()
                graph.add_nodes_from([s.name for s in self.species])

                for species in self.species:
                    for regulator in species.regulators:
                        graph.add_edge(regulator.of.name, regulator.species.name)

                nx.draw(graph, with_labels = labels)
            except ImportError:
                raise ImportError("Unable to draw using networkx. Please install networkx.")
        elif engine == "cytoscape":
            pass

    def summary(self):
        table    = Table(header = ["Internal Components (+, -)", "External Components"])

        internal = self.get_species(key = lambda x: x.type == "internal")
        external = self.get_species(key = lambda x: x.type == "external")

        maximum  = max(len(internal), len(external))

        for _ in range(maximum):
            row = [ ]

            if len(internal):
                species     = internal.pop(0)
                value       = "%s (%s,%s)" % (
                    species.name,
                    len(species.positive_regulators),
                    len(species.negative_regulators)
                )
                row.append(value)

            if len(external):
                species = external.pop(0)
                row.append(species.name)

            table.insert(row)

        string = table.render()

        print(string)

    def export(self, path = None, type_ = "sbml", **kwargs):
        url             = self._client._build_url("_api", "model", "export", self.id)
        type_           = MODEL_EXPORT_TYPE_MAP[type_]
        params          = { "version": self.version, "type": type_ }

        response        = self._client._request("GET", url, params = params)

        default_path    = False

        if not path:
            default_path = True

            header  = response.headers["content-disposition"]
            name    = re.findall("filename=(.+)", header)[0]

            path    = abspath(name)

        nchunk      = kwargs.get("nchunk", 1024)

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size = nchunk):
                if chunk:
                    f.write(chunk)

        if default_path:
            return path