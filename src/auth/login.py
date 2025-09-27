"""
User login functionality for the version-build project.
"""

from ..utils import hash_password, validate_username

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

def login(username, password):
    """
    Authenticate user with username and password.
    
    Args:
        username (str): Username
        password (str): Password
        
    Returns:
        dict: Authentication result with status and message
    """
    # Validate input
    if not username or not password:
        return {
            "status": "error",
            "message": "Username and password are required"
        }
    
    # Validate username format
    if not validate_username(username):
        return {
            "status": "error",
            "message": "Invalid username format"
        }
    
    # Check if user exists
    if username not in USERS:
        return {
            "status": "error",
            "message": "Invalid username or password"
        }
    
    # Verify password
    hashed_password = hash_password(password)
    if USERS[username]["password"] != hashed_password:
        return {
            "status": "error",
            "message": "Invalid username or password"
        }
    
    return {
        "status": "success",
        "message": f"Login successful for user: {username}",
        "user": {
            "username": username,
            "email": USERS[username]["email"],
            "role": USERS[username]["role"]
        }
    }

def logout():
    """
    Logout current user.
    
    Returns:
        dict: Logout result with status and message
    """
    return {
        "status": "success",
        "message": "Logged out successfully"
    }

def get_user_info(username):
    """
    Get user information by username.
    
    Args:
        username (str): Username
        
    Returns:
        dict: User information or None if not found
    """
    if username in USERS:
        user_data = USERS[username].copy()
        user_data.pop("password", None)  # Remove password from response
        user_data["username"] = username
        return user_data
    return None
