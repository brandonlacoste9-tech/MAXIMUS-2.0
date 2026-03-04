FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment setup
ENV PYTHONUNBUFFERED=1

# Run the persistence engine by default
# (You can override this in docker-compose for the main bot)
CMD ["python", "sovereign_247_mode.py"]
