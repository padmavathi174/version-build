"""
Structured logging functionality for the version-build project.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StructuredLogger:
    """Structured logger that outputs JSON formatted logs."""
    
    def __init__(self, name: str, log_file: str = None):
        """
        Initialize structured logger.
        
        Args:
            name (str): Logger name
            log_file (str, optional): Log file path
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)
    
    def _format_log(self, level: str, message: str, **kwargs) -> str:
        """
        Format log entry as JSON.
        
        Args:
            level (str): Log level
            message (str): Log message
            **kwargs: Additional fields
            
        Returns:
            str: JSON formatted log entry
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "logger": self.name,
            "message": message,
            **kwargs
        }
        
        return json.dumps(log_entry, default=str)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        formatted = self._format_log("DEBUG", message, **kwargs)
        self.logger.debug(formatted)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        formatted = self._format_log("INFO", message, **kwargs)
        self.logger.info(formatted)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        formatted = self._format_log("WARNING", message, **kwargs)
        self.logger.warning(formatted)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        formatted = self._format_log("ERROR", message, **kwargs)
        self.logger.error(formatted)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        formatted = self._format_log("CRITICAL", message, **kwargs)
        self.logger.critical(formatted)
    
    def log_user_action(self, action: str, user_id: Optional[str] = None, **kwargs):
        """
        Log user action with structured data.
        
        Args:
            action (str): Action performed
            user_id (str, optional): User identifier
            **kwargs: Additional context
        """
        self.info(f"User action: {action}", 
                 action=action, 
                 user_id=user_id, 
                 category="user_action",
                 **kwargs)
    
    def log_system_event(self, event: str, level: LogLevel = LogLevel.INFO, **kwargs):
        """
        Log system event with structured data.
        
        Args:
            event (str): Event description
            level (LogLevel): Log level
            **kwargs: Additional context
        """
        log_method = getattr(self, level.value.lower())
        log_method(f"System event: {event}", 
                  event=event, 
                  category="system_event",
                  **kwargs)
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """
        Log performance metrics with structured data.
        
        Args:
            operation (str): Operation name
            duration (float): Duration in seconds
            **kwargs: Additional metrics
        """
        self.info(f"Performance: {operation} took {duration:.3f}s",
                 operation=operation,
                 duration=duration,
                 category="performance",
                 **kwargs)
    
    def log_security_event(self, event: str, severity: str = "medium", **kwargs):
        """
        Log security event with structured data.
        
        Args:
            event (str): Security event description
            severity (str): Event severity (low, medium, high, critical)
            **kwargs: Additional context
        """
        self.warning(f"Security event: {event}",
                    event=event,
                    severity=severity,
                    category="security",
                    **kwargs)
    
    def log_business_event(self, event: str, **kwargs):
        """
        Log business event with structured data.
        
        Args:
            event (str): Business event description
            **kwargs: Additional context
        """
        self.info(f"Business event: {event}",
                 event=event,
                 category="business",
                 **kwargs)

def get_structured_logger(name: str, log_file: str = None) -> StructuredLogger:
    """
    Get or create structured logger instance.
    
    Args:
        name (str): Logger name
        log_file (str, optional): Log file path
        
    Returns:
        StructuredLogger: Logger instance
    """
    return StructuredLogger(name, log_file)
