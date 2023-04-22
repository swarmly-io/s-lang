from typing import Any, List, Optional
from pydantic import BaseModel

from goals.graph import Edge, Node
    
class GraphModel(BaseModel):
    node: Optional[Node]
    edges: Optional[List[Edge]]
    
    def refresh(self):
        self.node = None
        self.edges = []
        
    def save_node(self, node: Node):
        self.node = node
        return node
    
    def save_edges(self, edges: List[Edge]):
        self.edges = edges
        return edges
    
    def to_node(self):
        pass
    
    # todo get subgraph?
    
    def get_subnodes(self):
        return []
    
    def get_direct_nodes(self, nl: List[Any]):
        return [n for n in nl]
    
    def _get_child_edges(self, nl: List[Any]):
        child_nodes = self.get_direct_nodes(nl)
        edges = []
        for child in child_nodes:
            if hasattr(child, 'get_child_edges'):
                edges = edges + child.get_child_edges()
            edges.append(Edge(source=self.to_node(), target=child.to_node()))
        
        return edges