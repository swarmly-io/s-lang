from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import Field

from goals.id_model import IdModel

class NodeType(str, Enum):
    GOAL = "GOAL"
    ATTRIBUTE = "ATTRIBUTE"
    MODIFIER = "MODIFIER"
    ITEM = "ITEM"
    SKILL = "SKILL"
    TASK = "TASK"
    AGENT = "AGENT"
    RECIPE = "RECIPE"
    BELIEF = "BELIEF"
    KNOWLEDGE = "KNOWLEDGE"
    
    GOAL_CONTRIBUTION = "GOAL_CONTRIBUTION"
    CRITERIA = "CRITERIA"
    RESULT = "RESULT"
    ACTION = "ACTION"

class Node(IdModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    cost: float
    type: NodeType
    is_active: Optional[bool]

class Edge(IdModel):
    source: Node
    target: Node
    
class Graph(IdModel):
    edges: List[Edge]
    nodes: List[Node]