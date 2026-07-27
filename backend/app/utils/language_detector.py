import ast
import subprocess
import os
import tempfile
import json

def detect_language(code: str) -> str:
    # 1. Attempt Python AST parse
    try:
        ast.parse(code)
        return "python"
    except SyntaxError:
        pass
        
    # 2. Attempt JS ESLint parse
    eslint_bin = os.path.join(os.getcwd(), "node_modules", "eslint", "bin", "eslint.js")
    config_path = os.path.join(os.getcwd(), "eslint.config.js")
    
    if os.path.exists(eslint_bin) and os.path.exists(config_path):
        with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode='w', dir=os.getcwd()) as f:
            f.write(code)
            temp_path = f.name
            
        try:
            cmd = ["node", eslint_bin, "-c", config_path, "--format", "json", temp_path]
            result = subprocess.run(cmd, capture_output=True, text=True, shell=os.name == 'nt')
            
            is_js = True
            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    if data and len(data) > 0:
                        messages = data[0].get("messages", [])
                        for msg in messages:
                            if msg.get("fatal") or msg.get("ruleId") is None and "Parsing error" in msg.get("message", ""):
                                is_js = False
                                break
                except json.JSONDecodeError:
                    is_js = False
            else:
                is_js = False
                
            if is_js:
                return "javascript"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    # 3. Fallback to basic heuristics if BOTH have fatal syntax errors
    python_patterns = ["def ", "import ", "class ", "elif ", "from ", "pass", "True", "False", "None"]
    js_patterns = ["function ", "const ", "let ", "var ", "=>", "console.log", "===", "!=="]
    
    python_score = sum(1 for p in python_patterns if p in code)
    js_score = sum(1 for p in js_patterns if p in code)
    
    if python_score > js_score:
        return "python"
    elif js_score > python_score:
        return "javascript"
        
    return "unknown"
