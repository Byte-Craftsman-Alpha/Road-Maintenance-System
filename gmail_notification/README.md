# Email Notification Module 📧

A comprehensive Python module for sending email notifications through SMTP and Gmail with beautiful HTML templates for various use cases including event notifications, verification emails, OTP emails, and road maintenance reports.

## Features ✨

- **Gmail SMTP Integration**: Easy setup with Gmail using App Passwords
- **Multiple Email Templates**: Pre-built templates for common use cases
- **Professional HTML Design**: Beautiful, responsive email templates
- **Bulk Email Support**: Send emails to multiple recipients
- **Security Best Practices**: Environment variable configuration
- **Comprehensive Logging**: Built-in logging for debugging
- **Flexible Configuration**: Support for multiple SMTP providers

## Quick Start 🚀

### 1. Installation

```bash
# Clone or download the module
cd mail_notificationModule

# Install dependencies
pip install -r requirements.txt
```

### 2. Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security → 2-Step Verification
3. Scroll down to "App passwords"
4. Generate an app password for "Mail"
5. Use this 16-character password (not your regular Gmail password)

### 3. Environment Configuration

Set up your email credentials as environment variables:

```bash
# Windows
set EMAIL_ADDRESS=your_email@gmail.com
set EMAIL_PASSWORD=your_16_character_app_password

# Linux/Mac
export EMAIL_ADDRESS=your_email@gmail.com
export EMAIL_PASSWORD=your_16_character_app_password
```

### 4. Basic Usage

```python
from email_notifier import EmailNotifier, send_winner_notification

# Initialize notifier
notifier = EmailNotifier()
notifier.configure_from_env()

# Send a winner notification
success = send_winner_notification(
    notifier=notifier,
    recipient_email="winner@example.com",
    winner_name="John Doe",
    event_name="Photography Contest 2025",
    prize="First Place - $500",
    event_date="September 1, 2025"
)
```

## Available Templates 📋

### 1. Event Winner Notification 🏆
Perfect for contests, competitions, and prize announcements.

```python
from email_notifier import send_winner_notification

send_winner_notification(
    notifier=notifier,
    recipient_email="winner@example.com",
    winner_name="Jane Smith",
    event_name="Annual Art Competition",
    prize="Grand Prize - $1000 + Art Supplies",
    event_date="August 15, 2025"
)
```

### 2. Email Verification 📧
For user registration and email confirmation.

```python
from email_notifier import send_verification_email

send_verification_email(
    notifier=notifier,
    recipient_email="user@example.com",
    user_name="New User",
    verification_link="https://yoursite.com/verify?token=abc123"
)
```

### 3. OTP Authentication 🔐
For two-factor authentication and secure login.

```python
from email_notifier import send_otp_email

send_otp_email(
    notifier=notifier,
    recipient_email="user@example.com",
    user_name="John Doe",
    otp_code="123456",
    purpose="login"
)
```

### 4. Road Maintenance Reports 🛣️
For government authorities to update citizens on infrastructure issues.

```python
from email_notifier import send_road_maintenance_update

send_road_maintenance_update(
    notifier=notifier,
    recipient_email="citizen@example.com",
    citizen_name="Maria Garcia",
    report_id="RD-2025-001234",
    issue_description="Large pothole causing traffic disruption",
    location="Main Street between 5th and 6th Avenue",
    status="in_progress",
    estimated_completion="September 15, 2025",
    assigned_team="Road Repair Team Alpha"
)
```

## Advanced Usage 🔧

### Custom Templates

```python
from email_notifier import EmailNotifier, EmailTemplates

# Create custom email using base template
notifier = EmailNotifier()
notifier.configure_from_env()

custom_html = EmailTemplates.get_base_template().format(
    title="Custom Notification",
    organization="Your Company",
    content="<h2>Your custom content here</h2>",
    contact_email="support@yourcompany.com",
    year=2025
)

notifier.send_email(
    recipient_email="user@example.com",
    subject="Custom Email",
    html_content=custom_html
)
```

### Bulk Email Sending

```python
recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]

results = notifier.send_bulk_email(
    recipients=recipients,
    subject="Bulk Notification",
    html_content=your_html_content
)

# Check results
for email, success in results.items():
    print(f"{email}: {'✅' if success else '❌'}")
```

### Multiple SMTP Providers

```python
from email_notifier import EmailNotifier
from config import EmailConfig

# Use Outlook instead of Gmail
outlook_config = EmailConfig.get_smtp_config('outlook')
notifier = EmailNotifier(
    smtp_server=outlook_config['server'],
    smtp_port=outlook_config['port']
)
```

## File Structure 📁

```
mail_notificationModule/
├── email_notifier.py      # Main module with EmailNotifier class and templates
├── example_usage.py       # Comprehensive usage examples
├── config.py             # Configuration settings and helpers
├── requirements.txt      # Python dependencies
└── README.md            # This documentation
```

## Security Best Practices 🔒

1. **Never hardcode credentials** in your source code
2. **Use environment variables** for sensitive information
3. **Use App Passwords** for Gmail (not your regular password)
4. **Validate email addresses** before sending
5. **Implement rate limiting** for production use
6. **Log email activities** for audit trails

## Error Handling 🚨

The module includes comprehensive error handling:

```python
try:
    notifier = EmailNotifier()
    notifier.configure_from_env()
    
    success = notifier.send_email(
        recipient_email="user@example.com",
        subject="Test Email",
        html_content="<h1>Test</h1>"
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email")
        
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing 🧪

Run the example script to test all functionality:

```bash
python example_usage.py
```

This will:
- Test all email templates
- Demonstrate bulk sending
- Show custom template usage
- Validate your configuration

## Troubleshooting 🔍

### Common Issues

1. **"Authentication failed"**
   - Make sure you're using an App Password, not your regular Gmail password
   - Verify 2FA is enabled on your Gmail account

2. **"Connection refused"**
   - Check your internet connection
   - Verify SMTP server and port settings

3. **"Environment variables not set"**
   - Ensure EMAIL_ADDRESS and EMAIL_PASSWORD are properly set
   - Try running `python config.py` to set them interactively

4. **Emails not received**
   - Check spam/junk folders
   - Verify recipient email addresses
   - Check Gmail's sent folder to confirm sending

### Getting Help

1. Check the logs for detailed error messages
2. Verify your Gmail App Password setup
3. Test with the provided example script
4. Ensure all dependencies are installed

## License 📄

This module is provided as-is for educational and development purposes. Feel free to modify and use according to your needs.

## Contributing 🤝

Feel free to submit issues, feature requests, or improvements to make this module even better!

---

**Happy Emailing! 📧✨**
