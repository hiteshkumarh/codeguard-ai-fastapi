import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.repositories.result_repository import ResultRepository

router = APIRouter()

@router.get("/reports")
def get_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    repo = ResultRepository(db)
    reports = repo.get_reports(skip=skip, limit=limit)
    
    result = []
    for r in reports:
        result.append({
            "id": r.id,
            "language": r.language,
            "score": r.score,
            "timestamp": r.timestamp,
            "severity_breakdown": json.loads(r.severity_breakdown) if r.severity_breakdown else {}
        })
    return result

@router.get("/report/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    repo = ResultRepository(db)
    report = repo.get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    issues_data = json.loads(report.issues_json) if report.issues_json else {}
    
    return {
        "id": report.id,
        "language": report.language,
        "score": report.score,
        "timestamp": report.timestamp,
        "severity_breakdown": json.loads(report.severity_breakdown),
        "static_issues": issues_data.get("static_issues", []),
        "ai_issues": issues_data.get("ai_issues", []),
        "summary": issues_data.get("summary", ""),
        "llm_status": issues_data.get("llm_status", "unknown")
    }

@router.get("/results")
def get_results(db: Session = Depends(get_db)):
    repo = ResultRepository(db)
    latest_report = repo.get_latest_report()
    if not latest_report:
        print("No reports found in DB")
        return {"issues": []}
    
    issues_data = json.loads(latest_report.issues_json) if latest_report.issues_json else {}
    static_issues = issues_data.get("static_issues", [])
    ai_issues = issues_data.get("ai_issues", [])
    
    combined_issues = []
    
    def transform_issue(issue, default_type):
        return {
            "type": issue.get("type", default_type),
            "severity": issue.get("severity", "Medium"),
            "description": issue.get("description", ""),
            "line_number": issue.get("line_number", 0)
        }
        
    print(f"Loading results: {len(static_issues)} static, {len(ai_issues)} AI")
        
    for issue in static_issues:
        combined_issues.append(transform_issue(issue, "Static Analysis"))
    for issue in ai_issues:
        combined_issues.append(transform_issue(issue, "AI Analysis"))
        
    return {"issues": combined_issues}
