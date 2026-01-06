from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, FloatField, DateTimeField, PasswordField, SubmitField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    role = SelectField('Role', choices=[('citizen', 'Citizen'), ('authority', 'Authority')], default='citizen')
    department = StringField('Department (for Authority users)', validators=[Optional(), Length(max=100)])
    authority_password = PasswordField('Authority Registration Password', validators=[Optional()])
    submit = SubmitField('Send OTP')

class OTPVerificationForm(FlaskForm):
    otp_code = StringField('Enter 6-digit OTP', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify & Register')

class ReportForm(FlaskForm):
    title = StringField('Issue Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('infrastructure_roads', 'Infrastructure & Roads'),
        ('sanitation_waste', 'Sanitation & Waste Management'),
        ('water_supply_drainage', 'Water Supply & Drainage'),
        ('electricity_lighting', 'Electricity & Street Lighting'),
        ('public_safety_security', 'Public Safety & Security'),
        ('environment_pollution', 'Environment & Pollution'),
        ('transportation_traffic', 'Transportation & Traffic'),
        ('healthcare_public_health', 'Healthcare & Public Health'),
        ('digital_egovernance', 'Digital & E-Governance'),
        ('education_public_spaces', 'Education & Public Spaces'),
        ('emergency_disaster', 'Emergency & Disaster Management'),
        ('citizen_rights_governance', 'Citizen Rights & Governance')
    ], validators=[DataRequired()])
    severity = SelectField('Severity', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium', validators=[DataRequired()])
    latitude = HiddenField('Latitude', validators=[Optional()])
    longitude = HiddenField('Longitude', validators=[Optional()])
    address = StringField('Address', validators=[Optional(), Length(max=300)])
    postal_code = StringField('PIN/Postal/Zip Code', validators=[DataRequired(), Length(max=20)])
    photo = FileField('Photo', validators=[
        FileRequired('Photo is mandatory for all reports'),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    is_anonymous = BooleanField('Report Anonymously (Hide my identity in public views)')
    submit = SubmitField('Submit Report')

class TicketForm(FlaskForm):
    assigned_to_id = SelectField('Assign To', coerce=int, validators=[Optional()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    estimated_cost = FloatField('Estimated Cost', validators=[Optional(), NumberRange(min=0)])
    estimated_completion = DateTimeField('Estimated Completion', validators=[Optional()], format='%Y-%m-%d')
    work_description = TextAreaField('Work Description', validators=[Optional()])
    submit = SubmitField('Update Ticket')

class StatusUpdateForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('reported', 'Reported'),
        ('verified', 'Verified'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional()])
    image = FileField('Status Update Image', validators=[
        FileRequired('Photo is mandatory for all status updates'),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Update Status')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Code')

class ResetPasswordForm(FlaskForm):
    otp_code = StringField('Enter 6-digit Reset Code', validators=[DataRequired(), Length(min=6, max=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Reset Password')

class ReportTrackingForm(FlaskForm):
    report_id = StringField('Report ID', validators=[DataRequired()], render_kw={"placeholder": "Enter Report ID (e.g., 123)"})
    submit = SubmitField('Track Report')
