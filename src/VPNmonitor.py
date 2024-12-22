"""
VPN Monitor Module with optional AWS integration
"""

import pandas as pd
from datetime import datetime, timedelta
import logging
import random

# Make boto3 import optional
try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False
    print("AWS boto3 not available, using mock data only")

class VPNMonitor:
    def __init__(self, use_mock=True, region='us-east-1'):
        self.use_mock = use_mock or not AWS_AVAILABLE
        self.region = region
        self.logger = logging.getLogger(__name__)
        
        if not self.use_mock and AWS_AVAILABLE:
            try:
                self.ec2_client = boto3.client('ec2', region_name=region)
                self.cloudwatch = boto3.client('cloudwatch', region_name=region)
                self.logger.info(f"Connected to AWS in region {region}")
            except Exception as e:
                self.logger.error(f"Failed to connect to AWS: {str(e)}")
                self.use_mock = True

    # Rest of your VPNMonitor class implementation...
