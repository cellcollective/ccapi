# imports - third-party imports
import networkx as nx

# imports - module imports
from cc.model.resource import Resource

class BooleanModel(Resource):
    def __init__(self):
        self.species = [ ]

    def save(self):
        pass

    def draw(self, *args, **kwargs):
        labels = kwargs.get("labels", True)

        graph = nx.Graph()
        graph.add_nodes_from([s.name for s in self.species])

        nx.draw(graph, with_labels = labels)