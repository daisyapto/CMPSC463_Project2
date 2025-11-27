class Graph:
    def __init__(self):
        self.graph = {}
        self.snapped_centers = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def get_neighbors(self, node):
        return self.graph.get(node, {}).items()
