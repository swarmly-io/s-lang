
from typing import List
from app.models.priority import Tag
from lang.statements.goal_statements import Action, GoalStatement, Group
from pydantic import BaseModel

class AgentDto(BaseModel):
    name: str
    goals: List[GoalStatement]
    actions: List[Action]
    tag_list: List[Tag]
    groups: List[Group]