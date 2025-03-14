#!/usr/bin/env python3
"""
Package the mobile app for IPA conversion.
This script creates a zip file of the mobile app that can be used with services
like AppMaker.io or as a starting point for Capacitor/Cordova conversion.
"""

import os
import zipfile
import shutil
import sys
from datetime import datetime

def create_package():
    """Create a package of the mobile app for IPA conversion."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create a timestamp for the package name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"news_app_package_{timestamp}"
    
    # Create a temporary directory for the package
    temp_dir = os.path.join(script_dir, package_name)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Files and directories to include in the package
    include_files = [
        "index.html",
        "manifest.json",
        "service-worker.js",
        "README.md",
        "DEPLOYMENT.md",
        "IPA_CONVERSION_GUIDE.md"
    ]
    
    include_dirs = [
        "icons"
    ]
    
    # Copy files to the temporary directory
    print("Copying files to package...")
    for file in include_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(temp_dir, file))
            print(f"  Added {file}")
        else:
            print(f"  Warning: {file} not found, skipping")
    
    # Copy directories to the temporary directory
    for directory in include_dirs:
        if os.path.exists(directory):
            dest_dir = os.path.join(temp_dir, directory)
            shutil.copytree(directory, dest_dir, dirs_exist_ok=True)
            print(f"  Added directory {directory}")
        else:
            print(f"  Warning: Directory {directory} not found, skipping")
    
    # Create a zip file of the package
    zip_file = os.path.join(script_dir, f"{package_name}.zip")
    print(f"Creating zip file: {zip_file}")
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
    
    print("\nPackage created successfully!")
    print(f"Package location: {zip_file}")
    print("\nNext steps:")
    print("1. Use this package with a service like AppMaker.io")
    print("   or as a starting point for Capacitor/Cordova conversion.")
    print("2. Follow the instructions in IPA_CONVERSION_GUIDE.md")
    print("   to convert the package to an IPA file.")

if __name__ == "__main__":
    try:
        create_package()
    except Exception as e:
        print(f"Error creating package: {e}", file=sys.stderr)
        sys.exit(1)
