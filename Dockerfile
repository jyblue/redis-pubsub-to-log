FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app \
    APP_BASE_DIR=/data \
    TZ=Etc/UTC

WORKDIR ${APP_HOME}

# System deps (for tzdata, locales if needed)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends tzdata ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create data volume mount point for logs/messages
RUN mkdir -p /data && chmod -R 777 /data
VOLUME ["/data"]

# Default config path can be overridden by APP_CONFIG
ENV APP_CONFIG=config/default.json

# Expose nothing (client to Redis internally/externally)

ENTRYPOINT ["python", "main.py"]
