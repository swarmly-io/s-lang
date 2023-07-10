import json
from typing import List

from pydantic import BaseModel
from app.agent_state import AgentMCState
from app.endpoints import KNOWLEDGE_URL, PROCESSES_URL, json_headers
from app.models.knowledge import AgentDto
from app.models.priority import Priority, Tag, TagToPriority
from fastapi import Depends, FastAPI
from lang.statements.goal_statements import Action, parse_goals_config
import requests

app = FastAPI()

def number_objects(objects):
    group_counter = {}
    for obj in objects:
        group = obj.group
        if group not in group_counter:
            group_counter[group] = 0
        obj.value = group_counter[group]
        group_counter[group] += 1
    return objects

@app.get("/config/{name}")
def configure_agent(name: str):
    print(f"making {name}")
    config = parse_goals_config(f"./data/{name}.yaml")
    
    # tags go to prioritisation service - create Goal to tag objects
    tags_to_priority = TagToPriority(**{})
    tags = []
    config.tags = number_objects(config.tags)
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
    agent_response = requests.post(KNOWLEDGE_URL + "/create_agent", data=agent.json(), headers=json_headers)
    call_responses.append((agent_response.status_code, agent_response.json()))
    #requests.post(PRIORITIES_URL + "add_tag_to_priority", tags_to_priority)
    
    # tag_links go to knowledge -> parsed to connect goals to end nodes of paths
    invalid_data = []
    for tl in config.tag_links:
        tag, action, index, node = (tl + ",,,").split(",")[0:4]
        action = action.replace(" ", "")
        index = index.replace(" ", "")
        node = node.replace(" ", "")
        if tag not in list(map(lambda x: x.name, tags)):
            print("invalid tag", tag)
            invalid_data.append(tag)
        if action not in list(map(lambda x: x.name, actions)):
            print("invalid action", action)
            invalid_data.append(action)
        if index not in config.indexes:
            print("invalid index", index)
            invalid_data.append(index)
        
    if invalid_data:
        raise Exception("Invalid data")
        
    links_response = requests.post(KNOWLEDGE_URL + f"/{name}/tag_links", data=json.dumps(config.tag_links), headers=json_headers)
    call_responses.append((links_response.status_code, links_response.json()))
    # todo post agent_config.py to knowledge
    
    try:
        processes_response = requests.get(PROCESSES_URL + f"/start/{name}")
        call_responses.append((processes_response.status_code, {}))
    except:
        processes_response = requests.get(PROCESSES_URL + f"/stop/{name}")
        call_responses.append((processes_response.status_code, {}))

    return call_responses


class SimulationEvent(BaseModel):
    agent_name: str
    expected_tags: List[str]
    
class McSimulationEvent(SimulationEvent):
    state: AgentMCState

class History:
    def __init__(self):
        self.state_updates: List[McSimulationEvent] = []
        self.current_state: McSimulationEvent = {}
        
    def add(self, state):
        self.current_state = state
        self.state_updates.append(state)
        
    def get_history(self):
        return self

history = History()

@app.post("/simulate/state")
def simulate_state(state: McSimulationEvent, history: History = Depends(history.get_history)):
    history.add(state)
    
    # post to processes
    response = requests.post(PROCESSES_URL, data=state.state.json(), headers=json_headers)
    if response.status_code == 200:
        print("Added state successfully")
    
    # post to knowledge
    response = requests.post(KNOWLEDGE_URL + f"/update_state/{state.agent_name}", data=state.state.json(), headers=json_headers)
    if response.status_code == 200:
        print("Added state successfully to knowledge")
    
    # todo query processes for active tags, assert active tags with expected

@app.get("/state/{name}")
def state(name: str, history: History = Depends(history.get_history)):
    if not history.current_state:
        raise Exception("Current state doesn't exist")
    
    print("fetched state", name)
    return history.current_state.state

@app.get("/health")
def health():
    return { 'health': 'OK' }