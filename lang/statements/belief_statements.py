from copy import deepcopy
from typing import List

from lang.core.belief import BeliefOperator
from lang.operators.base_lang import BaseLangState
from lang.statements.statements import BaseStatement


class BeliefStatements(BaseStatement):
    name: str
    rules: List[BeliefOperator]

    def set_state(self):
        state = BaseLangState(original_state=self.state, running_state=deepcopy(self.state))
        state.set_state()
        for l in self.rules:
            l.state = state
        self.stateWrapper = state

    def evaluate(self):
        results = []
        for r in self.rules:
            answer, result = r.evaluate()
            results = results + result
            if 'stop' in result:
                break
        return results

    def graph(self):
        nodes = []
        edges = []
        for r in self.rules:
            pn, n,e = r.to_graph()
            nodes = nodes + n + pn
            edges = edges + e
            for p in pn:
                edges.append((self.stateWrapper.state[self.name], p))
        return (nodes, edges)
