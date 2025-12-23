# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set timezone to UTC
ENV TZ=UTC

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app.py .
COPY scripts/ ./scripts/
COPY cron/ ./cron/

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Install cron job
RUN chmod 0644 ./cron/2fa-cron && \
    crontab ./cron/2fa-cron

# Make scripts executable
RUN chmod +x ./scripts/*.py

# Expose port
EXPOSE 8080

# Start cron and API server
CMD ["sh", "-c", "cron && python app.py"]
