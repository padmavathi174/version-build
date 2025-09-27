"""
Test cases for logging module.
"""

import pytest
import sys
import os
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.logging.logger import (
    setup_logger, 
    log_user_action, 
    log_system_event, 
    log_error, 
    log_performance,
    cleanup_old_logs
)

class TestLogging:
    """Test cases for logging functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_setup_logger(self):
        """Test logger setup."""
        logger = setup_logger("test_logger", self.log_file)
        
        assert logger is not None
        assert logger.name == "test_logger"
        assert len(logger.handlers) == 2  # File and console handlers
    
    def test_log_user_action(self):
        """Test user action logging."""
        log_file = os.path.join(self.temp_dir, "user_actions.log")
        
        # Test basic user action
        log_user_action("login", "user123")
        
        # Check if log file was created
        assert os.path.exists(log_file)
        
        # Read log content
        with open(log_file, 'r') as f:
            content = f.read()
            assert "User action: login" in content
            assert "User ID: user123" in content
    
    def test_log_user_action_with_details(self):
        """Test user action logging with details."""
        log_file = os.path.join(self.temp_dir, "user_actions.log")
        
        details = {"ip": "192.168.1.1", "browser": "Chrome"}
        log_user_action("register", "newuser", details)
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert "User action: register" in content
            assert "Details: {'ip': '192.168.1.1', 'browser': 'Chrome'}" in content
    
    def test_log_system_event(self):
        """Test system event logging."""
        log_file = os.path.join(self.temp_dir, "system.log")
        
        log_system_event("Application started", "INFO")
        
        assert os.path.exists(log_file)
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert "System event: Application started" in content
            assert "INFO" in content
    
    def test_log_error(self):
        """Test error logging."""
        log_file = os.path.join(self.temp_dir, "errors.log")
        
        try:
            raise ValueError("Test error")
        except ValueError as e:
            log_error(e, "Test context")
        
        assert os.path.exists(log_file)
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert "Error occurred: Test error" in content
            assert "Context: Test context" in content
    
    def test_log_performance(self):
        """Test performance logging."""
        log_file = os.path.join(self.temp_dir, "performance.log")
        
        log_performance("database_query", 1.234, {"rows": 100})
        
        assert os.path.exists(log_file)
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert "Performance: database_query took 1.234s" in content
            assert "Details: {'rows': 100}" in content
    
    def test_logger_reuse(self):
        """Test that logger instances are reused."""
        logger1 = setup_logger("reuse_test", self.log_file)
        logger2 = setup_logger("reuse_test", self.log_file)
        
        assert logger1 is logger2
    
    def test_multiple_loggers(self):
        """Test multiple logger instances."""
        logger1 = setup_logger("logger1", os.path.join(self.temp_dir, "log1.log"))
        logger2 = setup_logger("logger2", os.path.join(self.temp_dir, "log2.log"))
        
        assert logger1 is not logger2
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"
