# Road Maintenance System

A comprehensive digital platform that connects citizen feedback with municipal road maintenance efforts, enabling faster response times, transparency, and long-term infrastructure improvement. Built with Python Flask and modern web technologies, this system bridges the gap between citizens and local authorities for efficient road maintenance management.

## Latest Updates (v2.2.0)

### 🌍 Multilingual Support (NEW)
- **Flask-Babel Integration**: Complete internationalization (i18n) support
- **4 Languages Supported**: English, Hindi (हिन्दी), Spanish (Español), French (Français)
- **Dynamic Language Switching**: Session-based language persistence with browser preference detection
- **Localized UI**: Translated navigation, forms, messages, and system text
- **Language Selector**: Intuitive dropdown with flag emojis in navbar

### 🔧 Enhanced System Features
- **Image Upload for Status Updates**: Mandatory image requirement for completed status
- **Advanced Status Flow Validation**: Proper workflow enforcement (reported → verified/rejected → in-progress → completed)
- **Public Report Tracking**: Track any report status by ID without login required
- **Enhanced Voting System**: Real-time vote counts with points system integration
- **Improved Email Notifications**: Comprehensive updates for ticket generation and status changes
- **Image Viewing in Reports**: Modal popups for image viewing with fallback messages
- **Form Validation Enhancements**: Better error handling and user feedback

### 🚀 Technical Improvements
- **Flask-Babel 4.0.0**: Modern internationalization framework
- **UTF-8 Encoding Support**: Proper handling of multilingual content
- **Enhanced Form Processing**: Support for both JSON and form data in status updates
- **Database Migration Scripts**: Automated schema updates for new features
- **Improved Error Handling**: Better Unicode and encoding error management
- **Performance Optimizations**: Faster translation loading and caching

## Key Features

### For Citizens
- **Easy Reporting**: Report road issues with GPS location and photo upload
- **Real-time Tracking**: Monitor the status of submitted reports with email notifications
- **Mobile-First Design**: Fully responsive interface optimized for all devices
- **Smart Location**: Automatic GPS detection with map integration
- **User Dashboard**: Interactive map showing all personal reports with status tracking
- **Nearby Reports**: View and vote on nearby issues within 3km radius
- **Community Voting**: Vote on other citizens' reports to prioritize issues
- **Leaderboard System**: Gamified points system for active community participation
- **Email Notifications**: Comprehensive email updates for all report changes
- **Report History**: Complete history of all your submitted reports with status changes
- **Photo Verification**: Upload multiple photos with each report for better documentation
- **Anonymous Reporting**: Option to submit reports anonymously while maintaining accountability
- **Public Report Tracking**: Track any report by ID without requiring login
- **Multilingual Interface**: Use the system in your preferred language

### For Authorities
- **Comprehensive Dashboard**: Centralized view with analytics, recent reports, and priority maps
- **Advanced Filtering**: Filter reports by status, category, severity, and date ranges
- **Automated Workflow**: Intelligent maintenance ticket generation and assignment
- **Priority Management**: Dynamic prioritization with visual severity indicators
- **Real-time Analytics**: Performance metrics, completion rates, and trend analysis
- **Status Updates with Images**: Upload completion photos and detailed comments
- **Team Management**: Assign tickets to authority users with email notifications
- **Bulk Operations**: Perform batch status updates with progress indicators
- **Interactive Maps**: Visual representation of all reports with severity-based markers
- **Custom Reports**: Generate and export detailed reports in multiple formats
- **Resource Allocation**: Tools to optimize team assignments and resource distribution
- **Audit Logs**: Comprehensive logging of all system activities for accountability
- **Multi-department Support**: Assign reports to different municipal departments
- **Multilingual Administration**: Manage system in multiple languages

### Transparency Features
- **Public Reports Page**: Public visibility of all reports and their status with voting
- **Interactive Maps**: Visual representation of reports across the city with clustering
- **Progress Tracking**: Real-time status updates for all stakeholders
- **Performance Metrics**: Completion rates and response time analytics
- **Vote Counts**: Community engagement metrics visible to authorities
- **Public Report Tracking**: Anyone can track report status using report ID
- **Multilingual Public Interface**: Public pages available in multiple languages

## Technology Stack

### Backend
- **Framework**: Python Flask 2.3.3
- **Database**: SQLite (Development) / PostgreSQL (Production-ready)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: Flask-Login with bcrypt hashing and JWT support
- **Internationalization**: Flask-Babel 4.0.0 with UTF-8 support
- **Email**: SMTP with OTP verification and HTML email templates
- **API**: RESTful API with rate limiting and request validation
- **File Storage**: Local filesystem with image processing and validation
- **Image Processing**: PIL/Pillow for image resizing and optimization

### Frontend
- **UI Framework**: Bootstrap 5.3 with custom CSS
- **Maps**: Leaflet.js with OpenStreetMap and marker clustering
- **Charts**: Chart.js for analytics and trend visualization
- **Responsive Design**: Mobile-first approach with touch-friendly interfaces
- **Interactive UI**: AJAX for dynamic updates, loading spinners, and real-time feedback
- **Image Handling**: Automatic resizing, fallback placeholders, and validation
- **Internationalization**: Dynamic language switching with session persistence
- **Accessibility**: WCAG 2.1 compliant with ARIA labels and keyboard navigation

### Internationalization & Localization
- **Flask-Babel**: Complete i18n framework integration
- **Language Support**: English, Hindi, Spanish, French
- **Translation Files**: Properly encoded .po/.mo files with UTF-8 support
- **Dynamic Switching**: Session-based language persistence
- **Browser Detection**: Automatic language detection from browser preferences
- **Template Integration**: Jinja2 template translation markers
- **Form Localization**: Translated form labels, placeholders, and validation messages

### Security & Communication
- **Authentication**: Email verification with OTP system and 2FA support
- **Authorization**: Role-based access control (Citizen/Authority/Admin)
- **Data Protection**: CSRF protection, input validation, SQL injection prevention
- **Secure File Uploads**: Image processing, validation, and virus scanning
- **Email System**: Comprehensive notification system with HTML templates
- **Password Security**: Bcrypt hashing with secure password reset and complexity requirements
- **Unicode Security**: Proper UTF-8 handling and encoding validation
- **Form Security**: Enhanced validation for multilingual input

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd road-maintenance-system
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize translations (if needed)**
   ```bash
   python clean_translations.py
   ```

6. **Initialize the database**
   ```bash
   python migrate_db.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - Use the language selector (🌐) in the navbar to switch languages

## Multilingual Features

### Supported Languages
- **🇺🇸 English** - Default language
- **🇮🇳 हिन्दी (Hindi)** - Complete Hindi translation
- **🇪🇸 Español (Spanish)** - Full Spanish localization
- **🇫🇷 Français (French)** - Complete French translation

### Language Switching
- **Navbar Selector**: Click the 🌐 globe icon to access language dropdown
- **Session Persistence**: Selected language persists across browser sessions
- **Browser Detection**: Automatic language detection from browser preferences
- **URL Parameters**: Support for ?lang=hi URL parameter for direct language setting

### Translation Coverage
- **Navigation Elements**: All menu items, buttons, and links
- **Form Labels**: Input fields, placeholders, and validation messages
- **System Messages**: Success, error, and informational messages
- **Dashboard Content**: Statistics, charts, and data labels
- **Email Templates**: Notification emails in user's preferred language
- **Public Pages**: Complete translation of public-facing content

## Default Login Credentials

### Admin Account
- **Email**: `admin@roadmaintenance.com`
- **Password**: `admin123`
- **Role**: Authority (Full access)

> **Note**: Change the default credentials after first login for security.

## User Roles & Capabilities

### Citizen Role
- **Registration & Authentication**: Email verification with OTP system
- **Report Submission**: Create detailed reports with photos, GPS location, and severity levels
- **Personal Dashboard**: Interactive map view of all personal reports with status tracking
- **Community Features**: Vote on nearby reports within 3km radius to prioritize issues
- **Leaderboard Participation**: Earn points for reporting, voting, and verified reports
- **Real-time Updates**: Email notifications for all status changes and ticket assignments
- **Mobile Experience**: Fully responsive interface optimized for mobile reporting
- **Public Tracking**: Track any report status using report ID
- **Multilingual Interface**: Use system in preferred language

### Authority Role
- **Advanced Dashboard**: Analytics overview with charts, recent reports, and priority maps
- **Report Management**: View, filter, and manage all citizen reports with advanced search
- **Status Control**: Update report statuses with mandatory images for completion
- **Ticket Assignment**: Assign maintenance tickets to team members with notifications
- **Bulk Operations**: Perform batch status updates with progress indicators
- **Analytics Access**: Performance metrics, completion rates, and trend analysis
- **Team Coordination**: Email notifications for assignments and status changes
- **Map Integration**: Interactive maps showing all reports with severity-based markers
- **Multilingual Administration**: Manage system in multiple languages

## Key Workflows

### 1. Enhanced Citizen Report Submission
1. Citizen registers with email verification (OTP system)
2. Selects preferred language from navbar dropdown
3. Uses GPS-enabled "Report Issue" form with photo upload
4. Provides detailed information: title, description, category, severity, location
5. System automatically creates maintenance ticket and assigns unique ID
6. Citizen receives email confirmation in their preferred language
7. Can view nearby reports within 3km and vote on priority issues
8. Tracks progress on personal dashboard with interactive map
9. Receives multilingual email notifications for all status changes

### 2. Advanced Authority Response Process
1. Authority receives email notification of new reports and assignments
2. Reviews reports on comprehensive dashboard with filtering options
3. Views report details with photos, location maps, and community votes
4. Updates status with mandatory image upload for completion
5. Assigns maintenance tickets to team members with email notifications
6. Uses bulk operations for efficient status management
7. Monitors analytics and performance metrics
8. Tracks completion through interactive maps and progress indicators
9. Manages system in preferred language

### 3. Public Transparency & Tracking
1. Anyone can visit public reports page to view all active issues
2. Public report tracking available by entering report ID
3. Citizens vote on reports to prioritize community issues
4. Real-time status updates visible to all stakeholders
5. Performance metrics and completion rates available for accountability
6. All public interfaces available in multiple languages
7. Vote counts displayed to authorities for priority decision-making

## File Structure

```
Road-Maintenance-System/
├── app.py                     # Main Flask application with i18n
├── models.py                  # Database models
├── forms.py                   # WTForms with validation
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── babel.cfg                 # Babel configuration
├── clean_translations.py     # Translation cleanup script
├── migrate_db.py             # Database migration script
├── .env.example              # Environment variables template
├── static/
│   ├── css/
│   │   └── custom.css        # Custom styling
│   └── uploads/              # User uploaded photos
├── templates/
│   ├── base.html             # Base template with i18n
│   ├── index.html            # Home page
│   ├── public_reports.html   # Public transparency page
│   ├── track_report.html     # Public tracking form
│   ├── track_report_result.html # Public tracking results
│   ├── auth/
│   │   ├── login.html        # Login page
│   │   └── register.html     # Registration page
│   ├── citizen/
│   │   ├── dashboard.html    # Citizen dashboard
│   │   ├── nearby_reports.html # Nearby reports with voting
│   │   ├── leaderboard.html  # Community leaderboard
│   │   └── report.html       # Report submission form
│   └── authority/
│       ├── dashboard.html    # Authority dashboard
│       ├── reports.html      # All reports view
│       ├── report_detail.html # Individual report details
│       └── analytics.html    # Analytics dashboard
└── translations/             # Internationalization files
    ├── en/LC_MESSAGES/       # English translations
    ├── hi/LC_MESSAGES/       # Hindi translations
    ├── es/LC_MESSAGES/       # Spanish translations
    └── fr/LC_MESSAGES/       # French translations
```

## API Endpoints

### Public APIs
- `GET /` - Home page with system overview
- `GET /public/reports` - Public transparency page with voting
- `GET /track` - Public report tracking form
- `GET /track/<id>` - Public report tracking results
- `POST /api/track` - API endpoint for report tracking
- `GET /set_language/<language>` - Language switching endpoint

### Authentication APIs
- `POST /login` - User authentication with email/password
- `POST /register` - User registration with email verification
- `POST /verify-otp` - OTP verification for registration
- `POST /resend-otp` - Resend OTP for verification
- `POST /forgot-password` - Initiate password reset with OTP
- `POST /reset-password` - Complete password reset with OTP verification
- `GET /logout` - User logout

### Citizen APIs
- `GET /citizen/dashboard` - Citizen dashboard with personal reports and map
- `GET /citizen/report/<id>` - View specific citizen report details
- `GET /citizen/report` - Report submission form
- `POST /citizen/report` - Submit new road maintenance report
- `GET /citizen/nearby-reports/<id>` - View nearby reports for voting
- `POST /api/reports/<id>/votes` - Toggle vote on community reports
- `GET /citizen/leaderboard` - Community leaderboard with points system

### Authority APIs
- `GET /authority/dashboard` - Authority dashboard with analytics and maps
- `GET /authority/reports` - View all reports with advanced filtering
- `GET /authority/report/<id>` - Detailed report view with ticket management
- `POST /authority/update_status/<id>` - Update report status with image upload
- `POST /authority/assign_ticket/<id>` - Assign maintenance tickets with email alerts
- `POST /authority/edit_ticket/<id>` - Edit maintenance ticket details
- `GET /authority/analytics` - Analytics dashboard with performance metrics

## Current System Status

### ✅ Fully Implemented Features
- **Complete Authentication System**: Email verification, OTP, password reset
- **Multilingual Support**: 4 languages with dynamic switching
- **Advanced Reporting**: GPS location, photo upload, severity classification
- **Enhanced Status Flow**: Proper workflow validation with image requirements
- **Community Engagement**: Voting system, leaderboard, points gamification
- **Real-time Notifications**: Comprehensive email system for all stakeholders
- **Interactive Maps**: Leaflet.js with clustering, severity markers, and filtering
- **Authority Dashboard**: Analytics, filtering, bulk operations, team management
- **Maintenance Tickets**: Automated generation, assignment, and tracking
- **Public Transparency**: Public reports page with voting and tracking
- **Image Handling**: Upload validation, resizing, and modal viewing
- **Public Report Tracking**: Track any report by ID without login

### 🔧 Technical Achievements
- **Flask-Babel Integration**: Complete internationalization framework
- **UTF-8 Encoding**: Proper multilingual content handling
- **Database Optimization**: Efficient queries, proper relationships, and indexing
- **Security Implementation**: CSRF protection, input validation, secure file handling
- **Email Templates**: Professional HTML emails for all notification types
- **Error Handling**: Graceful error management with user-friendly feedback
- **Performance**: Optimized loading times and responsive user interactions
- **Code Quality**: Clean architecture, proper separation of concerns

### 🌍 Multilingual Implementation
- **Translation Infrastructure**: Complete .po/.mo file system
- **Language Detection**: Browser preference and session persistence
- **UI Localization**: All interface elements translated
- **Form Validation**: Multilingual error messages and labels
- **Email Localization**: Notifications in user's preferred language
- **Public Interface**: Complete translation of public-facing pages

## Future Enhancements

### Planned Features
- [ ] Enhanced translation coverage for all system messages
- [ ] Push Notifications for mobile browsers
- [ ] SMS Alerts for critical updates in multiple languages
- [ ] Progressive Web App (PWA) capabilities
- [ ] Advanced ML-based report classification
- [ ] Social media integration for broader reach
- [ ] Third-party API integrations
- [ ] Contractor portal for work assignment
- [ ] Advanced analytics with predictive insights
- [ ] Mobile application for iOS/Android with multilingual support

### Multilingual Enhancements
- [ ] Additional language support (Arabic, German, Japanese)
- [ ] Right-to-left (RTL) language support
- [ ] Cultural localization (date formats, number formats)
- [ ] Voice input in multiple languages
- [ ] Automated translation for user-generated content

## Support

For technical support or questions about the system:
1. Check the documentation in this README
2. Review the code comments for implementation details
3. Test the system with the provided demo accounts
4. Use the language selector to test multilingual functionality

## License

This project is licensed under the terms of the MIT license. See `LICENSE`.

### Community

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
