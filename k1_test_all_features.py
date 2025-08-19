#!/usr/bin/env python3
"""
K1 All Features Test Script

Comprehensive testing of all K1 multi-folder watermark processing features.
This script demonstrates all configurations, batch processing, and custom settings.
"""

import os
import subprocess
import time
import sys

def run_command(cmd, description):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING: {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.time()
        
        print(f"✅ SUCCESS in {end_time - start_time:.2f} seconds")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        if result.stderr:
            print("Warnings:")
            print(result.stderr)
        
        return True
        
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        print(f"❌ FAILED in {end_time - start_time:.2f} seconds")
        print(f"Error: {e}")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        return False

def main():
    """Run all K1 feature tests."""
    print("🚀 K1 ALL FEATURES TEST SUITE")
    print("=" * 60)
    print("This script will test all K1 multi-folder watermark features.")
    print("Make sure you have test_nico, test_nico_folder2, and test_nico_folder3 ready.")
    print()
    
    # Test 1: List configurations
    print("📋 TEST 1: List Available Configurations")
    run_command(
        ["py", "k1_multi_folder.py", "--list-configs"],
        "List all available configurations"
    )
    
    # Test 2: Dry run with final_v2
    print("\n📋 TEST 2: Dry Run with final_v2 Configuration")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output", "--config", "final_v2", "--dry-run"],
        "Dry run with final_v2 configuration"
    )
    
    # Test 3: Process with final_v2
    print("\n📋 TEST 3: Process with final_v2 Configuration")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output", "--config", "final_v2"],
        "Process all folders with final_v2 configuration"
    )
    
    # Test 4: Process with glow_effect
    print("\n📋 TEST 4: Process with glow_effect Configuration")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output", "--config", "glow_effect"],
        "Process all folders with glow_effect configuration"
    )
    
    # Test 5: Process with dramatic_shadow
    print("\n📋 TEST 5: Process with dramatic_shadow Configuration")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output", "--config", "dramatic_shadow"],
        "Process all folders with dramatic_shadow configuration"
    )
    
    # Test 6: Custom configuration
    print("\n📋 TEST 6: Custom Configuration")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output", "--config", "custom", "--custom-text", "K1-CUSTOM", "--custom-text-shadow-offset", "18", "--custom-text-shadow-blur", "9", "--custom-text-opacity", "0.65"],
        "Process all folders with custom configuration"
    )
    
    # Test 7: Batch processing with multiple configs
    print("\n📋 TEST 7: Batch Processing with Multiple Configurations")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output", "--config", "batch", "--batch-configs", "final_v2,glow_effect,dramatic_shadow"],
        "Batch process with final_v2, glow_effect, and dramatic_shadow"
    )
    
    # Test 8: Parallel processing
    print("\n📋 TEST 8: Parallel Processing")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output_parallel", "--config", "final_v2", "--parallel", "2"],
        "Process with 2 parallel workers"
    )
    
    # Test 9: Verbose logging
    print("\n📋 TEST 9: Verbose Logging")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output_verbose", "--config", "final_v2", "--verbose"],
        "Process with verbose logging enabled"
    )
    
    # Test 10: Custom configuration with all parameters
    print("\n📋 TEST 10: Full Custom Configuration")
    run_command(
        ["py", "k1_multi_folder.py", "--base-input", "test_nico", "--base-output", "k1_test_output_full_custom", "--config", "custom", 
         "--custom-text", "K1-FULL", "--google-font", "Rubik", "--custom-text-position", "center-bottom", 
         "--custom-text-size-ratio", "0.055", "--margin", "140", "--custom-text-shadow-offset", "22", 
         "--custom-text-shadow-blur", "11", "--custom-text-shadow-color", "#FFFFFF", "--custom-text-opacity", "0.55",
         "--shadow-offset", "0", "--shadow-blur", "7", "--number-opacity", "0.3"],
        "Process with full custom configuration"
    )
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS COMPLETED!")
    print("="*60)
    print("Check the output folders to verify results:")
    print("- k1_test_output/ - Single configuration outputs")
    print("- k1_test_output_parallel/ - Parallel processing output")
    print("- k1_test_output_verbose/ - Verbose logging output")
    print("- k1_test_output_full_custom/ - Full custom configuration output")
    print()
    print("Expected folder structure:")
    print("- test_nico_[config_name]/")
    print("- test_nico_folder2_[config_name]/")
    print("- test_nico_folder3_[config_name]/")
    print()
    print("Each folder should contain 2 watermarked images:")
    print("- IMG_2314.JPG")
    print("- IMG_2384.JPG")

if __name__ == "__main__":
    main()
