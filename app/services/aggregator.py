from typing import List
from app.schemas.request_response import Issue

def aggregate_issues(static_issues: List[Issue], llm_issues: List[Issue]) -> List[Issue]:
    """
    Merge static issues and LLM issues. 
    Can be expanded to deduplicate if LLM finds the same issue as static analyzer.
    """
    combined = []
    seen = set()
    
    for issue in static_issues + llm_issues:
        key = (issue.type, issue.line, issue.message)
        if key not in seen:
            seen.add(key)
            combined.append(issue)
            
    return combined
