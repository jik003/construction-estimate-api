import os
import uuid

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def api():
    """Shared HTTP session. Fails fast if the server isn't running."""
    s = requests.Session()
    try:
        s.get(f"{BASE_URL}/health", timeout=3).raise_for_status()
    except requests.RequestException as e:
        pytest.exit(f"API not reachable at {BASE_URL}: start it with `uvicorn app.main:app` ({e})")
    yield s
    s.close()


@pytest.fixture
def customer_payload() -> dict:
    """A valid customer body. Unique name so tests don't collide."""
    return {
        "name": f"Test {uuid.uuid4().hex[:6]}",
        "phone": "010-1234-5678",
        "address": "123 Main St",
    }


@pytest.fixture
def customer(api, base_url, customer_payload):
    """Creates a customer before the test and deletes it afterwards."""
    r = api.post(f"{base_url}/customers", json=customer_payload)
    assert r.status_code == 201, r.text
    created = r.json()
    yield created
    api.delete(f"{base_url}/customers/{created['id']}")
