#!/usr/bin/env python3
"""
Main application entry point for the version-build project.
This demonstrates a simple application with authentication and logging.
"""

import sys
import os
from src.auth.login import login, logout
from src.auth.register import register
from src.logging.logger import setup_logger, log_user_action

def main():
    """Main application function."""
    # Set up logging
    logger = setup_logger('main_app', 'logs/app.log')
    logger.info("Application started")
    
    print("Welcome to Version Build Project!")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Register")
        print("3. Logout")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            
            result = login(username, password)
            print(f"Login result: {result['message']}")
            
            if result['status'] == 'success':
                log_user_action("login", username)
            
        elif choice == "2":
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            
            result = register(username, email, password)
            print(f"Registration result: {result['message']}")
            
            if result['status'] == 'success':
                log_user_action("register", username)
                
        elif choice == "3":
            result = logout()
            print(f"Logout result: {result['message']}")
            log_user_action("logout")
            
        elif choice == "4":
            logger.info("Application shutting down")
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
