import json
import logging
from typing import Any, Dict, Optional

import requests

class APIClient:
    """Reusable API client around requests.Session with auth support."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        # basic logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        self.log = logging.getLogger("APIClient")

    # ---------------- Core HTTP methods ----------------
    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        self.log.info("%s %s", method.upper(), url)
        if 'json' in kwargs:
            self.log.info("Payload: %s", json.dumps(kwargs['json'], ensure_ascii=False))
        if 'headers' in kwargs:
            self.log.info("Headers: %s", kwargs['headers'])

        resp = self.session.request(method=method, url=url, timeout=self.timeout, **kwargs)
        self.log.info("Status: %s", resp.status_code)
        try:
            self.log.info("Response: %s", resp.text[:500])
        except Exception:
            pass
        return resp

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request('GET', path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request('POST', path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request('PUT', path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._request('PATCH', path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request('DELETE', path, **kwargs)

    # ---------------- Auth helpers (Restful Booker) ----------------
    def create_token(self, username: str, password: str) -> Optional[str]:
        """POST /auth → returns token string."""
        resp = self.post("/auth", json={"username": username, "password": password})
        if resp.status_code == 200 and 'token' in resp.json():
            token = resp.json().get('token')
            # Restful Booker expects token as Cookie header
            self.session.headers.update({"Cookie": f"token={token}"})
            return token
        return None
