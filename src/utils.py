"""
Utility functions for the version-build project.
"""

import hashlib
import re
from datetime import datetime

def hash_password(password):
    """
    Hash a password using SHA-256.
    In a real application, use bcrypt or similar.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """
    Validate email format using regex.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """
    Validate username format.
    Username should be 3-20 characters, alphanumeric and underscores only.
    """
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def get_current_timestamp():
    """
    Get current timestamp as string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_user_data(username, email, timestamp=None):
    """
    Format user data for display.
    """
    if timestamp is None:
        timestamp = get_current_timestamp()
    
    return {
        'username': username,
        'email': email,
        'created_at': timestamp
    }
