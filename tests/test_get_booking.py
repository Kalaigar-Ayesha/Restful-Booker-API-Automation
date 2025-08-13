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
    return APIClient(base_url=CONFIG['base_url'], timeout=CONFIG.get('timeout_seconds', 10))

def create_sample_booking(client, payload):
    resp = client.post("/booking", json=payload)
    assert resp.status_code in [200, 201], f"Expected status 200 or 201, got {resp.status_code}"
    return resp.json()['bookingid']

def test_get_booking_by_id_200(client):
    sample_payload = {
        "firstname": "GetTest", "lastname": "User", "totalprice": 123,
        "depositpaid": True, "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-05"},
        "additionalneeds": "Breakfast"
    }
    booking_id = create_sample_booking(client, sample_payload)
    resp = client.get(f"/booking/{booking_id}")
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    data = resp.json()
    assert data['firstname'] == "GetTest"
    assert data['lastname'] == "User"

def test_get_booking_not_found_404(client):
    resp = client.get("/booking/0")  # unlikely id
    assert resp.status_code in [404, 405], f"Expected status 404 or 405, got {resp.status_code}"  # API may return 404 or 405 when not found/invalid
