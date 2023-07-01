from pydantic import BaseModel
from typing import Dict, List, Optional
from enum import Enum

class TagType(str, Enum):
    THREAT = "threat"
    SURVIVAL = "survival"
    GOAL = "goal"
    VALUE = "value"

class Tag(BaseModel):
    name: str
    group: str
    type: Optional[TagType]

class Priority(BaseModel):
    name: str
    tags: List[Tag]
        
class TagToPriority(Dict[str, List[str]]):
    pass
