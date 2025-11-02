# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (optional, needed for some packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY main.py .

# Copy the CSV into the image
COPY data/out/abfall_abc_cleaned.csv ./data/out/abfall_abc_cleaned.csv

# Command to run the script
CMD ["python", "main.py"]
