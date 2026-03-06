# Use stable Python version
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (Important for PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Cloud / Railway / Production port
ENV PORT=8080

# Run production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]