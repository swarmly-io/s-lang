
from typing import Any, Dict, Optional
from lang.operators.base_lang import BaseLang
from lang.util import reverse_selector_combinations, update_nested_dict

class EffectOperator(BaseLang):
    THEN: Optional[Any]
    ELSE: Optional[Any]
    
    CHOOSE: Optional[Any] # choose takes two elements and a probability. Order matters.
    
    def resolve_effects(self, result):
        event_results = []  
        if result:
            if self.THEN:
                self.run_statements(self.THEN, event_results)
        else:
            if self.ELSE:
                self.run_statements(self.ELSE, event_results)
        event_results = list(filter(lambda x: x != None, event_results))
        norm_event_results = []
        for e in event_results:
            if e == 'stop':
                return ['stop']
            if isinstance(e, str):
                norm_event_results.append(e)
                continue
            if isinstance(e, Dict):
                e = reverse_selector_combinations(e)
                self.state.running_state.update(e)
                self.state.update_flat_state()
                norm_event_results.append(e)
        
        return norm_event_results