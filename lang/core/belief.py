
import re
from typing import List
from lang.operators.conditionals import ConditionalOperators
from lang.operators.effects import EffectOperator
from lang.operators.equivalence import EquivalanceOperators
from lang.util import rec_flatten

class BeliefOperator(ConditionalOperators, EquivalanceOperators, EffectOperator):
    
    def evaluate(self):
        value = self.evaluate_conditionals()
        result = self.evaluate_equivalance(value)
        results = self.resolve_effects(result)
        return result, results
    
    def to_graph(self):
        def extract_nodes(statement, state):
            nodes = []
            if isinstance(statement, List):
                return list(map(lambda x: extract_nodes(x, state), statement))
            
            if isinstance(statement, float) or isinstance(statement, int):
                return None    
            
            if '=' in statement:
                s1, s2 = statement.replace(' ', '').split('=')
                s1 = s1.strip()
                
                variables = re.findall(r'\b\w+(?:\.\w+)*\b', s2)
                for name in variables:
                    if name in state:
                        state_var = str(state[name])
                        if isinstance(state_var, type):
                            nodes.append(state_var)
                        else:
                            nodes.append(name)
            else:
                if statement in state:
                    value = state[statement]
                    if isinstance(value, type):
                        nodes.append(value)
                    if isinstance(value, List):
                        for v in value:
                            nodes.append(v)
                    else:
                        nodes.append(statement)
                else:
                    nodes.append(statement)
            return nodes
        
        parent = extract_nodes(self.WHEN, self.state)
        children = [self.EQ, self.GT, self.GTE, self.LT, self.LTE, self.NE, self.CONTAINS, self.CHOOSE, self.THEN, self.ELSE]
        children = map(lambda x: extract_nodes(x, self.state), filter(lambda x: x not in ['?', None, 'stop'], children))
        children = list(filter(lambda x: x != None, children))
        children = rec_flatten(children)
        edges = []
        for p in parent:
            for c in children:
                if isinstance(c, List):
                    for subc in c:
                        edges.append((p, subc))
                else:
                    edges.append((p, c))
        
        nodes = children
        return parent, nodes, edges
