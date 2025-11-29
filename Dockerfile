# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (if needed for pip or SSL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI/Uvicorn will run on
EXPOSE 8080

# Environment variable for port (Cloud Run uses PORT)
ENV PORT=8080

# Use uvicorn as the server
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
