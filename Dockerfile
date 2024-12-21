# Use official Python runtime as a base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY . .

# Expose the port
EXPOSE 8050

# Run the dashboard
CMD ["python", "-m", "src.dashboard"]
