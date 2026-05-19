import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, index=True)
    score = Column(Float)
    severity_breakdown = Column(Text)  # Store as JSON string
    issues_json = Column(Text)  # Store as JSON string
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
