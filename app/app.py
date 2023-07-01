from app.models.knowledge import AgentDto
from app.models.priority import Priority, Tag, TagToPriority
from fastapi import Depends, FastAPI
from lang.statements.goal_statements import parse_goals_config
import requests


app = FastAPI()

PRIORITIES_URL = "http://localhost:9001"
KNOWLEDGE_URL = "http://localhost:9000"

app.get("/config/{agent}")
def configure_agent(name: str):
    config = parse_goals_config(f"./data/{name}.yaml")
    
    # tags go to prioritisation service - create Goal to tag objects
    tags_to_priority = TagToPriority(**{})
    goals = []
    tags = []
    tags = { t.name:t for t in config.tags }
    for goal in config.goals:
        priority = Priority(name = goal.name)
        requests.post(PRIORITIES_URL + "/add_priority", priority.json())
        
        # todo some tags may not match the goal type
        goal_tags = [tags[t] for t in goal.success + goal.failure]
        for t in goal_tags:
            tags_to_priority[t] = (tags_to_priority.get(t) or []) + [goal.name]
            
        tags = tags + goal_tags
    
    agent = AgentDto(name=name, goals = goals, tag_list = tags, actions = config.actions, groups = config.groups)
    requests.post(KNOWLEDGE_URL + "/create_agent", agent)
    
    requests.post(PRIORITIES_URL + "add_tag_to_priority", tags_to_priority)
    
    # tag_links go to knowledge -> parsed to connect goals to end nodes of paths
    requests.post(KNOWLEDGE_URL + f"/{name}/tag_links", config.tag_links)
    
    # todo post agent_config.py to knowledge