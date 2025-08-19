# Project Overview - Bulk Image Watermark Script

## 🎯 Project Summary
A comprehensive Python-based solution for bulk watermarking images with dual watermarks: custom PNG logos and auto-generated numbers extracted from filenames.

## 📁 File Structure
```
watermark-01/
├── watermark_script.py          # Main watermark processing script
├── requirements.txt             # Python dependencies
├── README.md                   # Comprehensive documentation
├── PROJECT_OVERVIEW.md         # This file - quick reference
├── quick_start.py              # Demo script with sample data
├── enhanced_examples.py        # Comprehensive feature examples
├── create_sample_watermark.py  # Helper to create sample watermark
├── create_test_images.py       # Helper to create test images
├── run_watermark.bat           # Windows batch file runner
└── run_watermark.ps1           # PowerShell script runner
```

## 🚀 Quick Start Options

### Option 1: Full Demo (Recommended for first-time users)
```bash
py quick_start.py
```
This creates sample data and demonstrates the full functionality.

### Option 2: Direct Script Usage
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering
```

### Option 3: Windows Batch File
```bash
run_watermark.bat "C:\Photos" "C:\Watermarked" "C:\logo.png"
```

### Option 4: PowerShell Script
```powershell
.\run_watermark.ps1 -InputFolder ".\photos" -OutputFolder ".\output" -WatermarkFile ".\logo.png"
```

## 🔧 Core Features

### Dual Watermark System
- **PNG Watermark**: Custom logo positioned center-bottom (optional)
- **Custom Text Watermark**: User-defined text (e.g., "mypage.com", "@mytaghere")
- **Number Watermark**: Auto-extracted from filename, positioned bottom-right

### Smart Processing
- Automatic PNG scaling (max 20% of image width)
- Professional text styling with drop shadows
- High-quality LANCZOS resampling
- Preserves exact original image quality with no optimization

### Batch Operations
- Recursive folder scanning
- Multiple image format support (JPG, PNG, TIFF, BMP)
- Progress tracking and comprehensive logging
- Error handling and validation

## 📋 Requirements

### System Requirements
- Windows 10/11 (tested)
- Python 3.7 or higher
- pip package manager

### Dependencies
- Pillow (PIL) >= 10.0.0
- Standard library modules (argparse, os, re, logging, pathlib)

## 🎨 Watermark Specifications

### PNG Watermark
- **Position**: Center-bottom
- **Scaling**: Proportional, max 20% of image width
- **Transparency**: Configurable (0.1-1.0, default: 0.7)
- **Quality**: High-quality LANCZOS resampling

### Number Watermark
- **Position**: Configurable (top-left, top-right, bottom-left, bottom-right, center)
- **Extraction**: Regex pattern matching (default: `\d+`)
- **Styling**: Customizable colors, drop shadow effects
- **Font**: Google Fonts, custom fonts, or system fonts
- **Size**: Proportional to image dimensions
- **Shadow**: Configurable offset, blur, and colors

## 📊 Supported Image Formats
- **JPEG**: .jpg, .jpeg
- **PNG**: .png
- **TIFF**: .tiff, .tif
- **BMP**: .bmp

## ⚙️ Configuration Options

### Required Parameters
- `--input-folder`: Source directory
- `--output-folder`: Destination directory
- `--png-watermark`: PNG watermark file path
- `--enable-numbering`: Enable number extraction

### Optional Parameters
- `--png-opacity`: PNG transparency (0.1-1.0)
- `--number-opacity`: Number transparency (0.1-1.0)
- `--font-size-ratio`: Font size ratio (0.01-0.1)
- `--margin`: Edge margin in pixels (10-100)
- `--number-pattern`: Custom regex pattern
- `--number-position`: Number watermark position
- `--number-color`: Number text color
- `--shadow-color`: Drop shadow color
- `--shadow-offset`: Shadow offset in pixels
- `--shadow-blur`: Shadow blur radius
- `--custom-font`: Custom font file path
- `--google-font`: Google Font name
- `--custom-text`: Custom text watermark
- `--custom-text-position`: Custom text position
- `--custom-text-color`: Custom text color
- `--custom-text-shadow-color`: Custom text shadow color
- `--custom-text-shadow-offset`: Custom text shadow offset
- `--custom-text-shadow-blur`: Custom text shadow blur
- `--custom-text-size-ratio`: Custom text font size ratio
- `--dry-run`: Preview without processing

## 🔍 File Naming Examples

The script automatically extracts numbers from filenames:

| Filename | Extracted Number | Watermark Result |
|----------|------------------|------------------|
| `IMG_001.jpg` | `001` | ✓ Number watermark: "001" |
| `photo_123_2024.png` | `123` | ✓ Number watermark: "123" |
| `vacation_456.jpg` | `456` | ✓ Number watermark: "456" |
| `image.jpg` | None | ⚠️ Warning logged |

## 📈 Performance Features

### Memory Efficiency
- Processes images one at a time
- Minimal memory footprint
- Handles large image files gracefully

### Batch Processing
- Recursive folder scanning
- Progress indicators
- Comprehensive error handling
- Resume capability

## 🛠️ Error Handling

### Validation Checks
- Input folder existence
- Watermark file validity
- PNG format verification
- File permissions

### Processing Errors
- Corrupted image handling
- Font loading fallbacks
- Memory management
- Detailed error logging

## 📝 Logging & Output

### Log File
- `watermark_script.log`
- Timestamped entries
- Success/failure tracking
- Detailed error information

### Console Output
- Real-time progress updates
- File-by-file status
- Summary statistics
- Error notifications

## 🔧 Troubleshooting

### Common Issues
1. **Python not found**: Install Python 3.7+ and ensure `py` command works
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **No numbers in filenames**: Check regex pattern or rename files
4. **Font issues**: Script falls back to system default fonts
5. **Memory errors**: Process smaller batches or reduce image resolution

### Debug Mode
Use `--dry-run` to preview what would be processed:
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./output" --png-watermark "./logo.png" --enable-numbering --dry-run
```

## 🎯 Use Cases

### Professional Photography
- Brand watermarking for portfolios
- Copyright protection
- Client delivery numbering

### Business Applications
- Product image branding
- Marketing material preparation
- Document identification

### Personal Projects
- Family photo organization
- Travel photo collections
- Event photography

## 🚀 Advanced Usage

### Custom Regex Patterns
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
# Basic custom text
--custom-text "mypage.com" --enable-numbering

# Styled custom text
--custom-text "@mytaghere" --custom-text-color "#FF0000" --custom-text-position "top-right"

# Professional custom text
--custom-text "mypage.com" --google-font "Roboto" --custom-text-size-ratio 0.05
```

### Batch Processing Multiple Folders
```bash
# PowerShell example
$folders = @("photos1", "photos2", "photos3")
foreach ($folder in $folders) {
    .\run_watermark.ps1 -InputFolder ".\$folder" -OutputFolder ".\output\$folder" -WatermarkFile ".\logo.png"
}
```

## 📚 Documentation Files

- **README.md**: Comprehensive user guide
- **PROJECT_OVERVIEW.md**: This quick reference
- **watermark_script.py**: Inline code documentation
- **Help command**: `py watermark_script.py --help`

## 🤝 Support & Contributing

### Getting Help
1. Check the log file (`watermark_script.log`)
2. Review console error messages
3. Use `--dry-run` to test configuration
4. Verify all paths and permissions

### Contributing
- Report issues with detailed error messages
- Suggest new features
- Submit pull requests for improvements
- Test with different image types and sizes

---

**Ready to start?** Run `py quick_start.py` for a complete demonstration!
