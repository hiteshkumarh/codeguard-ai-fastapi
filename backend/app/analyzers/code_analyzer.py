import re
from typing import List

def analyze_code(code: str) -> List[dict]:
    issues = []
    lines = code.split('\n')
    
    in_if_block = False
    if_indent = 0
    
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
            
        print(f"Analyzing line: {line}")
        
        # eval() rule - Critical
        if "eval(" in stripped:
            issues.append({
                "type": "no-eval",
                "severity": "critical",
                "line_number": i,
                "description": "Use of eval() is dangerous"
            })
            
        # SQL injection (string + SELECT) - Critical
        upper_line = stripped.upper()
        if "SELECT " in upper_line and ("+" in stripped or "f\"" in stripped or f"f'" in stripped or "%" in stripped):
            issues.append({
                "type": "sql-injection",
                "severity": "critical",
                "line_number": i,
                "description": "Potential SQL injection detected via string concatenation"
            })
            
        # Hardcoded password - High
        if re.search(r'(password|pwd)\s*=\s*[\'"].+[\'"]', stripped, re.IGNORECASE):
            issues.append({
                "type": "hardcoded-credentials",
                "severity": "high",
                "line_number": i,
                "description": "Hardcoded password found in source code"
            })
            
        # print / console.log - Low
        if "print(" in stripped or "console.log(" in stripped:
            issues.append({
                "type": "debug-statement",
                "severity": "low",
                "line_number": i,
                "description": "Debug statement found in code"
            })
            
        # nested if - Medium
        current_indent = len(line) - len(line.lstrip())
        if stripped.startswith("if "):
            if in_if_block and current_indent > if_indent:
                issues.append({
                    "type": "nested-if",
                    "severity": "medium",
                    "line_number": i,
                    "description": "Nested if statements reduce code readability"
                })
            in_if_block = True
            if_indent = current_indent
        elif current_indent <= if_indent and not stripped.startswith("elif ") and not stripped.startswith("else:"):
            # Exited the if block
            in_if_block = False
            
    return issues
