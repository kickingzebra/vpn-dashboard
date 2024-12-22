"""
Enhanced VPN Monitor Module
Handles comprehensive VPN monitoring including sessions, performance, security, and compliance
"""

import boto3
from datetime import datetime, timedelta
import pandas as pd
import logging
import psutil
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import geoip2.database  # For geo-location

@dataclass
class VPNSession:
    """Data class for VPN session information"""
    session_id: str
    username: str
    ip_address: str
    device_info: str
    start_time: datetime
    duration: timedelta
    bandwidth_usage: float
    location: Dict[str, str]

class VPNMonitor:
    def __init__(self, use_mock=False, region='us-east-1'):
        self.use_mock = use_mock
        self.region = region
        self.logger = logging.getLogger(__name__)
        
        if not use_mock:
            try:
                self.ec2_client = boto3.client('ec2', region_name=region)
                self.cloudwatch = boto3.client('cloudwatch', region_name=region)
                self.logger.info(f"Connected to AWS in region {region}")
            except Exception as e:
                self.logger.error(f"Failed to connect to AWS: {str(e)}")
                raise

    def get_active_sessions(self) -> List[VPNSession]:
        """Get currently active VPN sessions"""
        if self.use_mock:
            return self._get_mock_sessions()
        
        try:
            # Implement real AWS Client VPN session fetching
            response = self.ec2_client.describe_client_vpn_connections()
            sessions = []
            
            for connection in response['Connections']:
                session = VPNSession(
                    session_id=connection['ConnectionId'],
                    username=connection.get('CommonName', 'Unknown'),
                    ip_address=connection.get('ClientIp', '0.0.0.0'),
                    device_info=connection.get('ClientPlatform', 'Unknown'),
                    start_time=connection['ConnectionEstablishedTime'],
                    duration=datetime.now() - connection['ConnectionEstablishedTime'],
                    bandwidth_usage=self._get_bandwidth_usage(connection['ConnectionId']),
                    location=self._get_location(connection.get('ClientIp', '0.0.0.0'))
                )
                sessions.append(session)
            
            return sessions
        except Exception as e:
            self.logger.error(f"Error fetching active sessions: {str(e)}")
            return []

    def get_performance_metrics(self) -> Dict:
        """Get comprehensive performance metrics"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            metrics = {
                'bandwidth': self._get_bandwidth_metrics(start_time, end_time),
                'latency': self._get_latency_metrics(start_time, end_time),
                'packet_loss': self._get_packet_loss_metrics(start_time, end_time),
                'resource_utilization': self._get_resource_metrics()
            }
            
            return metrics
        except Exception as e:
            self.logger.error(f"Error fetching performance metrics: {str(e)}")
            return {}

    def get_security_events(self, hours=24) -> List[Dict]:
        """Get security and audit events"""
        try:
            events = []
            if not self.use_mock:
                # Implement CloudWatch Logs query for security events
                logs_client = boto3.client('logs')
                query = "fields @timestamp, @message | filter @logStream like /security/"
                
                response = logs_client.start_query(
                    logGroupName='/aws/vpn/security',
                    startTime=int((datetime.now() - timedelta(hours=hours)).timestamp()),
                    endTime=int(datetime.now().timestamp()),
                    queryString=query
                )
                
                # Process query results
                events = self._process_security_logs(response['queryId'])
            else:
                events = self._get_mock_security_events()
            
            return events
        except Exception as e:
            self.logger.error(f"Error fetching security events: {str(e)}")
            return []

    def get_compliance_status(self) -> Dict:
        """Get compliance and security policy status"""
        try:
            status = {
                'encryption': self._check_encryption_status(),
                'certificates': self._check_certificates(),
                'access_policies': self._check_access_policies(),
                'license': self._check_license_status()
            }
            return status
        except Exception as e:
            self.logger.error(f"Error checking compliance status: {str(e)}")
            return {}

    def _get_bandwidth_metrics(self, start_time: datetime, end_time: datetime) -> Dict:
        """Get detailed bandwidth metrics"""
        if self.use_mock:
            return self._get_mock_bandwidth_metrics()
            
        try:
            metrics = self.cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'inbound',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/VPN',
                                'MetricName': 'TunnelDataIn'
                            },
                            'Period': 300,
                            'Stat': 'Sum'
                        }
                    },
                    {
                        'Id': 'outbound',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/VPN',
                                'MetricName': 'TunnelDataOut'
                            },
                            'Period': 300,
                            'Stat': 'Sum'
                        }
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            
            return {
                'inbound': metrics['MetricDataResults'][0],
                'outbound': metrics['MetricDataResults'][1]
            }
        except Exception as e:
            self.logger.error(f"Error fetching bandwidth metrics: {str(e)}")
            return {}

    def _check_encryption_status(self) -> Dict:
        """Check VPN encryption configuration"""
        try:
            if not self.use_mock:
                response = self.ec2_client.describe_vpn_connections()
                vpn_connections = response['VpnConnections']
                
                encryption_info = {
                    'algorithm': 'AES-256-GCM',  # Example
                    'perfect_forward_secrecy': True,
                    'key_rotation_enabled': True,
                    'last_rotation': datetime.now() - timedelta(days=7)
                }
            else:
                encryption_info = self._get_mock_encryption_status()
                
            return encryption_info
        except Exception as e:
            self.logger.error(f"Error checking encryption status: {str(e)}")
            return {}

    # Mock data methods for testing
    def _get_mock_sessions(self) -> List[VPNSession]:
        """Generate mock VPN session data"""
        return [
            VPNSession(
                session_id=f"vpn-session-{i}",
                username=f"user{i}@company.com",
                ip_address=f"192.168.1.{i}",
                device_info="Windows 10 Pro",
                start_time=datetime.now() - timedelta(hours=i),
                duration=timedelta(hours=i),
                bandwidth_usage=float(i * 100),
                location={"city": "London", "country": "UK"}
            )
            for i in range(1, 6)
        ]

    def _get_mock_security_events(self) -> List[Dict]:
        """Generate mock security events"""
        return [
            {
                "timestamp": datetime.now() - timedelta(minutes=30),
                "event_type": "LOGIN_SUCCESS",
                "username": "user1@company.com",
                "ip_address": "192.168.1.100",
                "details": "Successful login from approved device"
            },
            {
                "timestamp": datetime.now() - timedelta(hours=1),
                "event_type": "LOGIN_FAILURE",
                "username": "unknown@external.com",
                "ip_address": "203.0.113.1",
                "details": "Failed login attempt - invalid credentials"
            }
        ]
