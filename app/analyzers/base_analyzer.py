from abc import ABC, abstractmethod
from typing import List
from app.schemas.request_response import Issue

class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, code: str) -> List[Issue]:
        pass
