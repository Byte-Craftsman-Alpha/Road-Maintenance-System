"""
Configuration file for Email Notification Module

This file contains configuration settings and helper functions
for the email notification system.

Author: Cascade AI Assistant
Date: 2025-09-06
"""

import os
from typing import Dict, Any

class EmailConfig:
    """
    Configuration class for email settings.
    """
    
    # SMTP Settings
    GMAIL_SMTP_SERVER = "smtp.gmail.com"
    GMAIL_SMTP_PORT = 587
    
    # Other popular SMTP servers
    SMTP_SERVERS = {
        'gmail': {'server': 'smtp.gmail.com', 'port': 587},
        'outlook': {'server': 'smtp-mail.outlook.com', 'port': 587},
        'yahoo': {'server': 'smtp.mail.yahoo.com', 'port': 587},
        'hotmail': {'server': 'smtp-mail.outlook.com', 'port': 587},
        'icloud': {'server': 'smtp.mail.me.com', 'port': 587},
    }
    
    # Default organization settings
    DEFAULT_ORGANIZATION = "Your Organization"
    DEFAULT_CONTACT_EMAIL = "contact@yourorganization.com"
    
    # Email template settings
    MAX_SUBJECT_LENGTH = 78  # RFC 2822 recommendation
    MAX_EMAIL_SIZE = 25 * 1024 * 1024  # 25MB limit for most email providers
    
    # OTP settings
    DEFAULT_OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    
    # Verification link settings
    VERIFICATION_LINK_EXPIRY_HOURS = 24
    
    @classmethod
    def get_smtp_config(cls, provider: str) -> Dict[str, Any]:
        """
        Get SMTP configuration for a specific email provider.
        
        Args:
            provider (str): Email provider name
            
        Returns:
            Dict[str, Any]: SMTP configuration
        """
        return cls.SMTP_SERVERS.get(provider.lower(), cls.SMTP_SERVERS['gmail'])
    
    @classmethod
    def validate_email_credentials(cls) -> bool:
        """
        Validate that required environment variables are set.
        
        Returns:
            bool: True if credentials are available
        """
        return bool(os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'))
    
    @classmethod
    def get_credentials(cls) -> tuple:
        """
        Get email credentials from environment variables.
        
        Returns:
            tuple: (email, password) or (None, None) if not available
        """
        return (os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))


class TemplateConfig:
    """
    Configuration for email templates.
    """
    
    # Color schemes for different email types
    COLOR_SCHEMES = {
        'success': {'primary': '#27ae60', 'secondary': '#2ecc71', 'background': '#d5f4e6'},
        'warning': {'primary': '#f39c12', 'secondary': '#e67e22', 'background': '#fff3cd'},
        'error': {'primary': '#e74c3c', 'secondary': '#c0392b', 'background': '#f8d7da'},
        'info': {'primary': '#3498db', 'secondary': '#2980b9', 'background': '#d1ecf1'},
        'neutral': {'primary': '#95a5a6', 'secondary': '#7f8c8d', 'background': '#ecf0f1'},
    }
    
    # Status colors for road maintenance
    ROAD_STATUS_COLORS = {
        'received': '#f39c12',
        'in_progress': '#3498db',
        'completed': '#27ae60',
        'on_hold': '#e74c3c',
        'cancelled': '#95a5a6'
    }
    
    # Default template variables
    DEFAULT_VARS = {
        'organization': EmailConfig.DEFAULT_ORGANIZATION,
        'contact_email': EmailConfig.DEFAULT_CONTACT_EMAIL,
        'year': 2025
    }


# Environment setup helper
def setup_environment():
    """
    Helper function to set up environment variables for testing.
    This should only be used for development/testing purposes.
    """
    print("Email Notification Module Setup")
    print("=" * 40)
    print("For Gmail, you need to use an App Password instead of your regular password.")
    print("\nSteps to create Gmail App Password:")
    print("1. Go to your Google Account settings")
    print("2. Navigate to Security > 2-Step Verification")
    print("3. Scroll down to 'App passwords'")
    print("4. Select 'Mail' and generate a password")
    print("5. Use this 16-character password in EMAIL_PASSWORD")
    
    email = input("\nEnter your Gmail address: ").strip()
    password = input("Enter your Gmail App Password: ").strip()
    
    if email and password:
        os.environ['EMAIL_ADDRESS'] = email
        os.environ['EMAIL_PASSWORD'] = password
        print("Environment variables set successfully!")
        return True
    else:
        print("Invalid credentials provided.")
        return False


if __name__ == "__main__":
    # Run setup if this file is executed directly
    setup_environment()
