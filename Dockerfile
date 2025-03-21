FROM python:3.8-slim

WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY setup.py .
COPY README.md .
COPY dvmcp/ ./dvmcp/
COPY example_model.py .
COPY model-card.yaml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Create upload directory
RUN mkdir -p uploads

# Create a non-root user
RUN useradd -m dvmcp
RUN chown -R dvmcp:dvmcp /app
USER dvmcp

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"] 