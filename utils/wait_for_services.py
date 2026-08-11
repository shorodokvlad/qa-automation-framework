"""Wait for the application HTTP endpoints to become ready before running tests."""

import logging
import os
import time
from typing import Dict

import requests

logger = logging.getLogger(__name__)


def wait_for_services(timeout_seconds: int = 180) -> None:
    services: Dict[str, str] = {
        "Spring Boot API": f"{os.getenv('API_BASE_URL', 'http://localhost:2424').rstrip('/')}/auth/health",
        "React UI": os.getenv("UI_BASE_URL", "http://localhost:3000"),
    }
    pending = dict(services)
    deadline = time.monotonic() + timeout_seconds

    with requests.Session() as session:
        while pending and time.monotonic() < deadline:
            for service_name, url in list(pending.items()):
                try:
                    response = session.get(url, timeout=3)
                    if response.status_code == 200:
                        logger.info("%s is ready at %s", service_name, url)
                        pending.pop(service_name)
                except requests.RequestException:
                    pass

            if pending:
                time.sleep(2)

    if pending:
        unavailable = ", ".join(f"{name} ({url})" for name, url in pending.items())
        raise TimeoutError(f"Services did not become ready within {timeout_seconds}s: {unavailable}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    wait_for_services(int(os.getenv("SERVICE_STARTUP_TIMEOUT", "180")))
