"""
Email Notification Module

A comprehensive Python module for sending email notifications through SMTP and Gmail
with support for various email templates including event notifications, verification emails,
OTP emails, and road maintenance reports.

Author: Cascade AI Assistant
Date: 2025-09-06
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailNotifier:
    """
    A comprehensive email notification class that supports Gmail SMTP
    and various email templates for different use cases.
    """
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize the EmailNotifier with SMTP configuration.
        
        Args:
            smtp_server (str): SMTP server address (default: Gmail)
            smtp_port (int): SMTP server port (default: 587 for TLS)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.sender_password = None
        
    def configure_credentials(self, email: str, password: str):
        """
        Configure sender email credentials.
        
        Args:
            email (str): Sender's email address
            password (str): Sender's email password or app password
        """
        self.sender_email = email
        self.sender_password = password
        
    def configure_from_env(self):
        """
        Configure credentials from environment variables.
        Expected variables: EMAIL_ADDRESS, EMAIL_PASSWORD
        """
        self.sender_email = os.getenv('EMAIL_ADDRESS')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        
        if not self.sender_email or not self.sender_password:
            raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD environment variables must be set")
    
    def send_email(self, 
                   recipient_email: str, 
                   subject: str, 
                   html_content: str, 
                   text_content: Optional[str] = None,
                   attachments: Optional[List[str]] = None) -> bool:
        """
        Send an email with HTML content and optional attachments.
        
        Args:
            recipient_email (str): Recipient's email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text version of the email
            attachments (List[str], optional): List of file paths to attach
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message container
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Add text content if provided
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        message.attach(part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False
    
    def send_bulk_email(self, 
                       recipients: List[str], 
                       subject: str, 
                       html_content: str,
                       text_content: Optional[str] = None) -> Dict[str, bool]:
        """
        Send emails to multiple recipients.
        
        Args:
            recipients (List[str]): List of recipient email addresses
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text version of the email
            
        Returns:
            Dict[str, bool]: Dictionary mapping email addresses to success status
        """
        results = {}
        for recipient in recipients:
            results[recipient] = self.send_email(
                recipient, subject, html_content, text_content
            )
        return results


class EmailTemplates:
    """
    Collection of email templates for various use cases.
    """
    
    @staticmethod
    def get_base_template() -> str:
        """
        Get the base HTML template for emails.
        
        Returns:
            str: Base HTML template
        """
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #eee;
                }}
                .logo {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                .content {{
                    margin-bottom: 30px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .button:hover {{
                    background-color: #2980b9;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 12px;
                }}
                .highlight {{
                    background-color: #f39c12;
                    color: white;
                    padding: 2px 8px;
                    border-radius: 3px;
                    font-weight: bold;
                }}
                .success {{
                    color: #27ae60;
                    font-weight: bold;
                }}
                .warning {{
                    color: #e74c3c;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">{organization}</div>
                    <h1>{title}</h1>
                </div>
                <div class="content">
                    {content}
                </div>
                <div class="footer">
                    <p>This email was sent from {organization}</p>
                    <p>If you have any questions, please contact us at {contact_email}</p>
                    <p>&copy; {year} {organization}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def event_winner_template(winner_name: str, 
                            event_name: str, 
                            prize: str, 
                            event_date: str,
                            organization: str = "Event Organization",
                            contact_email: str = "contact@organization.com") -> str:
        """
        Generate HTML template for event winner notification.
        
        Args:
            winner_name (str): Name of the winner
            event_name (str): Name of the event
            prize (str): Prize description
            event_date (str): Date of the event
            organization (str): Organization name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        content = f"""
        <h2>🎉 Congratulations, {winner_name}!</h2>
        <p>We are thrilled to inform you that you have won the <span class="highlight">{prize}</span> 
        in our <strong>{event_name}</strong> event held on {event_date}!</p>
        
        <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3>Prize Details:</h3>
            <ul>
                <li><strong>Event:</strong> {event_name}</li>
                <li><strong>Prize:</strong> {prize}</li>
                <li><strong>Winner:</strong> {winner_name}</li>
                <li><strong>Event Date:</strong> {event_date}</li>
            </ul>
        </div>
        
        <p>To claim your prize, please reply to this email with your contact information and preferred 
        method of prize delivery within <span class="warning">7 days</span> of receiving this notification.</p>
        
        <p>Once again, congratulations on your achievement! We hope you enjoyed participating in our event.</p>
        
        <p class="success">Best regards,<br>The {organization} Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="🏆 You're a Winner!",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )
    
    @staticmethod
    def verification_email_template(user_name: str, 
                                  verification_link: str,
                                  organization: str = "Your Service",
                                  contact_email: str = "support@yourservice.com") -> str:
        """
        Generate HTML template for email verification.
        
        Args:
            user_name (str): Name of the user
            verification_link (str): Verification URL
            organization (str): Organization name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        content = f"""
        <h2>Welcome to {organization}, {user_name}!</h2>
        <p>Thank you for signing up with us. To complete your registration and activate your account, 
        please verify your email address by clicking the button below:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_link}" class="button">Verify Email Address</a>
        </div>
        
        <p>If the button doesn't work, you can also copy and paste the following link into your browser:</p>
        <p style="background-color: #ecf0f1; padding: 10px; border-radius: 5px; word-break: break-all;">
            {verification_link}
        </p>
        
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>⚠️ Important:</strong></p>
            <ul>
                <li>This verification link will expire in <span class="highlight">24 hours</span></li>
                <li>If you didn't create an account with us, please ignore this email</li>
                <li>For security reasons, do not share this link with anyone</li>
            </ul>
        </div>
        
        <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
        
        <p class="success">Welcome aboard!<br>The {organization} Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="📧 Verify Your Email Address",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )
    
    @staticmethod
    def otp_email_template(user_name: str, 
                          otp_code: str,
                          purpose: str = "login",
                          organization: str = "Your Service",
                          contact_email: str = "support@yourservice.com") -> str:
        """
        Generate HTML template for OTP email.
        
        Args:
            user_name (str): Name of the user
            otp_code (str): OTP code
            purpose (str): Purpose of OTP (login, password reset, etc.)
            organization (str): Organization name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        content = f"""
        <h2>🔐 Your One-Time Password (OTP)</h2>
        <p>Hello {user_name},</p>
        <p>You have requested a one-time password for <strong>{purpose}</strong>. 
        Please use the following OTP to complete your request:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <div style="background-color: #2c3e50; color: white; padding: 20px; border-radius: 10px; 
                        font-size: 32px; font-weight: bold; letter-spacing: 5px; display: inline-block;">
                {otp_code}
            </div>
        </div>
        
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>⚠️ Security Information:</strong></p>
            <ul>
                <li>This OTP is valid for <span class="highlight">10 minutes</span> only</li>
                <li>Do not share this code with anyone</li>
                <li>If you didn't request this OTP, please contact us immediately</li>
                <li>This code can only be used once</li>
            </ul>
        </div>
        
        <p>If you're having trouble with the {purpose} process or didn't request this OTP, 
        please contact our support team immediately.</p>
        
        <p class="success">Stay secure!<br>The {organization} Security Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="🔒 Your Security Code",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )
    
    @staticmethod
    def password_reset_template(user_name: str,
                              reset_code: str,
                              organization: str = "Road Maintenance System",
                              contact_email: str = "support@roadmaintenance.com") -> str:
        """
        Generate HTML template for password reset email.
        
        Args:
            user_name (str): Name of the user
            reset_code (str): Password reset code
            organization (str): Organization name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        content = f"""
        <h2>🔐 Password Reset Request</h2>
        <p>Hello {user_name},</p>
        <p>We received a request to reset your password for your {organization} account. 
        Please use the following code to reset your password:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <div style="background-color: #e74c3c; color: white; padding: 20px; border-radius: 10px; 
                        font-size: 32px; font-weight: bold; letter-spacing: 5px; display: inline-block;">
                {reset_code}
            </div>
        </div>
        
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>⚠️ Security Information:</strong></p>
            <ul>
                <li>This reset code is valid for <span class="highlight">10 minutes</span> only</li>
                <li>Do not share this code with anyone</li>
                <li>If you didn't request a password reset, please ignore this email</li>
                <li>This code can only be used once</li>
            </ul>
        </div>
        
        <p>If you didn't request this password reset or are having trouble, 
        please contact our support team immediately at {contact_email}.</p>
        
        <p class="warning">For your security, please create a strong password that you haven't used before.</p>
        
        <p class="success">Stay secure!<br>The {organization} Security Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="🔐 Password Reset Code",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )
    
    @staticmethod
    def status_update_template(citizen_name: str,
                             report_id: str,
                             report_title: str,
                             old_status: str,
                             new_status: str,
                             comment: str,
                             updated_by: str,
                             update_date: str,
                             location: str,
                             organization: str = "Road Maintenance Authority",
                             contact_email: str = "support@roadmaintenance.com") -> str:
        """
        Generate HTML template for report status update notification.
        
        Args:
            citizen_name (str): Name of the citizen who reported
            report_id (str): Report ID
            report_title (str): Title of the report
            old_status (str): Previous status
            new_status (str): New status
            comment (str): Update comment from authority
            updated_by (str): Name of authority who updated
            update_date (str): Date of update
            location (str): Location of the issue
            organization (str): Organization name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        # Status color mapping
        status_colors = {
            'reported': '#f39c12',
            'verified': '#3498db', 
            'in_progress': '#2980b9',
            'completed': '#27ae60',
            'rejected': '#e74c3c'
        }
        
        # Status icons
        status_icons = {
            'reported': '📝',
            'verified': '✅',
            'in_progress': '🔧',
            'completed': '✨',
            'rejected': '❌'
        }
        
        old_color = status_colors.get(old_status, '#95a5a6')
        new_color = status_colors.get(new_status, '#95a5a6')
        new_icon = status_icons.get(new_status, '📋')
        
        content = f"""
        <h2>🛣️ Report Status Update</h2>
        <p>Hello {citizen_name},</p>
        <p>We have an update on your road maintenance report. Here are the details:</p>
        
        <div style="background-color: #f8f9fa; border-left: 4px solid {new_color}; padding: 20px; margin: 20px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: {new_color};">{new_icon} Report #{report_id}</h3>
            <p><strong>Title:</strong> {report_title}</p>
            <p><strong>Location:</strong> {location}</p>
        </div>
        
        <div style="background-color: #fff; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin: 20px 0;">
            <h4 style="color: #2c3e50; margin-top: 0;">Status Change</h4>
            <div style="display: flex; align-items: center; margin: 15px 0;">
                <span style="background-color: {old_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; text-transform: capitalize;">
                    {old_status.replace('_', ' ')}
                </span>
                <span style="margin: 0 15px; font-size: 18px;">→</span>
                <span style="background-color: {new_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; text-transform: capitalize;">
                    {new_icon} {new_status.replace('_', ' ')}
                </span>
            </div>
            
            <div style="margin-top: 20px;">
                <p><strong>Updated by:</strong> {updated_by}</p>
                <p><strong>Update Date:</strong> {update_date}</p>
                {f'<p><strong>Comment:</strong> {comment}</p>' if comment else ''}
            </div>
        </div>
        
        <div style="background-color: #e8f5e8; border: 1px solid #c3e6c3; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>💡 What's Next?</strong></p>
            <ul style="margin: 10px 0;">
                {'<li>Your report has been received and is under review.</li>' if new_status == 'reported' else ''}
                {'<li>Your report has been verified and will be scheduled for maintenance.</li>' if new_status == 'verified' else ''}
                {'<li>Work has begun on your reported issue. We will keep you updated on progress.</li>' if new_status == 'in_progress' else ''}
                {'<li>Great news! The maintenance work has been completed. Thank you for reporting this issue.</li>' if new_status == 'completed' else ''}
                {'<li>Unfortunately, this report could not be processed. Please contact us if you have questions.</li>' if new_status == 'rejected' else ''}
            </ul>
        </div>
        
        <p>You can track your report and view all updates by logging into your account on our website.</p>
        
        <p>Thank you for helping us maintain our roads and infrastructure!</p>
        
        <p class="success">Best regards,<br>The {organization} Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="🛣️ Report Status Update",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )

    @staticmethod
    def maintenance_ticket_assignment_template(authority_name: str,
                                             report_id: int,
                                             report_title: str,
                                             location: str,
                                             priority: str,
                                             citizen_name: str,
                                             assigned_by: str,
                                             assignment_date: str,
                                             organization: str = "Road Maintenance Authority",
                                             contact_email: str = "support@roadmaintenance.com") -> str:
        """
        Generate HTML template for maintenance ticket assignment notification to authority.
        """
        priority_colors = {
            'low': '#28a745',
            'medium': '#ffc107', 
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        priority_color = priority_colors.get(priority.lower(), '#6c757d')
        
        content = f"""
        <h2>🛠️ New Maintenance Ticket Assignment</h2>
        <p>Hello {authority_name},</p>
        <p>You have been assigned a new maintenance ticket. Please review the details below:</p>
        
        <div style="background-color: #f8f9fa; border-left: 4px solid {priority_color}; padding: 20px; margin: 20px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: {priority_color};">🎫 Ticket #{report_id}</h3>
            <p><strong>📋 Title:</strong> {report_title}</p>
            <p><strong>📍 Location:</strong> {location}</p>
            <p><strong>⚠️ Priority:</strong> <span style="color: {priority_color}; font-weight: bold;">{priority.upper()}</span></p>
            <p><strong>👤 Reported by:</strong> {citizen_name}</p>
            <p><strong>👨‍💼 Assigned by:</strong> {assigned_by}</p>
            <p><strong>📅 Assignment Date:</strong> {assignment_date}</p>
        </div>
        
        <div style="background-color: #e3f2fd; padding: 15px; margin: 20px 0; border-radius: 5px;">
            <h4 style="color: #1976d2; margin-top: 0;">📋 Next Steps</h4>
            <ul style="margin-bottom: 0;">
                <li>Review the ticket details in the system</li>
                <li>Update the work description and estimated completion date</li>
                <li>Begin work on the assigned maintenance task</li>
                <li>Keep the citizen updated on progress</li>
            </ul>
        </div>
        
        <p>Please log into the system to view complete details and update the ticket status.</p>
        """
        
        return EmailTemplates._get_base_template(
            content=content,
            organization=organization,
            contact_email=contact_email
        )

    @staticmethod
    def maintenance_ticket_update_template(citizen_name: str, 
                                         report_id: int, 
                                         report_title: str, 
                                         location: str, 
                                         assigned_to: str, 
                                         priority: str, 
                                         status: str, 
                                         estimated_completion: str, 
                                         work_description: str, 
                                         updated_by: str, 
                                         update_date: str,
                                         organization: str = "Road Maintenance Authority",
                                         contact_email: str = "support@roadmaintenance.com") -> str:
        """
        Generate HTML template for maintenance ticket update notification.
{{ ... }}
        
        Args:
            citizen_name (str): Name of the citizen who reported
            report_id (str): Report ID
            report_title (str): Title of the report
            location (str): Location of the issue
            assigned_to (str): Personnel assigned to the ticket
            priority (str): Priority level
            estimated_cost (str): Estimated cost
            estimated_completion (str): Estimated completion date
            work_description (str): Description of work to be done
            materials_used (str): Materials that will be used
            updated_by (str): Name of authority who updated
            update_date (str): Date of update
            organization (str): Organization name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        # Priority color mapping
        priority_colors = {
            'low': '#27ae60',
            'medium': '#f39c12', 
            'high': '#e74c3c',
            'critical': '#8e44ad'
        }
        
        # Priority icons
        priority_icons = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴',
            'critical': '🚨'
        }
        
        priority_color = priority_colors.get(priority.lower(), '#95a5a6')
        priority_icon = priority_icons.get(priority.lower(), '📋')
        
        content = f"""
        <h2>🔧 Maintenance Ticket Updated</h2>
        <p>Hello {citizen_name},</p>
        <p>We have updated the maintenance ticket for your reported issue. Here are the latest details:</p>
        
        <div style="background-color: #f8f9fa; border-left: 4px solid {priority_color}; padding: 20px; margin: 20px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: {priority_color};">🛠️ Ticket #{report_id}</h3>
            <p><strong>Title:</strong> {report_title}</p>
            <p><strong>Location:</strong> {location}</p>
        </div>
        
        <div style="background-color: #fff; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin: 20px 0;">
            <h4 style="color: #2c3e50; margin-top: 0;">📋 Ticket Details</h4>
            
            <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6; font-weight: bold; width: 30%;">Assigned To:</td>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{assigned_to}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6; font-weight: bold;">Priority:</td>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">
                        <span style="background-color: {priority_color}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 12px; font-weight: bold;">
                            {priority_icon} {priority.upper()}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6; font-weight: bold;">Estimated Cost:</td>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{estimated_cost or 'Not specified'}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6; font-weight: bold;">Est. Completion:</td>
                    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{estimated_completion or 'Not specified'}</td>
                </tr>
            </table>
            
            {f'''
            <div style="margin-top: 20px;">
                <h5 style="color: #2c3e50;">🔨 Work Description:</h5>
                <p style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">{work_description}</p>
            </div>
            ''' if work_description else ''}
            
            {f'''
            <div style="margin-top: 20px;">
                <h5 style="color: #2c3e50;">📦 Materials Required:</h5>
                <p style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">{materials_used}</p>
            </div>
            ''' if materials_used else ''}
            
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                <p><strong>Updated by:</strong> {updated_by}</p>
                <p><strong>Update Date:</strong> {update_date}</p>
            </div>
        </div>
        
        <div style="background-color: #e8f5e8; border: 1px solid #c3e6c3; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>💡 What This Means:</strong></p>
            <ul style="margin: 10px 0;">
                <li>Our maintenance team has reviewed and planned the work for your reported issue</li>
                <li>The assigned personnel will handle the maintenance work according to the schedule</li>
                <li>You will receive further updates as work progresses</li>
                <li>If you have any questions about the planned work, please contact us</li>
            </ul>
        </div>
        
        <p>You can track your report and view all updates by logging into your account on our website.</p>
        
        <p>Thank you for your patience as we work to resolve this issue!</p>
        
        <p class="success">Best regards,<br>The {organization} Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="🔧 Maintenance Ticket Update",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )

    @staticmethod
    def road_maintenance_report_template(citizen_name: str,
                                       report_id: str,
                                       issue_description: str,
                                       location: str,
                                       status: str,
                                       estimated_completion: str,
                                       assigned_team: str,
                                       organization: str = "City Road Maintenance Authority",
                                       contact_email: str = "roads@cityauthority.gov") -> str:
        """
        Generate HTML template for road maintenance report to citizens.
        
        Args:
            citizen_name (str): Name of the citizen who reported
            report_id (str): Unique report ID
            issue_description (str): Description of the road issue
            location (str): Location of the issue
            status (str): Current status of the report
            estimated_completion (str): Estimated completion date
            assigned_team (str): Team assigned to handle the issue
            organization (str): Authority name
            contact_email (str): Contact email
            
        Returns:
            str: HTML email content
        """
        status_color = {
            "received": "#f39c12",
            "in_progress": "#3498db", 
            "completed": "#27ae60",
            "on_hold": "#e74c3c"
        }.get(status.lower(), "#95a5a6")
        
        content = f"""
        <h2>🛣️ Road Maintenance Report Update</h2>
        <p>Dear {citizen_name},</p>
        <p>Thank you for reporting the road maintenance issue. We appreciate your civic responsibility 
        in helping us maintain our city's infrastructure. Here's an update on your report:</p>
        
        <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3>📋 Report Details:</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;"><strong>Report ID:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;">{report_id}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;"><strong>Location:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;">{location}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;"><strong>Issue:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;">{issue_description}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;"><strong>Status:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;">
                        <span style="background-color: {status_color}; color: white; padding: 4px 12px; 
                                     border-radius: 15px; font-size: 12px; font-weight: bold;">
                            {status.upper()}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;"><strong>Assigned Team:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #bdc3c7;">{assigned_team}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Est. Completion:</strong></td>
                    <td style="padding: 8px;">{estimated_completion}</td>
                </tr>
            </table>
        </div>
        
        <div style="background-color: #d5f4e6; border: 1px solid #27ae60; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>📞 Need to Follow Up?</strong></p>
            <p>You can track your report status online using Report ID: <span class="highlight">{report_id}</span></p>
            <p>For urgent issues or questions, contact us at: <strong>{contact_email}</strong></p>
        </div>
        
        <p>We are committed to maintaining safe and well-maintained roads for all citizens. 
        Your report helps us prioritize and address infrastructure issues effectively.</p>
        
        <p class="success">Thank you for your civic participation!<br>The {organization} Team</p>
        """
        
        base_template = EmailTemplates.get_base_template()
        return base_template.format(
            title="🏗️ Road Maintenance Update",
            organization=organization,
            content=content,
            contact_email=contact_email,
            year=datetime.now().year
        )


# Convenience functions for quick email sending
def send_winner_notification(notifier: EmailNotifier, 
                           recipient_email: str,
                           winner_name: str,
                           event_name: str,
                           prize: str,
                           event_date: str) -> bool:
    """
    Quick function to send winner notification email.
    """
    html_content = EmailTemplates.event_winner_template(
        winner_name, event_name, prize, event_date
    )
    return notifier.send_email(
        recipient_email, 
        f"🏆 Congratulations! You won {prize}",
        html_content
    )


def send_verification_email(notifier: EmailNotifier,
                          recipient_email: str,
                          user_name: str,
                          verification_link: str) -> bool:
    """
    Quick function to send verification email.
    """
    html_content = EmailTemplates.verification_email_template(
        user_name, verification_link
    )
    return notifier.send_email(
        recipient_email,
        "📧 Please verify your email address",
        html_content
    )


def send_otp_email(notifier: EmailNotifier,
                  recipient_email: str,
                  user_name: str,
                  otp_code: str,
                  purpose: str = "login") -> bool:
    """
    Quick function to send OTP email.
    """
    html_content = EmailTemplates.otp_email_template(
        user_name, otp_code, purpose
    )
    return notifier.send_email(
        recipient_email,
        f"🔐 Your OTP for {purpose}",
        html_content
    )


def send_road_maintenance_update(notifier: EmailNotifier,
                               recipient_email: str,
                               citizen_name: str,
                               report_id: str,
                               issue_description: str,
                               location: str,
                               status: str,
                               estimated_completion: str,
                               assigned_team: str) -> bool:
    """
    Quick function to send road maintenance update email.
    """
    html_content = EmailTemplates.road_maintenance_report_template(
        citizen_name, report_id, issue_description, location,
        status, estimated_completion, assigned_team
    )
    return notifier.send_email(
        recipient_email,
        f"🛣️ Road Maintenance Update - Report #{report_id}",
        html_content
    )


def send_password_reset_email(notifier: EmailNotifier,
                            recipient_email: str,
                            user_name: str,
                            reset_code: str) -> bool:
    """
    Quick function to send password reset email.
    """
    html_content = EmailTemplates.password_reset_template(
        user_name, reset_code
    )
    return notifier.send_email(
        recipient_email,
        "🔐 Password Reset Code - Road Maintenance System",
        html_content
    )


def send_status_update_email(notifier: EmailNotifier,
                           recipient_email: str,
                           citizen_name: str,
                           report_id: str,
                           report_title: str,
                           old_status: str,
                           new_status: str,
                           comment: str,
                           updated_by: str,
                           update_date: str,
                           location: str) -> bool:
    """
    Quick function to send report status update email to citizen.
    """
    html_content = EmailTemplates.status_update_template(
        citizen_name, report_id, report_title, old_status, 
        new_status, comment, updated_by, update_date, location
    )
    return notifier.send_email(
        recipient_email,
        f"🛣️ Report Update - #{report_id} Status Changed",
        html_content
    )


def send_maintenance_ticket_update_email(notifier: EmailNotifier,
                                       recipient_email: str,
                                       citizen_name: str,
                                       report_id: int,
                                       report_title: str,
                                       location: str,
                                       assigned_to: str,
                                       priority: str,
                                       status: str,
                                       estimated_completion: str,
                                       work_description: str,
                                       updated_by: str,
                                       update_date: str) -> bool:
    """
    Quick function to send maintenance ticket update email to citizen.
    """
    html_content = EmailTemplates.maintenance_ticket_update_template(
        citizen_name, report_id, report_title, location, assigned_to,
        priority, status, estimated_completion, work_description,
        updated_by, update_date
    )
    
    subject = f"🔧 Maintenance Ticket Update - Report #{report_id}"
    
    return notifier.send_email(
        to_email=recipient_email,
        subject=subject,
        html_content=html_content
    )


def send_maintenance_ticket_assignment_email(notifier: EmailNotifier,
                                           recipient_email: str,
                                           authority_name: str,
                                           report_id: int,
                                           report_title: str,
                                           location: str,
                                           priority: str,
                                           citizen_name: str,
                                           assigned_by: str,
                                           assignment_date: str) -> bool:
    """
    Send maintenance ticket assignment notification to authority user.
    """
    html_content = EmailTemplates.maintenance_ticket_assignment_template(
        authority_name, report_id, report_title, location, priority,
        citizen_name, assigned_by, assignment_date
    )
    
    subject = f"🛠️ New Maintenance Ticket Assignment - Report #{report_id}"
    
    return notifier.send_email(
        to_email=recipient_email,
        subject=subject,
        html_content=html_content
    )
