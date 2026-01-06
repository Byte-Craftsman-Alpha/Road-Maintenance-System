from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import random
import string

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='citizen')  # citizen or authority
    phone = db.Column(db.String(15))
    department = db.Column(db.String(100))  # For authority users
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    reports = db.relationship('Report', backref='reporter', lazy=True)
    assigned_tickets = db.relationship('MaintenanceTicket', backref='assigned_to', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # pothole, crack, broken_structure, etc.
    severity = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high, critical
    latitude = db.Column(db.Float, nullable=True)  # Made optional
    longitude = db.Column(db.Float, nullable=True)  # Made optional
    address = db.Column(db.String(300))
    postal_code = db.Column(db.String(20))  # PIN/Postal/Zip code
    photo_path = db.Column(db.String(200), nullable=False)  # Made mandatory
    status = db.Column(db.String(20), default='reported')  # reported, verified, in_progress, completed, rejected
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)  # New field for anonymous reporting
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ticket = db.relationship('MaintenanceTicket', backref='report', uselist=False)
    updates = db.relationship('StatusUpdate', backref='report', lazy=True, order_by='StatusUpdate.created_at.desc()')

class MaintenanceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    estimated_cost = db.Column(db.Float)
    estimated_completion = db.Column(db.DateTime)
    actual_completion = db.Column(db.DateTime)
    work_description = db.Column(db.Text)
    materials_used = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StatusUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text)
    image_path = db.Column(db.String(200))  # New field for status update images
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    updated_by = db.relationship('User', backref='status_updates')

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    date_recorded = db.Column(db.Date, default=datetime.utcnow().date())
    category = db.Column(db.String(50))  # response_time, completion_rate, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    voter = db.relationship('User', backref='votes')
    voted_report = db.relationship('Report', backref='votes')
    
    # Ensure one vote per user per report
    __table_args__ = (db.UniqueConstraint('user_id', 'report_id', name='unique_user_report_vote'),)

class CitizenPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, default=0)
    reports_submitted = db.Column(db.Integer, default=0)
    votes_cast = db.Column(db.Integer, default=0)
    reports_verified = db.Column(db.Integer, default=0)  # Reports that got verified by authorities
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    citizen = db.relationship('User', backref=db.backref('points_record', uselist=False))
    
    @staticmethod
    def add_points(user_id, points, reason):
        """Add points to a citizen's record"""
        citizen_points = CitizenPoints.query.filter_by(user_id=user_id).first()
        if not citizen_points:
            citizen_points = CitizenPoints(user_id=user_id)
            db.session.add(citizen_points)
        
        # Handle None values by initializing to 0
        if citizen_points.points is None:
            citizen_points.points = 0
        if citizen_points.reports_submitted is None:
            citizen_points.reports_submitted = 0
        if citizen_points.votes_cast is None:
            citizen_points.votes_cast = 0
        if citizen_points.reports_verified is None:
            citizen_points.reports_verified = 0
        
        citizen_points.points += points
        
        # Update counters based on reason
        if reason == 'report_submitted':
            citizen_points.reports_submitted += 1
        elif reason == 'vote_cast':
            citizen_points.votes_cast += 1
        elif reason == 'vote_removed':
            citizen_points.votes_cast -= 1
        elif reason == 'report_verified':
            citizen_points.reports_verified += 1
        
        # Commit the changes
        db.session.commit()
        
        citizen_points.updated_at = datetime.utcnow()
        db.session.commit()

class OTPVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(50), nullable=False)  # registration, password_reset, etc.
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def create_otp(email, purpose='registration', validity_minutes=10):
        """Create a new OTP for the given email and purpose"""
        # Delete any existing OTPs for this email and purpose
        OTPVerification.query.filter_by(email=email, purpose=purpose, is_used=False).delete()
        
        otp_code = OTPVerification.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=validity_minutes)
        
        otp = OTPVerification(
            email=email,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )
        db.session.add(otp)
        db.session.commit()
        return otp_code
    
    @staticmethod
    def verify_otp(email, otp_code, purpose='registration'):
        """Verify OTP code for the given email and purpose"""
        otp = OTPVerification.query.filter_by(
            email=email,
            otp_code=otp_code,
            purpose=purpose,
            is_used=False
        ).first()
        
        if not otp:
            return False
        
        if datetime.utcnow() > otp.expires_at:
            return False
        
        otp.is_used = True
        db.session.commit()
        return True
