from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_babel import Babel, _, get_locale, ngettext
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from PIL import Image
import sys
sys.path.append('gmail_notification')
from gmail_notification.email_notifier import EmailNotifier, send_otp_email, send_password_reset_email, send_status_update_email, send_maintenance_ticket_update_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///road_maintenance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Babel configuration - All 22 Official Indian Languages + English
app.config['LANGUAGES'] = {
    'en': 'English',           # Default
    'hi': 'हिन्दी',            # Hindi
    'as': 'অসমীয়া',           # Assamese
    'bn': 'বাংলা',            # Bengali
    'gu': 'ગુજરાતી',          # Gujarati
    'kn': 'ಕನ್ನಡ',            # Kannada
    'ks': 'کٲشُر',            # Kashmiri
    'kok': 'कोंकणी',          # Konkani
    'ml': 'മലയാളം',          # Malayalam
    'mni': 'মৈতৈলোন্',        # Manipuri
    'mr': 'मराठी',            # Marathi
    'ne': 'नेपाली',           # Nepali remaining translations
    'or': 'ଓଡ଼ିଆ',            # Odia/Oriya
    'pa': 'ਪੰਜਾਬੀ',           # Punjabi
    'sa': 'संस्कृतम्',        # Sanskrit
    'sd': 'سنڌي',            # Sindhi
    'ta': 'தமிழ்',           # Tamil
    'te': 'తెలుగు',          # Telugu
    'ur': 'اردو',            # Urdu
    'brx': 'बर\'',            # Bodo
    'sat': 'ᱥᱟᱱᱛᱟᱲᱤ',         # Santhali
    'mai': 'मैथिली',          # Maithili
    'doi': 'डोगरी'            # Dogri
}
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Initialize Babel
babel = Babel()
babel.init_app(app)

@babel.localeselector
def get_locale():
    # 1. Check if user manually selected a language
    if 'language' in session and session['language'] in app.config['LANGUAGES']:
        return session['language']

    # 2. Check if user is logged in and has a preferred language
    if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        if hasattr(current_user, 'preferred_language') and current_user.preferred_language in app.config['LANGUAGES']:
            return current_user.preferred_language

    # 3. Try to guess the language from the user Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or app.config['BABEL_DEFAULT_LOCALE']

def get_user_locale():
    return get_locale()

# Make get_locale available in templates
app.jinja_env.globals['get_locale'] = get_user_locale

@app.route('/set_language/<language>')
def set_language(language=None):
    """Set the user's preferred language"""
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Email configuration
app.config['EMAIL_ADDRESS'] = os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com')
app.config['EMAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD', 'your-app-password')
app.config['AUTHORITY_REGISTRATION_PASSWORD'] = 'ADMIN2025!'  # Change this in production

# Initialize email notifier
email_notifier = EmailNotifier()
try:
    email_notifier.configure_credentials(app.config['EMAIL_ADDRESS'], app.config['EMAIL_PASSWORD'])
except:
    print("Warning: Email credentials not configured. OTP functionality will not work.")

from models import db, User, Report, MaintenanceTicket, StatusUpdate, Analytics, OTPVerification, Vote, CitizenPoints
from forms import LoginForm, RegisterForm, ReportForm, TicketForm, OTPVerificationForm, ForgotPasswordForm, ResetPasswordForm, StatusUpdateForm, ReportTrackingForm, ChangePasswordForm, ChangeEmailRequestForm, VerifyEmailChangeForm

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def generate_ticket_number():
    return f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'authority':
            return redirect(url_for('authority_dashboard'))
        else:
            return redirect(url_for('citizen_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('auth/register.html', form=form)

        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken')
            return render_template('auth/register.html', form=form)

        # Check authority registration password
        if form.role.data == 'authority':
            if not form.authority_password.data or form.authority_password.data != app.config['AUTHORITY_REGISTRATION_PASSWORD']:
                flash('Invalid authority registration password')
                return render_template('auth/register.html', form=form)

        # Store registration data in session
        session['registration_data'] = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'role': form.role.data,
            'phone': form.phone.data,
            'department': form.department.data if form.role.data == 'authority' else None
        }

        # Generate and send OTP
        try:
            otp_code = OTPVerification.create_otp(form.email.data, 'registration')
            otp_sent = send_otp_email(email_notifier, form.email.data, form.username.data, otp_code, 'registration')
            if otp_sent:
                flash('OTP sent to your email. Please check and verify.', 'success')
                return redirect(url_for('verify_otp'))
            else:
                flash('Failed to send OTP. Please try again later.', 'danger')
                return render_template('auth/register.html', form=form)
        except Exception as e:
            flash('Failed to send OTP. Please try again.', 'error')
            print(f"OTP sending error: {e}")
            return render_template('auth/register.html', form=form)

    return render_template('auth/register.html', form=form)

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if 'registration_data' not in session:
        flash('Registration session expired. Please register again.', 'error')
        return redirect(url_for('register'))

    form = OTPVerificationForm()
    if form.validate_on_submit():
        registration_data = session['registration_data']

        # Verify OTP
        if OTPVerification.verify_otp(registration_data['email'], form.otp_code.data, 'registration'):
            # Create user account
            user = User(
                username=registration_data['username'],
                email=registration_data['email'],
                password_hash=generate_password_hash(registration_data['password']),
                role=registration_data['role'],
                phone=registration_data['phone'],
                department=registration_data['department'],
                email_verified=True
            )
            db.session.add(user)
            db.session.commit()

            # Clear session data
            session.pop('registration_data', None)

            flash('Registration successful! Your email has been verified.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'error')

    return render_template('auth/verify_otp.html', form=form, email=session['registration_data']['email'])

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    if 'registration_data' not in session:
        return jsonify({'success': False, 'message': 'Registration session expired'})

    registration_data = session['registration_data']

    try:
        otp_code = OTPVerification.create_otp(registration_data['email'], 'registration')
        otp_sent = send_otp_email(email_notifier, registration_data['email'], registration_data['username'], otp_code, 'registration')
        if otp_sent:
            return jsonify({'success': True, 'message': 'OTP resent successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to resend OTP. Please try again later.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to resend OTP'})

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                # Generate OTP for password reset
                otp_code = OTPVerification.create_otp(form.email.data, 'password_reset')
                reset_sent = send_password_reset_email(email_notifier, form.email.data, user.username, otp_code)
                if reset_sent:
                    session['reset_email'] = form.email.data
                    flash('Password reset code sent to your email. Please check and enter the code.', 'success')
                    return redirect(url_for('reset_password'))
                else:
                    flash('Failed to send reset code. Please try again later.', 'danger')
            except Exception as e:
                flash('Failed to send reset code. Please try again.', 'error')
                print(f"Password reset email error: {e}")
        else:
            # Don't reveal if email exists or not for security
            flash('If an account with this email exists, a reset code has been sent.', 'info')

    return render_template('auth/forgot_password.html', form=form)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if 'reset_email' not in session:
        flash('Password reset session expired. Please request a new reset code.', 'error')
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.new_password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('auth/reset_password.html', form=form, email=session['reset_email'])

        # Verify OTP
        if OTPVerification.verify_otp(session['reset_email'], form.otp_code.data, 'password_reset'):
            user = User.query.filter_by(email=session['reset_email']).first()
            if user:
                user.password_hash = generate_password_hash(form.new_password.data)
                db.session.commit()

                # Clear session data
                session.pop('reset_email', None)

                flash('Password reset successful! You can now login with your new password.', 'success')
                return redirect(url_for('login'))
            else:
                flash('User not found. Please try again.', 'error')
        else:
            flash('Invalid or expired reset code. Please try again.', 'error')

    return render_template('auth/reset_password.html', form=form, email=session['reset_email'])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    password_form = ChangePasswordForm()
    email_form = ChangeEmailRequestForm()

    if password_form.submit_password.data and password_form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, password_form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('account/settings.html', password_form=password_form, email_form=email_form)

        if password_form.new_password.data != password_form.confirm_password.data:
            flash('Passwords do not match.', 'error')
            return render_template('account/settings.html', password_form=password_form, email_form=email_form)

        user = User.query.get(current_user.id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('index'))

        user.password_hash = generate_password_hash(password_form.new_password.data)
        db.session.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('account_settings'))

    if email_form.submit_email.data and email_form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, email_form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('account/settings.html', password_form=password_form, email_form=email_form)

        new_email = (email_form.new_email.data or '').strip().lower()

        if new_email == (current_user.email or '').strip().lower():
            flash('That is already your current email.', 'info')
            return redirect(url_for('account_settings'))

        if User.query.filter_by(email=new_email).first():
            flash('Email already registered.', 'error')
            return render_template('account/settings.html', password_form=password_form, email_form=email_form)

        try:
            otp_code = OTPVerification.create_otp(new_email, 'email_change')
            otp_sent = send_otp_email(email_notifier, new_email, current_user.username, otp_code, 'email_change')
            if otp_sent:
                session['email_change_user_id'] = current_user.id
                session['email_change_new_email'] = new_email
                flash('Verification code sent to your new email. Please check and verify.', 'success')
                return redirect(url_for('verify_email_change'))
            else:
                flash('Failed to send verification code. Please try again later.', 'danger')
        except Exception as e:
            flash('Failed to send verification code. Please try again.', 'error')
            print(f"Email change OTP sending error: {e}")

    return render_template('account/settings.html', password_form=password_form, email_form=email_form)


@app.route('/account/verify-email-change', methods=['GET', 'POST'])
@login_required
def verify_email_change():
    if 'email_change_user_id' not in session or 'email_change_new_email' not in session:
        flash('Email change session expired. Please try again.', 'error')
        return redirect(url_for('account_settings'))

    if session.get('email_change_user_id') != current_user.id:
        flash('Email change session is invalid.', 'error')
        session.pop('email_change_user_id', None)
        session.pop('email_change_new_email', None)
        return redirect(url_for('account_settings'))

    new_email = session.get('email_change_new_email')
    form = VerifyEmailChangeForm()

    if form.validate_on_submit():
        if OTPVerification.verify_otp(new_email, form.otp_code.data, 'email_change'):
            if User.query.filter_by(email=new_email).first():
                flash('Email already registered.', 'error')
                return redirect(url_for('account_settings'))

            user = User.query.get(current_user.id)
            if not user:
                flash('User not found.', 'error')
                return redirect(url_for('index'))

            user.email = new_email
            user.email_verified = True
            db.session.commit()

            session.pop('email_change_user_id', None)
            session.pop('email_change_new_email', None)

            flash('Email updated successfully.', 'success')
            return redirect(url_for('account_settings'))
        else:
            flash('Invalid or expired verification code. Please try again.', 'error')

    return render_template('account/verify_email_change.html', form=form, new_email=new_email)

@app.route('/citizen/dashboard')
@login_required
def citizen_dashboard():
    if current_user.role != 'citizen':
        return redirect(url_for('authority_dashboard'))

    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()

    # Convert reports to dictionaries for JSON serialization
    reports_data = []
    for report in reports:
        report_dict = {
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'category': report.category,
            'severity': report.severity,
            'status': report.status,
            'address': report.address,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'photo_path': report.photo_path.replace('\\', '/') if report.photo_path else None,
            'created_at': report.created_at.isoformat(),
            'updated_at': report.updated_at.isoformat(),
            'updates': []
        }

        # Add status updates if they exist
        if report.updates:
            for update in report.updates:
                report_dict['updates'].append({
                    'status': update.status,
                    'comment': update.comment,
                    'created_at': update.created_at.isoformat(),
                    'updated_by': update.updated_by.username if update.updated_by else 'System'
                })

        reports_data.append(report_dict)

    return render_template('citizen/dashboard.html', reports=reports, reports_data=reports_data)

@app.route('/citizen/report/<int:report_id>')
@login_required
def view_citizen_report(report_id):
    if current_user.role != 'citizen':
        flash('Access denied')
        return redirect(url_for('index'))

    # Citizens can only view their own reports
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    return render_template('citizen/report_detail.html', report=report)

@app.route('/citizen/report', methods=['GET', 'POST'])
@login_required
def create_report():
    if current_user.role != 'citizen':
        flash('Access denied')
        return redirect(url_for('index'))

    form = ReportForm()
    if form.validate_on_submit():
        # Handle mandatory file upload
        photo_path = None
        if not form.photo.data:
            return jsonify({
                'success': False,
                'message': 'Photo is mandatory for all reports. Please upload an image.',
                'error_type': 'validation'
            })

        file = form.photo.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(photo_path)

            # Resize image for web display
            with Image.open(photo_path) as img:
                img.thumbnail((800, 600))
                img.save(photo_path)
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid file format. Please upload a valid image (JPG, PNG, JPEG, GIF).',
                'error_type': 'validation'
            })

        report = Report(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            severity=form.severity.data,
            latitude=float(form.latitude.data) if form.latitude.data else None,
            longitude=float(form.longitude.data) if form.longitude.data else None,
            address=form.address.data,
            postal_code=form.postal_code.data,
            photo_path=photo_path,
            is_anonymous=form.is_anonymous.data,
            user_id=current_user.id
        )
        db.session.add(report)
        db.session.commit()

        # Add points for submitting a report
        CitizenPoints.add_points(current_user.id, 10, 'report_submitted')

        # Create maintenance ticket automatically
        ticket = MaintenanceTicket(
            ticket_number=generate_ticket_number(),
            report_id=report.id,
            priority=form.severity.data
        )
        db.session.add(ticket)
        db.session.commit()

        # Return JSON response for AJAX handling with success popup
        return jsonify({
            'success': True,
            'message': 'Report submitted successfully!',
            'report_id': report.id,
            'redirect_url': url_for('view_citizen_report', report_id=report.id),
            'dashboard_url': url_for('citizen_dashboard')
        })

    return render_template('citizen/report.html', form=form)

@app.route('/citizen/nearby-reports/<int:report_id>')
@login_required
def view_nearby_reports(report_id):
    if current_user.role != 'citizen':
        flash('Access denied')
        return redirect(url_for('index'))

    # Get the current report
    current_report = Report.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()

    # Find nearby reports within 1km radius from the last week
    from datetime import timedelta
    from sqlalchemy import func, and_

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # Calculate distance using Haversine formula (approximate for small distances)
    # 1 degree ≈ 111km, so 1km ≈ 0.009 degrees
    lat_range = 0.009
    lng_range = 0.009

    nearby_reports = Report.query.filter(
        and_(
            Report.id != report_id,
            Report.created_at >= one_week_ago,
            Report.latitude.between(current_report.latitude - lat_range, current_report.latitude + lat_range),
            Report.longitude.between(current_report.longitude - lng_range, current_report.longitude + lng_range),
            Report.status != 'rejected'
        )
    ).all()

    # Get user's existing votes
    user_votes = {vote.report_id for vote in Vote.query.filter_by(user_id=current_user.id).all()}

    return render_template('citizen/nearby_reports.html',
                         current_report=current_report,
                         nearby_reports=nearby_reports,
                         user_votes=user_votes)

@app.route('/citizen/vote/<int:report_id>', methods=['POST'])
@login_required
def vote_for_report(report_id):
    if current_user.role != 'citizen':
        return jsonify({'error': 'Access denied'}), 403

    report = Report.query.get_or_404(report_id)

    # Check if user already voted for this report
    existing_vote = Vote.query.filter_by(user_id=current_user.id, report_id=report_id).first()

    if existing_vote:
        # Remove vote (toggle)
        db.session.delete(existing_vote)
        CitizenPoints.add_points(current_user.id, -2, 'vote_removed')  # Deduct points
        action = 'removed'
    else:
        # Add vote
        vote = Vote(user_id=current_user.id, report_id=report_id)
        db.session.add(vote)
        CitizenPoints.add_points(current_user.id, 2, 'vote_cast')  # Add points
        action = 'added'

    db.session.commit()

    # Get updated vote count
    vote_count = Vote.query.filter_by(report_id=report_id).count()

    return jsonify({
        'success': True,
        'action': action,
        'vote_count': vote_count
    })

@app.route('/citizen/leaderboard')
@login_required
def citizen_leaderboard():
    if current_user.role != 'citizen':
        flash('Access denied')
        return redirect(url_for('index'))

    # Get top citizens by points
    top_citizens = db.session.query(
        CitizenPoints, User
    ).join(User).order_by(CitizenPoints.points.desc()).limit(50).all()

    # Get current user's rank
    user_rank = None
    current_user_points = CitizenPoints.query.filter_by(user_id=current_user.id).first()
    if current_user_points:
        higher_points = CitizenPoints.query.filter(
            CitizenPoints.points > current_user_points.points
        ).count()
        user_rank = higher_points + 1

    return render_template('citizen/leaderboard.html',
                         top_citizens=top_citizens,
                         user_rank=user_rank)

@app.route('/authority/dashboard')
@login_required
def authority_dashboard():
    if current_user.role != 'authority':
        return redirect(url_for('citizen_dashboard'))

    # Get statistics
    total_reports = Report.query.count()
    pending_reports = Report.query.filter(Report.status.in_(['reported', 'verified'])).count()
    in_progress = Report.query.filter_by(status='in_progress').count()
    completed = Report.query.filter_by(status='completed').count()

    # Get recent reports
    recent_reports = Report.query.order_by(Report.created_at.desc()).limit(10).all()

    # Convert recent reports to dictionaries for JSON serialization
    recent_reports_data = []
    for report in recent_reports:
        recent_reports_data.append({
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'severity': report.severity,
            'status': report.status,
            'created_at': report.created_at.isoformat(),
            'reporter_username': 'Anonymous' if report.is_anonymous else (report.reporter.username if report.reporter else 'Anonymous'),
            'photo_path': report.photo_path.replace('\\', '/') if report.photo_path else None
        })

    return render_template('authority/dashboard.html',
                         total_reports=total_reports,
                         pending_reports=pending_reports,
                         in_progress=in_progress,
                         completed=completed,
                         recent_reports=recent_reports,
                         recent_reports_data=recent_reports_data)

@app.route('/authority/analytics')
@login_required
def analytics_dashboard():
    if current_user.role != 'authority':
        flash('Access denied')
        return redirect(url_for('index'))

    # Category statistics
    category_stats = db.session.query(
        Report.category,
        db.func.count(Report.id).label('count')
    ).group_by(Report.category).all()

    # Status statistics
    status_stats = db.session.query(
        Report.status,
        db.func.count(Report.id).label('count')
    ).group_by(Report.status).all()

    # Severity statistics
    severity_stats = db.session.query(
        Report.severity,
        db.func.count(Report.id).label('count')
    ).group_by(Report.severity).all()

    # Monthly statistics for the last 12 months
    from datetime import datetime, timedelta
    import calendar

    # Get data for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    monthly_data = db.session.query(
        db.func.strftime('%Y-%m', Report.created_at).label('month'),
        db.func.count(Report.id).label('count')
    ).filter(
        Report.created_at >= start_date
    ).group_by(
        db.func.strftime('%Y-%m', Report.created_at)
    ).order_by(
        db.func.strftime('%Y-%m', Report.created_at)
    ).all()

    # Format monthly data for chart
    monthly_stats = []
    for month_data in monthly_data:
        year, month = month_data.month.split('-')
        month_name = calendar.month_abbr[int(month)] + ' ' + year
        monthly_stats.append({
            'month': month_name,
            'count': month_data.count
        })

    # Calculate average response time (completed reports only)
    completed_reports = Report.query.filter_by(status='completed').all()
    total_response_time = 0
    response_count = 0

    for report in completed_reports:
        # Find the completion date from status updates
        completion_update = StatusUpdate.query.filter_by(
            report_id=report.id,
            status='completed'
        ).first()

        if completion_update:
            response_time = (completion_update.created_at - report.created_at).days
            total_response_time += response_time
            response_count += 1

    avg_response_time = total_response_time / response_count if response_count > 0 else 0

    # Convert query results to list of dictionaries for JSON serialization
    category_stats_list = [{'category': item.category, 'count': item.count} for item in category_stats]
    status_stats_list = [{'status': item.status, 'count': item.count} for item in status_stats]
    severity_stats_list = [{'severity': item.severity, 'count': item.count} for item in severity_stats]

    return render_template('authority/analytics.html',
                         category_stats=category_stats_list,
                         status_stats=status_stats_list,
                         severity_stats=severity_stats_list,
                         monthly_stats=monthly_stats,
                         avg_response_time=avg_response_time)

@app.route('/authority/reports')
@login_required
def view_reports():
    if current_user.role != 'authority':
        flash('Access denied')
        return redirect(url_for('index'))

    status_filter = request.args.get('status', 'all')
    category_filter = request.args.get('category', 'all')

    query = Report.query

    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if category_filter != 'all':
        query = query.filter_by(category=category_filter)

    reports = query.order_by(Report.created_at.desc()).all()

    return render_template('authority/reports.html', reports=reports,
                         status_filter=status_filter, category_filter=category_filter)

@app.route('/authority/report/<int:report_id>')
@login_required
def view_report_detail(report_id):
    if current_user.role != 'authority':
        flash('Access denied')
        return redirect(url_for('index'))

    report = Report.query.get_or_404(report_id)
    # Get all authority users for the assigned to dropdown
    authority_users = User.query.filter_by(role='authority').all()
    return render_template('authority/report_detail.html', report=report, authority_users=authority_users)

@app.route('/authority/update_status/<int:report_id>', methods=['POST'])
@login_required
def update_report_status(report_id):
    if current_user.role != 'authority':
        return jsonify({'error': 'Access denied'}), 403

    report = Report.query.get_or_404(report_id)
    old_status = report.status

    # Handle both JSON and form data
    if request.is_json:
        new_status = request.json.get('status')
        comment = request.json.get('comment', '')
        image_file = None
        # For JSON requests, image is mandatory for all status updates
        return jsonify({'error': 'Image upload is mandatory for all status updates. Please use the form interface.'}), 400
    else:
        # Handle form data with file uploads
        new_status = request.form.get('status')
        comment = request.form.get('comment', '')
        image_file = request.files.get('image')

    # Validate that image is provided for all status updates
    if not image_file or not image_file.filename:
        return jsonify({'error': 'Photo upload is mandatory for all status updates'}), 400

    # Validate status flow
    valid_transitions = {
        'reported': ['verified', 'rejected'],
        'verified': ['in_progress'],
        'in_progress': ['completed'],
        'completed': [],
        'rejected': []
    }

    if new_status not in valid_transitions.get(old_status, []) and new_status != old_status:
        return jsonify({'error': f'Invalid status transition from {old_status} to {new_status}'}), 400

    if new_status in ['reported', 'verified', 'in_progress', 'completed', 'rejected']:
        report.status = new_status
        report.updated_at = datetime.utcnow()

        # Handle mandatory image upload
        image_path = None
        if image_file and image_file.filename:
            try:
                # Generate unique filename
                filename = str(uuid.uuid4()) + '_' + secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Resize and save image
                image = Image.open(image_file)
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                image.save(filepath, optimize=True, quality=85)

                image_path = filename
            except Exception as e:
                return jsonify({'error': f'Failed to process image: {str(e)}'}), 400

        # Create status update record
        status_update = StatusUpdate(
            report_id=report.id,
            status=new_status,
            comment=comment,
            image_path=image_path,
            updated_by_id=current_user.id
        )
        db.session.add(status_update)

        # Add points to citizen if report is verified
        if new_status == 'verified' and old_status != 'verified':
            CitizenPoints.add_points(report.user_id, 5, 'report_verified')

        # Update ticket completion if status is completed
        if new_status == 'completed' and report.ticket:
            report.ticket.actual_completion = datetime.utcnow()

        db.session.commit()

        # Send email notification to the citizen who reported the issue
        try:
            citizen = report.reporter
            if citizen and citizen.email and old_status != new_status:
                send_status_update_email(
                    email_notifier,
                    citizen.email,
                    'Anonymous' if report.is_anonymous else citizen.username,
                    str(report.id),
                    report.title,
                    old_status,
                    new_status,
                    comment,
                    current_user.username,
                    datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                    report.address or f"Lat: {report.latitude}, Lng: {report.longitude}"
                )
        except Exception as e:
            print(f"Failed to send status update email: {e}")
            # Don't fail the status update if email fails

        return jsonify({'success': True, 'message': 'Status updated successfully'})

    return jsonify({'error': 'Invalid status'}), 400

@app.route('/authority/edit_ticket/<int:report_id>', methods=['POST'])
@login_required
def edit_maintenance_ticket(report_id):
    if current_user.role != 'authority':
        return jsonify({'error': 'Access denied'}), 403

    report = Report.query.get_or_404(report_id)
    if not report.ticket:
        return jsonify({'error': 'No ticket found for this report'}), 400

    ticket = report.ticket
    data = request.json

    # Update ticket fields
    if 'assigned_to_id' in data:
        ticket.assigned_to_id = data['assigned_to_id'] if data['assigned_to_id'] else None
    if 'priority' in data:
        ticket.priority = data['priority']
    if 'estimated_cost' in data:
        ticket.estimated_cost = float(data['estimated_cost']) if data['estimated_cost'] else None
    if 'estimated_completion' in data:
        ticket.estimated_completion = datetime.strptime(data['estimated_completion'], '%Y-%m-%d') if data['estimated_completion'] else None
    if 'work_description' in data:
        ticket.work_description = data['work_description']
    if 'materials_used' in data:
        ticket.materials_used = data['materials_used']

    ticket.updated_at = datetime.utcnow()
    db.session.commit()

    # Send email notification to the citizen who reported the issue
    try:
        # Get the citizen who reported this issue
        citizen = report.user

        # Get assigned person name
        assigned_person = "Not assigned"
        if ticket.assigned_to_id:
            assigned_user = User.query.get(ticket.assigned_to_id)
            if assigned_user:
                assigned_person = assigned_user.username

        # Format dates and values for email
        estimated_completion_str = ticket.estimated_completion.strftime('%B %d, %Y') if ticket.estimated_completion else "Not specified"
        estimated_cost_str = f"${ticket.estimated_cost:,.2f}" if ticket.estimated_cost else "Not specified"
        update_date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')

        # Initialize email notifier
        notifier = EmailNotifier()
        notifier.configure_from_env()

        # Send maintenance ticket update email
        email_sent = send_maintenance_ticket_update_email(
            notifier=notifier,
            recipient_email=citizen.email,
            citizen_name='Anonymous' if report.is_anonymous else citizen.username,
            report_id=str(report.id),
            report_title=report.title,
            location=report.location,
            assigned_to=assigned_person,
            priority=ticket.priority,
            estimated_cost=estimated_cost_str,
            estimated_completion=estimated_completion_str,
            work_description=ticket.work_description or "Work details to be updated",
            materials_used=ticket.materials_used or "",
            updated_by=current_user.username,
            update_date=update_date_str
        )

        if email_sent:
            print(f"Maintenance ticket update email sent to {citizen.email}")
        else:
            print(f"Failed to send maintenance ticket update email to {citizen.email}")

    except Exception as e:
        print(f"Error sending maintenance ticket update email: {str(e)}")
        # Don't fail the request if email fails

    return jsonify({'success': True, 'message': 'Ticket updated successfully and citizen notified'})

@app.route('/track')
def track_report():
    """Public report tracking page"""
    form = ReportTrackingForm()
    return render_template('track_report.html', form=form)

@app.route('/track-report/<int:report_id>')
def track_report_status(report_id):
    """Track a specific report by ID"""
    report = Report.query.get_or_404(report_id)

    # Get status updates
    status_updates = StatusUpdate.query.filter_by(report_id=report_id).order_by(StatusUpdate.created_at.desc()).all()

    # Get maintenance tickets
    maintenance_tickets = MaintenanceTicket.query.filter_by(report_id=report_id).all()

    # Get vote count
    vote_count = Vote.query.filter_by(report_id=report_id).count()

    return render_template('track_report_result.html',
                         report=report,
                         status_updates=status_updates,
                         maintenance_tickets=maintenance_tickets,
                         vote_count=vote_count)

@app.route('/api/check_duplicates', methods=['POST'])
@login_required
def check_duplicates():
    """Check for existing reports with same category and postal code"""
    try:
        data = request.get_json()
        category = data.get('category')
        postal_code = data.get('postal_code')

        if not category or not postal_code:
            return jsonify({
                'success': False,
                'message': 'Category and postal code are required'
            })

        # Find reports with same category and postal code that are not completed or rejected
        existing_reports = Report.query.filter(
            Report.category == category,
            Report.postal_code == postal_code,
            Report.status.notin_(['completed', 'rejected'])
        ).order_by(Report.created_at.desc()).all()

        reports_data = []
        for report in existing_reports:
            # Get vote count for each report
            vote_count = Vote.query.filter_by(report_id=report.id).count()

            # Check if current user has voted
            user_voted = False
            if current_user.is_authenticated:
                user_voted = Vote.query.filter_by(
                    user_id=current_user.id,
                    report_id=report.id
                ).first() is not None

            # Determine reporter name based on anonymous setting
            reporter_name = "Anonymous" if report.is_anonymous else report.reporter.username

            reports_data.append({
                'id': report.id,
                'title': report.title,
                'description': report.description,
                'category': report.category,
                'severity': report.severity,
                'status': report.status,
                'photo_path': report.photo_path,
                'address': report.address,
                'created_at': report.created_at.strftime('%B %d, %Y at %I:%M %p'),
                'vote_count': vote_count,
                'user_voted': user_voted,
                'reporter_name': reporter_name
            })

        return jsonify({
            'success': True,
            'reports': reports_data,
            'count': len(reports_data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error checking duplicates: {str(e)}'
        })

@app.route('/api/nearby-reports')
def get_nearby_reports():
    """API endpoint to get nearby reports for a given location with duplicate detection"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    category = request.args.get('category', type=str)
    exclude_duplicates = request.args.get('exclude_duplicates', type=bool, default=False)

    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Find nearby reports within 1km radius from the last week
    from datetime import timedelta
    from sqlalchemy import func, and_
    import math

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # Calculate distance using Haversine formula (approximate for small distances)
    # 1 degree ≈ 111km, so 1km ≈ 0.009 degrees
    lat_range = 0.009
    lng_range = 0.009

    nearby_reports = Report.query.filter(
        and_(
            Report.created_at >= one_week_ago,
            Report.latitude.between(lat - lat_range, lat + lat_range),
            Report.longitude.between(lng - lng_range, lng + lng_range),
            Report.status != 'rejected',
            Report.status != 'completed',
            Report.category == category
        )
    ).all()

    # Check for exact duplicates (same category, very close coordinates, not completed)
    duplicate_report = None
    if not exclude_duplicates:
        exact_match_threshold = 0.0005  # Approximately 50 meters

        for report in nearby_reports:
            # Check if this is an exact duplicate (very close location)
            if (abs(report.latitude - lat) <= exact_match_threshold and
                abs(report.longitude - lng) <= exact_match_threshold):
                duplicate_report = {
                    'id': report.id,
                    'title': report.title,
                    'description': report.description,
                    'category': report.category,
                    'severity': report.severity,
                    'status': report.status,
                    'location': report.address,
                    'postal_code': report.postal_code,
                    'photo_path': f"/static/{report.photo_path.replace(os.sep, '/')}" if report.photo_path else None,
                    'created_at': report.created_at.strftime('%Y-%m-%d %H:%M'),
                    'reporter_username': 'Anonymous' if report.is_anonymous else (report.reporter.username if report.reporter else 'Anonymous')
                }
                break

        # If duplicate found, return it separately
        if duplicate_report:
            return jsonify({
                'duplicate_found': True,
                'duplicate_report': duplicate_report,
                'reports': []
            })

    # Convert to JSON format with distance calculation
    reports_data = []
    for report in nearby_reports:
        # Calculate accurate distance using Haversine formula
        def haversine_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Earth's radius in kilometers
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat/2) * math.sin(dlat/2) +
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                 math.sin(dlon/2) * math.sin(dlon/2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        distance = haversine_distance(lat, lng, report.latitude, report.longitude)

        # Only include reports within 1km
        if distance <= 1.0:
            # Get vote count
            vote_count = Vote.query.filter_by(report_id=report.id).count()

            reports_data.append({
                'id': report.id,
                'title': report.title,
                'description': report.description,
                'category': report.category,
                'severity': report.severity,
                'status': report.status,
                'location': report.address,
                'postal_code': report.postal_code,
                'photo_path': f"/static/{report.photo_path.replace(os.sep, '/')}" if report.photo_path else None,
                'vote_count': vote_count,
                'created_at': report.created_at.strftime('%Y-%m-%d %H:%M'),
                'distance': round(distance, 2),
                'same_category': report.category == category if category else False,
                'reporter_username': 'Anonymous' if report.is_anonymous else (report.reporter.username if report.reporter else 'Anonymous')
            })

    # Smart sorting: same category first, then by distance
    def sort_key(report):
        # Primary sort: same category (0 for same, 1 for different)
        category_priority = 0 if report['same_category'] else 1
        # Secondary sort: distance
        return (category_priority, report['distance'])

    reports_data.sort(key=sort_key)

    return jsonify({
        'duplicate_found': False,
        'duplicate_report': None,
        'reports': reports_data
    })

@app.route('/api/reports/map')
def get_reports_for_map():
    # Filter reports that have valid coordinates and are not rejected
    reports = Report.query.filter(
        Report.status != 'rejected',
        Report.latitude.isnot(None),
        Report.longitude.isnot(None)
    ).all()
    reports_data = []

    for report in reports:
        # Additional validation to ensure coordinates are valid numbers
        if report.latitude is not None and report.longitude is not None:
            try:
                lat = float(report.latitude)
                lng = float(report.longitude)
                # Check if coordinates are within valid ranges
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    reports_data.append({
                        'id': report.id,
                        'title': report.title,
                        'category': report.category,
                        'severity': report.severity,
                        'status': report.status,
                        'latitude': lat,
                        'longitude': lng,
                        'address': report.address,
                        'postal_code': report.postal_code,
                        'created_at': report.created_at.isoformat(),
                        'photo_path': report.photo_path.replace('\\', '/') if report.photo_path else None,
                        'reporter_username': 'Anonymous' if report.is_anonymous else (report.reporter.username if report.reporter else 'Anonymous')
                    })
            except (ValueError, TypeError):
                # Skip reports with invalid coordinate values
                continue

    return jsonify(reports_data)

@app.route('/api/reports/<int:report_id>/votes', methods=['POST'])
@login_required
def toggle_vote(report_id):
    """Toggle vote for a report"""
    if current_user.role != 'citizen':
        return jsonify({'error': 'Only citizens can vote'}), 403

    report = Report.query.get_or_404(report_id)

    # Check if user already voted
    existing_vote = Vote.query.filter_by(user_id=current_user.id, report_id=report_id).first()

    if existing_vote:
        # Remove vote
        db.session.delete(existing_vote)
        # Remove points from citizen
        CitizenPoints.add_points(current_user.id, -1, 'vote_removed')
        voted = False
    else:
        # Add vote
        new_vote = Vote(user_id=current_user.id, report_id=report_id)
        db.session.add(new_vote)
        # Add points to citizen
        CitizenPoints.add_points(current_user.id, 1, 'vote_cast')
        voted = True

    db.session.commit()

    # Get updated vote count
    vote_count = Vote.query.filter_by(report_id=report_id).count()

    return jsonify({
        'success': True,
        'voted': voted,
        'vote_count': vote_count
    })

@app.route('/api/reports/<int:report_id>')
@login_required
def get_report_details(report_id):
    """Get detailed information about a specific report"""
    try:
        report = Report.query.get_or_404(report_id)

        # Get vote count
        vote_count = Vote.query.filter_by(report_id=report.id).count()

        # Check if current user has voted
        user_voted = False
        if current_user.is_authenticated:
            user_voted = Vote.query.filter_by(
                user_id=current_user.id,
                report_id=report.id
            ).first() is not None

        # Determine reporter name based on anonymous setting
        reporter_name = "Anonymous" if report.is_anonymous else report.reporter.username

        return jsonify({
            'success': True,
            'report': {
                'id': report.id,
                'title': report.title,
                'description': report.description,
                'category': report.category,
                'severity': report.severity,
                'status': report.status,
                'photo_path': report.photo_path,
                'address': report.address,
                'postal_code': report.postal_code,
                'latitude': report.latitude,
                'longitude': report.longitude,
                'created_at': report.created_at.strftime('%B %d, %Y at %I:%M %p'),
                'vote_count': vote_count,
                'user_voted': user_voted,
                'reporter_name': reporter_name
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching report details: {str(e)}'
        })

@app.route('/api/vote', methods=['POST'])
@login_required
def vote_report():
    """Vote for a report"""
    try:
        data = request.get_json()
        report_id = data.get('report_id')

        if not report_id:
            return jsonify({
                'success': False,
                'message': 'Report ID is required'
            })

        report = Report.query.get_or_404(report_id)

        # Check if user already voted
        existing_vote = Vote.query.filter_by(
            user_id=current_user.id,
            report_id=report_id
        ).first()

        if existing_vote:
            return jsonify({
                'success': False,
                'message': 'You have already voted for this report'
            })

        # Create new vote
        vote = Vote(user_id=current_user.id, report_id=report_id)
        db.session.add(vote)
        db.session.commit()

        # Add points for voting
        CitizenPoints.add_points(current_user.id, 2, 'vote_cast')

        return jsonify({
            'success': True,
            'message': 'Vote added successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error voting: {str(e)}'
        })

@app.route('/api/public-reports')
def api_public_reports():
    """API endpoint for map data"""
    reports = Report.query.filter(
        Report.status.notin_(['rejected']),
        Report.latitude.isnot(None),
        Report.longitude.isnot(None)
    ).all()

    reports_data = []
    for report in reports:
        reports_data.append({
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'status': report.status,
            'severity': report.severity,
            'latitude': float(report.latitude),
            'longitude': float(report.longitude),
            'created_at': report.created_at.isoformat()
        })

    return jsonify(reports_data)

@app.route('/public-reports')
def public_reports():
    """Public reports page showing all non-rejected reports"""
    # Get all reports that are not rejected
    reports = Report.query.filter(Report.status.notin_(['rejected'])).order_by(Report.created_at.desc()).all()

    # Get vote counts and user votes
    vote_counts = {}
    user_votes = set()

    for report in reports:
        vote_count = Vote.query.filter_by(report_id=report.id).count()
        vote_counts[report.id] = vote_count

        if current_user.is_authenticated:
            user_vote = Vote.query.filter_by(user_id=current_user.id, report_id=report.id).first()
            if user_vote:
                user_votes.add(report.id)

    # Add reporter information with anonymous handling as temporary attribute
    for report in reports:
        report.reporter_name = "Anonymous" if report.is_anonymous else report.reporter.username

    # Calculate statistics
    total_reports = len(reports)
    completed_reports = len([r for r in reports if r.status == 'completed'])
    completion_rate = (completed_reports / total_reports * 100) if total_reports > 0 else 0

    return render_template('public_reports.html',
                         reports=reports,
                         vote_counts=vote_counts,
                         user_votes=user_votes,
                         total_reports=total_reports,
                         completed_reports=completed_reports,
                         completion_rate=completion_rate)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        admin = User.query.filter_by(email='admin@roadmaintenance.com').first()
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@roadmaintenance.com',
                password_hash=generate_password_hash('admin123'),
                role='authority',
                department='Municipal Corporation'
            )
            db.session.add(admin_user)
            db.session.commit()
if __name__ == '__main__':
    app.run(debug=True, host='192.168.31.138', port=5000)
