"""
Comprehensive logging system for the version-build project.
"""

import logging
import os
from datetime import datetime
from typing import Optional

# Global logger instances
_loggers = {}

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up logger with file and console handlers.
    
    Args:
        name (str): Logger name
        log_file (str): Log file path
        level (int): Logging level
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Return existing logger if already configured
    if name in _loggers:
        return _loggers[name]
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        _loggers[name] = logger
        return logger
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Store logger instance
    _loggers[name] = logger
    
    return logger

def get_logger(name: str) -> Optional[logging.Logger]:
    """
    Get existing logger instance.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger or None: Logger instance if exists
    """
    return _loggers.get(name)

def log_user_action(action: str, user_id: Optional[str] = None, details: Optional[dict] = None):
    """
    Log user actions with structured format.
    
    Args:
        action (str): Action performed
        user_id (str, optional): User identifier
        details (dict, optional): Additional details
    """
    logger = setup_logger('user_actions', 'logs/user_actions.log')
    
    # Create log message
    message = f"User action: {action}"
    if user_id:
        message += f" (User ID: {user_id})"
    
    if details:
        message += f" | Details: {details}"
    
    logger.info(message)

def log_system_event(event: str, level: str = "INFO", details: Optional[dict] = None):
    """
    Log system events.
    
    Args:
        event (str): Event description
        level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        details (dict, optional): Additional details
    """
    logger = setup_logger('system', 'logs/system.log')
    
    message = f"System event: {event}"
    if details:
        message += f" | Details: {details}"
    
    # Log with appropriate level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.log(log_level, message)

def log_error(error: Exception, context: Optional[str] = None):
    """
    Log errors with context.
    
    Args:
        error (Exception): Error instance
        context (str, optional): Additional context
    """
    logger = setup_logger('errors', 'logs/errors.log')
    
    message = f"Error occurred: {str(error)}"
    if context:
        message += f" | Context: {context}"
    
    logger.error(message, exc_info=True)

def log_performance(operation: str, duration: float, details: Optional[dict] = None):
    """
    Log performance metrics.
    
    Args:
        operation (str): Operation name
        duration (float): Duration in seconds
        details (dict, optional): Additional details
    """
    logger = setup_logger('performance', 'logs/performance.log')
    
    message = f"Performance: {operation} took {duration:.3f}s"
    if details:
        message += f" | Details: {details}"
    
    logger.info(message)

def cleanup_old_logs(log_directory: str = "logs", days_to_keep: int = 30):
    """
    Clean up old log files.
    
    Args:
        log_directory (str): Log directory path
        days_to_keep (int): Number of days to keep logs
    """
    import glob
    import time
    
    if not os.path.exists(log_directory):
        return
    
    current_time = time.time()
    cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
    
    # Find all log files
    log_files = glob.glob(os.path.join(log_directory, "*.log*"))
    
    for log_file in log_files:
        if os.path.getmtime(log_file) < cutoff_time:
            try:
                os.remove(log_file)
                print(f"Removed old log file: {log_file}")
            except OSError as e:
                print(f"Error removing {log_file}: {e}")
