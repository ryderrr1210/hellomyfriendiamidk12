# Use Python 3.10 to ensure crypto libraries (coincurve/cffi) compile perfectly
FROM python:3.10-slim

# Install system utilities and Node.js
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements first (caches this step)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node requirements
COPY package*.json ./
RUN npm install

# Copy everything else, including your gorgeous public folder
COPY . .

# Make the boot script executable
RUN chmod +x start.sh

# The cloud platform will inject the $PORT variable natively
CMD ["./start.sh"]
