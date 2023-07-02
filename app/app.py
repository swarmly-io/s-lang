import json
from app.models.knowledge import AgentDto
from app.models.priority import Priority, Tag, TagToPriority
from fastapi import Depends, FastAPI
from lang.statements.goal_statements import Action, parse_goals_config
import requests


app = FastAPI()

PRIORITIES_URL = "http://localhost:9001"
KNOWLEDGE_URL = "http://localhost:9000"

@app.get("/config/{agent}")
def configure_agent(name: str):
    config = parse_goals_config(f"./data/{name}.yaml")
    
    # tags go to prioritisation service - create Goal to tag objects
    tags_to_priority = TagToPriority(**{})
    tags = []
    tags_dict = { t.name:t for t in config.tags }
    map_tag = lambda x: list(map(lambda z: z.tag, x))
    for goal in config.goals:
        #priority = Priority(name = goal.name, tags = )
        #requests.post(PRIORITIES_URL + "/add_priority", priority.json())
        
        # todo some tags may not match the goal type
        goal_tags = [tags_dict[t] for t in map_tag(goal.success) + map_tag(goal.failure)]
        #for t in goal_tags:
         #   tags_to_priority[t] = (tags_to_priority.get(t) or []) + [goal.name]
        
        tags = tags + goal_tags

    actions = list(map(lambda x: Action(name=x), config.actions))
    call_responses = []
    agent = AgentDto(name=name, goals = config.goals, tag_list = tags, actions = actions, groups = config.groups)
    headers = {
    'Content-Type': 'application/json'
    }
    agent_response = requests.post(KNOWLEDGE_URL + "/create_agent", data=agent.json(), headers=headers)
    call_responses.append((agent_response.status_code, agent_response.json()))
    #requests.post(PRIORITIES_URL + "add_tag_to_priority", tags_to_priority)
    
    # tag_links go to knowledge -> parsed to connect goals to end nodes of paths
    links_response = requests.post(KNOWLEDGE_URL + f"/{name}/tag_links", data=json.dumps(config.tag_links), headers=headers)
    call_responses.append((links_response.status_code, links_response.json()))
    # todo post agent_config.py to knowledge
    return call_responses