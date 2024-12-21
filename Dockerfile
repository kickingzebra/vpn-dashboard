# Use official Python runtime as a base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source directory
COPY src/ ./src/

# Copy other necessary files
COPY tests/ ./tests/
COPY pytest.ini .

# Make port 8050 available
EXPOSE 8050

# Run the application
CMD ["python", "src/dashboard.py"]
