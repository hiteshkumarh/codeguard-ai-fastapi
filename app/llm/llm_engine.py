import json
import requests
from typing import List, Tuple
from app.schemas.request_response import Issue
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class LLMEngine:
    def __init__(self):
        self.base_url = settings.GROQ_BASE_URL
        self.model = settings.LLM_MODEL_NAME
        self.api_key = settings.GROQ_API_KEY

    def analyze(self, code: str, language: str) -> Tuple[List[Issue], str, str]:
        prompt = f"""
        Analyze the following {language} code and identify any bugs, security vulnerabilities, or code quality issues.
        Return the result EXACTLY as a JSON object with two keys:
        - "issues": a JSON array of objects with the following keys:
          - "type": A short category for the rule/issue (e.g. "Readability", "Code Style", "Security Risk")
          - "description": A description of the issue
          - "severity": Must be one of "critical", "high", "medium", or "low"
          - "line_number": The approximate line number where the issue occurs (integer)
        - "summary": A 1-2 sentence overall summary of the code and its issues.
        
        Do not include any markdown formatting, only the raw JSON object.
        
        Code to analyze:
        ```
        {code}
        ```
        """
        
        issues = []
        llm_status = "success"
        summary = ""
        
        if not self.api_key:
            logger.info("GROQ_API_KEY not set, AI features disabled")
            return [], "GROQ_API_KEY not configured. AI analysis skipped.", "skipped"

        logger.info(f"LLM Engine starting - Key Loaded: {bool(self.api_key)}, Model: {self.model}, Base URL: {self.base_url}")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a code analysis bot. Always format your output strictly as a JSON object matching the requested schema. No markdown formatting."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.2
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Defensive parsing of the Groq response structure
            choices = data.get("choices")
            if not isinstance(choices, list) or len(choices) == 0:
                raise ValueError("Malformed Groq response: missing or empty 'choices'")
                
            message = choices[0].get("message")
            if not isinstance(message, dict):
                raise ValueError("Malformed Groq response: missing 'message' dictionary")
                
            response_text = message.get("content")
            if not isinstance(response_text, str):
                raise ValueError("Malformed Groq response: 'content' is not a string")
            
            parsed = json.loads(response_text)
            
            # To handle if it returns {"issues": [...], "summary": "..."}
            issues_list = parsed.get("issues", []) if isinstance(parsed, dict) else (parsed if isinstance(parsed, list) else [])
            summary = parsed.get("summary", "") if isinstance(parsed, dict) else ""
            
            allowed_severities = {"critical", "high", "medium", "low"}
            
            for item in issues_list:
                if len(issues) >= 10:
                    break
                    
                if not isinstance(item, dict):
                    continue
                    
                sev = item.get("severity")
                if not sev or not isinstance(sev, str):
                    continue
                    
                sev_lower = sev.strip().lower()
                if sev_lower not in allowed_severities:
                    continue
                
                # Cleanup fields
                issue_type = str(item.get("type", "Code Quality")).strip()
                issue_msg = str(item.get("description", "Unknown issue")).strip()
                
                # Ensure line is int or None
                line_val = item.get("line_number")
                try:
                    line_parsed = int(line_val) if line_val is not None else None
                except (ValueError, TypeError):
                    line_parsed = None
                
                issues.append(Issue(
                    type=issue_type,
                    description=issue_msg,
                    severity=sev_lower,
                    line_number=line_parsed
                ))

                
        except (requests.exceptions.RequestException, json.JSONDecodeError, Exception) as e:
            logger.error(f"LLM Engine error: {e}")
            llm_status = "failed"
            summary = "AI analysis skipped due to API failure or timeout."
            issues = []
            
        return issues, summary, llm_status
