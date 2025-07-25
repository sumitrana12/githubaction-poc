# Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY src/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

# Create a non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Set working directory
WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies from wheels
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY src/ /app/src/

# Create data directory and set proper permissions
RUN mkdir -p /app/data && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    HOST=0.0.0.0 \
    DB_PATH="/app/data"

# Create volume for database
VOLUME /app/data

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application with gunicorn
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5000", "src.app:app"] 