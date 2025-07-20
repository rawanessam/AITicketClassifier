# tests/conftest.py
import sys
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add src directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "/Users/reb9482/Documents/SensryLabs/SenaryLabTask/backend/src")))

from api.main import app as fastapi_app, engine_loaded # type: ignore

@pytest.fixture
def client():
    return TestClient(fastapi_app)

@pytest.fixture(autouse=True)
def check_engine():
    # Ensure engine_loaded flag is correctly set
    assert engine_loaded, "engine.py did not load correctly"
