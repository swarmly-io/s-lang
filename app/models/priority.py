from pydantic import BaseModel
from typing import Dict, List
from enum import Enum

class TagType(str, Enum):
    SURVIVAL = "survival"
    GOAL = "goal"
    VALUE = "value"

class Tag(BaseModel):
    name: str
    type: TagType

class Priority(BaseModel):
    name: str
    tags: List[Tag]
        
class TagToPriority(Dict[str, List[str]]):
    pass
