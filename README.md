# Bulk Image Watermark Script

A powerful Python script for bulk watermarking images with custom PNG logos and auto-generated number watermarks extracted from filenames.

## Features

- **Dual Watermark System**: Custom PNG watermark + auto-generated number watermark
- **Smart Positioning**: PNG watermark centered at bottom, numbers at bottom-right
- **Batch Processing**: Process entire folders of images automatically
- **Quality Preservation**: Maintains original image quality and resolution
- **Flexible Configuration**: Customizable opacity, margins, and font sizes
- **Professional Output**: Drop shadow effects and anti-aliased text
- **Comprehensive Logging**: Detailed progress tracking and error reporting

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
pip install Pillow
```

## Usage

### Basic Command Structure
```bash
py watermark_script.py --input-folder "path/to/input" --output-folder "path/to/output" --png-watermark "logo.png" --enable-numbering
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

### Basic Usage
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering
```

### Custom Settings
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --png-opacity 0.5 --font-size-ratio 0.04 --margin 30
```

### Test Run (Dry Run)
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --dry-run
```

### Custom Number Pattern
```bash
py watermark_script.py --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --number-pattern "IMG_(\d+)_"
```

## How It Works

### PNG Watermark
- **Position**: Center-bottom of image
- **Scaling**: Automatically resized to max 20% of image width
- **Transparency**: Configurable opacity (0.1-1.0)
- **Quality**: High-quality LANCZOS resampling

### Custom Text Watermark
- **Position**: 6 configurable positions including center-bottom
- **Text**: Any custom text (e.g., "mypage.com", "@mytaghere")
- **Styling**: Full color, shadow, and font customization
- **Size**: Proportional to image dimensions
- **Fonts**: Google Fonts, custom fonts, or system fonts

### Number Watermark
- **Position**: Bottom-right corner
- **Extraction**: Uses regex to find numbers in filenames
- **Styling**: Black text with white drop shadow
- **Font**: Professional fonts with fallback to system default
- **Size**: Proportional to image dimensions

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
```

## License

This script is provided as-is for educational and commercial use.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the script.

## Support

For issues or questions:
1. Check the log file (`watermark_script.log`)
2. Review error messages in console output
3. Use `--dry-run` to test configuration
4. Verify all paths and file permissions
