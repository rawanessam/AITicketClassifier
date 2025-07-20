# tests/test_main.py
import json
import pytest

def test_root_endpoint(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "API is running"}

def test_submit_ticket_missing_text(client):
    # Missing 'text' input -> 422 validation error
    resp = client.post("/submit-ticket", data={
        "ticket_id": "1",
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com"
    })
    assert resp.status_code == 422

def test_submit_ticket_empty_text(client, monkeypatch):
    # Simulate empty text field -> 400
    data = {
        "ticket_id": "1",
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "text": "   "
    }
    resp = client.post("/submit-ticket", data=data)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Issue description cannot be empty."

def test_submit_ticket_success(client, monkeypatch):
    # Mock prompt_llm to return a JSON string
    expected = {
        "feedback_text": "Test response",
        "category": "General Inquiry",
        "urgency_score": None
    }
    def fake_llm(user_input):
        return json.dumps(expected)
    monkeypatch.setattr("api.main.prompt_llm", fake_llm)

    data = {
        "ticket_id": "42",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@doe.com",
        "text": "Hello world!"
    }
    resp = client.post("/submit-ticket", data=data)
    assert resp.status_code == 200
    assert resp.json() == expected

def test_submit_ticket_llm_invalid_json(client, monkeypatch):
    # Simulate LLM returning invalid JSON
    def fake_llm(user_input):
        return "not a json"
    monkeypatch.setattr("api.main.prompt_llm", fake_llm)

    data = {
        "ticket_id": "100",
        "first_name": "Foo",
        "last_name": "Bar",
        "email": "foo@bar.com",
        "text": "Test"
    }
    resp = client.post("/submit-ticket", data=data)
    assert resp.status_code == 502
    assert "Invalid JSON from LLM" in resp.json()["detail"]
