# Use official Microsoft Playwright image pre-packaged with Python and Chromium browser binaries
FROM mcr.microsoft.com/playwright/python:v1.62.0-jammy

# Set working directory inside container
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install the complete, shared dependency set. Browser binaries are in the base image.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application test code
COPY . .

# Set environment variables with defaults for docker network
ENV API_BASE_URL=http://host.docker.internal:2424
ENV UI_BASE_URL=http://host.docker.internal:3000
ENV DB_HOST=host.docker.internal
ENV DB_PORT=5432
ENV DB_NAME=postgres

# Default execution command runs pytest with HTML report output
CMD ["pytest", "--html=report.html", "--self-contained-html", "-v"]
