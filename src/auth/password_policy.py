"""
Password policy enforcement for the version-build project.
"""

import re
from typing import List, Dict

class PasswordPolicy:
    """Password policy enforcement class."""
    
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special_chars = True
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def validate_password(self, password: str) -> Dict[str, any]:
        """
        Validate password against policy.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Dict: Validation result with status and details
        """
        errors = []
        warnings = []
        
        # Check minimum length
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        # Check for uppercase letters
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        # Check for lowercase letters
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        # Check for digits
        if self.require_digits and not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        # Check for special characters
        if self.require_special_chars:
            special_pattern = f"[{re.escape(self.special_chars)}]"
            if not re.search(special_pattern, password):
                errors.append(f"Password must contain at least one special character: {self.special_chars}")
        
        # Check for common patterns
        if self._has_common_patterns(password):
            warnings.append("Password contains common patterns that may be weak")
        
        # Check for repeated characters
        if self._has_repeated_chars(password):
            warnings.append("Password contains repeated characters")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "strength_score": self._calculate_strength_score(password)
        }
    
    def _has_common_patterns(self, password: str) -> bool:
        """Check for common weak patterns."""
        common_patterns = [
            r'123',  # Sequential numbers
            r'abc',  # Sequential letters
            r'qwerty',  # Keyboard patterns
            r'password',  # Common words
            r'admin',  # Common words
        ]
        
        password_lower = password.lower()
        for pattern in common_patterns:
            if re.search(pattern, password_lower):
                return True
        return False
    
    def _has_repeated_chars(self, password: str) -> bool:
        """Check for repeated characters."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def _calculate_strength_score(self, password: str) -> int:
        """Calculate password strength score (0-100)."""
        score = 0
        
        # Length bonus
        score += min(len(password) * 2, 40)
        
        # Character variety bonus
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(f'[{re.escape(self.special_chars)}]', password):
            score += 10
        
        # Penalty for common patterns
        if self._has_common_patterns(password):
            score -= 20
        
        # Penalty for repeated characters
        if self._has_repeated_chars(password):
            score -= 10
        
        return max(0, min(100, score))
    
    def get_strength_description(self, score: int) -> str:
        """Get human-readable strength description."""
        if score < 30:
            return "Very Weak"
        elif score < 50:
            return "Weak"
        elif score < 70:
            return "Fair"
        elif score < 90:
            return "Good"
        else:
            return "Strong"

def validate_password_strength(password: str) -> Dict[str, any]:
    """
    Convenience function to validate password strength.
    
    Args:
        password (str): Password to validate
        
    Returns:
        Dict: Validation result
    """
    policy = PasswordPolicy()
    return policy.validate_password(password)
