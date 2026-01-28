import pytest
import requests
import json
from typing import Dict, Any

# JSONPlaceholder is a free fake API service perfect for testing
BASE_URL = "https://fakerestapi.azurewebsites.net"

@pytest.fixture(scope="session")
def api_base_url():
    """Provides the base URL for API calls"""
    return BASE_URL

@pytest.fixture
def api_client():
    """Provides a requests session for API calls"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    return session
