"""
Test Monitor Module for VPN Dashboard
Tracks and stores VPN test results
"""

import pandas as pd
from datetime import datetime, timedelta
import json
import os

class TestMonitor:
    def __init__(self):
        self.test_results_file = 'test_results.json'
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize or load existing test results"""
        if not os.path.exists(self.test_results_file):
            self.test_results = {
                'connection_tests': [],
                'performance_tests': [],
                'security_tests': []
            }
            self._save_results()
        else:
            with open(self.test_results_file, 'r') as f:
                self.test_results = json.load(f)

    def _save_results(self):
        """Save test results to file"""
        with open(self.test_results_file, 'w') as f:
            json.dump(self.test_results, f)

    def add_test_result(self, test_type, test_name, status, details=None):
        """
        Add a new test result

        Args:
            test_type (str): Type of test (connection, performance, security)
            test_name (str): Name of the specific test
            status (str): Test status (passed, failed, warning)
            details (dict): Additional test details
        """
        test_result = {
            'timestamp': datetime.now().isoformat(),
            'test_name': test_name,
            'status': status,
            'details': details or {}
        }

        self.test_results[f'{test_type}_tests'].append(test_result)
        self._save_results()

    def get_recent_results(self, hours=24):
        """Get test results from the last specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_results = {
            'connection_tests': [],
            'performance_tests': [],
            'security_tests': []
        }

        for test_type in self.test_results:
            recent_results[test_type] = [
                result for result in self.test_results[test_type]
                if datetime.fromisoformat(result['timestamp']) > cutoff
            ]

        return recent_results

    def get_test_summary(self):
        """Get summary of test results"""
        summary = {}
        for test_type in self.test_results:
            if not self.test_results[test_type]:
                continue

            total = len(self.test_results[test_type])
            passed = sum(1 for t in self.test_results[test_type]
                        if t['status'] == 'passed')

            summary[test_type] = {
                'total': total,
                'passed': passed,
                'failed': total - passed,
                'success_rate': (passed / total * 100) if total > 0 else 0
            }

        return summary