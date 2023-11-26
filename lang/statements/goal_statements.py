from enum import Enum
from typing import List
from domain_models.decisions.goals import Tag, GoalStatement, Group
from pydantic import BaseModel
import yaml
    
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