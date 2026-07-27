from app.analyzers.code_analyzer import analyze_code

def test_analyze_endpoint(client):
    code = "def my_function():\n    print('hello world')"
    response = client.post("/api/v1/analyze", json={"code": code})
    assert response.status_code == 200
    # Returns a list of issues
    data = response.json()
    assert isinstance(data, list)
    # Check if print statement is caught as a low severity debug-statement
    assert any(issue.get("type") == "debug-statement" for issue in data)

def test_invalid_request(client):
    response = client.post("/api/v1/analyze", json={"invalid": "data"})
    assert response.status_code == 422 # Unprocessable Entity for bad Pydantic validation

def test_code_analyzer_eval():
    code = "eval('1 + 1')"
    issues = analyze_code(code)
    assert any(issue["type"] == "no-eval" and issue["severity"] == "critical" for issue in issues)

def test_code_analyzer_sql_injection():
    code = "query = f\"SELECT * FROM users WHERE name = {user_input}\""
    issues = analyze_code(code)
    assert any(issue["type"] == "sql-injection" for issue in issues)
