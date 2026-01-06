"""
Quick Test Script for Email Notification Module

This script allows you to test the email functionality by setting
credentials directly in the script (for testing only).

Instructions:
1. Replace 'your_email@gmail.com' with your Gmail address
2. Replace 'your_app_password' with your 16-character Gmail App Password
3. Replace 'recipient@example.com' with the email where you want to receive test emails
4. Run: py quick_test.py

Author: Cascade AI Assistant
Date: 2025-09-06
"""

from email_notifier import (
    EmailNotifier, 
    send_winner_notification,
    send_verification_email,
    send_otp_email,
    send_road_maintenance_update
)
import random
import string

def generate_otp(length=6):
    """Generate a random OTP code."""
    return ''.join(random.choices(string.digits, k=length))

def main():
    print("Email Notification Module - Quick Test")
    print("=" * 45)
    
    # CONFIGURE YOUR CREDENTIALS HERE
    # ================================
    SENDER_EMAIL = "aditya463615@gmail.com"  # Replace with your Gmail
    SENDER_APP_PASSWORD = "pjff uzdk lbjl hmuc"  # Replace with your 16-char App Password
    RECIPIENT_EMAIL = "gmdw34gxcm@ibolinva.com"  # Replace with test recipient
    
    # Check if credentials are configured
    if SENDER_EMAIL == "your_email@gmail.com" or SENDER_APP_PASSWORD == "your_app_password":
        print("ERROR: Please configure your credentials in the script first!")
        print("\nSteps to configure:")
        print("1. Open quick_test.py in your editor")
        print("2. Replace 'your_email@gmail.com' with your Gmail address")
        print("3. Replace 'your_app_password' with your Gmail App Password")
        print("4. Replace 'recipient@example.com' with test recipient email")
        print("\nTo get Gmail App Password:")
        print("1. Go to Google Account settings")
        print("2. Security > 2-Step Verification > App passwords")
        print("3. Generate password for 'Mail'")
        return
    
    # Initialize notifier
    notifier = EmailNotifier()
    notifier.configure_credentials(SENDER_EMAIL, SENDER_APP_PASSWORD)
    
    print(f"Sender: {SENDER_EMAIL}")
    print(f"Recipient: {RECIPIENT_EMAIL}")
    print("-" * 45)
    
    # Test 1: Winner Notification
    print("\n1. Testing Winner Notification...")
    success = send_winner_notification(
        notifier=notifier,
        recipient_email=RECIPIENT_EMAIL,
        winner_name="Test Winner",
        event_name="Email Module Test Contest",
        prize="Successfully Configured Email System",
        event_date="September 6, 2025"
    )
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Test 2: Verification Email
    print("\n2. Testing Verification Email...")
    success = send_verification_email(
        notifier=notifier,
        recipient_email=RECIPIENT_EMAIL,
        user_name="Test User",
        verification_link="https://example.com/verify?token=test123"
    )
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Test 3: OTP Email
    print("\n3. Testing OTP Email...")
    otp = generate_otp()
    success = send_otp_email(
        notifier=notifier,
        recipient_email=RECIPIENT_EMAIL,
        user_name="Test User",
        otp_code=otp,
        purpose="testing"
    )
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"   OTP Code: {otp}")
    
    # Test 4: Road Maintenance Report
    print("\n4. Testing Road Maintenance Report...")
    success = send_road_maintenance_update(
        notifier=notifier,
        recipient_email=RECIPIENT_EMAIL,
        citizen_name="Test Citizen",
        report_id="TEST-2025-001",
        issue_description="Test pothole report for email system verification",
        location="Test Street, Test City",
        status="in_progress",
        estimated_completion="September 10, 2025",
        assigned_team="Test Repair Team"
    )
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    
    print("\n" + "=" * 45)
    print("Test completed! Check your email inbox.")
    print("Note: Check spam folder if emails are not in inbox.")

if __name__ == "__main__":
    main()
