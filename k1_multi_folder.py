#!/usr/bin/env python3
"""
K1 Multi-Folder Watermark Processing Script

Processes multiple folders with pre-configured watermark settings optimized for K1 printing workflows.
Supports batch processing, custom configurations, and parallel processing.

FOLDER STRUCTURE:
- Input: Parent folder (e.g., "k1_test_input") containing multiple subfolders
- Output: Creates output folders for each subfolder with configuration suffix
- Example: k1_test_input/folder1/ -> k1_output/folder1_final_v2/

CONFIGURATION EDITING:
- Edit the "final_v2" configuration in the _load_configurations() method below
- All parameters are documented with comments for easy customization
"""

import argparse
import os
import sys
import logging
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import concurrent.futures

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('k1_multi_folder.log')
    ]
)
logger = logging.getLogger(__name__)

class K1MultiFolderProcessor:
    """Handles multi-folder watermark processing with pre-configured settings."""
    
    def __init__(self):
        """Initialize the K1 multi-folder processor."""
        self.configs = self._load_configurations()
        self.base_script = "watermark_script.py"
        
    def _load_configurations(self) -> Dict[str, Dict[str, str]]:
        """Load pre-configured watermark settings."""
        return {
            # ========================================
            # 🎨 FINAL_V2 CONFIGURATION - EDIT HERE
            # ========================================
            # This is the main configuration for K1 printing workflows
            # Modify the values below to fine-tune the watermark appearance
            "final_v2": {
                "custom_text": "hamacak1.com",           # Watermark text
                "google_font": "Rubik",                  # Font family
                "custom_text_position": "center-bottom", # Position: top-left, top-right, center, center-bottom, bottom-left, bottom-right
                "custom_text_size_ratio": "0.05",        # Text size (0.01-0.1, higher = larger)
                "margin": "120",                         # Margin from edges in pixels
                "custom_text_shadow_offset": "8",        # Shadow offset in pixels (reduced from 10 to 8)
                "custom_text_shadow_blur": "4",          # Shadow blur radius (increased from 1 to 4 for better effect)
                "custom_text_opacity": "0.5",            # Text transparency (0.1-1.0)
                "shadow_offset": "0",                    # Number shadow offset
                "shadow_blur": "8",                      # Number shadow blur
                "number_opacity": "0.4"                  # Number transparency
            },
            # ========================================
            # 🎨 FINAL_V3 CONFIGURATION - PNG WATERMARK
            # ========================================
            # This configuration uses PNG watermark instead of custom text
            # PNG watermark is positioned at bottom-left, numbers remain as V2
            "final_v3": {
                "png_watermark": "k1_watermark.png",     # PNG watermark file path
                "png_position": "bottom-left",           # PNG watermark position
                "png_opacity": "1.0",                    # PNG watermark transparency (0.1-1.0)
                "margin": "100",                         # Base margin (PNG will be exactly 100px from left and bottom edges)
                "png_x_offset": "0",                     # X offset for fine-tuning PNG position (can be negative)
                "png_y_offset": "250",                   # Y offset for fine-tuning PNG position (can be negative)
                "google_font": "Rubik",
                "shadow_offset": "0",                    # Number shadow offset
                "shadow_blur": "4",                      # Number shadow blur 
                "number_opacity": "0.4",                 # Number transparency
                "number_color": "#ffffff",               # Number color (white)
                "shadow_color": "#000000",               # Shadow color (black)
                "shadow_opacity": "0.9"                  # Shadow opacity
            },
            "glow_effect": {
                "custom_text": "K1-PRINT",
                "google_font": "Rubik",
                "custom_text_position": "center-bottom",
                "custom_text_size_ratio": "0.06",
                "margin": "150",
                "custom_text_shadow_offset": "0",
                "custom_text_shadow_blur": "8",
                "custom_text_shadow_color": "#FFFFFF",
                "custom_text_opacity": "0.8",
                "shadow_offset": "0",
                "shadow_blur": "4",
                "number_opacity": "0.3"
            },
            "dramatic_shadow": {
                "custom_text": "K1-PRINT",
                "google_font": "Rubik",
                "custom_text_position": "center-bottom",
                "custom_text_size_ratio": "0.05",
                "margin": "200",
                "custom_text_shadow_offset": "25",
                "custom_text_shadow_blur": "12",
                "custom_text_opacity": "0.5",
                "shadow_offset": "0",
                "shadow_blur": "8",
                "number_opacity": "0.25"
            }
        }
    
    def get_folder_variants(self, base_folder: str) -> List[str]:
        """Get all subfolders within the parent folder."""
        if not os.path.exists(base_folder) or not os.path.isdir(base_folder):
            logger.error(f"Parent folder not found: {base_folder}")
            return []
        
        # Get all subfolders within the parent folder
        subfolders = []
        try:
            for item in os.listdir(base_folder):
                item_path = os.path.join(base_folder, item)
                if os.path.isdir(item_path):
                    subfolders.append(item)
            
            if not subfolders:
                logger.warning(f"No subfolders found in: {base_folder}")
                return []
            
            logger.info(f"Found {len(subfolders)} subfolders in {base_folder}: {subfolders}")
            return subfolders
            
        except Exception as e:
            logger.error(f"Error scanning folder {base_folder}: {e}")
            return []
    
    def build_command(self, config_name: str, input_folder: str, output_folder: str, 
                     custom_settings: Optional[Dict[str, str]] = None) -> List[str]:
        """Build the watermark command with specified configuration."""
        if config_name not in self.configs:
            raise ValueError(f"Unknown configuration: {config_name}")
        
        config = self.configs[config_name].copy()
        
        # Override with custom settings if provided
        if custom_settings:
            config.update(custom_settings)
        
        # Build base command
        cmd = [
            "py", self.base_script,
            "--input-folder", input_folder,
            "--output-folder", output_folder,
            "--enable-numbering"
        ]
        
        # Add configuration parameters
        for key, value in config.items():
            if key == "custom_text":
                cmd.extend(["--custom-text", value])
            elif key == "google_font":
                cmd.extend(["--google-font", value])
            elif key == "png_watermark":
                cmd.extend(["--png-watermark", value])
            elif key == "png_opacity":
                cmd.extend(["--png-opacity", value])
            elif key == "png_position":
                cmd.extend(["--png-position", value])
            elif key == "png_x_offset":
                cmd.extend(["--png-x-offset", value])
            elif key == "png_y_offset":
                cmd.extend(["--png-y-offset", value])
            elif key == "custom_text_position":
                cmd.extend(["--custom-text-position", value])
            elif key == "custom_text_size_ratio":
                cmd.extend(["--custom-text-size-ratio", value])
            elif key == "margin":
                cmd.extend(["--margin", value])
            elif key == "custom_text_shadow_offset":
                cmd.extend(["--custom-text-shadow-offset", value])
            elif key == "custom_text_shadow_blur":
                cmd.extend(["--custom-text-shadow-blur", value])
            elif key == "custom_text_shadow_color":
                cmd.extend(["--custom-text-shadow-color", value])
            elif key == "custom_text_opacity":
                cmd.extend(["--custom-text-opacity", value])
            elif key == "shadow_offset":
                cmd.extend(["--shadow-offset", value])
            elif key == "shadow_blur":
                cmd.extend(["--shadow-blur", value])
            elif key == "shadow_color":
                cmd.extend(["--shadow-color", value])
            elif key == "shadow_opacity":
                cmd.extend(["--shadow-opacity", value])
            elif key == "number_opacity":
                cmd.extend(["--number-opacity", value])
            elif key == "number_color":
                cmd.extend(["--number-color", value])
        
        return cmd
    
    def process_single_folder(self, input_folder: str, output_folder: str, 
                            config_name: str, custom_settings: Optional[Dict[str, str]] = None,
                            dry_run: bool = False) -> bool:
        """Process a single folder with the specified configuration."""
        try:
            # Ensure output directory exists
            os.makedirs(output_folder, exist_ok=True)
            
            # For custom configurations, use a default config as base
            if config_name == "custom":
                base_config = "final_v2"  # Use final_v2 as base for custom
            else:
                base_config = config_name
            
            # Build command
            cmd = self.build_command(base_config, input_folder, output_folder, custom_settings)
            
            if dry_run:
                logger.info(f"DRY RUN - Would process: {input_folder} -> {output_folder}")
                logger.info(f"Command: {' '.join(cmd)}")
                return True
            
            logger.info(f"Processing: {input_folder} -> {output_folder}")
            logger.info(f"Configuration: {config_name}")
            
            # Execute command
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            end_time = time.time()
            
            processing_time = end_time - start_time
            logger.info(f"Completed: {input_folder} in {processing_time:.2f} seconds")
            
            # Log output
            if result.stdout:
                logger.info(f"Output: {result.stdout.strip()}")
            if result.stderr:
                logger.warning(f"Warnings: {result.stderr.strip()}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to process {input_folder}: {e}")
            if e.stdout:
                logger.error(f"STDOUT: {e.stdout}")
            if e.stderr:
                logger.error(f"STDERR: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error processing {input_folder}: {e}")
            return False
    
    def process_folders(self, base_input: str, base_output: str, config_name: str,
                       custom_settings: Optional[Dict[str, str]] = None, 
                       dry_run: bool = False, parallel: int = 1) -> Dict[str, bool]:
        """Process multiple folders with the specified configuration."""
        # Get folder variants
        input_folders = self.get_folder_variants(base_input)
        
        if not input_folders:
            logger.error(f"No valid input folders found for base: {base_input}")
            return {}
        
        logger.info(f"Found {len(input_folders)} folders to process: {input_folders}")
        
        # Create output folders
        output_folders = []
        for input_folder in input_folders:
            # Use full path for input folder
            full_input_path = os.path.join(base_input, input_folder)
            output_folder = os.path.join(base_output, f"{input_folder}_{config_name}")
            output_folders.append(output_folder)
        
        results = {}
        
        if parallel > 1 and not dry_run:
            # Parallel processing
            logger.info(f"Processing {len(input_folders)} folders with {parallel} parallel workers")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
                future_to_folder = {}
                
                for input_folder, output_folder in zip(input_folders, output_folders):
                    # Use full path for input folder
                    full_input_path = os.path.join(base_input, input_folder)
                    future = executor.submit(
                        self.process_single_folder,
                        full_input_path, output_folder, config_name, custom_settings, dry_run
                    )
                    future_to_folder[future] = input_folder
                
                for future in concurrent.futures.as_completed(future_to_folder):
                    input_folder = future_to_folder[future]
                    try:
                        success = future.result()
                        results[input_folder] = success
                    except Exception as e:
                        logger.error(f"Exception in {input_folder}: {e}")
                        results[input_folder] = False
        else:
            # Sequential processing
            for input_folder, output_folder in zip(input_folders, output_folders):
                # Use full path for input folder
                full_input_path = os.path.join(base_input, input_folder)
                success = self.process_single_folder(
                    full_input_path, output_folder, config_name, custom_settings, dry_run
                )
                results[input_folder] = success
        
        return results
    
    def process_batch_configs(self, base_input: str, base_output: str, 
                            config_names: List[str], custom_settings: Optional[Dict[str, str]] = None,
                            dry_run: bool = False, parallel: int = 1) -> Dict[str, Dict[str, bool]]:
        """Process folders with multiple configurations."""
        logger.info(f"Batch processing with configurations: {config_names}")
        
        batch_results = {}
        
        for config_name in config_names:
            if config_name not in self.configs:
                logger.warning(f"Skipping unknown configuration: {config_name}")
                continue
            
            logger.info(f"Processing with configuration: {config_name}")
            results = self.process_folders(
                base_input, base_output, config_name, custom_settings, dry_run, parallel
            )
            batch_results[config_name] = results
        
        return batch_results
    
    def list_configurations(self) -> None:
        """List all available configurations."""
        logger.info("Available configurations:")
        for config_name, config in self.configs.items():
            logger.info(f"\n{config_name}:")
            for key, value in config.items():
                logger.info(f"  {key}: {value}")
    
    def validate_configuration(self, config_name: str) -> bool:
        """Validate that a configuration exists."""
        if config_name not in self.configs:
            logger.error(f"Unknown configuration: {config_name}")
            logger.info("Available configurations:")
            for config in self.configs.keys():
                logger.info(f"  - {config}")
            return False
        return True

def main():
    """Main function for K1 multi-folder processing."""
    parser = argparse.ArgumentParser(
        description="K1 Multi-Folder Watermark Processing Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process with final_v2 configuration (processes all subfolders in k1_test_input)
  py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "final_v2"
  
  # Process with custom settings
  py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "custom" --custom-text "K1-PRINT"
  
  # Batch processing with multiple configs
  py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "batch" --batch-configs "final_v2,glow_effect"
  
  # List available configurations
  py k1_multi_folder.py --list-configs
        """
    )
    
    # Required arguments
    parser.add_argument('--base-input', required=False,
                       help='Parent input folder containing subfolders to process (e.g., "k1_test_input")')
    parser.add_argument('--base-output', required=False,
                       help='Base output folder name (e.g., "k1_output")')
    parser.add_argument('--config', required=False,
                       help='Configuration name or "custom" for custom settings')
    
    # Optional arguments
    parser.add_argument('--batch-configs', required=False,
                       help='Comma-separated list of configurations for batch processing')
    parser.add_argument('--custom-text', required=False,
                       help='Custom text watermark (overrides config)')
    parser.add_argument('--google-font', required=False,
                       help='Google Font name (overrides config)')
    parser.add_argument('--custom-text-position', required=False,
                       help='Custom text position (overrides config)')
    parser.add_argument('--custom-text-size-ratio', required=False,
                       help='Custom text size ratio (overrides config)')
    parser.add_argument('--margin', required=False,
                       help='Margin in pixels (overrides config)')
    parser.add_argument('--custom-text-shadow-offset', required=False,
                       help='Custom text shadow offset (overrides config)')
    parser.add_argument('--custom-text-shadow-blur', required=False,
                       help='Custom text shadow blur (overrides config)')
    parser.add_argument('--custom-text-shadow-color', required=False,
                       help='Custom text shadow color (overrides config)')
    parser.add_argument('--custom-text-opacity', required=False,
                       help='Custom text opacity (overrides config)')
    parser.add_argument('--shadow-offset', required=False,
                       help='Number shadow offset (overrides config)')
    parser.add_argument('--shadow-blur', required=False,
                       help='Number shadow blur (overrides config)')
    parser.add_argument('--shadow-color', required=False,
                       help='Number shadow color (overrides config)')
    parser.add_argument('--shadow-opacity', required=False,
                       help='Number shadow opacity (overrides config)')
    parser.add_argument('--number-opacity', required=False,
                       help='Number opacity (overrides config)')
    parser.add_argument('--number-color', required=False,
                       help='Number color (overrides config)')
    parser.add_argument('--png-x-offset', required=False,
                       help='PNG watermark X offset (can be negative, overrides config)')
    parser.add_argument('--png-y-offset', required=False,
                       help='PNG watermark Y offset (can be negative, overrides config)')
    parser.add_argument('--parallel', type=int, default=1,
                       help='Number of parallel workers (default: 1)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without actually processing')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--list-configs', action='store_true',
                       help='List all available configurations')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize processor
    processor = K1MultiFolderProcessor()
    
    # List configurations if requested
    if args.list_configs:
        processor.list_configurations()
        return
    
    # Validate required arguments
    if not args.base_input or not args.base_output or not args.config:
        if not args.list_configs:
            parser.error("--base-input, --base-output, and --config are required unless using --list-configs")
        return
    
    # Validate configuration (skip validation for batch processing)
    if args.config != "custom" and args.config != "batch" and not processor.validate_configuration(args.config):
        return
    
    # Build custom settings if provided
    custom_settings = None
    if args.config == "custom" or any([
        args.custom_text, args.google_font, args.custom_text_position,
        args.custom_text_size_ratio, args.margin, args.custom_text_shadow_offset,
        args.custom_text_shadow_blur, args.custom_text_shadow_color,
        args.custom_text_opacity, args.shadow_offset, args.shadow_blur, args.shadow_color, args.shadow_opacity, args.number_opacity, args.number_color,
        args.png_x_offset, args.png_y_offset
    ]):
        custom_settings = {}
        
        if args.custom_text:
            custom_settings["custom_text"] = args.custom_text
        if args.google_font:
            custom_settings["google_font"] = args.google_font
        if args.custom_text_position:
            custom_settings["custom_text_position"] = args.custom_text_position
        if args.custom_text_size_ratio:
            custom_settings["custom_text_size_ratio"] = args.custom_text_size_ratio
        if args.margin:
            custom_settings["margin"] = args.margin
        if args.custom_text_shadow_offset:
            custom_settings["custom_text_shadow_offset"] = args.custom_text_shadow_offset
        if args.custom_text_shadow_blur:
            custom_settings["custom_text_shadow_blur"] = args.custom_text_shadow_blur
        if args.custom_text_shadow_color:
            custom_settings["custom_text_shadow_color"] = args.custom_text_shadow_color
        if args.custom_text_opacity:
            custom_settings["custom_text_opacity"] = args.custom_text_opacity
        if args.shadow_offset:
            custom_settings["shadow_offset"] = args.shadow_offset
        if args.shadow_blur:
            custom_settings["shadow_blur"] = args.shadow_blur
        if args.shadow_color:
            custom_settings["shadow_color"] = args.shadow_color
        if args.shadow_opacity:
            custom_settings["shadow_opacity"] = args.shadow_opacity
        if args.number_opacity:
            custom_settings["number_opacity"] = args.number_opacity
        if args.number_color:
            custom_settings["number_color"] = args.number_color
        if args.png_x_offset:
            custom_settings["png_x_offset"] = args.png_x_offset
        if args.png_y_offset:
            custom_settings["png_y_offset"] = args.png_y_offset
    
    # Process folders
    start_time = time.time()
    
    if args.batch_configs:
        # Batch processing with multiple configurations
        config_names = [name.strip() for name in args.batch_configs.split(',')]
        results = processor.process_batch_configs(
            args.base_input, args.base_output, config_names, 
            custom_settings, args.dry_run, args.parallel
        )
        
        # Summary
        logger.info("\n" + "="*50)
        logger.info("BATCH PROCESSING SUMMARY")
        logger.info("="*50)
        
        total_success = 0
        total_failed = 0
        
        for config_name, config_results in results.items():
            config_success = sum(1 for success in config_results.values() if success)
            config_failed = len(config_results) - config_success
            
            logger.info(f"\n{config_name}:")
            logger.info(f"  Success: {config_success}")
            logger.info(f"  Failed: {config_failed}")
            
            total_success += config_success
            total_failed += config_failed
        
        logger.info(f"\nTOTAL:")
        logger.info(f"  Success: {total_success}")
        logger.info(f"  Failed: {total_failed}")
        
    else:
        # Single configuration processing
        results = processor.process_folders(
            args.base_input, args.base_output, args.config,
            custom_settings, args.dry_run, args.parallel
        )
        
        # Summary
        success_count = sum(1 for success in results.values() if success)
        failed_count = len(results) - success_count
        
        logger.info("\n" + "="*50)
        logger.info("PROCESSING SUMMARY")
        logger.info("="*50)
        logger.info(f"Configuration: {args.config}")
        logger.info(f"Success: {success_count}")
        logger.info(f"Failed: {failed_count}")
        
        for folder, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"  {folder}: {status}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    logger.info(f"\nTotal processing time: {total_time:.2f} seconds")
    
    if args.dry_run:
        logger.info("DRY RUN COMPLETED - No files were processed")
    else:
        logger.info("Processing completed!")

if __name__ == "__main__":
    main()
