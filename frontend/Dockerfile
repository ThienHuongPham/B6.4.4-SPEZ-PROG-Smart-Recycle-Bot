# Use a lightweight official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Health check (ping the Streamlit port)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Streamlit configuration: prevent auto browser launch, set host to 0.0.0.0
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
