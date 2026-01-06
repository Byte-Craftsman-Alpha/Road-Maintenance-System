# OTP Verification & Authority Registration Setup Guide

## New Features Added

### 1. OTP Verification for Registration
- All new users (both citizens and authorities) must verify their email with a 6-digit OTP
- OTP is valid for 10 minutes
- Users can resend OTP if needed
- Registration is only completed after successful OTP verification

### 2. Authority Registration Password Protection
- Authority users need a special password to register
- Default password: `ADMIN2025!`
- This prevents unauthorized authority registrations

## Setup Instructions

### 1. Email Configuration

To enable OTP functionality, you need to configure Gmail SMTP:

1. **Create a Gmail App Password:**
   - Go to your Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for "Mail"
   - Copy the 16-character password

2. **Set Environment Variables:**
   ```bash
   # Option 1: Create .env file
   cp .env.example .env
   # Edit .env with your credentials
   
   # Option 2: Set system environment variables
   set EMAIL_ADDRESS=your-email@gmail.com
   set EMAIL_PASSWORD=your-16-character-app-password
   ```

### 2. Database Migration

The new features require database updates:

```bash
# Delete existing database to recreate with new schema
del instance\road_maintenance.db

# Run the application to create new tables
python app.py
```

### 3. Configuration

Update these settings in `app.py` if needed:

```python
# Authority registration password (change in production)
app.config['AUTHORITY_REGISTRATION_PASSWORD'] = 'ADMIN2025!'

# Email settings (loaded from environment variables)
app.config['EMAIL_ADDRESS'] = os.getenv('EMAIL_ADDRESS')
app.config['EMAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
```

## How It Works

### Registration Flow

1. **User Registration:**
   - User fills registration form
   - For authority users: must provide authority password
   - System validates input and sends OTP to email
   - User redirected to OTP verification page

2. **OTP Verification:**
   - User enters 6-digit OTP received via email
   - System verifies OTP and creates user account
   - User account is marked as email_verified=True
   - User can now login normally

3. **Authority Protection:**
   - Authority registration requires special password
   - Default password: `ADMIN2025!`
   - Only users with this password can register as authorities

### New Database Tables

- **OTPVerification:** Stores OTP codes with expiration
- **User.email_verified:** Boolean field to track email verification

### New Routes

- `/register` - Enhanced with OTP sending
- `/verify-otp` - OTP verification page
- `/resend-otp` - AJAX endpoint to resend OTP

## Testing

### Test Citizen Registration:
1. Go to `/register`
2. Fill form with role "Citizen"
3. Submit to receive OTP
4. Check email and enter OTP
5. Complete registration

### Test Authority Registration:
1. Go to `/register`
2. Fill form with role "Authority"
3. Enter authority password: `ADMIN2025!`
4. Submit to receive OTP
5. Check email and enter OTP
6. Complete registration

### Test Authority Password Protection:
1. Try registering as authority without password
2. Try with wrong password
3. Should see error messages

## Security Features

- **OTP Expiration:** 10-minute validity
- **One-time Use:** OTP becomes invalid after use
- **Email Verification:** Required for all registrations
- **Authority Protection:** Password-protected authority registration
- **Session Management:** Registration data stored in session temporarily

## Troubleshooting

### Email Not Sending:
- Check Gmail App Password is correct
- Verify 2FA is enabled on Gmail account
- Check environment variables are set
- Look for error messages in console

### OTP Not Working:
- Check OTP hasn't expired (10 minutes)
- Verify email address is correct
- Try resending OTP
- Check spam folder

### Authority Registration Failing:
- Verify authority password is correct: `ADMIN2025!`
- Check case sensitivity
- Ensure all required fields are filled

## Production Deployment

Before deploying to production:

1. **Change Default Passwords:**
   ```python
   app.config['AUTHORITY_REGISTRATION_PASSWORD'] = 'your-secure-password'
   app.config['SECRET_KEY'] = 'your-secure-secret-key'
   ```

2. **Secure Environment Variables:**
   - Use proper environment variable management
   - Don't commit .env files to version control

3. **Email Configuration:**
   - Consider using dedicated email service
   - Set up proper email templates
   - Configure email rate limiting

## Files Modified/Added

### Modified:
- `models.py` - Added OTPVerification model and email_verified field
- `forms.py` - Added OTPVerificationForm and authority_password field
- `app.py` - Enhanced registration flow with OTP
- `templates/auth/register.html` - Added authority password field
- `requirements.txt` - Added email dependencies

### Added:
- `templates/auth/verify_otp.html` - OTP verification page
- `.env.example` - Environment variables template
- `OTP_SETUP_GUIDE.md` - This setup guide
