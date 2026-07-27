from abc import ABC, abstractmethod
from typing import List
from app.schemas.analysis import Issue

class BaseAnalyzer(ABC):  
    @abstractmethod
    def analyze(self, code: str) -> List[Issue]:
        pass
