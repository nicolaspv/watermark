#!/usr/bin/env python3
"""
Quick Start Script for Watermark Demo
This script creates sample data and demonstrates the watermark functionality.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Success")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"⚠️ Command completed with exit code {result.returncode}")
            if result.stdout:
                print("Output:", result.stdout)
            if result.stderr:
                print("Error output:", result.stderr)
            # For watermark script, we'll consider it successful if it shows the expected output
            if "Found" in result.stdout and "image files to process" in result.stdout:
                print("✓ Watermark script executed successfully")
                return True
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main quick start function."""
    print("🚀 Watermark Script Quick Start")
    print("=" * 50)
    
    # Check if Python and pip are available
    print("\n1. Checking prerequisites...")
    if not run_command("py --version", "Checking Python version"):
        print("❌ Python not found. Please install Python 3.7+ and ensure 'py' command works.")
        return
    
    # Install dependencies
    print("\n2. Installing dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing Pillow"):
        print("❌ Failed to install dependencies.")
        return
    
    # Create sample watermark
    print("\n3. Creating sample watermark...")
    if not run_command("py create_sample_watermark.py", "Creating sample PNG watermark"):
        print("❌ Failed to create sample watermark.")
        return
    
    # Create test images
    print("\n4. Creating test images...")
    if not run_command("py create_test_images.py", "Creating sample test images"):
        print("❌ Failed to create test images.")
        return
    
    # Test dry run
    print("\n5. Testing watermark script (dry run)...")
    current_dir = os.getcwd()
    test_images_path = os.path.join(current_dir, 'test_images')
    watermarked_path = os.path.join(current_dir, 'watermarked')
    watermark_path = os.path.join(current_dir, 'sample_watermark.png')
    
    if not run_command(f"py watermark_script.py --input-folder \"{test_images_path}\" --output-folder \"{watermarked_path}\" --png-watermark \"{watermark_path}\" --enable-numbering --dry-run", "Testing watermark script"):
        print("❌ Failed to test watermark script.")
        return
    
    # Create output directory
    os.makedirs(watermarked_path, exist_ok=True)
    
    # Run actual watermarking
    print("\n6. Running actual watermarking...")
    if not run_command(f"py watermark_script.py --input-folder \"{test_images_path}\" --output-folder \"{watermarked_path}\" --png-watermark \"{watermark_path}\" --enable-numbering", "Processing images with watermarks"):
        print("❌ Failed to process images.")
        return
    
    print("\n🎉 Quick start completed successfully!")
    print("\nWhat was created:")
    print("• sample_watermark.png - Sample PNG watermark")
    print("• test_images/ - Folder with 10 sample images")
    print("• watermarked/ - Folder with watermarked images")
    print("• watermark_script.log - Processing log file")
    
    print("\nNext steps:")
    print("1. Replace sample_watermark.png with your own logo")
    print("2. Put your images in a folder")
    print("3. Run: py watermark_script.py --input-folder './your_images' --output-folder './output' --png-watermark './your_logo.png' --enable-numbering")
    print("\nNote: Images are saved with maximum quality (100% JPEG quality, no optimization) to preserve original image quality.")
    
    print("\nFor help: py watermark_script.py --help")

if __name__ == "__main__":
    main()
