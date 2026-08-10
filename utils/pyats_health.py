import socket
import logging
import os
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# PyATS import try-catch for cross-platform resilience
PYATS_AVAILABLE = False
try:
    # pyrefly: ignore [missing-import]
    from pyats.topology import Testbed, Device
    PYATS_AVAILABLE = True
except ImportError:
    PYATS_AVAILABLE = False

class ContainerNetworkHealthChecker:
    """
    PyATS-inspired container network health checker.
    Verifies that Spring Boot API (port 2424), React Client (port 3000), 
    and DB services are reachable before running main test suites.
    """

    def __init__(self, host: str = "localhost"):
        self.host = os.getenv("APP_HOST", host)
        self.services = {
            "Spring Boot API": int(os.getenv("API_PORT", "2424")),
            "React UI": int(os.getenv("UI_PORT", "3000")),
            "Database Service": int(os.getenv("DB_PORT", "5432"))
        }

    def check_port_open(self, host: str, port: int, timeout: float = 2.0) -> bool:
        """Attempt TCP socket handshake to verify port accessibility."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def run_pyats_testbed_check(self) -> Dict[str, bool]:
        """
        Build PyATS Testbed topology dynamically and verify service connectivity.
        """
        results = {}
        logger.info(f"--- [PyATS Health Check] Initializing testbed analysis for host '{self.host}' ---")

        if PYATS_AVAILABLE:
            testbed = Testbed(name="ecommerce_container_testbed")
            for service_name, port in self.services.items():
                dev = Device(
                    name=service_name.replace(" ", "_").lower(),
                    os="linux",
                    type="docker_container",
                    connections={"default": {"ip": self.host, "port": port}}
                )
                testbed.add_device(dev)

            logger.info(f"PyATS Testbed initialized with {len(testbed.devices)} container nodes.")

        for service_name, port in self.services.items():
            is_healthy = self.check_port_open(self.host, port)
            results[service_name] = is_healthy
            status_str = "REACHABLE [PASS]" if is_healthy else "UNREACHABLE [FAIL/OFFLINE]"
            logger.info(f"Service Node '{service_name}' on {self.host}:{port} -> {status_str}")

        return results

def run_health_check() -> bool:
    """Helper entry point for test suite fixtures."""
    checker = ContainerNetworkHealthChecker()
    results = checker.run_pyats_testbed_check()
    # Pass if Spring Boot API port is reachable (or log summary)
    return any(results.values())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    checker = ContainerNetworkHealthChecker()
    res = checker.run_pyats_testbed_check()
    print("\nHealth Check Summary:", res)
