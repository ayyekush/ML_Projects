FROM python:3.10-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install first (better caching)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for models and dataset if they don't exist in the image
RUN mkdir -p ./MODELS ./DATASET ./static/Meta

# Copy the rest of the app
COPY . .

# Create static directories if they don't exist
RUN mkdir -p ./static/uploads

# Expose port for Cloud Run
EXPOSE 8080

# Run FastAPI using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]