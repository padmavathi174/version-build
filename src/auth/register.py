"""
User registration functionality for the version-build project.
"""

from ..utils import hash_password, validate_username, validate_email

# In-memory user storage (in a real app, use a database)
USERS = {
    "admin": {
        "password": hash_password("admin123"),
        "email": "admin@example.com",
        "role": "admin"
    },
    "user1": {
        "password": hash_password("password123"),
        "email": "user1@example.com",
        "role": "user"
    }
}

def register(username, email, password):
    """
    Register a new user.
    
    Args:
        username (str): Username
        email (str): Email address
        password (str): Password
        
    Returns:
        dict: Registration result with status and message
    """
    # Validate input
    if not username or not email or not password:
        return {
            "status": "error",
            "message": "Username, email, and password are required"
        }
    
    # Validate username format
    if not validate_username(username):
        return {
            "status": "error",
            "message": "Username must be 3-20 characters, alphanumeric and underscores only"
        }
    
    # Validate email format
    if not validate_email(email):
        return {
            "status": "error",
            "message": "Invalid email format"
        }
    
    # Check password length
    if len(password) < 8:
        return {
            "status": "error",
            "message": "Password must be at least 8 characters long"
        }
    
    # Check if user already exists
    if username in USERS:
        return {
            "status": "error",
            "message": "Username already exists"
        }
    
    # Check if email already exists
    for user_data in USERS.values():
        if user_data.get("email") == email:
            return {
                "status": "error",
                "message": "Email already registered"
            }
    
    # Register new user
    USERS[username] = {
        "password": hash_password(password),
        "email": email,
        "role": "user"
    }
    
    return {
        "status": "success",
        "message": f"User {username} registered successfully",
        "user": {
            "username": username,
            "email": email,
            "role": "user"
        }
    }

def check_username_availability(username):
    """
    Check if username is available.
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if available, False if taken
    """
    return username not in USERS

def check_email_availability(email):
    """
    Check if email is available.
    
    Args:
        email (str): Email to check
        
    Returns:
        bool: True if available, False if taken
    """
    for user_data in USERS.values():
        if user_data.get("email") == email:
            return False
    return True
