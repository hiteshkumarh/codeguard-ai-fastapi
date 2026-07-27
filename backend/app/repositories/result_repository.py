import json
from sqlalchemy.orm import Session
from app.models.analysis import Report
from typing import List, Dict, Any

class ResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_report(self, language: str, score: float, severity_breakdown: dict, issues_dict: dict) -> Report:
        db_report = Report(
            language=language,
            score=score,
            severity_breakdown=json.dumps(severity_breakdown),
            issues_json=json.dumps(issues_dict)
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def get_reports(self, skip: int = 0, limit: int = 10) -> List[Report]:
        return self.db.query(Report).order_by(Report.timestamp.desc()).offset(skip).limit(limit).all()

    def get_report_by_id(self, report_id: int) -> Report | None:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def get_latest_report(self) -> Report | None:
        return self.db.query(Report).order_by(Report.timestamp.desc()).first()
