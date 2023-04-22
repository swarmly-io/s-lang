
from typing import Any, Optional
from lang.operators.base_lang import BaseLang

class ListOperators(BaseLang):
    CONTAINS: Optional[Any]
    LEN: Optional[int]
    LENGT: Optional[int]
    LENLT: Optional[int]
    
    def evaluate_lists(self, value):
        if self.CONTAINS:
            def in_list(value):
                for v in self.CONTAINS:
                    if v in value:
                        return True
                return False
            
            return next(filter(lambda x: in_list(x.get('name')), value), False)
        if self.LEN != None:
            return len(value) == self.LEN
        if self.LENGT != None:
            return len(value) > self.LENGT
        if self.LENLT != None:
            return len(value) < self.LENLT
            
        