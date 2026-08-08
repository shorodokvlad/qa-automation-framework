import os
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BaseClient:
    """
    Base HTTP client wrapping Python 'requests' library.
    Manages session headers, JWT token injection, and request logging.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or os.getenv("API_BASE_URL", "http://localhost:2424")).rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def set_auth_token(self, token: str):
        """Inject JWT Bearer token into Authorization header for subsequent API calls."""
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            logger.info("JWT Auth Bearer token set on session.")

    def clear_auth_token(self):
        """Remove Authorization header."""
        self.session.headers.pop("Authorization", None)

    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        return self.session.post(url, json=json_data, **kwargs)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        return self.session.get(url, params=params, **kwargs)

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        return self.session.put(url, json=json_data, **kwargs)
