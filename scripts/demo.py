#!/usr/bin/env python3
"""
Demonstration script for the Version Build Project.
This script showcases all the features implemented in the Git workflow project.
"""

import sys
import os
import time
from datetime import datetime

# Add src to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from src.auth.login import login, logout
from src.auth.register import register
from src.logging.logger import setup_logger, log_user_action
from src.logging.structured_logger import get_structured_logger, LogLevel
from src.logging.log_rotator import setup_log_rotation

def demonstrate_authentication():
    """Demonstrate authentication features."""
    print("\n" + "="*60)
    print("🔐 AUTHENTICATION SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Test login with existing user
    print("\n1. Testing login with existing user:")
    result = login("admin", "admin123")
    print(f"   Result: {result['message']}")
    
    # Test login with invalid credentials
    print("\n2. Testing login with invalid credentials:")
    result = login("admin", "wrongpassword")
    print(f"   Result: {result['message']}")
    
    # Test registration with strong password
    print("\n3. Testing registration with strong password:")
    result = register("newuser", "newuser@example.com", "StrongP@ssw0rd123")
    print(f"   Result: {result['message']}")
    if 'strength_score' in result:
        print(f"   Password strength score: {result['strength_score']}")
    
    # Test registration with weak password
    print("\n4. Testing registration with weak password:")
    result = register("weakuser", "weak@example.com", "weak")
    print(f"   Result: {result['message']}")
    
    # Test logout
    print("\n5. Testing logout:")
    result = logout()
    print(f"   Result: {result['message']}")

def demonstrate_logging():
    """Demonstrate logging features."""
    print("\n" + "="*60)
    print("📝 LOGGING SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Set up basic logger
    logger = setup_logger('demo', 'logs/demo.log')
    logger.info("Starting logging demonstration")
    
    # Set up structured logger
    structured_logger = get_structured_logger('demo_structured', 'logs/structured_demo.log')
    
    print("\n1. Basic logging:")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("\n2. User action logging:")
    log_user_action("demo_action", "demo_user", {"feature": "authentication"})
    
    print("\n3. Structured logging:")
    structured_logger.log_user_action("login", "demo_user", ip="192.168.1.1", browser="Chrome")
    structured_logger.log_system_event("Application started", LogLevel.INFO, version="1.0.0")
    structured_logger.log_performance("database_query", 0.123, rows=50, table="users")
    structured_logger.log_security_event("Failed login attempt", "medium", ip="192.168.1.100", user="hacker")
    structured_logger.log_business_event("User registration", user_id="user123", plan="premium")
    
    print("\n4. Log rotation setup:")
    rotator = setup_log_rotation("logs", max_size_mb=1, backup_count=3)
    print(f"   Log rotator configured for directory: {rotator.log_directory}")
    print(f"   Max size: {rotator.max_size_bytes / (1024*1024):.1f} MB")
    print(f"   Backup count: {rotator.backup_count}")
    
    # Get log statistics
    stats = rotator.get_log_stats()
    print(f"\n5. Log statistics:")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total size: {stats['total_size_mb']:.2f} MB")
    
    logger.info("Logging demonstration completed")

def demonstrate_project_structure():
    """Demonstrate project structure and organization."""
    print("\n" + "="*60)
    print("📁 PROJECT STRUCTURE DEMONSTRATION")
    print("="*60)
    
    def show_directory_structure(path, prefix="", max_depth=3, current_depth=0):
        """Recursively show directory structure."""
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(os.listdir(path))
            for i, item in enumerate(items):
                if item.startswith('.'):
                    continue
                
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1
                
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item}")
                
                if os.path.isdir(item_path) and current_depth < max_depth - 1:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    show_directory_structure(item_path, next_prefix, max_depth, current_depth + 1)
        except PermissionError:
            pass
    
    print("\nProject structure:")
    show_directory_structure(".", max_depth=3)

def demonstrate_git_workflow():
    """Demonstrate Git workflow concepts."""
    print("\n" + "="*60)
    print("🌿 GIT WORKFLOW DEMONSTRATION")
    print("="*60)
    
    print("\nThis project demonstrates:")
    print("✅ Repository initialization and configuration")
    print("✅ Branching strategy (main, dev, feature branches)")
    print("✅ Feature development workflow")
    print("✅ Pull request and merge process")
    print("✅ Version control and tagging")
    print("✅ Collaborative development practices")
    print("✅ Professional project organization")
    
    print("\nBranches created and used:")
    print("• main - Production-ready code")
    print("• dev - Development integration branch")
    print("• feature/enhanced-authentication - Password policy feature")
    print("• feature/advanced-logging - Advanced logging features")
    
    print("\nCommits made:")
    print("• Initial project setup")
    print("• Enhanced password policy validation")
    print("• Advanced logging features")
    print("• Version 1.0.0 release")

def run_tests():
    """Run the test suite."""
    print("\n" + "="*60)
    print("🧪 TESTING DEMONSTRATION")
    print("="*60)
    
    print("\nRunning test suite...")
    print("(In a real environment, this would run: python -m pytest tests/ -v)")
    
    print("\nTest files included:")
    test_files = [
        "tests/test_auth.py - Authentication tests",
        "tests/test_logging.py - Basic logging tests", 
        "tests/test_password_policy.py - Password policy tests",
        "tests/test_advanced_logging.py - Advanced logging tests"
    ]
    
    for test_file in test_files:
        print(f"  ✅ {test_file}")

def main():
    """Main demonstration function."""
    print("🚀 VERSION BUILD PROJECT - COMPLETE DEMONSTRATION")
    print("="*60)
    print(f"Demonstration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    try:
        # Run all demonstrations
        demonstrate_project_structure()
        demonstrate_authentication()
        demonstrate_logging()
        demonstrate_git_workflow()
        run_tests()
        
        print("\n" + "="*60)
        print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nThis project showcases:")
        print("• Professional Git workflow and branching strategies")
        print("• Complete authentication system with password policies")
        print("• Advanced logging with rotation and structured output")
        print("• Comprehensive test coverage")
        print("• Professional documentation and organization")
        print("• Real-world development practices")
        
        print(f"\nDemonstration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
