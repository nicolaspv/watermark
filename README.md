# Bulk Image Watermark Script

A powerful Python script for bulk watermarking images with custom PNG logos, custom text watermarks, and auto-generated number watermarks extracted from filenames.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Performance & Quality](#performance--quality)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [Support](#support)

## Features

- **Triple Watermark System**: Custom PNG watermark + Custom text watermark + Auto-generated number watermark
- **Smart Positioning**: 6 configurable positions for custom text, 5 for numbers, PNG centered at bottom
- **Batch Processing**: Process entire folders of images automatically with recursive scanning
- **Quality Preservation**: Maintains exact original image quality with 100% JPEG quality, no optimization
- **Flexible Configuration**: Customizable opacity, margins, font sizes, colors, and shadow effects
- **Professional Output**: Drop shadow effects, anti-aliased text, and high-quality LANCZOS resampling
- **Advanced Font Support**: Google Fonts, custom fonts, and system font fallbacks
- **Comprehensive Logging**: Detailed progress tracking, error reporting, and dry-run mode

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Pillow requests
```

## Quick Start

### 🚀 Option 1: Full Demo (Recommended for first-time users)
```bash
py quick_start.py
```
This creates sample data and demonstrates the full functionality.

### 🎯 Option 2: Basic Watermarking
```bash
# Create output folder
mkdir watermarked

# Run with PNG watermark
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering

# Or use custom text instead
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --custom-text "mypage.com" --enable-numbering
```

### 📁 Option 3: Windows Batch Files
```bash
# Using batch file
run_watermark.bat "C:\Photos" "C:\Watermarked" "C:\logo.png"

# Using PowerShell
.\run_watermark.ps1 -InputFolder ".\photos" -OutputFolder ".\output" -WatermarkFile ".\logo.png"
```

## Usage

### 🔧 Command Structure Overview
The script supports three watermark modes:
1. **PNG Watermark Mode**: Use `--png-watermark` for logo watermarks
2. **Custom Text Mode**: Use `--custom-text` for text watermarks (e.g., "mypage.com")
3. **Combined Mode**: Use both PNG and custom text together

### 📝 Basic Command Structure
```bash
# PNG Watermark Mode
py watermark_script.py --input-folder "path/to/input" --output-folder "path/to/output" --png-watermark "logo.png" --enable-numbering

# Custom Text Mode
py watermark_script.py --input-folder "path/to/input" --output-folder "path/to/output" --custom-text "mypage.com" --enable-numbering

# Combined Mode
py watermark_script.py --input-folder "path/to/input" --output-folder "path/to/output" --png-watermark "logo.png" --custom-text "mypage.com" --enable-numbering
```

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--input-folder` | Source directory containing images | `"./photos"` |
| `--output-folder` | Destination directory for watermarked images | `"./watermarked"` |
| `--png-watermark` | Path to PNG watermark file | `"./logo.png"` |
| `--enable-numbering` | Flag to activate number extraction | (no value needed) |

### Optional Arguments

| Argument | Description | Default | Range |
|----------|-------------|---------|-------|
| `--png-opacity` | PNG watermark transparency | 0.7 | 0.1 - 1.0 |
| `--number-opacity` | Number watermark transparency | 0.8 | 0.1 - 1.0 |
| `--font-size-ratio` | Font size as ratio of image height | 0.03 | 0.01 - 0.1 |
| `--margin` | Margin from edges in pixels | 20 | 10 - 100 |
| `--number-pattern` | Regex pattern for number extraction | `\d+` | Any regex |
| `--number-position` | Position of number watermark | `bottom-right` | `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center` |
| `--number-color` | Color of number text | `#000000` | Hex color or color name |
| `--shadow-color` | Color of drop shadow | `#FFFFFF` | Hex color or color name |
| `--shadow-offset` | Offset of drop shadow in pixels | `3` | 0-20 |
| `--shadow-blur` | Blur radius of drop shadow | `1` | 0-5 |
| `--custom-font` | Path to custom font file | None | `.ttf`, `.otf` files |
| `--google-font` | Google Font name to download | None | Any Google Font name |
| `--custom-text` | Custom text watermark | None | Any text (e.g., "mypage.com", "@mytaghere") |
| `--custom-text-position` | Position of custom text | `center-bottom` | 6 positions including `center-bottom` |
| `--custom-text-color` | Color of custom text | `#000000` | Hex color or color name |
| `--custom-text-shadow-color` | Color of custom text shadow | `#FFFFFF` | Hex color or color name |
| `--custom-text-shadow-offset` | Custom text shadow offset | `3` | 0-20 |
| `--custom-text-shadow-blur` | Custom text shadow blur | `1` | 0-5 |
| `--custom-text-size-ratio` | Custom text font size ratio | `0.04` | 0.01-0.1 |
| `--dry-run` | Show what would be processed | False | (flag) |

## Examples

### 🎯 Basic Usage Examples
```bash
# PNG watermark with numbering
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering

# Custom text watermark with numbering
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --custom-text "mypage.com" --enable-numbering

# Combined watermarks
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --custom-text "@mytaghere" --enable-numbering
```

### ⚙️ Custom Settings Examples
```bash
# Adjust PNG opacity and margins
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --png-opacity 0.5 --margin 30

# Custom number styling
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --number-color "#FF0000" --shadow-color "#000000" --number-position "top-right"

# Custom text with Google Font
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --custom-text "mypage.com" --google-font "Roboto" --custom-text-size-ratio 0.05 --enable-numbering
```

### 🔍 Test and Debug Examples
```bash
# Dry run to preview processing
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --dry-run

# Custom number pattern extraction
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --number-pattern "IMG_(\d+)_"

# Test with enhanced examples script
py enhanced_examples.py
```

### 🌟 Professional Styling Examples
```bash
# Professional branding with custom text
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --custom-text "mypage.com" --custom-text-color "#2E8B57" --custom-text-shadow-color "#F5F5DC" --custom-text-shadow-offset 5 --custom-text-shadow-blur 2 --enable-numbering

# Social media style with custom text
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --custom-text "@mytaghere" --custom-text-color "#FF0000" --custom-text-position "top-right" --custom-text-shadow-color "#000000" --custom-text-shadow-offset 5 --custom-text-shadow-blur 2 --enable-numbering

# Corporate style with PNG and enhanced numbering
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --number-color "#2E8B57" --shadow-color "#F5F5DC" --shadow-offset 2 --shadow-blur 1 --number-position "bottom-left"
```

## How It Works

### 🔍 **Processing Flow**
1. **Input Validation**: Checks folders, watermark files, and permissions
2. **Image Discovery**: Recursively scans input folder for supported image formats
3. **Watermark Application**: Applies PNG, custom text, and/or number watermarks
4. **Quality Preservation**: Saves with maximum quality settings
5. **Progress Tracking**: Real-time logging and progress indicators

### 🖼️ **PNG Watermark**
- **Position**: Center-bottom of image (traditional logo placement)
- **Scaling**: Automatically resized to max 20% of image width, 15% of height
- **Transparency**: Configurable opacity (0.1-1.0, default: 0.7)
- **Quality**: High-quality LANCZOS resampling for smooth scaling
- **Format Support**: PNG with alpha channel for transparency

### 📝 **Custom Text Watermark**
- **Position**: 6 configurable positions including `center-bottom`
- **Text**: Any custom text (e.g., "mypage.com", "@mytaghere", company names)
- **Styling**: Full color, shadow, and font customization
- **Size**: Proportional to image dimensions (default: 4% of image height)
- **Fonts**: Google Fonts, custom fonts, or system font fallbacks
- **Use Cases**: Branding, URLs, social media tags, copyright notices

### 🔢 **Number Watermark**
- **Position**: 5 configurable positions (default: bottom-right)
- **Extraction**: Uses regex pattern matching to find numbers in filenames
- **Styling**: Fully customizable colors, shadows, and effects
- **Font**: Professional fonts with fallback to system default
- **Size**: Proportional to image dimensions (default: 3% of image height)
- **Pattern Examples**: `IMG_001.jpg` → "001", `photo_123_2024.png` → "123"

### 🎨 **Advanced Features**
- **Drop Shadows**: Configurable offset, blur, and colors for professional look
- **Font Management**: Automatic Google Font download and caching
- **Color Support**: Hex codes, color names, and opacity control
- **Positioning System**: Smart calculation based on image dimensions and margins
- **Quality Preservation**: 100% JPEG quality, no optimization, exact original quality

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)

## File Naming Convention

The script automatically extracts numbers from image filenames:

**Examples:**
- `IMG_001.jpg` → Number watermark: "001"
- `photo_123_2024.png` → Number watermark: "123"
- `vacation_456.jpg` → Number watermark: "456"
- `image.jpg` → No number watermark (warning logged)

## Output

- **Processed Images**: Saved to output folder with original names
- **Log File**: `watermark_script.log` with detailed processing information
- **Console Output**: Real-time progress and status updates
- **Quality**: Maximum quality preservation with 100% JPEG quality, no optimization

## Error Handling

The script includes comprehensive error handling:
- Invalid input paths
- Corrupted image files
- Missing watermark files
- Font loading issues
- File permission problems
- Memory issues with large images

## Performance

- **Memory Efficient**: Processes images one at a time
- **Batch Processing**: Handles large numbers of files
- **Progress Tracking**: Shows current file and overall progress
- **Resume Capability**: Can be re-run on same folders safely

## Troubleshooting

### Common Issues

**"No numbers found in filename"**
- Ensure filenames contain numbers
- Check regex pattern with `--number-pattern`
- Use `--dry-run` to see what would be processed

**"Failed to load PNG watermark"**
- Verify PNG file exists and is valid
- Check file permissions
- Ensure file is actually a PNG format

**"Could not load custom font"**
- Script will fallback to system default font
- This is normal and won't affect functionality

**Memory errors with large images**
- Process images in smaller batches
- Ensure sufficient system memory
- Consider reducing image resolution first

## Advanced Usage

### Custom Regex Patterns

Extract specific number formats:
```bash
# Extract numbers after "IMG_"
--number-pattern "IMG_(\d+)"

# Extract year numbers
--number-pattern "(\d{4})"

# Extract sequence numbers
--number-pattern "seq_(\d+)"
```

### Custom Number Watermark Styling

```bash
# Red text with black shadow, positioned top-right
--number-color "#FF0000" --shadow-color "#000000" --number-position "top-right"

# Blue text with white shadow, increased blur
--number-color "blue" --shadow-color "white" --shadow-blur 3

# Custom shadow offset
--shadow-offset 5 --shadow-blur 2
```

### Custom Fonts

```bash
# Use Google Font
--google-font "Roboto" --google-font "Open Sans"

# Use custom font file
--custom-font "C:/Fonts/MyFont.ttf"
```

### Custom Text Watermarks

```bash
# Basic custom text watermark
--custom-text "mypage.com" --enable-numbering

# Styled custom text with positioning
--custom-text "@mytaghere" --custom-text-color "#FF0000" --custom-text-position "top-right"

# Professional custom text with enhanced shadows
--custom-text "mypage.com" --custom-text-color "#2E8B57" --custom-text-shadow-color "#F5F5DC" --custom-text-shadow-offset 5 --custom-text-shadow-blur 2

# Custom text with Google Font
--custom-text "mypage.com" --google-font "Roboto" --custom-text-size-ratio 0.05
```

### Batch Processing Multiple Folders

```bash
# Process multiple input folders
for folder in folder1 folder2 folder3; do
    py watermark_script.py --input-folder "./$folder" --output-folder "./watermarked/$folder" --png-watermark "./logo.png" --enable-numbering
done

# PowerShell example
$folders = @("photos1", "photos2", "photos3")
foreach ($folder in $folders) {
    py watermark_script.py --input-folder ".\$folder" --output-folder ".\output\$folder" --png-watermark ".\logo.png" --enable-numbering
}
```

### 🎨 **Professional Use Cases**

#### **Branding & Marketing**
```bash
# Company logo with custom text
py watermark_script.py --input-folder "./product_photos" --output-folder "./branded" --png-watermark "./company_logo.png" --custom-text "mypage.com" --enable-numbering

# Social media style
py watermark_script.py --input-folder "./social_media" --output-folder "./tagged" --custom-text "@mytaghere" --custom-text-color "#FF0000" --custom-text-position "top-right" --enable-numbering
```

#### **Photography & Events**
```bash
# Event photography with sequence numbers
py watermark_script.py --input-folder "./event_photos" --output-folder "./watermarked" --custom-text "Event 2024" --custom-text-position "center-bottom" --enable-numbering --number-pattern "IMG_(\d+)"

# Portfolio with copyright
py watermark_script.py --input-folder "./portfolio" --output-folder "./copyrighted" --custom-text "© 2024 MyName" --custom-text-color "#2E8B57" --custom-text-position "bottom-left" --enable-numbering
```

#### **E-commerce & Products**
```bash
# Product images with branding
py watermark_script.py --input-folder "./products" --output-folder "./branded_products" --png-watermark "./brand_logo.png" --custom-text "mypage.com" --enable-numbering --number-pattern "PROD_(\d+)"
```

## File Structure

```
watermark-01/
├── watermark_script.py          # Main watermark processing script
├── requirements.txt             # Python dependencies
├── README.md                   # This comprehensive documentation
├── PROJECT_OVERVIEW.md         # Quick reference guide
├── ENHANCEMENTS_SUMMARY.md     # Feature summary and changelog
├── quick_start.py              # Demo script with sample data creation
├── enhanced_examples.py        # Comprehensive feature demonstrations
├── create_sample_watermark.py  # Helper to create sample watermark
├── create_test_images.py       # Helper to create test images
├── run_watermark.bat           # Windows batch file runner
└── run_watermark.ps1           # PowerShell script runner
```

## Performance & Quality

### 🚀 **Performance Features**
- **Memory Efficient**: Processes images one at a time, minimal memory footprint
- **Batch Processing**: Handles large numbers of files with progress tracking
- **Resume Capability**: Can be re-run on same folders safely
- **Recursive Scanning**: Automatically discovers images in subfolders

### 🎯 **Quality Preservation**
- **JPEG Quality**: 100% quality with no optimization (`quality=100, optimize=False`)
- **PNG Support**: Preserves all image data and transparency
- **Format Conversion**: Maintains original image modes and quality
- **High-Quality Scaling**: LANCZOS resampling for watermark resizing

### 📊 **Supported Formats & Sizes**
- **Image Formats**: JPEG, PNG, TIFF, BMP with full format support
- **File Sizes**: Handles images from small thumbnails to large professional photos
- **Color Spaces**: RGB, RGBA, and grayscale with proper conversion
- **Metadata**: Preserves original image metadata where possible

## Troubleshooting

### 🔍 **Common Issues & Solutions**

#### **"No numbers found in filename"**
- **Cause**: Filenames don't contain numbers matching the regex pattern
- **Solution**: 
  - Ensure filenames contain numbers (e.g., `IMG_001.jpg`, `photo_123.png`)
  - Use `--number-pattern` to customize extraction pattern
  - Use `--dry-run` to preview what would be processed

#### **"Failed to load PNG watermark"**
- **Cause**: PNG file issues or missing file
- **Solution**:
  - Verify PNG file exists and is valid
  - Check file permissions and path
  - Ensure file is actually a PNG format
  - Use `--custom-text` as alternative

#### **"Could not load custom font"**
- **Cause**: Font file issues or missing fonts
- **Solution**:
  - Script automatically falls back to system fonts
  - This is normal and won't affect functionality
  - Check font file paths and permissions
  - Use Google Fonts for reliable font loading

#### **Memory errors with large images**
- **Cause**: Insufficient system memory for very large images
- **Solution**:
  - Process images in smaller batches
  - Ensure sufficient system memory
  - Consider reducing image resolution first
  - Close other memory-intensive applications

#### **"Either PNG watermark file or custom text must be provided"**
- **Cause**: No watermark source specified
- **Solution**:
  - Provide either `--png-watermark` or `--custom-text`
  - Both can be used together for combined watermarks

### 🛠️ **Debug Mode**
Use `--dry-run` to preview without processing:
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./output" --png-watermark "./logo.png" --enable-numbering --dry-run
```

### 📝 **Log Files**
- **Console Output**: Real-time progress and error messages
- **Log File**: `watermark_script.log` with detailed processing information
- **Error Details**: Comprehensive error messages with context

## License

This script is provided as-is for educational and commercial use.

## Contributing

We welcome contributions to improve the watermark script! Here's how you can help:

### 🐛 **Report Issues**
- Use the GitHub Issues page
- Include detailed error messages and log files
- Provide steps to reproduce the issue
- Include system information (OS, Python version)

### 💡 **Feature Requests**
- Describe the desired functionality
- Explain the use case and benefits
- Suggest implementation approach if possible

### 🔧 **Code Contributions**
- Fork the repository
- Create a feature branch
- Make your changes with proper testing
- Submit a pull request with clear description

### 🧪 **Testing**
- Test with different image formats and sizes
- Verify quality preservation
- Test edge cases and error conditions
- Ensure backward compatibility

## Support

### 📚 **Documentation Resources**
- **README.md**: This comprehensive guide
- **PROJECT_OVERVIEW.md**: Quick reference and feature summary
- **ENHANCEMENTS_SUMMARY.md**: Detailed feature documentation
- **Help Command**: `py watermark_script.py --help`

### 🔍 **Getting Help**
1. **Check Documentation**: Review this README and related files
2. **Use Dry Run**: Test configuration with `--dry-run` flag
3. **Review Logs**: Check `watermark_script.log` for detailed information
4. **Console Output**: Review real-time error messages
5. **Verify Paths**: Ensure all file paths and permissions are correct
6. **Test Examples**: Run `py enhanced_examples.py` for demonstrations

### 🆘 **Emergency Help**
- **Script Won't Start**: Check Python installation and dependencies
- **No Images Found**: Verify input folder path and image files
- **Watermark Issues**: Check watermark file format and permissions
- **Quality Problems**: Ensure output format and quality settings
- **Memory Errors**: Process smaller batches or reduce image resolution

### 📞 **Community Support**
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community help
- **Code Examples**: Check the `enhanced_examples.py` script
- **Documentation**: Review all markdown files for detailed information
