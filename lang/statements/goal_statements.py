from copy import deepcopy
from typing import List

from lang.core.goal import GoalOperator
from lang.operators.base_lang import BaseLangState
from lang.statements.statements import BaseStatement


class GoalStatements(BaseStatement):
    name: str
    success: List[GoalOperator] = []
    failure: List[GoalOperator] = []

    def set_state(self):
        state = BaseLangState(original_state=self.state, running_state=deepcopy(self.state))
        state.set_state()
        for l in self.success:
            l.state = state
        for l in self.failure:
            l.state = state
        self.stateWrapper = state

    def evaluate(self):
        sresults = []
        total_successes = []
        for s in self.success:
            result = s.evaluate()
            if s.TOTAL:
                total_successes.append(result)
            sresults.append(result)

        total_success = any(total_successes)
        success = all(sresults)
        success = total_success or success

        total_failures = []
        fresults = []
        for f in self.failure:
            result = f.evaluate()
            if f.TOTAL:
                total_failures.append(result)
            fresults.append(result)

        total_fail = any(total_failures) if len(total_failures) > 0 else False
        failed = all(fresults) if len(fresults) > 0 else False
        failed = total_fail or failed

        if failed:
            return False
        return success
