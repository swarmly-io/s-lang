
from lang.operators.conditionals import MISSING, ConditionalOperators
from lang.operators.equivalence import EquivalanceOperators

class GoalOperator(ConditionalOperators, EquivalanceOperators):
    TOTAL: bool = False
    
    def evaluate(self):
        value = self.evaluate_conditionals()
        if value == MISSING:
            return False
        return self.evaluate_equivalance(value)
    
    