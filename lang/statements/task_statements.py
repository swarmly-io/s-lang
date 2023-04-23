from copy import deepcopy
from typing import List

from lang.operators.base_lang import BaseLangState
from lang.statements.statements import BaseStatement
from lang.operators.core.task import TaskOperator

class TaskStatements(BaseStatement):
    task: str
    perform: List[TaskOperator]

    # evaluate get actions to perform from the state object
    # gets parameters values from state which actions need

    # should only be called once
    def evaluate(self):
        results = []
        for p in self.perform:
            result = p.evaluate_task()
            if result:
                results.append(result)

        acts = list(map(lambda x: x[0], filter(lambda x: x[0], results)))
        params = list(map(lambda x: x[1], filter(lambda x: not x[0], results)))

        return (acts, params)

    # needs to be polled until task is errored or completed
    def evaluate_status(self):
        results = []
        for p in self.perform:
            result = p.evaluate_verify(self.stateWrapper)
            if result != None:
                results.append(result)
        return results

    # set state is used to go through each 'statement' and propate the state
    def set_state(self):
        state = BaseLangState(original_state=self.state, running_state=deepcopy(self.state))
        state.set_state()
        for l in self.perform:
            l.state = state
        self.stateWrapper = state

    def to_graph():
        pass
