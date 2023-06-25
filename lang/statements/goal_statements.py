from enum import Enum
from typing import List
from app.models.priority import TagType
from pydantic import BaseModel
import yaml

# class GoalTag(str, Enum):
#     SURVIVAL = "survival"
#     GOAL = "goal"
#     SWARM = "swarm"

class GoalSuccess(BaseModel):
    tag: str

class GoalFailure(BaseModel):
    tag: str

class GoalStatement(BaseModel):
    name: str
    type: TagType
    success: List[GoalSuccess] = []
    failure: List[GoalFailure] = []
    
class GoalsConfig(BaseModel):
    indexes: List[str]
    tags: List[str]
    goals: List[GoalStatement]
    actions: List[str]
    tag_links: List[str]

class Action(BaseModel):
    name: str

def parse_goals_config(file_path: str) -> GoalsConfig:
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        config = GoalsConfig(**data)
        return config