import requests
from data.booking_url_api import AUTH, HEADERS_DATA

class BaseBookApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.auth_token = None
        self.session = requests.Session()
        self.session.headers.update(HEADERS_DATA)

    def _check_status(self, code: int, expected: int = 200):
        assert code == expected, f"Ожидали {expected}, получили {code}"

    def login(self):
        response = self.session.post(
            f"{self.base_url}{AUTH}",
            json={"username": "admin", "password": "password123"}
        )
        response.raise_for_status()
        self.auth_token = response.json()["token"]
        self.session.headers.update({"Cookie": f"token={self.auth_token}"})
        return self.auth_token

    def get(self, endpoint: str, expected: int = 200):
        response = self.session.get(f"{self.base_url}{endpoint}")
        self._check_status(response.status_code, expected)
        try:
            return response.json()
        except Exception:
            return None

    def post(self, endpoint: str, data_json: dict, expected: int = 200):
        response = self.session.post(f"{self.base_url}{endpoint}", json=data_json)
        self._check_status(response.status_code, expected)
        return response.json()

    def put(self, endpoint: str, data_json: dict, expected: int = 200):
        response = self.session.put(f"{self.base_url}{endpoint}", json=data_json)
        self._check_status(response.status_code, expected)
        return response.json()

    def patch(self, endpoint: str, data_json: dict, expected: int = 200):
        response = self.session.patch(f"{self.base_url}{endpoint}", json=data_json)
        self._check_status(response.status_code, expected)
        return response.json()

    def delete(self, endpoint: str, expected: int = 201):
        response = self.session.delete(f"{self.base_url}{endpoint}")
        self._check_status(response.status_code, expected)

    def close(self):
        self.session.close()