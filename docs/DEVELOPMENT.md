# VPN Dashboard Development Guide

## Architecture Overview
```
python-dashboard/
├── .github/
│   └── workflows/          # CI/CD configurations
├── tests/                  # Test files
├── Dockerfile             # Container configuration
├── VPNmonitor.py         # VPN monitoring logic
├── dashboard.py          # Main dashboard application
├── requirements.txt      # Python dependencies
└── docker-compose.yml    # Docker compose configuration
```

## Development Setup

### Prerequisites
- Python 3.9+
- Docker Desktop
- Git
- PyCharm (recommended) or other IDE

### Local Development Environment
1. **Create Virtual Environment**:
```bash
# Create virtual environment
python -m venv dashboard_env

# Activate virtual environment
# On Windows:
dashboard_env\Scripts\activate
# On macOS/Linux:
source dashboard_env/bin/activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Environment Variables**:
```bash
# Development
export FLASK_ENV=development
export FLASK_DEBUG=1
export VPN_MOCK_DATA=true
```

## Docker Configuration

### Basic Docker Commands
```bash
# Build image
docker build -t vpn-dashboard .

# Run container
docker run -p 4000:8050 vpn-dashboard

# View logs
docker logs vpn-dashboard

# Stop container
docker stop vpn-dashboard

# Remove container
docker rm vpn-dashboard
```

### Port Configuration
- Default internal port: 8050
- Default external port: 4000
- Alternative port mapping: `docker run -p <host-port>:8050 vpn-dashboard`

### Volume Mounting (for development)
```bash
docker run -p 4000:8050 -v $(pwd):/app vpn-dashboard
```

## Testing

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_vpn_monitor.py

# Run with coverage
pytest --cov=. tests/
```

### Performance Tests
```bash
# Run performance tests
pytest tests/test_performance.py
```

## Troubleshooting Guide

### Common Issues and Solutions

1. **Port Already in Use**
```bash
# Check what's using the port
lsof -i :4000

# Kill process using the port
kill -9 <PID>

# Or use alternative port
docker run -p 5000:8050 vpn-dashboard
```

2. **Docker Connection Issues**
```bash
# Check Docker status
docker info

# Restart Docker Desktop
# Or from command line:
killall Docker && open /Applications/Docker.app
```

3. **Dashboard Not Loading**
- Check container logs: `docker logs vpn-dashboard`
- Verify network settings: `docker network inspect bridge`
- Check firewall settings

4. **Performance Issues**
- Monitor container resources: `docker stats vpn-dashboard`
- Check system resources: `top` or Activity Monitor
- Review performance test results

## Maintenance Procedures

### Regular Updates
1. Pull latest code:
```bash
git pull origin main
```

2. Update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

3. Rebuild container:
```bash
docker build -t vpn-dashboard .
```

### Backup Procedures
1. Export container data:
```bash
docker export vpn-dashboard > vpn-dashboard-backup.tar
```

2. Save Docker image:
```bash
docker save vpn-dashboard > vpn-dashboard-image.tar
```

## Development Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document all functions and classes
- Add comments for complex logic

### Git Workflow
1. Create feature branch:
```bash
git checkout -b feature/new-feature
```

2. Make changes and commit:
```bash
git add .
git commit -m "Description of changes"
```

3. Push changes:
```bash
git push origin feature/new-feature
```

### Testing Guidelines
- Write tests for new features
- Maintain 80%+ code coverage
- Include performance tests for critical paths
- Test Docker builds locally before pushing

### Deployment Steps
1. Test locally
2. Update version numbers
3. Run full test suite
4. Build and test Docker image
5. Push to repository
6. Monitor deployment

## Monitoring and Logging

### Container Monitoring
```bash
# View container metrics
docker stats vpn-dashboard

# Export metrics
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" vpn-dashboard
```

### Application Logging
- Logs location: `/app/logs`
- View logs: `docker exec vpn-dashboard cat /app/logs/app.log`
- Log rotation: Configured for 7 days

### Health Checks
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' vpn-dashboard

# Manual health check
curl http://localhost:4000/

Happy Coding! 
```

