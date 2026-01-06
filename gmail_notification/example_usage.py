"""
Example Usage Script for Email Notification Module

This script demonstrates how to use the email_notifier module to send
various types of email notifications.

Before running this script:
1. Set up environment variables: EMAIL_ADDRESS and EMAIL_PASSWORD
2. For Gmail, use an App Password instead of your regular password
3. Install required dependencies: pip install -r requirements.txt

Author: Cascade AI Assistant
Date: 2025-09-06
"""

import os
import random
import string
from datetime import datetime, timedelta
from email_notifier import (
    EmailNotifier, 
    EmailTemplates,
    send_winner_notification,
    send_verification_email,
    send_otp_email,
    send_road_maintenance_update
)

def generate_otp(length: int = 6) -> str:
    """Generate a random OTP code."""
    return ''.join(random.choices(string.digits, k=length))

def generate_verification_link(user_id: str) -> str:
    """Generate a mock verification link."""
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return f"https://yourservice.com/verify?user={user_id}&token={token}"

def main():
    """
    Main function demonstrating various email notification scenarios.
    """
    print("🚀 Email Notification Module - Example Usage")
    print("=" * 50)
    
    # Initialize the email notifier
    notifier = EmailNotifier()
    
    # Option 1: Configure credentials directly (not recommended for production)
    # notifier.configure_credentials("your_email@gmail.com", "your_app_password")
    
    # Option 2: Configure from environment variables (recommended)
    try:
        notifier.configure_from_env()
        print("✅ Email credentials configured from environment variables")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n📝 Setup Instructions:")
        print("1. Set EMAIL_ADDRESS environment variable to your Gmail address")
        print("2. Set EMAIL_PASSWORD environment variable to your Gmail App Password")
        print("3. To create an App Password:")
        print("   - Go to Google Account settings")
        print("   - Security > 2-Step Verification > App passwords")
        print("   - Generate a new app password for 'Mail'")
        return
    
    # Get recipient email for testing
    recipient_email = input("\n📧 Enter recipient email address for testing: ").strip()
    if not recipient_email:
        print("❌ No recipient email provided. Exiting.")
        return
    
    print(f"\n📤 Sending test emails to: {recipient_email}")
    print("-" * 40)
    
    # Example 1: Event Winner Notification
    print("\n1️⃣ Sending Event Winner Notification...")
    success = send_winner_notification(
        notifier=notifier,
        recipient_email=recipient_email,
        winner_name="John Doe",
        event_name="Annual Photography Contest 2025",
        prize="First Place - $500 Cash Prize + Professional Camera",
        event_date="September 1, 2025"
    )
    print(f"   {'✅ Success' if success else '❌ Failed'}")
    
    # Example 2: Email Verification
    print("\n2️⃣ Sending Email Verification...")
    verification_link = generate_verification_link("user123")
    success = send_verification_email(
        notifier=notifier,
        recipient_email=recipient_email,
        user_name="Jane Smith",
        verification_link=verification_link
    )
    print(f"   {'✅ Success' if success else '❌ Failed'}")
    print(f"   🔗 Verification link: {verification_link}")
    
    # Example 3: OTP Email
    print("\n3️⃣ Sending OTP Email...")
    otp_code = generate_otp()
    success = send_otp_email(
        notifier=notifier,
        recipient_email=recipient_email,
        user_name="Alex Johnson",
        otp_code=otp_code,
        purpose="password reset"
    )
    print(f"   {'✅ Success' if success else '❌ Failed'}")
    print(f"   🔐 OTP Code: {otp_code}")
    
    # Example 4: Road Maintenance Report
    print("\n4️⃣ Sending Road Maintenance Report...")
    success = send_road_maintenance_update(
        notifier=notifier,
        recipient_email=recipient_email,
        citizen_name="Maria Garcia",
        report_id="RD-2025-001234",
        issue_description="Large pothole causing traffic disruption and vehicle damage",
        location="Main Street between 5th and 6th Avenue, near City Park",
        status="in_progress",
        estimated_completion="September 15, 2025",
        assigned_team="Road Repair Team Alpha"
    )
    print(f"   {'✅ Success' if success else '❌ Failed'}")
    
    # Example 5: Custom Email using Templates
    print("\n5️⃣ Sending Custom Template Email...")
    custom_html = EmailTemplates.get_base_template().format(
        title="🎯 Custom Notification",
        organization="Demo Organization",
        content="""
        <h2>This is a custom email!</h2>
        <p>You can create your own email content using the base template.</p>
        <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>✨ Features:</strong></p>
            <ul>
                <li>Professional HTML styling</li>
                <li>Responsive design</li>
                <li>Consistent branding</li>
                <li>Easy customization</li>
            </ul>
        </div>
        <p>This demonstrates the flexibility of the email notification system!</p>
        """,
        contact_email="demo@organization.com",
        year=datetime.now().year
    )
    
    success = notifier.send_email(
        recipient_email=recipient_email,
        subject="🎯 Custom Email Template Demo",
        html_content=custom_html
    )
    print(f"   {'✅ Success' if success else '❌ Failed'}")
    
    # Example 6: Bulk Email Sending
    print("\n6️⃣ Demonstrating Bulk Email (sending to same address multiple times)...")
    recipients = [recipient_email] * 3  # Send to same address 3 times for demo
    bulk_results = notifier.send_bulk_email(
        recipients=recipients,
        subject="📢 Bulk Email Test",
        html_content=EmailTemplates.get_base_template().format(
            title="Bulk Email Test",
            organization="Test Organization",
            content="<h2>This is a bulk email test!</h2><p>This email was sent as part of a bulk email demonstration.</p>",
            contact_email="test@organization.com",
            year=datetime.now().year
        )
    )
    
    successful_sends = sum(1 for success in bulk_results.values() if success)
    print(f"   📊 Bulk email results: {successful_sends}/{len(recipients)} successful")
    
    print("\n🎉 Email notification examples completed!")
    print("\n📋 Summary:")
    print("- Event winner notification")
    print("- Email verification") 
    print("- OTP authentication")
    print("- Road maintenance report")
    print("- Custom template email")
    print("- Bulk email sending")
    
    print(f"\n📧 Check {recipient_email} for the test emails!")

if __name__ == "__main__":
    main()
