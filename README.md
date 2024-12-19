# VPN Dashboard Docker Configuration

## Overview
This repository contains a Docker-based VPN monitoring dashboard that provides real-time status and metrics visualization.

## Configuration Details
- Internal Container Port: 8050
- External Access Port: 4000
- Dashboard URL: http://localhost:4000

## Quick Start

### Build the Docker Image
```bash
docker build -t vpn-dashboard .
```

### Run the Container
```bash
docker run -p 4000:8050 vpn-dashboard
```

## Port Configuration
- The application runs on port 8050 inside the container
- Port 4000 is mapped to access the dashboard from your host machine
- If port 4000 is in use, you can use a different port:
  ```bash
  docker run -p <alternative-port>:8050 vpn-dashboard
  ```

## Development Setup
1. Clone the repository
2. Install Docker Desktop
3. Build and run the container
4. Access the dashboard at http://localhost:4000

## Files
- `dashboard.py`: Main application code
- `VPNmonitor.py`: VPN monitoring functionality
- `Dockerfile`: Container configuration
- `requirements.txt`: Python dependencies

## Troubleshooting
- If port 4000 is already in use, try a different port
- Ensure Docker Desktop is running
- Check container logs: `docker logs vpn-dashboard`

## Updates and Maintenance
1. Make code changes
2. Rebuild Docker image
3. Stop old container
4. Run new container