


import yaml
from lang.statements.belief_statements import BeliefStatements
from lang.util import to_network_x


class TestBeliefLang:
    
    def setup(self):
        state = {
            'health': type('Attribute', (), { 'name': 'health' }),
            'health_level': 17,
            'max_health_level': 17,
            'health_decay_rate': 0.1,
            'animal': { 'type': 'cow', 'meat': {'state': 'raw'} },
            'furnace': [(1,1,1)],
            'needed_food_level': 10,
            'food_level': 4,
            'inventory': [{ 'name': 'iron_sword' }],
            'eat': 'eat',
            'hunting': 'hunting',
            'select_weapon': 'select_weapon',
            'cook': 'cook',
            'keep_health_level_high': 'keep_health_level_high'
        }
        
        with open("./test/config/base_belief.yaml", 'r') as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            self.beliefs = list(map(lambda x: BeliefStatements(**x, state=state), data))
            for s in self.beliefs:
                s.set_state()
    
    def test_correct_future_state_generated_for_file(self):
        results = []
        for b in self.beliefs:
            result = b.evaluate()
            results.append(result)
        
        expected_result = [[{"meat": {"state": "raw"}}, "cook", {"meat": {"state": "cooked"}}, {"food_level": 6}, "eat", "select_weapon"]]
        
        assert results == expected_result
        
    def test_correct_graph_is_generated_for_file(self):
        graphs = []
        for b in self.beliefs:
            graph = b.graph()
            graphs.append(graph)
            
        expected_nodes = ["cat", "animal.type", "meat", "needed_food_level", "food_level", "cook", "craft_furnace", "furnace", "cooked", "meat.state", "raw", "meat.state", "eat", "food_level", "sword", "axe", "pickaxe", "shovel", "hoe", "select_weapon", "inventory"]
        expected_edges = [("animal.type", "cat"), ("hunting", "animal.type"), ("hunting", "meat"), ("food_level", "needed_food_level"), ("hunting", "food_level"), ("furnace", "cook"), ("furnace", "craft_furnace"), ("hunting", "furnace"), ("meat.state", "cooked"), ("hunting", "meat.state"), ("meat.state", "raw"), ("hunting", "meat.state"), ("food_level", "eat"), ("hunting", "food_level"), ("inventory", "sword"), ("inventory", "axe"), ("inventory", "pickaxe"), ("inventory", "shovel"), ("inventory", "hoe"), ("inventory", "select_weapon"), ("hunting", "inventory")]
        assert graphs[0][0] == expected_nodes
        assert graphs[0][1] == expected_edges
        print(graph[0])
        assert 1 == 2
        
    def test_draw_graph(self):
        graphs = []
        for b in self.beliefs:
            graph = b.graph()
            graphs.append(graph)
            
        expected_nodes = ["cat", "animal.type", "meat", "needed_food_level", "food_level", "cook", "craft_furnace", "furnace", "cooked", "meat.state", "raw", "meat.state", "eat", "food_level", "sword", "axe", "pickaxe", "shovel", "hoe", "select_weapon", "inventory"]
        expected_edges = [("animal.type", "cat"), ("hunting", "animal.type"), ("hunting", "meat"), ("food_level", "needed_food_level"), ("hunting", "food_level"), ("furnace", "cook"), ("furnace", "craft_furnace"), ("hunting", "furnace"), ("meat.state", "cooked"), ("hunting", "meat.state"), ("meat.state", "raw"), ("hunting", "meat.state"), ("food_level", "eat"), ("hunting", "food_level"), ("inventory", "sword"), ("inventory", "axe"), ("inventory", "pickaxe"), ("inventory", "shovel"), ("inventory", "hoe"), ("inventory", "select_weapon"), ("hunting", "inventory")]
        assert graphs[0][0] == expected_nodes
        assert graphs[0][1] == expected_edges
        
        for g in graphs:
            G = to_network_x(g)
            print(G)