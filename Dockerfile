FROM python:3.11-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]