"""
VPN Dashboard Performance Test Suite

This module provides comprehensive performance testing for the VPN Dashboard application.
It includes tests for response times, concurrent requests, memory usage, and load testing.

Key Test Categories:
1. Response Time Testing - Measures how quickly the application responds
2. Concurrent Request Testing - Tests application behavior under multiple simultaneous requests
3. Memory Usage Testing - Monitors application memory consumption
4. Load Testing - Simulates multiple users accessing the dashboard

Author: [Your Name]
Date: December 2024
"""

import pytest
import time
import requests
import statistics
from locust import HttpUser, task, between
from VPNmonitor import VPNMonitor
import asyncio
import aiohttp
import numpy as np
import psutil
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceTests:
    """
    Main performance testing class that contains all test methods and utilities.

    This class provides methods to test various performance aspects of the VPN Dashboard:
    - Response time measurements
    - Concurrent request handling
    - Memory usage monitoring
    - Load testing capabilities
    """

    def __init__(self):
        """
        Initialize the performance testing environment.
        Sets up the VPN monitor and defines base configuration.
        """
        self.vpn_monitor = VPNMonitor()
        self.base_url = "http://localhost:8050"
        logger.info("Initialized Performance Testing Suite")

    def measure_response_time(self, func, *args):
        """
        Measure the execution time of any given function.

        Args:
            func (callable): The function to measure
            *args: Arguments to pass to the function

        Returns:
            tuple: (execution_time, function_result)
        """
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        execution_time = end_time - start_time

        logger.debug(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        return execution_time, result

    async def async_request(self, session, url):
        """
        Perform an asynchronous HTTP request.

        Args:
            session (aiohttp.ClientSession): Active HTTP session
            url (str): URL to request

        Returns:
            str: Response text
        """
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            logger.error(f"Async request failed: {str(e)}")
            raise

    def test_vpn_status_response_time(self):
        """
        Test the response time of VPN status retrieval.

        Performs 100 consecutive requests and measures:
        - Average response time
        - 95th percentile response time
        - Minimum and maximum response times

        Thresholds:
        - Average response time should be < 0.1 seconds
        - 95th percentile should be < 0.2 seconds

        Returns:
            dict: Performance metrics including average, p95, min, and max times
        """
        logger.info("Starting VPN status response time test")
        times = []

        # Perform 100 test iterations
        for i in range(100):
            execution_time, _ = self.measure_response_time(
                self.vpn_monitor.get_vpn_status
            )
            times.append(execution_time)
            logger.debug(f"Iteration {i + 1}: {execution_time:.4f} seconds")

        # Calculate statistics
        avg_time = statistics.mean(times)
        p95_time = np.percentile(times, 95)

        # Verify against thresholds
        assert avg_time < 0.1, f"Average response time {avg_time:.4f}s exceeds 0.1s threshold"
        assert p95_time < 0.2, f"95th percentile response time {p95_time:.4f}s exceeds 0.2s threshold"

        results = {
            'average': avg_time,
            'p95': p95_time,
            'min': min(times),
            'max': max(times)
        }

        logger.info(f"VPN status response time test completed: {json.dumps(results, indent=2)}")
        return results

    def test_memory_usage(self):
        """
        Monitor and test memory usage during application operations.

        This test:
        1. Measures initial memory usage
        2. Performs memory-intensive operations
        3. Measures final memory usage
        4. Verifies memory increase is within acceptable limits

        Threshold:
        - Memory increase should be < 50MB

        Returns:
            dict: Memory usage statistics
        """
        logger.info("Starting memory usage test")

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
        logger.info(f"Initial memory usage: {initial_memory:.2f}MB")

        # Perform memory-intensive operations
        logger.info("Performing memory-intensive operations...")
        operations = [
            self.vpn_monitor.get_vpn_status(),
            self.vpn_monitor.get_vpn_metrics('vpn-123456a')
        ]

        # Measure final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory

        logger.info(f"Final memory usage: {final_memory:.2f}MB")
        logger.info(f"Memory increase: {memory_increase:.2f}MB")

        # Verify against threshold
        assert memory_increase < 50, (
            f"Memory usage increased by {memory_increase:.2f}MB, "
            "exceeds 50MB threshold"
        )

        return {
            'initial_memory_mb': initial_memory,
            'final_memory_mb': final_memory,
            'increase_mb': memory_increase,
            'passed_threshold': memory_increase < 50
        }


# Locust load testing configuration
class VPNDashboardUser(HttpUser):
    """
    Locust user class for load testing the VPN Dashboard.

    Simulates real user behavior with:
    - Random wait times between requests (1-3 seconds)
    - Different task weights for various endpoints
    """

    wait_time = between(1, 3)  # Random wait between requests

    @task(3)  # Higher weight for status checks
    def get_vpn_status(self):
        """Simulate user checking VPN status"""
        self.client.get("/vpn-status")

    @task(2)  # Lower weight for metrics checks
    def get_vpn_metrics(self):
        """Simulate user checking VPN metrics"""
        self.client.get("/vpn-metrics/vpn-123456a")


def run_performance_suite():
    """
    Run the complete performance test suite and collect results.

    This function:
    1. Initializes the test environment
    2. Runs all performance tests
    3. Collects and formats results
    4. Logs completion status

    Returns:
        dict: Complete performance test results
    """
    logger.info("Starting complete performance test suite")

    try:
        perf_tests = PerformanceTests()
        results = {
            'status_response': perf_tests.test_vpn_status_response_time(),
            'memory_usage': perf_tests.test_memory_usage()
        }

        # Run concurrent request test
        logger.info("Running concurrent request tests")
        loop = asyncio.get_event_loop()
        results['concurrent_performance'] = loop.run_until_complete(
            perf_tests.test_concurrent_requests()
        )

        logger.info("Performance test suite completed successfully")
        return results

    except Exception as e:
        logger.error(f"Performance test suite failed: {str(e)}")
        raise


if __name__ == "__main__":
    """
    Main entry point for running the performance tests.

    Execute this file directly to run the complete test suite:
    python test_performance.py
    """
    try:
        results = run_performance_suite()
        print("\nPerformance Test Results:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error running performance tests: {str(e)}")
        exit(1)