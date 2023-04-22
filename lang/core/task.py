
from enum import Enum
from typing import Dict, List, Optional, Union
from lang.operators.base_lang import BaseLang
from lang.operators.conditionals import ConditionalOperators
from lang.operators.equivalence import EquivalanceOperators
from lang.operators.time import TimeOperators
from lang.util import rec_flatten

class TaskVerifyOperator(ConditionalOperators, EquivalanceOperators, TimeOperators):
    
    def evaluate(self):
        if self.ELAPSED:
            return self.evaluate_time()
        else:
            value = self.evaluate_conditionals()
        
        return self.evaluate_equivalance(value)

# todo
class TaskAction(str, Enum):
    STOP = "STOP"
    CONTINUE = "CONTINUE"
    RESTART = "RESTART"
    
class TaskOperator(BaseLang):
    FIND: Optional[Union[str, List[str]]]
    LOOKUP: Optional[Union[str, List[str]]]
    ACT: Optional[Union[str, Dict]]
    VERIFY: Optional[List[TaskVerifyOperator]]
    FAILED: Optional[List[str]]
    SUCCESS: Optional[List[str]]
    
    def evaluate_verify(self, state):
        if not self.VERIFY:
            return None
        
        results = []
        for v in self.VERIFY:
            v.state = state
            results.append(v.evaluate())
        
        success = all(results)
        if success and self.SUCCESS:
            results = []
            for s in self.SUCCESS:
                results.append(self.state_or_val(s, self.state.state))
            return success, results
        if not success and self.FAILED:
            results = []
            for f in self.FAILED:
                results.append(self.state_or_val(f, self.state.state))
            return success, results
        return success, []
    
    def evaluate_task(self):
        if self.VERIFY or self.FAILED or self.SUCCESS:
            return None

        params = []
        for p in rec_flatten([self.FIND, self.LOOKUP]):
            if not p:
                continue
            params.append(self.state_or_val(p, self.state.state))
        
        act = self.state_or_val(self.ACT, self.state.state)
        return (act, params)
        
        
        
    