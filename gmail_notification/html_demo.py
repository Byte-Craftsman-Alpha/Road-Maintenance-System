"""
HTML Template Demonstration

This script shows the actual HTML content that gets sent in emails,
so you can see the professional templates in action.

Author: Cascade AI Assistant
Date: 2025-09-06
"""

from email_notifier import EmailTemplates
from datetime import datetime

def save_html_samples():
    """Generate and save HTML samples of all email templates."""
    
    # 1. Winner Notification Template
    winner_html = EmailTemplates.event_winner_template(
        winner_name="John Doe",
        event_name="Annual Photography Contest 2025",
        prize="First Place - $500 Cash Prize + Professional Camera",
        event_date="September 1, 2025",
        organization="Photography Club International",
        contact_email="contests@photoclub.com"
    )
    
    with open("sample_winner_email.html", "w", encoding="utf-8") as f:
        f.write(winner_html)
    
    # 2. Verification Email Template
    verification_html = EmailTemplates.verification_email_template(
        user_name="Jane Smith",
        verification_link="https://yourservice.com/verify?token=abc123xyz789",
        organization="Your Service Platform",
        contact_email="support@yourservice.com"
    )
    
    with open("sample_verification_email.html", "w", encoding="utf-8") as f:
        f.write(verification_html)
    
    # 3. OTP Email Template
    otp_html = EmailTemplates.otp_email_template(
        user_name="Alex Johnson",
        otp_code="123456",
        purpose="password reset",
        organization="Secure Banking App",
        contact_email="security@securebank.com"
    )
    
    with open("sample_otp_email.html", "w", encoding="utf-8") as f:
        f.write(otp_html)
    
    # 4. Road Maintenance Report Template
    road_html = EmailTemplates.road_maintenance_report_template(
        citizen_name="Maria Garcia",
        report_id="RD-2025-001234",
        issue_description="Large pothole causing traffic disruption and vehicle damage",
        location="Main Street between 5th and 6th Avenue, near City Park",
        status="in_progress",
        estimated_completion="September 15, 2025",
        assigned_team="Road Repair Team Alpha",
        organization="City Road Maintenance Authority",
        contact_email="roads@cityauthority.gov"
    )
    
    with open("sample_road_maintenance_email.html", "w", encoding="utf-8") as f:
        f.write(road_html)
    
    # 5. Custom Template Example
    custom_html = EmailTemplates.get_base_template().format(
        title="🎯 Custom Business Notification",
        organization="Your Business",
        content="""
        <h2>Welcome to Our Premium Service!</h2>
        <p>Thank you for choosing our premium business solution. Here's what you get:</p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #007bff;">
            <h3 style="color: #007bff; margin-top: 0;">✨ Premium Features Activated:</h3>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>Advanced Analytics Dashboard</strong> - Real-time insights</li>
                <li><strong>Priority Customer Support</strong> - 24/7 assistance</li>
                <li><strong>Custom Integrations</strong> - API access included</li>
                <li><strong>Advanced Security</strong> - Enterprise-grade protection</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="https://yourbusiness.com/dashboard" class="button" style="background-color: #28a745;">
                Access Your Dashboard
            </a>
        </div>
        
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>🚀 Getting Started:</strong></p>
            <ol>
                <li>Log into your dashboard using the link above</li>
                <li>Complete your profile setup</li>
                <li>Explore the new premium features</li>
                <li>Contact support if you need assistance</li>
            </ol>
        </div>
        
        <p>We're excited to have you as a premium member and look forward to helping your business grow!</p>
        """,
        contact_email="support@yourbusiness.com",
        year=datetime.now().year
    )
    
    with open("sample_custom_email.html", "w", encoding="utf-8") as f:
        f.write(custom_html)
    
    print("HTML Email Samples Generated!")
    print("=" * 40)
    print("Files created:")
    print("- sample_winner_email.html")
    print("- sample_verification_email.html") 
    print("- sample_otp_email.html")
    print("- sample_road_maintenance_email.html")
    print("- sample_custom_email.html")
    print("\nOpen these files in your browser to see the beautiful HTML templates!")

def show_template_features():
    """Display the features of the HTML templates."""
    print("\nHTML Template Features:")
    print("=" * 40)
    print("- Professional responsive design")
    print("- Modern CSS styling with gradients and shadows")
    print("- Mobile-friendly responsive layout")
    print("- Consistent branding across all templates")
    print("- Color-coded status indicators")
    print("- Interactive buttons with hover effects")
    print("- Professional typography (Segoe UI font family)")
    print("- Structured layouts with proper spacing")
    print("- Security warnings and important notices")
    print("- Footer with contact information and copyright")
    
    print("\nTemplate Types Available:")
    print("=" * 40)
    print("1. Event Winner Notifications")
    print("   - Prize details with highlighting")
    print("   - Event information in structured format")
    print("   - Call-to-action for prize claiming")
    
    print("\n2. Email Verification")
    print("   - Secure verification buttons")
    print("   - Expiration warnings")
    print("   - Security best practices")
    
    print("\n3. OTP Authentication")
    print("   - Large, prominent OTP display")
    print("   - Security warnings and expiration info")
    print("   - Professional security styling")
    
    print("\n4. Road Maintenance Reports")
    print("   - Detailed report tables")
    print("   - Status indicators with colors")
    print("   - Government authority branding")
    
    print("\n5. Custom Templates")
    print("   - Flexible base template system")
    print("   - Easy customization options")
    print("   - Consistent styling framework")

if __name__ == "__main__":
    print("HTML Email Template Demonstration")
    print("=" * 50)
    
    # Generate sample HTML files
    save_html_samples()
    
    # Show template features
    show_template_features()
    
    print(f"\n📁 Files saved in: {__file__.replace('html_demo.py', '')}")
    print("🌐 Open the .html files in your web browser to preview!")
