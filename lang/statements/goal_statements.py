from enum import Enum
from typing import List
from app.models.priority import Tag, TagType
from pydantic import BaseModel
import yaml

class GoalSuccess(BaseModel):
    tag: str

class GoalFailure(BaseModel):
    tag: str

class GoalStatement(BaseModel):
    name: str
    type: TagType
    success: List[GoalSuccess] = []
    failure: List[GoalFailure] = []

class GroupType(Enum, str):
    ORDERED_RANKED = "ordered_rank"
    BINARY = "binary"
    CUSTOM_FUNCTION = "function"

class Group(BaseModel):
    name: str
    type: GroupType
    
class GoalsConfig(BaseModel):
    indexes: List[str]
    tags: List[Tag]
    goals: List[GoalStatement]
    actions: List[str]
    tag_links: List[str]
    groups: List[Group]

class Action(BaseModel):
    name: str

def parse_goals_config(file_path: str) -> GoalsConfig:
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        config = GoalsConfig(**data)
        return config