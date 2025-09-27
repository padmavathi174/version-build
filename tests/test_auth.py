"""
Test cases for authentication module.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.auth.login import login, logout
from src.auth.register import register, check_username_availability, check_email_availability
from src.utils import validate_email, validate_username, hash_password

class TestLogin:
    """Test cases for login functionality."""
    
    def test_successful_login(self):
        """Test successful login with valid credentials."""
        result = login("admin", "admin123")
        assert result["status"] == "success"
        assert "Login successful" in result["message"]
        assert "user" in result
    
    def test_invalid_username(self):
        """Test login with invalid username."""
        result = login("nonexistent", "password")
        assert result["status"] == "error"
        assert "Invalid username or password" in result["message"]
    
    def test_invalid_password(self):
        """Test login with invalid password."""
        result = login("admin", "wrongpassword")
        assert result["status"] == "error"
        assert "Invalid username or password" in result["message"]
    
    def test_empty_credentials(self):
        """Test login with empty credentials."""
        result = login("", "")
        assert result["status"] == "error"
        assert "Username and password are required" in result["message"]
    
    def test_invalid_username_format(self):
        """Test login with invalid username format."""
        result = login("ab", "password")  # Too short
        assert result["status"] == "error"
        assert "Invalid username format" in result["message"]
    
    def test_logout(self):
        """Test logout functionality."""
        result = logout()
        assert result["status"] == "success"
        assert "Logged out successfully" in result["message"]

class TestRegister:
    """Test cases for registration functionality."""
    
    def test_successful_registration(self):
        """Test successful user registration."""
        result = register("newuser", "newuser@example.com", "password123")
        assert result["status"] == "success"
        assert "registered successfully" in result["message"]
        assert "user" in result
    
    def test_duplicate_username(self):
        """Test registration with duplicate username."""
        result = register("admin", "newemail@example.com", "password123")
        assert result["status"] == "error"
        assert "Username already exists" in result["message"]
    
    def test_duplicate_email(self):
        """Test registration with duplicate email."""
        result = register("newuser2", "admin@example.com", "password123")
        assert result["status"] == "error"
        assert "Email already registered" in result["message"]
    
    def test_invalid_email_format(self):
        """Test registration with invalid email format."""
        result = register("newuser3", "invalid-email", "password123")
        assert result["status"] == "error"
        assert "Invalid email format" in result["message"]
    
    def test_short_password(self):
        """Test registration with short password."""
        result = register("newuser4", "newuser4@example.com", "123")
        assert result["status"] == "error"
        assert "Password must be at least 8 characters long" in result["message"]
    
    def test_missing_fields(self):
        """Test registration with missing fields."""
        result = register("", "", "")
        assert result["status"] == "error"
        assert "Username, email, and password are required" in result["message"]
    
    def test_username_availability(self):
        """Test username availability check."""
        assert check_username_availability("admin") == False
        assert check_username_availability("availableuser") == True
    
    def test_email_availability(self):
        """Test email availability check."""
        assert check_email_availability("admin@example.com") == False
        assert check_email_availability("available@example.com") == True

class TestUtils:
    """Test cases for utility functions."""
    
    def test_validate_email(self):
        """Test email validation."""
        assert validate_email("test@example.com") == True
        assert validate_email("user.name@domain.co.uk") == True
        assert validate_email("invalid-email") == False
        assert validate_email("") == False
    
    def test_validate_username(self):
        """Test username validation."""
        assert validate_username("validuser") == True
        assert validate_username("user123") == True
        assert validate_username("user_name") == True
        assert validate_username("ab") == False  # Too short
        assert validate_username("a" * 21) == False  # Too long
        assert validate_username("user-name") == False  # Invalid character
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Same password should produce same hash
        assert hash1 == hash2
        
        # Hash should be different from original password
        assert hash1 != password
        
        # Different password should produce different hash
        hash3 = hash_password("differentpassword")
        assert hash1 != hash3
