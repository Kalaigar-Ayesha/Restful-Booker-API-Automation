import json
import pytest
import pathlib
from utils.api_client import APIClient

# Get the project root directory
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config' / 'config.json'
DATA_PATH = PROJECT_ROOT / 'config' / 'test_data.json'

CONFIG = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
DATA = json.loads(DATA_PATH.read_text(encoding='utf-8'))

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

def test_put_update_booking_200(client):
    booking_id = create_booking(client, DATA['bookings'][0])
    update_payload = DATA['update_payload']
    r = client.put(f"/booking/{booking_id}", json=update_payload)
    assert r.status_code == 200, f"Expected status 200, got {r.status_code}"
    body = r.json()
    assert body['firstname'] == update_payload['firstname']
    assert body['lastname'] == update_payload['lastname']

def test_patch_partial_update_booking_200(client):
    booking_id = create_booking(client, DATA['bookings'][1])
    patch_payload = DATA['partial_update_payload']
    r = client.patch(f"/booking/{booking_id}", json=patch_payload)
    assert r.status_code == 200, f"Expected status 200, got {r.status_code}"
    body = r.json()
    assert body['firstname'] == patch_payload['firstname']
