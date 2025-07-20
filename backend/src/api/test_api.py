import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import patch
from ..api.main import app  # adjust import based on your actual structure


@pytest.mark.asyncio
async def test_submit_ticket_success():
    mock_response = {
        "feedback_text": "Thanks for reporting this issue.",
        "category": "Bug Report",
        "urgency_score": 3
    }

    with patch("app.api.main.promt_llm", return_value=mock_response):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/submit-ticket",
                data={
                    "ticket_id": "123",
                    "first_name": "Rawan",
                    "last_name": "Essam",
                    "email": "rawan@example.com",
                    "phone": "0501234567",
                    "text": "There is a bug in the dashboard"
                },
                files=[]  # no file uploads in this test
            )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == mock_response
