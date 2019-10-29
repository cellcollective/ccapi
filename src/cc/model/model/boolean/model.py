# imports - module imports
from cc.model.resource  import Resource
from cc.util.types      import squash
from cc.table           import Table

class BooleanModel(Resource):
    def __init__(self, *args, **kwargs):
        self.name    = kwargs.get("name")
        self.species = kwargs.get("species", [ ])

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
        table    = Table(header = ["INTERNAL (+, -)", "EXTERNAL"])

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