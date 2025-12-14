# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies into a staging directory
RUN pip install --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Force UTC timezone
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
    && echo "UTC" > /etc/timezone

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app ./app
COPY scripts ./scripts

# Copy cron job
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy required keys
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Create required directories
RUN mkdir -p /data /cron \
    && chmod 755 /data /cron

# FIX Windows CRLF + set correct permissions
# (This is the CRITICAL FIX)
# Fix Windows CRLF + set correct permissions
RUN sed -i 's/\r$//' /etc/cron.d/2fa-cron \
    && chmod 0644 /etc/cron.d/2fa-cron

EXPOSE 8080

# Start API + cron
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080 & cron -f"]
