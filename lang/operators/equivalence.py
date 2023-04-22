
from typing import Any, Optional
from lang.operators.lists import ListOperators
from lang.operators.memory import MemoryOperators


class EquivalanceOperators(ListOperators, MemoryOperators):
    EQ: Optional[Any] = '?'
    NE: Optional[Any] = '?'
    LT: Optional[Any] = '?'
    LTE: Optional[Any] = '?'
    GT: Optional[Any] = '?'
    GTE: Optional[Any] = '?'

    def evaluate_equivalance(self, value):
        if self.EQ != '?':
            return value == self.state_or_val(self.EQ, self.state.state)
        if self.NE != '?':
            return value != self.state_or_val(self.NE, self.state.state)
        if self.LT != '?':
            return value < self.state_or_val(self.LT, self.state.state)
        if self.LTE != '?':
            return value <= self.state_or_val(self.LTE, self.state.state)
        if self.GT != '?':
            return value > self.state_or_val(self.GT, self.state.state)
        if self.GTE != '?':
            return value >= self.state_or_val(self.GTE, self.state.state)
        if self.CONTAINS or self.LEN != None or self.LENGT != None or self.LENLT != None:
            return self.evaluate_lists(value)
        if self.INCREASED or self.DECREASED:
            return self.evaluate_memory(value)
        
        return bool(value)
