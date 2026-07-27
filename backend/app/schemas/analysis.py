from pydantic import BaseModel
from typing import Optional, List, Dict

class CodeRequest(BaseModel):
    code: str

class Issue(BaseModel):
    type: str
    description: str
    severity: str  # critical, high, medium, low
    line_number: Optional[int] = None

class AnalyzeResponse(BaseModel):
    language: str
    score: float
    severity_breakdown: Dict[str, int]
    static_issues: List[Issue]
    ai_issues: List[Issue]
    summary: str
    llm_status: str = "success"
