import json
import pytest
import pathlib
from utils.api_client import APIClient

# Get the project root directory
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config' / 'config.json'

CONFIG = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))

@pytest.fixture(scope="session")
def client():
    c = APIClient(base_url=CONFIG['base_url'], timeout=CONFIG.get('timeout_seconds', 10))
    token = c.create_token(CONFIG['username'], CONFIG['password'])
    assert token, "Auth token could not be created. Check credentials or base_url."
    return c

def create_booking(client, payload):
    r = client.post("/booking", json=payload)
    assert r.status_code in [200, 201], f"Expected status 200 or 201, got {r.status_code}"
    return r.json()['bookingid']

def test_delete_booking_201_or_200(client):
    payload = {
        "firstname": "DeleteMe", "lastname": "Now", "totalprice": 50, "depositpaid": True,
        "bookingdates": {"checkin": "2025-02-01", "checkout": "2025-02-03"}, "additionalneeds": "None"
    }
    booking_id = create_booking(client, payload)
    r = client.delete(f"/booking/{booking_id}")
    assert r.status_code in [200, 201, 204], f"Expected status 200, 201, or 204, got {r.status_code}"  # API typically returns 201 Created for delete(!) or 200
