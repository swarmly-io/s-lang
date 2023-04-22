from copy import deepcopy
from typing import Dict, Optional

from lang.lib.id_model import IdModel
from lang.operators.base_lang import BaseLangState


# The idea with statements is that they are effectless
# They parse declarations and map to state - which can be process by some 'Runner'
# as well as process state to return some answer 
class BaseStatement(IdModel):
    state: Dict
    stateWrapper: Optional[BaseLangState]
    
    def set_state(self, lst):
        state = BaseLangState(original_state=self.state, running_state=deepcopy(self.state))
        state.set_state()
        for l in lst:
            l.state = state
        self.stateWrapper = state


