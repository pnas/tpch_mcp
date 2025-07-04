# Stage 1: Builder
FROM python:3.10-slim as builder

WORKDIR /app

# Install system dependencies required for building packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip show fastmcp

# Stage 2: Final image
FROM python:3.10-slim

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Add the venv to the PATH
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

ENV PYTHONPATH=/app
COPY mcp_server /app/mcp_server
COPY data_generation /app/data_generation

# Expose the port if your MCP server uses HTTP/WebSockets
EXPOSE 8001

CMD ["python", "mcp_server/server.py"]
