FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-qt coverage

# Copy source code
COPY . .

# Default command: Run headless simulation validation
CMD ["python", "analysis/simulations/tracking_sim.py", "--headless"]
