
from typing import Any, Optional
from lang.operators.base_lang import BaseLang

MISSING = 'missing'

"""
todo
- when:
    - name: zombie
        is: hitting
    - or:
        - name: zombie
            is: spitting
        - name: zombie
            is: charging
"""
class ConditionalOperators(BaseLang):
    
    WHEN: Optional[Any]
    IF: Optional[Any]
    
    # todo
    #AND: Optional[str]
    # todo
    #OR: Optional[str]        
    
    def evaluate_conditionals(self):
        # look up value in state
        self.validate_expressions()

        key = self.get_key()
        value = self.state.state.get(key, MISSING)
        return value

    def get_key(self):
        key = self.WHEN or self.IF
        
        if not key:
            raise Exception(f"state property not valid {key}")
        return key

    def validate_expressions(self):
        if self.WHEN and self.IF:
            raise Exception(f"Can't have if and when {self.WHEN} {self.IF}")
        