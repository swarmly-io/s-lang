
from enum import Enum
from typing import Optional
from lang.operators.base_lang import BaseLang
from time import time

class TimeUnit(str, Enum):
    MILLI = 'milli'
    SECONDS = 'seconds'
    MINUTES = 'minutes'
    HOURS = 'hours'
    DAYS = 'days'
    
convert = { TimeUnit.MILLI: 1, TimeUnit.SECONDS: 1000, TimeUnit.MINUTES: 1000 * 60, TimeUnit.HOURS: 1000 * 60 * 60, TimeUnit.DAYS: 1000 * 60 * 60 * 24 } 

class TimeOperators(BaseLang):
    ELAPSED: Optional[float]
    UNIT: Optional[TimeUnit]
    started: Optional[float]
    
    def evaluate_time(self):
        t = lambda: time()*1000
        if not self.started:
            self.started = t()
        
        elapsed = t() - self.started
        elapsed = elapsed / convert[self.UNIT]
        
        return elapsed >= self.ELAPSED
        
        