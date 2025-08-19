#!/usr/bin/env python3
"""
Enhanced Watermark Examples
Demonstrates all the new configurable features of the watermark script.
"""

import os
import subprocess
import sys

def run_example(description, command):
    """Run an example command and show the results."""
    print(f"\n{'='*60}")
    print(f"EXAMPLE: {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print("Error:")
                print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - Command took too long")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Run various enhanced watermark examples."""
    print("🎨 Enhanced Watermark Script - Feature Examples")
    print("=" * 60)
    
    # Ensure test data exists
    if not os.path.exists("test_images") or not os.path.exists("sample_watermark.png"):
        print("❌ Test data not found. Please run 'py quick_start.py' first.")
        return
    
    # Example 1: Basic watermarking
    run_example(
        "Basic Watermarking with Default Settings",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/basic" --png-watermark "sample_watermark.png" --enable-numbering'
    )
    
    # Example 2: Custom positioning
    run_example(
        "Number Watermark in Center Position",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/center" --png-watermark "sample_watermark.png" --enable-numbering --number-position "center"'
    )
    
    # Example 3: Custom colors
    run_example(
        "Red Text with Black Shadow",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/red_text" --png-watermark "sample_watermark.png" --enable-numbering --number-color "#FF0000" --shadow-color "#000000"'
    )
    
    # Example 4: Enhanced shadow effects
    run_example(
        "Enhanced Shadow with Large Offset and Blur",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/enhanced_shadow" --png-watermark "sample_watermark.png" --enable-numbering --shadow-offset 8 --shadow-blur 4'
    )
    
    # Example 5: Top-right positioning
    run_example(
        "Number Watermark in Top-Right Position",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/top_right" --png-watermark "sample_watermark.png" --enable-numbering --number-position "top-right" --number-color "blue" --shadow-color "white"'
    )
    
    # Example 6: Google Font
    run_example(
        "Using Google Font 'Open Sans'",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/google_font" --png-watermark "sample_watermark.png" --enable-numbering --google-font "Open Sans" --number-color "#8B4513" --shadow-color "#F0E68C"'
    )
    
    # Example 7: Custom opacity and margins
    run_example(
        "Custom Opacity and Margins",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/custom_opacity" --png-watermark "sample_watermark.png" --enable-numbering --png-opacity 0.5 --number-opacity 0.9 --margin 40'
    )
    
    # Example 8: Professional styling
    run_example(
        "Professional Styling with Custom Colors",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/professional" --png-watermark "sample_watermark.png" --enable-numbering --number-color "#2E8B57" --shadow-color "#F5F5DC" --shadow-offset 2 --shadow-blur 1 --number-position "bottom-left"'
    )
    
    # Example 9: Custom text watermark
    run_example(
        "Custom Text Watermark - Basic",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/custom_text_basic" --custom-text "mypage.com" --enable-numbering'
    )
    
    # Example 10: Custom text with styling
    run_example(
        "Custom Text Watermark - Styled",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/custom_text_styled" --custom-text "@mytaghere" --custom-text-color "#FF0000" --custom-text-position "top-right" --custom-text-shadow-color "#000000" --custom-text-shadow-offset 5 --custom-text-shadow-blur 2 --enable-numbering'
    )
    
    # Example 11: Custom text with Google Font
    run_example(
        "Custom Text Watermark - Google Font",
        'py watermark_script.py --input-folder "test_images" --output-folder "examples/custom_text_google" --custom-text "mypage.com" --google-font "Open Sans" --custom-text-color "#8B4513" --custom-text-shadow-color "#F0E68C" --custom-text-size-ratio 0.05 --enable-numbering'
    )
    
    print(f"\n{'='*60}")
    print("🎉 All examples completed!")
    print(f"{'='*60}")
    print("\nGenerated output folders:")
    print("• examples/basic - Default settings")
    print("• examples/center - Center positioning")
    print("• examples/red_text - Red text with black shadow")
    print("• examples/enhanced_shadow - Enhanced shadow effects")
    print("• examples/top_right - Top-right positioning")
    print("• examples/google_font - Google Font example")
    print("• examples/custom_opacity - Custom opacity and margins")
    print("• examples/professional - Professional styling")
    print("• examples/custom_text_basic - Basic custom text watermark")
    print("• examples/custom_text_styled - Styled custom text watermark")
    print("• examples/custom_text_google - Custom text with Google Font")
    
    print("\n💡 Tips:")
    print("• Use --dry-run to preview without processing")
    print("• Combine multiple options for unique effects")
    print("• Google Fonts are automatically downloaded")
    print("• All colors support hex codes and color names")
    print("• Shadow effects can be completely customized")
    print("• Custom text watermarks can replace PNG watermarks")
    print("• Use custom text for branding, URLs, or social media tags")

if __name__ == "__main__":
    main()
