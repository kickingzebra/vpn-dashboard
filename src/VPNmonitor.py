"""
VPN Monitor Module with optional AWS integration
"""

import pandas as pd
from datetime import datetime, timedelta
import logging
import random

class VPNMonitor:
    def __init__(self, use_mock=True, region='us-east-1'):
        self.use_mock = use_mock
        self.region = region
        self.logger = logging.getLogger(__name__)

    def get_vpn_status(self):
        """
        Get VPN connection status
        Returns:
            pandas.DataFrame: VPN status information
        """
        if self.use_mock:
            # Return mock data
            mock_data = [
                {
                    'VPN ID': 'vpn-123456a',
                    'State': 'available',
                    'Type': 'ipsec.1',
                    'Static Route Only': True,
                    'Last Status Change': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'VPN ID': 'vpn-789012b',
                    'State': 'available',
                    'Type': 'ipsec.1',
                    'Static Route Only': False,
                    'Last Status Change': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
            return pd.DataFrame(mock_data)
        else:
            # Real AWS implementation would go here
            return pd.DataFrame()

