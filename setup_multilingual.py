#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Multilingual Setup Script
Sets up translation directories for all 22 official Indian languages + English
"""

import os
import sys
import subprocess
from pathlib import Path

# All 23 languages (English + 22 Indian languages)
LANGUAGES = {
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
    'ne': 'नेपाली',           # Nepali
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

def create_translation_directories():
    """Create translation directory structure for all languages"""
    print("🏗️  Creating translation directories...")
    
    base_dir = Path('translations')
    base_dir.mkdir(exist_ok=True)
    
    created_count = 0
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code == 'en':  # Skip English as it's the source language
            continue
            
        lang_dir = base_dir / lang_code / 'LC_MESSAGES'
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        if not (lang_dir / 'messages.po').exists():
            created_count += 1
            print(f"   ✅ Created directory for {lang_name} ({lang_code})")
        else:
            print(f"   ℹ️  Directory already exists for {lang_name} ({lang_code})")
    
    print(f"\n📁 Translation directories ready for {len(LANGUAGES)-1} languages!")
    return created_count

def extract_messages():
    """Extract all translatable strings from templates and Python files"""
    print("\n🔍 Extracting translatable messages...")
    
    try:
        # Extract messages using pybabel
        cmd = [
            'pybabel', 'extract',
            '-F', 'babel.cfg',
            '-k', '_l',
            '-o', 'messages.pot',
            '.'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Successfully extracted messages to messages.pot")
            return True
        else:
            print(f"   ❌ Error extracting messages: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("   ⚠️  pybabel not found. Installing Babel...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Babel'])
            print("   ✅ Babel installed successfully")
            return extract_messages()  # Retry
        except Exception as e:
            print(f"   ❌ Failed to install Babel: {e}")
            return False

def create_babel_config():
    """Create babel.cfg configuration file"""
    babel_config = """[python: **.py]
[jinja2: **/templates/**.html]
"""
    
    with open('babel.cfg', 'w', encoding='utf-8') as f:
        f.write(babel_config)
    
    print("   ✅ Created babel.cfg configuration")

def initialize_po_files():
    """Initialize .po files for all languages"""
    print("\n📝 Initializing .po files for all languages...")
    
    if not os.path.exists('messages.pot'):
        print("   ❌ messages.pot not found. Run extract_messages() first.")
        return False
    
    initialized_count = 0
    
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code == 'en':  # Skip English
            continue
        
        po_file = f'translations/{lang_code}/LC_MESSAGES/messages.po'
        
        if not os.path.exists(po_file):
            try:
                cmd = [
                    'pybabel', 'init',
                    '-i', 'messages.pot',
                    '-d', 'translations',
                    '-l', lang_code
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ✅ Initialized {lang_name} ({lang_code})")
                    initialized_count += 1
                else:
                    print(f"   ❌ Failed to initialize {lang_name}: {result.stderr}")
                    
            except Exception as e:
                print(f"   ❌ Error initializing {lang_name}: {e}")
        else:
            print(f"   ℹ️  {lang_name} ({lang_code}) already exists")
    
    print(f"\n📄 Initialized {initialized_count} new .po files!")
    return True

def update_existing_po_files():
    """Update existing .po files with new messages"""
    print("\n🔄 Updating existing .po files...")
    
    if not os.path.exists('messages.pot'):
        print("   ❌ messages.pot not found.")
        return False
    
    updated_count = 0
    
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code == 'en':  # Skip English
            continue
        
        po_file = f'translations/{lang_code}/LC_MESSAGES/messages.po'
        
        if os.path.exists(po_file):
            try:
                cmd = [
                    'pybabel', 'update',
                    '-i', 'messages.pot',
                    '-d', 'translations',
                    '-l', lang_code
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ✅ Updated {lang_name} ({lang_code})")
                    updated_count += 1
                else:
                    print(f"   ❌ Failed to update {lang_name}: {result.stderr}")
                    
            except Exception as e:
                print(f"   ❌ Error updating {lang_name}: {e}")
    
    print(f"\n🔄 Updated {updated_count} .po files!")
    return True

def compile_translations():
    """Compile all .po files to .mo files"""
    print("\n⚙️  Compiling translations...")
    
    compiled_count = 0
    
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code == 'en':  # Skip English
            continue
        
        po_file = f'translations/{lang_code}/LC_MESSAGES/messages.po'
        
        if os.path.exists(po_file):
            try:
                cmd = [
                    'pybabel', 'compile',
                    '-d', 'translations',
                    '-l', lang_code
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ✅ Compiled {lang_name} ({lang_code})")
                    compiled_count += 1
                else:
                    print(f"   ❌ Failed to compile {lang_name}: {result.stderr}")
                    
            except Exception as e:
                print(f"   ❌ Error compiling {lang_name}: {e}")
    
    print(f"\n⚙️  Compiled {compiled_count} translation files!")
    return compiled_count > 0

def add_sample_translations():
    """Add sample translations for major languages"""
    print("\n🌐 Adding sample translations for major languages...")
    
    # Sample translations for common phrases
    sample_translations = {
        'bn': {  # Bengali
            'Road Maintenance System': 'রাস্তা রক্ষণাবেক্ষণ সিস্টেম',
            'Dashboard': 'ড্যাশবোর্ড',
            'Report Issue': 'সমস্যা রিপোর্ট করুন',
            'Login': 'লগইন করুন',
            'Register': 'নিবন্ধন করুন',
            'Submit': 'জমা দিন',
            'Cancel': 'বাতিল',
        },
        'ta': {  # Tamil
            'Road Maintenance System': 'சாலை பராமரிப்பு அமைப்பு',
            'Dashboard': 'டாஷ்போர்டு',
            'Report Issue': 'பிரச்சினையை தெரிவிக்கவும்',
            'Login': 'உள்நுழைக',
            'Register': 'பதிவு செய்க',
            'Submit': 'சமர்ப்பிக்கவும்',
            'Cancel': 'ரத்து செய்',
        },
        'te': {  # Telugu
            'Road Maintenance System': 'రోడ్ మెయింటెనెన్స్ సిస్టమ్',
            'Dashboard': 'డాష్‌బోర్డ్',
            'Report Issue': 'సమస్యను నివేదించండి',
            'Login': 'లాగిన్ చేయండి',
            'Register': 'నమోదు చేసుకోండి',
            'Submit': 'సమర్పించండి',
            'Cancel': 'రద్దు చేయండి',
        },
        'gu': {  # Gujarati
            'Road Maintenance System': 'રોડ મેઇન્ટેનન્સ સિસ્ટમ',
            'Dashboard': 'ડેશબોર્ડ',
            'Report Issue': 'સમસ્યા રિપોર્ટ કરો',
            'Login': 'લોગિન કરો',
            'Register': 'નોંધણી કરો',
            'Submit': 'સબમિટ કરો',
            'Cancel': 'રદ કરો',
        },
        'mr': {  # Marathi
            'Road Maintenance System': 'रस्ता देखभाल प्रणाली',
            'Dashboard': 'डॅशबोर्ड',
            'Report Issue': 'समस्या नोंदवा',
            'Login': 'लॉगिन करा',
            'Register': 'नोंदणी करा',
            'Submit': 'सबमिट करा',
            'Cancel': 'रद्द करा',
        }
    }
    
    added_count = 0
    
    for lang_code, translations in sample_translations.items():
        po_file = f'translations/{lang_code}/LC_MESSAGES/messages.po'
        
        if os.path.exists(po_file):
            try:
                # Read existing .po file
                with open(po_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add sample translations
                for english, translated in translations.items():
                    if f'msgid "{english}"' in content and f'msgstr "{translated}"' not in content:
                        content = content.replace(
                            f'msgid "{english}"\nmsgstr ""',
                            f'msgid "{english}"\nmsgstr "{translated}"'
                        )
                
                # Write back to file
                with open(po_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                lang_name = LANGUAGES[lang_code]
                print(f"   ✅ Added sample translations for {lang_name}")
                added_count += 1
                
            except Exception as e:
                print(f"   ❌ Error adding translations for {lang_code}: {e}")
    
    print(f"\n🌐 Added sample translations for {added_count} languages!")

def main():
    """Main setup function"""
    print("🚀 Setting up Comprehensive Multilingual Support")
    print("=" * 60)
    print(f"📋 Languages to set up: {len(LANGUAGES)} total")
    print("   • English (default)")
    print("   • 22 Official Indian Languages")
    print("=" * 60)
    
    try:
        # Step 1: Create babel configuration
        create_babel_config()
        
        # Step 2: Create directories
        create_translation_directories()
        
        # Step 3: Extract messages
        if extract_messages():
            # Step 4: Initialize new .po files
            initialize_po_files()
            
            # Step 5: Update existing .po files
            update_existing_po_files()
            
            # Step 6: Add sample translations
            add_sample_translations()
            
            # Step 7: Compile translations
            compile_translations()
            
            print("\n" + "=" * 60)
            print("🎉 MULTILINGUAL SETUP COMPLETE!")
            print("=" * 60)
            print("✅ All 22 Indian languages + English are now configured")
            print("✅ Translation directories created")
            print("✅ .po files initialized")
            print("✅ Sample translations added for major languages")
            print("✅ Translations compiled to .mo files")
            print("\n🎯 Next Steps:")
            print("1. Restart your Flask app")
            print("2. Test language switching in the browser")
            print("3. Add more translations to .po files as needed")
            print("4. Run 'python setup_multilingual.py' again to update translations")
            
        else:
            print("\n❌ Setup failed during message extraction")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
    input("\nPress Enter to exit...")
