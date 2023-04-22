
from typing import Any, Optional
from lang.operators.base_lang import BaseLang

class MemoryOperators(BaseLang):
    INCREASED: Optional[Any]
    DECREASED: Optional[Any]
    
    def evaluate_memory(self, value):
        # get previous state with key
        # compare current state
        # return then if yes, return else if no
        key = self.get_key()
        def increased():
            start_state = self.state.get_start_state()
            start_val = start_state.get(key)
            if not start_val and value:
                return True
            elif start_val and not value:
                return False
            elif start_val < value:
                return True
            else:
                return False
        
        def decreased():
            start_state = self.state.get_start_state()
            start_val = start_state.get(key)
            if not start_val and value:
                return False
            elif not value and start_val:
                return True
            elif value < start_val:
                return True
            else:
                return False
        
        if self.INCREASED:
            result = increased()
        else:
            result = decreased()
        
        return result
            