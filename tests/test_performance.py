"""
Test module for VPN Performance monitoring
"""

import pandas as pd
from src.VPNmonitor import VPNMonitor

def test_vpn_monitor_initialization():
    """Test VPN monitor initialization with mock data"""
    monitor = VPNMonitor(use_mock=True)
    assert monitor is not None

def test_get_vpn_status():
    """Test getting VPN status with mock data"""
    monitor = VPNMonitor(use_mock=True)
    status = monitor.get_vpn_status()
    
    # Verify return type
    assert isinstance(status, pd.DataFrame)
    
    # Verify required columns exist
    required_columns = ['VPN ID', 'State', 'Type', 'Static Route Only', 'Last Status Change']
    for col in required_columns:
        assert col in status.columns
        
    # Verify data is not empty
    assert len(status) > 0
