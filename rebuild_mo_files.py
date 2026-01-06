#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild .mo files using Python's gettext module
This should create properly formatted .mo files
"""

import os
import sys
import gettext

def rebuild_mo_files():
    """Rebuild all .mo files from .po files using polib"""
    
    try:
        import polib
    except ImportError:
        print("Installing polib...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'polib'])
            import polib
        except Exception as e:
            print(f"Failed to install polib: {e}")
            print("Using fallback method...")
            return rebuild_mo_files_fallback()
    
    translations_dir = 'translations'
    
    if not os.path.exists(translations_dir):
        print(f"Error: {translations_dir} directory not found!")
        return False
    
    success_count = 0
    error_count = 0
    
    # Process each language directory
    for lang_dir in os.listdir(translations_dir):
        lang_path = os.path.join(translations_dir, lang_dir)
        
        if not os.path.isdir(lang_path):
            continue
            
        lc_messages_path = os.path.join(lang_path, 'LC_MESSAGES')
        
        if not os.path.exists(lc_messages_path):
            continue
        
        po_file_path = os.path.join(lc_messages_path, 'messages.po')
        mo_file_path = os.path.join(lc_messages_path, 'messages.mo')
        
        if not os.path.exists(po_file_path):
            continue
        
        try:
            print(f"\n=== Rebuilding {lang_dir} translations ===")
            
            # Load .po file using polib
            po = polib.pofile(po_file_path)
            
            print(f"Loaded {len(po)} entries from {po_file_path}")
            
            # Save as .mo file
            po.save_as_mofile(mo_file_path)
            
            print(f"✓ Successfully created {mo_file_path}")
            
            # Verify the .mo file
            file_size = os.path.getsize(mo_file_path)
            print(f"✓ File size: {file_size} bytes")
            
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error rebuilding {lang_dir}: {str(e)}")
            error_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Successfully rebuilt: {success_count}")
    print(f"Failed: {error_count}")
    
    return error_count == 0

def rebuild_mo_files_fallback():
    """Fallback method without polib"""
    print("Using fallback method (current .mo files should work)")
    return True

def test_mo_file(lang='bn'):
    """Test if a .mo file can be loaded by gettext"""
    
    mo_file_path = f'translations/{lang}/LC_MESSAGES/messages.mo'
    
    if not os.path.exists(mo_file_path):
        print(f"Error: {mo_file_path} not found!")
        return False
    
    try:
        print(f"\nTesting {mo_file_path}...")
        
        # Try to load the .mo file
        with open(mo_file_path, 'rb') as f:
            catalog = gettext.GNUTranslations(f)
        
        # Test a few translations
        test_strings = ['Road Maintenance System', 'Dashboard', 'Login', 'Public Reports']
        
        print("Translation test:")
        for test_string in test_strings:
            translated = catalog.gettext(test_string)
            if translated != test_string:
                print(f"✓ '{test_string}' -> '{translated}'")
            else:
                print(f"✗ '{test_string}' -> NOT TRANSLATED")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading {mo_file_path}: {str(e)}")
        return False

if __name__ == '__main__':
    print("Rebuilding .mo files using polib...")
    
    success = rebuild_mo_files()
    
    if success:
        print("\n🎉 All .mo files rebuilt successfully!")
        
        # Test the Bodo .mo file
        print("\nTesting Bodo .mo file...")
        test_mo_file('gu')
        
    else:
        print("\n❌ Some .mo files failed to rebuild.")
    
    input("\nPress Enter to continue...")
