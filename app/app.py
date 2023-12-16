import json
from aiokafka import AIOKafkaProducer

from app.endpoints import ENTITIES_URL, KNOWLEDGE_URL, json_headers
from domain_models.decisions.paths import AgentDto
from fastapi import FastAPI
from lang.statements.goal_statements import Action, parse_goals_config
import requests

from domain_models.messaging.task_events import SubscriberEvent


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
async def configure_agent(name: str):    
    print(f"making {name}")
    config = parse_goals_config(f"./data/{name}.yaml")
    
    tags = []
    config.tags = number_objects(config.tags)
    tags_dict = { t.name:t for t in config.tags }
    map_tag = lambda x: list(map(lambda z: z.tag, x))
    for goal in config.goals:        
        # todo some tags may not match the goal type
        goal_tags = [tags_dict[t] for t in map_tag(goal.success) + map_tag(goal.failure)]
        tags = tags + goal_tags

    actions = list(map(lambda x: Action(name=x), config.actions))
    call_responses = []
    agent = AgentDto(name=name, goals = config.goals, tag_list = tags, actions = actions, groups = config.groups)
    requests.post(KNOWLEDGE_URL + f"/{agent.name}/init", headers=json_headers)
    

    agent_response = requests.post(KNOWLEDGE_URL + f"/{agent.name}/create_agent", data=agent.json(), headers=json_headers)
    call_responses.append((agent_response.status_code, agent_response.json()))
    
    entities_agent_response = requests.post(ENTITIES_URL + f"/agent", data=agent.json(), headers=json_headers)
    call_responses.append((entities_agent_response.status_code, entities_agent_response.json()))

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

    entities_links_response = requests.post(ENTITIES_URL + f"/agent/{name}/state", data=json.dumps({ 'tag_links': config.tag_links }), headers=json_headers)
    call_responses.append((entities_links_response.status_code, entities_links_response.json()))
    
    try:
        bootstrap_servers = "localhost:9092"
        producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        await producer.start()
        subscriber = SubscriberEvent.default(agent.name)
        await producer.send("processes", subscriber.to_json())
    finally:
        await producer.stop()
    
    return call_responses

@app.get("/health")
def health():
    return { 'health': 'OK' }