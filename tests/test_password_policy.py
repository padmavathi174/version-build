"""
Test cases for password policy module.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.auth.password_policy import PasswordPolicy, validate_password_strength

class TestPasswordPolicy:
    """Test cases for password policy functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.policy = PasswordPolicy()
    
    def test_strong_password(self):
        """Test validation of strong password."""
        result = self.policy.validate_password("StrongP@ssw0rd123")
        
        assert result["is_valid"] == True
        assert len(result["errors"]) == 0
        assert result["strength_score"] > 70
    
    def test_weak_password_short(self):
        """Test validation of short password."""
        result = self.policy.validate_password("weak")
        
        assert result["is_valid"] == False
        assert "at least 8 characters" in result["errors"][0]
    
    def test_weak_password_no_uppercase(self):
        """Test validation of password without uppercase."""
        result = self.policy.validate_password("weakpassword123")
        
        assert result["is_valid"] == False
        assert "uppercase letter" in result["errors"][0]
    
    def test_weak_password_no_lowercase(self):
        """Test validation of password without lowercase."""
        result = self.policy.validate_password("WEAKPASSWORD123")
        
        assert result["is_valid"] == False
        assert "lowercase letter" in result["errors"][0]
    
    def test_weak_password_no_digits(self):
        """Test validation of password without digits."""
        result = self.policy.validate_password("WeakPassword")
        
        assert result["is_valid"] == False
        assert "digit" in result["errors"][0]
    
    def test_weak_password_no_special_chars(self):
        """Test validation of password without special characters."""
        result = self.policy.validate_password("WeakPassword123")
        
        assert result["is_valid"] == False
        assert "special character" in result["errors"][0]
    
    def test_common_patterns_detection(self):
        """Test detection of common weak patterns."""
        result = self.policy.validate_password("password123")
        
        assert "common patterns" in result["warnings"][0]
    
    def test_repeated_chars_detection(self):
        """Test detection of repeated characters."""
        result = self.policy.validate_password("aaabbb123")
        
        assert "repeated characters" in result["warnings"][0]
    
    def test_strength_score_calculation(self):
        """Test password strength score calculation."""
        # Very weak password
        weak_result = self.policy.validate_password("weak")
        assert weak_result["strength_score"] < 30
        
        # Strong password
        strong_result = self.policy.validate_password("StrongP@ssw0rd123")
        assert strong_result["strength_score"] > 70
    
    def test_strength_description(self):
        """Test strength description mapping."""
        assert self.policy.get_strength_description(20) == "Very Weak"
        assert self.policy.get_strength_description(40) == "Weak"
        assert self.policy.get_strength_description(60) == "Fair"
        assert self.policy.get_strength_description(80) == "Good"
        assert self.policy.get_strength_description(95) == "Strong"
    
    def test_validate_password_strength_function(self):
        """Test convenience function."""
        result = validate_password_strength("TestP@ssw0rd123")
        
        assert "is_valid" in result
        assert "errors" in result
        assert "warnings" in result
        assert "strength_score" in result
    
    def test_multiple_errors(self):
        """Test password with multiple validation errors."""
        result = self.policy.validate_password("weak")
        
        assert result["is_valid"] == False
        assert len(result["errors"]) > 1
    
    def test_edge_case_empty_password(self):
        """Test empty password."""
        result = self.policy.validate_password("")
        
        assert result["is_valid"] == False
        assert "at least 8 characters" in result["errors"][0]
    
    def test_edge_case_very_long_password(self):
        """Test very long password."""
        long_password = "A" * 1000 + "1" + "a" + "!"
        result = self.policy.validate_password(long_password)
        
        assert result["is_valid"] == True
        assert result["strength_score"] > 80
