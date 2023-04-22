

from time import sleep
import yaml

from lang.statements.task_statements import TaskStatements


class TestTaskLang:
    
    def setup(self):
        self.state = {
            'safe_location':  (1,1,1),
            'dangerous_entities': [{'name':'zombie', 'position': (1,2,3), 'health_estimate': 5 }],
            'closest_dangerous_entity': {'name':'zombie', 'position': (1,2,3), 'health_estimate': 5 },
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
            #'eat': type('Attribute', (), { 'name': 'eat', 'do': lambda x: ""}),
            #'hunting': type('Attribute', (), { 'name': 'hunting', 'do': lambda x: ""}),
            #'select_weapon': type('Attribute', (), { 'name': 'select_weapon', 'do': lambda x: ""}),
            # 'cook': type('Attribute', (), { 'name': 'select_weapon', 'do': lambda x: ""}),
            # 'keep_health_level_high': type('Goal')
        }
        
        with open("./test/config/base_task.yaml", 'r') as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            self.tasks = list(map(lambda x: TaskStatements(**x, state=self.state), data))
            for t in self.tasks:
                t.set_state()
                
    def test_tasks_resolved_for_task_file(self):
        results = []
        for t in self.tasks:
            result = t.evaluate()
            results.append(result)
        
        expected_results = [(["run_to_target"], [[(1, 1, 1)]]), (["fight"], [[{"name": "zombie", "position": (1, 2, 3), "health_estimate": 5}]])]
        assert results == expected_results
        
    def test_tasks_can_be_evaluated(self):
        results = []
        for t in self.tasks:
            result = t.evaluate_status()
            results.append(result)
        
        assert results == [[(False, [])], [(False, [])]]
        
        sleep(3)
        
        self.state['dangerous_entities'] = []
        for t in self.tasks:
            t.state = self.state
            t.set_state()
        
        results = []
        for t in self.tasks:
            result = t.evaluate_status()
            results.append(result)
        
        assert results == [[(True, [])], [(False, [])]]