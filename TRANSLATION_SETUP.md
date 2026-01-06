# Hindi Translation Setup Guide

This guide explains how to set up and troubleshoot Hindi translations in the Road Maintenance System Flask application.

## Overview

The application now supports multiple languages including Hindi (हिन्दी), with proper Unicode handling and automatic language detection.

## Fixed Issues

### 1. Locale Selector Function
- **Problem**: The `get_user_locale()` function was hardcoded to return `'en'`
- **Solution**: Implemented proper `@babel.localeselector` decorator with intelligent language selection:
  1. User's manually selected language (stored in session)
  2. User's preferred language (if logged in)
  3. Browser's Accept-Language header
  4. Default fallback to English

### 2. Translation Directory Path
- **Problem**: Babel was configured to look for translations in `'V4/translations'`
- **Solution**: Updated to correct path `'translations'`

### 3. Unicode Handling
- **Problem**: Unicode characters were not properly handled in JSON responses
- **Solution**: Added Flask configuration:
  ```python
  app.config['JSON_AS_ASCII'] = False
  app.config['JSON_SORT_KEYS'] = False
  ```

## Files Created/Modified

### 1. `app.py` - Main Application
- Fixed locale selector function
- Added proper Babel configuration
- Added Unicode support for JSON responses

### 2. `compile_translations.py` - Translation Compiler
- Compiles `.po` files to `.mo` files with proper UTF-8 encoding
- Handles all languages in the translations directory
- Provides detailed error reporting

### 3. `test_translations.py` - Translation Tester
- Tests Hindi translations in isolation
- Verifies translation file existence and integrity
- Provides debugging information

## How to Use

### 1. Compile Translations
Run the compilation script to generate `.mo` files:
```bash
python compile_translations.py
```

### 2. Test Translations
Verify Hindi translations are working:
```bash
python test_translations.py
```

### 3. Switch Languages
Users can switch languages using the language selector in the navigation bar:
- 🇺🇸 English
- 🇮🇳 हिन्दी (Hindi)
- 🇪🇸 Español
- 🇫🇷 Français

## Language Detection Priority

The application uses the following priority order for language selection:

1. **Session Language**: If user manually selected a language
2. **User Preference**: If logged-in user has a preferred language
3. **Browser Language**: Based on Accept-Language header
4. **Default**: Falls back to English

## Translation Files Structure

```
translations/
├── en/
│   └── LC_MESSAGES/
│       ├── messages.po
│       └── messages.mo
├── hi/
│   └── LC_MESSAGES/
│       ├── messages.po  (Hindi translations)
│       └── messages.mo  (Compiled binary)
├── es/
│   └── LC_MESSAGES/
│       ├── messages.po
│       └── messages.mo
└── fr/
    └── LC_MESSAGES/
        ├── messages.po
        └── messages.mo
```

## Adding New Translations

### 1. Extract Messages
```bash
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
```

### 2. Update Existing Translations
```bash
pybabel update -i messages.pot -d translations
```

### 3. Initialize New Language
```bash
pybabel init -i messages.pot -d translations -l <language_code>
```

### 4. Compile Translations
```bash
python compile_translations.py
```

## Troubleshooting

### Problem: Hindi text appears as question marks or boxes
**Solution**: Ensure your system has Hindi fonts installed and your terminal/browser supports UTF-8.

### Problem: Translations not appearing
**Causes & Solutions**:
1. **Missing .mo files**: Run `python compile_translations.py`
2. **Wrong locale**: Check browser language settings or manually switch language
3. **Cache issues**: Clear browser cache and restart Flask app

### Problem: Unicode errors in console
**Solution**: Set environment variable:
```bash
set PYTHONIOENCODING=utf-8  # Windows
export PYTHONIOENCODING=utf-8  # Linux/Mac
```

### Problem: Language not switching
**Causes & Solutions**:
1. **Session issues**: Clear browser cookies
2. **Missing route**: Ensure `/set_language/<language>` route exists
3. **Invalid language code**: Check that language exists in `app.config['LANGUAGES']`

## Testing Checklist

- [ ] Run `python compile_translations.py` successfully
- [ ] Run `python test_translations.py` shows Hindi translations
- [ ] Language selector appears in navigation
- [ ] Clicking Hindi option switches interface language
- [ ] Hindi text displays correctly (not as boxes/question marks)
- [ ] Form validation messages appear in Hindi
- [ ] Flash messages appear in Hindi

## Technical Details

### Babel Configuration
```python
app.config['LANGUAGES'] = {
    'en': 'English',
    'hi': 'हिन्दी',
    'es': 'Español',
    'fr': 'Français'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
```

### Template Usage
```html
<!-- In templates, use the _() function for translations -->
<h1>{{ _('Road Maintenance System') }}</h1>
<p>{{ _('Dashboard') }}</p>
```

### Python Code Usage
```python
from flask_babel import _
flash(_('Report submitted successfully!'))
```

## Browser Support

The Hindi translations work in all modern browsers that support:
- UTF-8 encoding
- Unicode font rendering
- Devanagari script display

Tested browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Notes

- Translation files are cached by Flask-Babel
- `.mo` files are binary and load faster than `.po` files
- Language switching requires a page reload
- No performance impact on English-only users
