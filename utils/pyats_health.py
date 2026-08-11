"""pyATS AEtest service-topology and network reachability checks."""

import logging
import os
import socket
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

try:
    from pyats import aetest
    from pyats.topology import Device, Testbed

    PYATS_AVAILABLE = True
except ImportError:  # pyATS is not available on Windows.
    aetest = None
    Device = None
    Testbed = None
    PYATS_AVAILABLE = False


def _host_and_port(url: str, default_port: int) -> Tuple[str, int]:
    parsed = urlparse(url)
    return parsed.hostname or "localhost", parsed.port or default_port


class ContainerNetworkHealthChecker:
    """Model the application services as a pyATS testbed and test TCP reachability."""

    def __init__(self):
        api_host, api_port = _host_and_port(
            os.getenv("API_BASE_URL", "http://localhost:2424"),
            2424,
        )
        ui_host, ui_port = _host_and_port(
            os.getenv("UI_BASE_URL", "http://localhost:3000"),
            3000,
        )

        self.services: Dict[str, Tuple[str, int]] = {
            "Spring Boot API": (api_host, api_port),
            "React UI": (ui_host, ui_port),
            "PostgreSQL": (
                os.getenv("DB_HOST", "localhost"),
                int(os.getenv("DB_PORT", "5432")),
            ),
        }

    def build_testbed(self) -> Optional["Testbed"]:
        """Build the service topology consumed by the AEtest test case."""
        if not PYATS_AVAILABLE:
            return None

        testbed = Testbed(name="ecommerce_service_topology")
        for service_name, (host, port) in self.services.items():
            device = Device(
                name=service_name.lower().replace(" ", "_"),
                os="linux",
                type="application_service",
                connections={
                    "default": {
                        "protocol": "tcp",
                        "ip": host,
                        "port": port,
                    }
                },
            )
            testbed.add_device(device)
        return testbed

    @staticmethod
    def check_port_open(host: str, port: int, timeout: float = 3.0) -> bool:
        """Attempt a TCP handshake to verify that a service is reachable."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def run_pyats_testbed_check(self) -> Dict[str, bool]:
        """Return reachability results for every node in the service testbed."""
        self.build_testbed()
        return {
            service_name: self.check_port_open(host, port)
            for service_name, (host, port) in self.services.items()
        }


if PYATS_AVAILABLE:

    class CommonSetup(aetest.CommonSetup):
        """Create and publish the application service topology."""

        @aetest.subsection
        def initialize_testbed(self):
            checker = ContainerNetworkHealthChecker()
            self.parent.parameters["checker"] = checker
            self.parent.parameters["testbed"] = checker.build_testbed()
            logger.info("Initialized pyATS testbed with %d service nodes", len(checker.services))


    class ServiceReachability(aetest.Testcase):
        """Validate every service endpoint using individually reported AEtest steps."""

        @aetest.test
        def check_service_ports(self, checker, steps):
            for service_name, (host, port) in checker.services.items():
                with steps.start(
                    f"Check {service_name} at {host}:{port}",
                    continue_=True,
                ) as step:
                    if checker.check_port_open(host, port):
                        step.passed(f"{service_name} is reachable")
                    else:
                        step.failed(f"{service_name} is unreachable")


    class CommonCleanup(aetest.CommonCleanup):
        """Record completion of the network-health test."""

        @aetest.subsection
        def report_completion(self):
            logger.info("Completed pyATS AEtest service reachability checks")


def run_health_check() -> bool:
    """Return True only when every required service is reachable."""
    return all(ContainerNetworkHealthChecker().run_pyats_testbed_check().values())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not PYATS_AVAILABLE:
        raise SystemExit("pyATS is required to run this AEtest health check")
    aetest.main()
