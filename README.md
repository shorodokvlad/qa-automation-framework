<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/shorodokvlad/qa-automation-framework">
    <img src="https://img.icons8.com/color/96/test-passed.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">QA Automation Framework</h3>

  <p align="center">
    A production-ready, multi-layered QA Test Automation Framework built with Python, Playwright, Pytest, REST API Clients, Direct Database Validation, Cisco PyATS, and Docker CI/CD.
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This is the dedicated automated test suite and QA framework designed to test the full-stack **[Spring E-Commerce Application](https://github.com/shorodokvlad/spring-ecommerce-app)** (Spring Boot backend + React frontend).

Instead of flat, monolithic test scripts, this repository implements industry-standard test design patterns to validate application behavior across the entire stack:

Key features include:
* **UI Automation with Playwright (POM)** — Implements the Page Object Model design pattern for the React UI (`LoginPage`, `DashboardPage`). Encapsulates CSS locators and leverages Playwright auto-waiting mechanisms for dynamic DOM node rendering.
* **REST API Testing & JWT Sessions** — Custom HTTP API clients (`AuthClient`, `OrderClient`) using `requests.Session` that automatically authenticate with the Spring Boot backend, capture JWT Bearer tokens, and execute POST/PUT/GET requests with HTTP status and JSON payload assertions.
* **Direct Database Validation** — Connects directly to the underlying PostgreSQL (or MySQL) database via `DBConnector` (`psycopg2` / `pymysql`) to run `SELECT` queries and verify physical data persistence (orders, user records) beyond API responses.
* **Cisco PyATS Network Health Checks** — Built-in Cisco PyATS testbed script (`utils/pyats_health.py`) that pings container ports (Spring Boot `2424`, React `3000`, DB `5432`) to verify network health before test execution.
* **Containerized CI/CD Pipeline** — Complete `Dockerfile` (built on Microsoft Playwright base images) and a 5-stage declarative `Jenkinsfile` for automated pipeline execution and HTML report generation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python-shield]][Python-url]
* [![Pytest][Pytest-shield]][Pytest-url]
* [![Playwright][Playwright-shield]][Playwright-url]
* [![Spring Boot][SpringBoot-shield]][SpringBoot-url]
* [![React][React-shield]][React-url]
* [![PostgreSQL][PostgreSQL-shield]][PostgreSQL-url]
* [![Docker][Docker-shield]][Docker-url]
* [![Jenkins][Jenkins-shield]][Jenkins-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these instructions to set up the QA Automation Framework locally or execute containerized builds.

### Prerequisites

You need the following installed on your machine:
* **Python 3.9+** and **pip**
* **[Spring E-Commerce App](https://github.com/shorodokvlad/spring-ecommerce-app)** (backend running on port `2424`, React UI running on port `3000`)
* **Docker Desktop** (optional, for containerized execution)

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/shorodokvlad/qa-automation-framework.git
   cd qa-automation-framework
   ```

2. **Create and activate a Python virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies and Playwright browser binaries**
   ```sh
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure Environment Variables (Optional)**
   The framework provides intelligent defaults for local dev. You can optionally override connection settings via environment variables:
   ```sh
   export API_BASE_URL=http://localhost:2424
   export UI_BASE_URL=http://localhost:3000
   export DB_HOST=aws-0-eu-central-1.pooler.supabase.com
   export DB_PORT=5432
   export DB_NAME=postgres
   export DB_USER=postgres.ztgssqhtytwtxzjdmdyu
   export DB_PASSWORD=<your-db-password>
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Running Automated Test Suites

Ensure your virtual environment is active (`source venv/bin/activate`).

* **Run all tests** (API, UI, and Integration):
  ```sh
  pytest
  ```

* **Run REST API tests only**:
  ```sh
  pytest -m api
  ```

* **Run Playwright UI tests with headed browser**:
  ```sh
  pytest -m ui --headed
  ```

* **Run End-to-End Integration tests**:
  ```sh
  pytest -m integration
  ```

### Test Reports

Running `pytest` automatically generates an interactive HTML execution report saved at:
`report.html`

Open it in your browser to view detailed step durations, stack traces, and test results:
```sh
open report.html
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CI/CD & DOCKER -->
## CI/CD and Docker

### Docker Execution

The framework is fully containerized with Microsoft Playwright Chromium pre-installed.

1. **Build the Docker container image**:
   ```sh
   docker build -t qa-automation-framework .
   ```

2. **Run tests inside Docker**:
   ```sh
   docker run --rm qa-automation-framework
   ```

### Jenkins Pipeline

The included [`Jenkinsfile`](Jenkinsfile) defines a declarative 5-stage pipeline:
1. **Checkout Code** — Pulls the latest test automation code.
2. **Build Docker Container** — Packages the test suite into a container.
3. **PyATS Health Check** — Verifies container network port reachability.
4. **Run Pytest Suite** — Executes Pytest inside the container.
5. **Publish Report** — Archives `report.html` as a build artifact in Jenkins.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Vladislav Shorodok - [@shorodokvlad](https://twitter.com/shorodokvlad) - vlad.shorodoc@gmail.com

Framework Repository: [https://github.com/shorodokvlad/qa-automation-framework](https://github.com/shorodokvlad/qa-automation-framework)  
Application Repository: [https://github.com/shorodokvlad/spring-ecommerce-app](https://github.com/shorodokvlad/spring-ecommerce-app)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Pytest-shield]: https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white
[Pytest-url]: https://docs.pytest.org/
[Playwright-shield]: https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white
[Playwright-url]: https://playwright.dev/python/
[SpringBoot-shield]: https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white
[SpringBoot-url]: https://spring.io/projects/spring-boot
[React-shield]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[PostgreSQL-shield]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Docker-shield]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Jenkins-shield]: https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white
[Jenkins-url]: https://www.jenkins.io/
