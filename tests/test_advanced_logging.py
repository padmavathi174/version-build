"""
Test cases for advanced logging functionality.
"""

import pytest
import sys
import os
import tempfile
import shutil
import json
import gzip

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.logging.log_rotator import LogRotator, setup_log_rotation
from src.logging.structured_logger import StructuredLogger, get_structured_logger, LogLevel

class TestLogRotator:
    """Test cases for log rotation functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.rotator = LogRotator(self.temp_dir, max_size_mb=1, backup_count=3)
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_should_rotate_small_file(self):
        """Test that small files don't need rotation."""
        log_file = os.path.join(self.temp_dir, "test.log")
        
        # Create small file
        with open(log_file, 'w') as f:
            f.write("Small log content")
        
        assert self.rotator.should_rotate(log_file) == False
    
    def test_should_rotate_large_file(self):
        """Test that large files need rotation."""
        log_file = os.path.join(self.temp_dir, "test.log")
        
        # Create large file (1.1 MB)
        with open(log_file, 'w') as f:
            f.write("x" * (1024 * 1024 + 100000))
        
        assert self.rotator.should_rotate(log_file) == True
    
    def test_rotate_log(self):
        """Test log rotation functionality."""
        log_file = os.path.join(self.temp_dir, "test.log")
        
        # Create test log file
        with open(log_file, 'w') as f:
            f.write("Test log content")
        
        # Rotate the log
        result = self.rotator.rotate_log(log_file)
        
        assert result == True
        assert not os.path.exists(log_file)  # Original file should be gone
        
        # Check that backup was created
        backup_files = [f for f in os.listdir(self.temp_dir) if f.startswith("test.log.")]
        assert len(backup_files) == 1
        
        # Check that backup is compressed
        backup_file = os.path.join(self.temp_dir, backup_files[0])
        assert backup_file.endswith('.gz')
    
    def test_cleanup_old_backups(self):
        """Test cleanup of old backup files."""
        log_file = os.path.join(self.temp_dir, "test.log")
        
        # Create multiple backup files
        for i in range(5):
            backup_file = f"{log_file}.{i:03d}"
            with open(back_file, 'w') as f:
                f.write(f"Backup {i}")
        
        # Rotate log (this should trigger cleanup)
        with open(log_file, 'w') as f:
            f.write("Test content")
        
        self.rotator.rotate_log(log_file)
        
        # Should only have 3 backup files (backup_count)
        backup_files = [f for f in os.listdir(self.temp_dir) if f.startswith("test.log.")]
        assert len(backup_files) <= 3
    
    def test_rotate_all_logs(self):
        """Test rotating all log files in directory."""
        # Create multiple log files
        for i in range(3):
            log_file = os.path.join(self.temp_dir, f"test{i}.log")
            with open(log_file, 'w') as f:
                f.write("x" * (1024 * 1024 + 100000))  # Large file
        
        rotated = self.rotator.rotate_all_logs()
        
        assert len(rotated) == 3
        for log_file in rotated:
            assert not os.path.exists(log_file)
    
    def test_get_log_stats(self):
        """Test log statistics functionality."""
        # Create some log files
        log_files = [
            os.path.join(self.temp_dir, "app.log"),
            os.path.join(self.temp_dir, "error.log"),
            os.path.join(self.temp_dir, "access.log")
        ]
        
        for log_file in log_files:
            with open(log_file, 'w') as f:
                f.write("Test log content")
        
        stats = self.rotator.get_log_stats()
        
        assert stats["total_files"] == 3
        assert stats["total_size_mb"] > 0
        assert len(stats["files"]) == 3
        
        for file_stat in stats["files"]:
            assert "name" in file_stat
            assert "size_mb" in file_stat
            assert "modified" in file_stat
    
    def test_setup_log_rotation(self):
        """Test log rotation setup function."""
        rotator = setup_log_rotation(self.temp_dir, max_size_mb=5, backup_count=2)
        
        assert isinstance(rotator, LogRotator)
        assert rotator.log_directory == self.temp_dir
        assert rotator.max_size_bytes == 5 * 1024 * 1024
        assert rotator.backup_count == 2

class TestStructuredLogger:
    """Test cases for structured logging functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "structured.log")
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_structured_logger_creation(self):
        """Test structured logger creation."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        assert logger.name == "test_logger"
        assert len(logger.logger.handlers) == 2  # Console and file handlers
    
    def test_log_levels(self):
        """Test all log levels."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        # Test each log level
        logger.debug("Debug message", test_field="debug_value")
        logger.info("Info message", test_field="info_value")
        logger.warning("Warning message", test_field="warning_value")
        logger.error("Error message", test_field="error_value")
        logger.critical("Critical message", test_field="critical_value")
        
        # Check that log file was created
        assert os.path.exists(self.log_file)
        
        # Read and verify log content
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 5
        
        # Verify JSON format
        for line in lines:
            log_entry = json.loads(line.strip())
            assert "timestamp" in log_entry
            assert "level" in log_entry
            assert "logger" in log_entry
            assert "message" in log_entry
            assert "test_field" in log_entry
    
    def test_log_user_action(self):
        """Test user action logging."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        logger.log_user_action("login", user_id="user123", ip="192.168.1.1")
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
        
        assert log_entry["action"] == "login"
        assert log_entry["user_id"] == "user123"
        assert log_entry["category"] == "user_action"
        assert log_entry["ip"] == "192.168.1.1"
    
    def test_log_system_event(self):
        """Test system event logging."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        logger.log_system_event("Application started", LogLevel.INFO, version="1.0.0")
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
        
        assert log_entry["event"] == "Application started"
        assert log_entry["level"] == "INFO"
        assert log_entry["category"] == "system_event"
        assert log_entry["version"] == "1.0.0"
    
    def test_log_performance(self):
        """Test performance logging."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        logger.log_performance("database_query", 1.234, rows=100, table="users")
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
        
        assert log_entry["operation"] == "database_query"
        assert log_entry["duration"] == 1.234
        assert log_entry["category"] == "performance"
        assert log_entry["rows"] == 100
        assert log_entry["table"] == "users"
    
    def test_log_security_event(self):
        """Test security event logging."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        logger.log_security_event("Failed login attempt", "high", ip="192.168.1.1", user="admin")
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
        
        assert log_entry["event"] == "Failed login attempt"
        assert log_entry["severity"] == "high"
        assert log_entry["category"] == "security"
        assert log_entry["ip"] == "192.168.1.1"
        assert log_entry["user"] == "admin"
    
    def test_log_business_event(self):
        """Test business event logging."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        logger.log_business_event("User registration", user_id="user123", plan="premium")
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
        
        assert log_entry["event"] == "User registration"
        assert log_entry["category"] == "business"
        assert log_entry["user_id"] == "user123"
        assert log_entry["plan"] == "premium"
    
    def test_get_structured_logger(self):
        """Test structured logger factory function."""
        logger = get_structured_logger("factory_logger", self.log_file)
        
        assert isinstance(logger, StructuredLogger)
        assert logger.name == "factory_logger"
    
    def test_json_serialization(self):
        """Test JSON serialization of complex objects."""
        logger = StructuredLogger("test_logger", self.log_file)
        
        # Test with complex data
        complex_data = {
            "user": {"id": 123, "name": "John Doe"},
            "metadata": {"source": "api", "version": "1.0"},
            "timestamp": datetime.now()
        }
        
        logger.info("Complex log entry", **complex_data)
        
        with open(self.log_file, 'r') as f:
            log_entry = json.loads(f.read().strip())
        
        assert "user" in log_entry
        assert "metadata" in log_entry
        assert log_entry["user"]["id"] == 123
        assert log_entry["metadata"]["source"] == "api"
