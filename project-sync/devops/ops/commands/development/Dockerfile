# SignalHire Agent Docker Container (API-only)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# No Node.js needed (browser automation removed)

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
COPY pyproject.toml ./
COPY requirements.txt* ./

## Browser automation dependencies removed

# Copy Python requirements and install
COPY run.py ./
RUN pip install --no-cache-dir \
    pandas \
    httpx \
    pydantic \
    fastapi \
    email-validator \
    structlog \
    click \
    python-dotenv \
    uvicorn \
    pydantic-settings

## Playwright removed (API-only)

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY *.py ./
COPY *.md ./

# Create directories for outputs
RUN mkdir -p screenshots test_screenshots downloads logs

# Set proper permissions
RUN chmod +x run.py
RUN chmod +x test_*.py

# Default command for development
CMD ["bash"]

# Labels for metadata
LABEL name="signalhire-agent"
LABEL version="1.0.0"
LABEL description="SignalHire lead generation agent (API-only)"
