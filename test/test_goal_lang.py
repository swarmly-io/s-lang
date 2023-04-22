


import yaml
from lang.statements.goal_statements import GoalStatements


class TestGoalsLang:
    
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
            'keep_health_level_high': 'keep_health_level_high',
            'mean.health_level': 11,
            'performed': { 'collect_wood': True, 'crafting_stone_pickaxe': True, 'crafting_wooden_pickaxe1': False },
            'basic_resource_levels': { 'iron_ore': 5, 'wood': 50, 'satisfied': True },
            'account': { 'balance': 0 }
        }
        
        with open("./test/config/base_goals.yaml", 'r') as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            self.goals = list(map(lambda x: GoalStatements(**x, state=state), data))
            for s in self.goals:
                s.set_state()
                
    def test_goals_evalute_correctly(self):
        results = []
        for g in self.goals:
            result = g.evaluate()
            results.append(result)
    
        assert results == [True, True, False, True, False, True]    