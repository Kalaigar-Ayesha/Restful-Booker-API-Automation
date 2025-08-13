import json
import pytest
import requests
from utils.api_client import APIClient
from utils.schema_validator import assert_schema
import pathlib
import os

# Get the project root directory
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config' / 'config.json'
DATA_PATH = PROJECT_ROOT / 'config' / 'test_data.json'

# Load config and data once
CONFIG = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
DATA = json.loads(DATA_PATH.read_text(encoding='utf-8'))

BASE_URL = CONFIG['base_url']

# Basic schema for /booking response
BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": {"type": "object"}
    },
    "required": ["bookingid", "booking"]
}

@pytest.fixture(scope="session")
def client():
    return APIClient(base_url=BASE_URL, timeout=CONFIG.get('timeout_seconds', 10))

@pytest.mark.parametrize("payload", DATA["bookings"])
def test_create_booking_201(client, payload):
    resp = client.post("/booking", json=payload)
    assert resp.status_code in [200, 201], f"Expected status 200 or 201, got {resp.status_code}"
    body = resp.json()
    assert_schema(body, BOOKING_SCHEMA)
    assert body['booking']['firstname'] == payload['firstname']
    assert body['booking']['lastname'] == payload['lastname']
    # Return id for other tests if needed (here just assert presence)
    assert isinstance(body['bookingid'], int)
