"""
Test module for VPN Performance monitoring
"""

from src.VPNmonitor import VPNMonitor

def test_vpn_monitor_initialization():
    """Test VPN monitor initialization with mock data"""
    monitor = VPNMonitor(use_mock=True)
    assert monitor is not None

def test_get_vpn_status():
    """Test getting VPN status with mock data"""
    monitor = VPNMonitor(use_mock=True)
    status = monitor.get_vpn_status()
    assert isinstance(status, pd.DataFrame)

# Add more test functions as needed...
