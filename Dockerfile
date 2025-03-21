FROM python:3.8-slim

WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY setup.py .
COPY README.md .
COPY dvmcp/ ./dvmcp/
COPY example_model.py .
COPY model-card.yaml .
COPY smithery.yaml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e . && \
    rm -rf /root/.cache/pip/*

# Create upload directory with proper permissions
RUN mkdir -p /app/uploads && \
    chown -R nobody:nogroup /app/uploads

# Use a non-root user
USER nobody

# Default port (can be overridden by smithery.yaml)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/v1/model/metadata || exit 1

# Entry point that allows for configuration via environment variables
ENTRYPOINT ["python", "-m", "flask"]
CMD ["run", "--host=0.0.0.0"] 