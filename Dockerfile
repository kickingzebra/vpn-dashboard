# Use official Python runtime as a base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy src directory
COPY src/ ./src/

# Create __init__.py if it doesn't exist
RUN touch src/__init__.py

# Make port 8050 available
EXPOSE 8050

# Run the application
CMD ["python", "-m", "src.dashboard"]
