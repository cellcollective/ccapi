# imports - standard imports
import os.path as osp
import re

# imports - module imports
from cc.core.querylist  import QueryList
from cc.core.mixins     import JupyterViewMixin
from cc.model.resource  import Resource
from cc.util.types      import squash
from cc.util.system     import read
from cc.table           import Table
from cc.template        import render_template

class BooleanModel(Resource, JupyterViewMixin):
    def __init__(self, *args, **kwargs):
        self.id      = kwargs.get("id")
        self.version = kwargs.get("version")
        self.name    = kwargs.get("name")
        self.species = kwargs.get("species", QueryList())
        self._client = kwargs.get("client")

    def get_species(self, *names, **params):
        def _find(filter_):
            found = squash(list(filter(filter_, self.species)))
            return found

        species = [ ]

        if names:
            found = _find(lambda x: x.name in names)
            species.append(found)

        key     = params.get("key")
        if key:
            found = _find(key)
            species.append(found)

        return squash(species)

    def save(self):
        pass

    def draw(self, *args, **kwargs):
        engine = kwargs.get("engine",  "networkx")
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

    def __repr__(self):
        repr_ = "<BooleanModel>"
        return repr_

    def _repr_html(self):
        repr_ = render_template("model")
        return repr_

    def export(self, path = None, type_ = "sbml", **kwargs):
        url         = self._client._build_url("_api", "model", "export", self.id)
        params      = { "version": self.version, "type": type_ }

        response    = self._client._request(url, params = params)

        if not path:
            header  = response.headers["content-disposition"]
            name    = re.findall("filename=(.+)", header)[0]

            path    = osp.abspath(name)

        nchunk      = kwargs.get("nchunk", 1024)

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size = nchunk):
                if chunk:
                    f.write(chunk)