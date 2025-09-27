"""
Authentication module for the version-build project.
"""

from .login import login, logout
from .register import register

__all__ = ['login', 'logout', 'register']
