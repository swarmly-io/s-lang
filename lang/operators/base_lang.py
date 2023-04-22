from copy import deepcopy
import re
from random import random
from types import FunctionType
from typing import Dict, List, Optional
from pydantic import BaseModel
from lang.util import generate_selector_combinations
from lang.lib.id_model import IdModel


STATE_RESULT = "state_result"

class BaseLangState(IdModel):
    original_state: Optional[Dict]
    running_state: Optional[Dict]
    # flat states
    state: Optional[Dict]
        
    def set_state(self):
        self.original_state = self.original_state
        self.running_state = deepcopy(self.original_state)
        self.state = generate_selector_combinations(self.original_state)
        
    def update_flat_state(self):
        self.state = generate_selector_combinations(self.running_state)
        
    def get_start_state(self):
        return generate_selector_combinations(self.original_state)

class BaseLang(BaseModel):
    state: Optional[BaseLangState]
    
    def __init__(self, **kwargs):
        kwargs = {k.upper(): v for k, v in kwargs.items()}
        super().__init__(**kwargs)
    
    def state_or_val(self, x, state):
            if x == None:
                return x
            if isinstance(x, Dict):
                return x
            
            if x in state:
                return state[x]
            else:
                return x
    
    def parse(self, statement):            
        if '=' in statement:
            s1, s2 = statement.replace(' ', '').split('=')
            s1 = s1.strip()
            
            variables = re.findall(r'\b\w+(?:\.\w+)*\b', s2)
            for name in variables:
                if name in self.state.state:
                    s2 = s2.replace(name, str(self.state.state[name]))
            result = eval(s2)
            if not s1 in self.state.state:
                self.state.state[s1] = None
            
            # return a dict so we can decide what to do
            return { s1: result, STATE_RESULT: True }
        else:
            if statement in self.state.state:
                value = self.state.state[statement]
                if isinstance(value, FunctionType):
                    return value(self.state.state)
                else:
                    return value
            else:
                return statement
            
    def run_or_return(self, result):
        if STATE_RESULT in result:
            del result[STATE_RESULT]
            return result
        else:
            return result
            
    def run_statements(self, statements, final_results):
        if isinstance(statements, List):
            results = []
            for item in statements:
                results.append(self.parse(item))
                    
            if self.CHOOSE:
                if random() < self.CHOOSE:
                    r = self.run_or_return(results[0])
                else:
                    r = self.run_or_return(results[1])
                final_results.append(r)
            else:
                        # apply all results
                for r in results:
                    final_results.append(self.run_or_return(r))
        else:
            parsed = self.parse(statements)
            ran = self.run_or_return(parsed)
            if ran:
                final_results.append(ran)