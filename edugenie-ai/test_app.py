import pytest
from fastapi.testclient import TestClient
from main import app
from quiz_module import clean_json_block

client = TestClient(app)

def test_read_root():
    """Verify home page loads successfully with HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to EduGenie" in response.text
    assert "text/html" in response.headers["content-type"]

def test_health_check():
    """Verify health check endpoint returns 200 and correct status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "EduGenie AI"

def test_qa_endpoint_missing_param():
    """Verify /qa returns 422 when question parameter is missing."""
    response = client.get("/qa")
    assert response.status_code == 422

def test_explain_endpoint_validation():
    """Verify /explain returns 400 when topic is missing."""
    response = client.post("/explain/", json={})
    assert response.status_code == 400
    assert "Please provide a topic." in response.json()["error"]

def test_summarize_endpoint_validation():
    """Verify /summarize returns 400 when text is missing."""
    response = client.post("/summarize/", json={})
    assert response.status_code == 400
    assert "Please provide text to summarize." in response.json()["error"]

def test_quiz_endpoint_validation():
    """Verify /quiz returns 400 when text is missing."""
    response = client.post("/quiz", json={})
    assert response.status_code == 400
    assert "Please provide text for quiz." in response.json()["error"]

def test_learning_recommendations_missing_param():
    """Verify /learn/recommendations returns 422 when topic parameter is missing."""
    response = client.get("/learn/recommendations")
    assert response.status_code == 422

def test_clean_json_block():
    """Verify markdown fences and whitespace are stripped accurately."""
    sample_fenced = '```json\n[{"question": "What is Python?", "options": ["A", "B", "C", "D"], "answer": "A"}]\n```'
    cleaned = clean_json_block(sample_fenced)
    assert cleaned.startswith('[')
    assert cleaned.endswith(']')
    assert "```" not in cleaned

if __name__ == "__main__":
    print("Running basic assertions...")
    test_read_root()
    test_health_check()
    test_clean_json_block()
    test_qa_endpoint_missing_param()
    test_explain_endpoint_validation()
    test_summarize_endpoint_validation()
    test_quiz_endpoint_validation()
    test_learning_recommendations_missing_param()
    print("All basic tests passed successfully!")
