import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.analysis import Report
from app.schemas.analysis import CodeRequest, AnalyzeResponse, Issue
from app.utils.language_detector import detect_language
from app.analyzers.python_analyzer import PythonAnalyzer
from app.analyzers.js_analyzer import JSAnalyzer
from app.services.ai_service import LLMEngine
from app.services.analysis_service import calculate_score, calculate_severity_breakdown
from app.services.analysis_service import aggregate_issues

router = APIRouter()

@router.post("/analyze")
def analyze_code_endpoint(request: CodeRequest, db: Session = Depends(get_db)):
    try:
        print("Incoming code:", request.code)
        
        from app.analyzers.code_analyzer import analyze_code
        issues = analyze_code(request.code)
        
        print("Generated issues:", issues)
        
        # Save to database
        try:
            lang = detect_language(request.code)
            
            # Invoke AI Analysis
            llm = LLMEngine()
            ai_issues, summary, llm_status = llm.analyze(request.code, lang)
            
            # Convert AI issues to dicts for JSON storage
            ai_issues_dicts = [issue.model_dump() if hasattr(issue, 'model_dump') else dict(issue) for issue in ai_issues]
            
            if not summary:
                summary = "Static analysis complete"
                
            issues_dict = {
                "static_issues": issues,
                "ai_issues": ai_issues_dicts,
                "summary": summary,
                "llm_status": llm_status
            }
            
            # Prepare Issue objects for scoring (static issues are currently dicts)
            from app.schemas.analysis import Issue
            scoring_issues = []
            for item in issues:
                scoring_issues.append(Issue(**item))
            for item in ai_issues:
                scoring_issues.append(item)
                
            score = calculate_score(scoring_issues)
            severity_breakdown = calculate_severity_breakdown(scoring_issues)
            
            from app.repositories.result_repository import ResultRepository
            repo = ResultRepository(db)
            db_report = repo.save_report(
                language=lang,
                score=score,
                severity_breakdown=severity_breakdown,
                issues_dict=issues_dict
            )
            print(f"Successfully saved Analysis Report (ID: {db_report.id}) to database.")
        except Exception as db_err:
            import traceback
            traceback.print_exc()
            print("Database save error:", db_err)
            
        return issues + ai_issues_dicts
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error during analysis:", e)
        return []
