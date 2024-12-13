import pandas as pd
from datetime import datetime, timedelta
import random


class VPNMonitor:
    def __init__(self, use_mock=True):
        """
        Initialize VPN Monitor
        Args:
            use_mock (bool): If True, use mock data instead of real AWS data
        """
        self.use_mock = use_mock

    def get_vpn_status(self):
        """
        Get current status of VPN connections
        Returns:
            pandas.DataFrame: VPN connection details
        """
        if self.use_mock:
            return self._get_mock_vpn_status()
        else:
            # Real AWS implementation would go here
            pass

    def get_vpn_metrics(self, vpn_id, hours=3):
        """
        Get metrics for a specific VPN connection
        Args:
            vpn_id (str): VPN connection ID
            hours (int): Hours of history to retrieve
        Returns:
            pandas.DataFrame: VPN metrics
        """
        if self.use_mock:
            return self._get_mock_vpn_metrics(vpn_id, hours)
        else:
            # Real AWS implementation would go here
            pass

    def _get_mock_vpn_status(self):
        """
        Generate mock VPN status data
        """
        vpn_data = [
            {
                'VPN ID': 'vpn-123456a',
                'State': random.choice(['available', 'pending', 'deleting']),
                'Type': 'ipsec.1',
                'Static Route Only': True,
                'Last Status Change': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'VPN ID': 'vpn-789012b',
                'State': random.choice(['available', 'pending', 'deleting']),
                'Type': 'ipsec.1',
                'Static Route Only': False,
                'Last Status Change': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        return pd.DataFrame(vpn_data)

    def _get_mock_vpn_metrics(self, vpn_id, hours=3):
        """
        Generate mock VPN metrics data
        """
        end_time = datetime.now()
        timestamps = [end_time - timedelta(minutes=5 * x) for x in range(36)]
        tunnel_states = [random.choice([0, 1, 1, 1]) for _ in range(len(timestamps))]

        return pd.DataFrame({
            'Timestamp': timestamps,
            'TunnelState': tunnel_states
        })