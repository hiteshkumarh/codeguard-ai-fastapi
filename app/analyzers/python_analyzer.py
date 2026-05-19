import ast
from typing import List
from app.schemas.request_response import Issue
from app.analyzers.base_analyzer import BaseAnalyzer

class PythonAnalyzer(BaseAnalyzer):
    def analyze(self, code: str) -> List[Issue]:
        issues = []
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                        issues.append(Issue(
                            type="Security Risk",
                            message="Use of eval() detected.",
                            severity="critical",
                            line=node.lineno
                        ))
                elif isinstance(node, ast.For):
                    for child in ast.walk(node):
                        if child != node and isinstance(child, (ast.For, ast.While)):
                            # Very basic nested loop check
                            issues.append(Issue(
                                type="High Complexity",
                                message="Nested loops increase time complexity (O(n^2)).",
                                severity="high",
                                line=child.lineno
                            ))
                            break
                            
        except SyntaxError as e:
            issues.append(Issue(
                type="Syntax Error",
                message=f"Syntax Error: {str(e)}",
                severity="critical",
                line=e.lineno
            ))
            
        return issues
