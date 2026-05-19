import tempfile
import subprocess
import os
import json
from typing import List
from app.schemas.request_response import Issue
from app.analyzers.base_analyzer import BaseAnalyzer
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class JSAnalyzer(BaseAnalyzer):
    def analyze(self, code: str) -> List[Issue]:
        issues = []
        
        # Temporary file for ESLint execution - must be in the project directory
        # so that ESLint flat configs don't ignore it for being outside the base path
        with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode='w', dir=os.getcwd()) as f:
            f.write(code)
            temp_path = f.name
            
        try:
            # Check if Node is installed
            try:
                subprocess.run(["node", "-v"], capture_output=True, check=True)
            except FileNotFoundError:
                issues.append(Issue(
                    type="Environment Error",
                    message="Node.js is not installed or not in PATH.",
                    severity="medium"
                ))
                return issues

            # We run the internal eslint.js using explicit node instead of `npx.cmd`.
            # This is significantly more resilient to WinError 2 pathing issues because 
            # node.exe is strictly in the PATH, and the eslint bin is local.
            eslint_bin = os.path.join(os.getcwd(), "js-analyzer", "node_modules", "eslint", "bin", "eslint.js")
            
            if not os.path.exists(eslint_bin):
                issues.append(Issue(
                    type="Environment Error",
                    message=f"Local ESLint not found. Ensure 'npm install eslint' was run. Path checked: {eslint_bin}",
                    severity="medium"
                ))
                return issues

            # We explicitly pass the config file because the target JS file is in %TEMP%
            # and ESLint wouldn't find the configuration in our project directory otherwise.
            config_path = os.path.join(os.getcwd(), "js-analyzer", "eslint.config.js")
            cmd = ["node", eslint_bin, "-c", config_path, "--format", "json", temp_path]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    shell=os.name == 'nt'
                )
            except Exception as e:
                issues.append(Issue(
                    type="Execution Error",
                    message=f"Failed to execute ESLint. Ensure 'npm install' ran. Error: {str(e)}",
                    severity="medium"
                ))
                return issues
            
            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    if data and len(data) > 0:
                        messages = data[0].get("messages", [])
                        for msg in messages:
                            severity_map = {1: "medium", 2: "high"}
                            severity = severity_map.get(msg.get("severity"), "low")
                            
                            issues.append(Issue(
                                type=msg.get("ruleId") or "Lint Error",
                                message=msg.get("message", "Unknown error"),
                                severity=severity,
                                line=msg.get("line")
                            ))
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse ESLint output: {result.stdout}")
        except Exception as e:
            logger.error(f"Error running ESLint: {e}")
            issues.append(Issue(
                type="Execution Error",
                message=f"Failed to execute static analysis: {str(e)}",
                severity="medium"
            ))
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
        return issues
