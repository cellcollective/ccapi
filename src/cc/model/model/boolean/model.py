# imports - third-party imports
import networkx as nx

# imports - module imports
from cc.model.resource  import Resource
from cc.util.types      import squash

class BooleanModel(Resource):
    def __init__(self, *args, **kwargs):
        self.name    = kwargs.get("name")
        self.species = kwargs.get("species", [ ])

    def get_species(self, *names, **params):
        species = [ ]

        if names:
            found = squash(list(filter(lambda x: x.name in names, self.species)))
            species.append(found)

        return squash(species)

    def save(self):
        pass

    def draw(self, *args, **kwargs):
        labels = kwargs.get("labels", True)

        graph = nx.Graph()
        graph.add_nodes_from([s.name for s in self.species])

        nx.draw(graph, with_labels = labels)

    def __repr__(self):
        repr_ = "<BooleanModel>"
        return repr_