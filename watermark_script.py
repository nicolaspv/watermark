#!/usr/bin/env python3
"""
Bulk Image Watermark Script
Adds custom PNG watermark and auto-generated number watermark to images in batch.
"""

import argparse
import os
import re
import logging
import requests
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('watermark_script.log')
    ]
)
logger = logging.getLogger(__name__)

class WatermarkProcessor:
    """Handles watermark processing for images."""
    
    def __init__(self, png_watermark_path: str = None, enable_numbering: bool = True,
                 png_opacity: float = 0.7, number_opacity: float = 0.8,
                 font_size_ratio: float = 0.03, margin: int = 20,
                 number_pattern: str = r'\d+', number_position: str = 'bottom-right',
                 number_color: str = '#000000', shadow_color: str = '#FFFFFF',
                 shadow_offset: int = 3, shadow_blur: int = 1, shadow_opacity: float = 0.8,
                 custom_font_path: str = None, google_font_name: str = None,
                 custom_text: str = None, custom_text_position: str = 'center-bottom',
                 custom_text_color: str = '#000000', custom_text_shadow_color: str = '#FFFFFF',
                 custom_text_shadow_offset: int = 3, custom_text_shadow_blur: int = 1,
                 custom_text_shadow_opacity: float = 0.8, custom_text_size_ratio: float = 0.04, custom_text_opacity: float = 0.8,
                 png_position: str = 'center-bottom', png_x_offset: int = 0, png_y_offset: int = 0,
                 number_x_offset: int = 0, number_y_offset: int = 0):
        """
        Initialize watermark processor.
        
        Args:
            png_watermark_path: Path to PNG watermark file (None for text-only mode)
            enable_numbering: Whether to add number watermarks
            png_opacity: PNG watermark transparency (0.1-1.0)
            number_opacity: Number watermark transparency
            font_size_ratio: Font size as ratio of image height
            margin: Margin from edges in pixels
            number_pattern: Regex pattern for number extraction
            number_position: Position of number watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
            number_color: Color of number text (hex color or color name)
            shadow_color: Color of drop shadow (hex color or color name)
            shadow_offset: Offset of drop shadow in pixels
            shadow_blur: Blur radius of drop shadow
            custom_font_path: Path to custom font file (.ttf, .otf)
            google_font_name: Google Font name to download and use
            custom_text: Custom text watermark (e.g., "mypage.com", "@mytaghere")
            custom_text_position: Position of custom text watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center', 'center-bottom')
            custom_text_color: Color of custom text (hex color or color name)
            custom_text_shadow_color: Color of custom text drop shadow (hex color or color name)
            custom_text_shadow_offset: Offset of custom text drop shadow in pixels
            custom_text_shadow_blur: Blur radius of custom text drop shadow
            custom_text_shadow_opacity: Custom text shadow transparency (0.1-1.0)
            custom_text_size_ratio: Custom text font size as ratio of image height
            custom_text_opacity: Custom text transparency (0.1-1.0)
            png_position: Position of PNG watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center', 'center-bottom')
            png_x_offset: X offset for PNG watermark position (can be negative)
            png_y_offset: Y offset for PNG watermark position (can be negative)
            number_x_offset: X offset for number watermark position (can be negative)
            number_y_offset: Y offset for number watermark position (can be negative)
        """
        self.png_watermark_path = png_watermark_path
        self.enable_numbering = enable_numbering
        self.png_opacity = max(0.1, min(1.0, png_opacity))
        self.number_opacity = max(0.1, min(1.0, number_opacity))
        self.font_size_ratio = font_size_ratio
        self.margin = margin
        self.number_pattern = number_pattern
        self.number_position = number_position
        self.number_color = number_color
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.shadow_blur = shadow_blur
        self.custom_font_path = custom_font_path
        self.google_font_name = google_font_name
        self.custom_text = custom_text
        self.custom_text_position = custom_text_position
        self.custom_text_color = custom_text_color
        self.custom_text_shadow_color = custom_text_shadow_color
        self.custom_text_shadow_offset = custom_text_shadow_offset
        self.custom_text_shadow_blur = custom_text_shadow_blur
        self.custom_text_shadow_opacity = max(0.1, min(1.0, custom_text_shadow_opacity))
        self.custom_text_size_ratio = custom_text_size_ratio
        self.custom_text_opacity = max(0.1, min(1.0, custom_text_opacity))
        self.png_position = png_position
        self.png_x_offset = png_x_offset
        self.png_y_offset = png_y_offset
        self.number_x_offset = number_x_offset
        self.number_y_offset = number_y_offset
        
        # Load PNG watermark (if provided)
        self.png_watermark = self._load_png_watermark() if png_watermark_path else None
        
        # Initialize font
        self.font = self._initialize_font()
    
    def _load_png_watermark(self) -> Optional[Image.Image]:
        """Load and validate PNG watermark."""
        try:
            watermark = Image.open(self.png_watermark_path).convert('RGBA')
            logger.info(f"Loaded PNG watermark: {self.png_watermark_path}")
            return watermark
        except Exception as e:
            logger.error(f"Failed to load PNG watermark: {e}")
            return None
    
    def _initialize_font(self) -> Optional[ImageFont.FreeTypeFont]:
        """Initialize font for number watermarks."""
        try:
            # Priority 1: Custom font file
            if self.custom_font_path and os.path.exists(self.custom_font_path):
                logger.info(f"Loading custom font: {self.custom_font_path}")
                return ImageFont.truetype(self.custom_font_path, 24)
            
            # Priority 2: Google Font
            if self.google_font_name:
                font_path = self._download_google_font(self.google_font_name)
                if font_path:
                    logger.info(f"Loaded Google Font: {self.google_font_name}")
                    return ImageFont.truetype(font_path, 24)
            
            # Priority 3: System fonts
            font_paths = [
                "arial.ttf",
                "C:/Windows/Fonts/arial.ttf",
                "/System/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    logger.info(f"Using system font: {font_path}")
                    return ImageFont.truetype(font_path, 24)
            
            # Fallback to default font
            logger.info("Using default system font")
            return ImageFont.load_default()
        except Exception as e:
            logger.warning(f"Could not load custom font, using default: {e}")
            return ImageFont.load_default()
    
    def _download_google_font(self, font_name: str) -> Optional[str]:
        """Download and cache a Google Font."""
        try:
            # Google Fonts API endpoint
            api_url = f"https://fonts.googleapis.com/css2?family={font_name.replace(' ', '+')}:wght@400;700&display=swap"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch Google Font {font_name}")
                return None
            
            # Extract font URL from CSS
            css_content = response.text
            font_url_match = re.search(r'src:\s*url\(([^)]+)\)', css_content)
            if not font_url_match:
                logger.warning(f"Could not extract font URL for {font_name}")
                return None
            
            font_url = font_url_match.group(1)
            if font_url.startswith('//'):
                font_url = 'https:' + font_url
            
            # Download font file
            font_response = requests.get(font_url, timeout=30)
            if font_response.status_code != 200:
                logger.warning(f"Failed to download font file for {font_name}")
                return None
            
            # Save to temporary file
            font_ext = '.ttf' if 'woff2' not in font_url else '.woff2'
            temp_font = tempfile.NamedTemporaryFile(delete=False, suffix=font_ext)
            temp_font.write(font_response.content)
            temp_font.close()
            
            logger.info(f"Downloaded Google Font: {font_name} -> {temp_font.name}")
            return temp_font.name
            
        except Exception as e:
            logger.warning(f"Failed to download Google Font {font_name}: {e}")
            return None
    
    def _extract_number_from_filename(self, filename: str) -> Optional[str]:
        """Extract number from filename using regex pattern."""
        if not self.enable_numbering:
            return None
        
        # Remove file extension
        name_without_ext = Path(filename).stem
        
        # Find all numbers in filename
        numbers = re.findall(self.number_pattern, name_without_ext)
        
        if numbers:
            # Return the first number found
            return numbers[0]
        
        logger.warning(f"No numbers found in filename: {filename}")
        return None
    
    def _calculate_watermark_positions(self, image: Image.Image) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Calculate positions for both watermarks."""
        img_width, img_height = image.size
        
        # PNG watermark position (center-bottom) or custom text position
        if self.png_watermark:
            png_width, png_height = self.png_watermark.size
            png_x, png_y = self._calculate_png_position(image, img_width, img_height, png_width, png_height)
        elif self.custom_text:
            # Create temporary text watermark to get dimensions
            temp_text_watermark = self._create_custom_text_watermark(self.custom_text, image)
            png_width, png_height = temp_text_watermark.size
            png_x, png_y = self._calculate_custom_text_position(image, img_width, img_height, png_width, png_height)
        else:
            # No watermark
            png_x, png_y = 0, 0
        
        # Number watermark position will be calculated later in process_image
        # after we have the actual number watermark dimensions
        number_x, number_y = 0, 0
        
        return (png_x, png_y), (number_x, number_y)
    
    def _calculate_number_position(self, image: Image.Image, img_width: int, img_height: int, number_width: int = None, number_height: int = None) -> Tuple[int, int]:
        """Calculate number watermark position based on configuration."""
        # Add extra safety margin for shadow effects to prevent cutting (same as custom text)
        # The watermark canvas now properly accounts for shadows, but we need safety margins for positioning
        # For small blur values, we need more safety margin to prevent cutting
        blur_safety = max(self.shadow_blur * 2, 15)  # Minimum 15px for blur safety
        safety_margin = max(self.shadow_offset + blur_safety + 25, 40)  # Increased from 20 to 25, min from 30 to 40
        
        # Use actual number dimensions if provided, otherwise use approximate dimensions
        if number_width is None:
            number_width = 100  # Approximate width for initial calculation
        if number_height is None:
            number_height = 30  # Approximate height for initial calculation
        
        if self.number_position == 'top-left':
            x_pos = self.margin + safety_margin + self.number_x_offset
            y_pos = self.margin + safety_margin + self.number_y_offset
            return (x_pos, y_pos)
        elif self.number_position == 'top-right':
            # For right-aligned positions, use the RIGHT edge of the number as reference point
            # This ensures all numbers align properly regardless of their width
            x_pos = img_width - self.margin - safety_margin - number_width + self.number_x_offset
            y_pos = self.margin + safety_margin + self.number_y_offset
            return (x_pos, y_pos)
        elif self.number_position == 'bottom-left':
            x_pos = self.margin + safety_margin + self.number_x_offset
            y_pos = img_height - number_height - self.margin - safety_margin + self.number_y_offset
            return (x_pos, y_pos)
        elif self.number_position == 'center':
            x_pos = (img_width - number_width) // 2 + self.number_x_offset
            y_pos = (img_height - number_height) // 2 + self.number_y_offset
            return (x_pos, y_pos)
        else:  # bottom-right (default)
            # For right-aligned positions, use the RIGHT edge of the number as reference point
            # This ensures all numbers align properly regardless of their width
            x_pos = img_width - self.margin - safety_margin - number_width + self.number_x_offset
            y_pos = img_height - number_height - self.margin - safety_margin + self.number_y_offset
            return (x_pos, y_pos)
    
    def _calculate_custom_text_position(self, image: Image.Image, img_width: int, img_height: int, text_width: int, text_height: int) -> Tuple[int, int]:
        """Calculate custom text watermark position based on configuration."""
        # IMPORTANT: text_width and text_height are actually the CANVAS dimensions (including shadows)
        # This is passed from _calculate_watermark_positions after creating the watermark
        
        # Add extra safety margin for shadow effects to prevent cutting
        # For small blur values, we need more safety margin to prevent cutting
        blur_safety = max(self.custom_text_shadow_blur * 2, 15)  # Minimum 15px for blur safety
        safety_margin = max(self.custom_text_shadow_offset + blur_safety + 25, 40)  # Increased from 20 to 25, min from 30 to 40
        
        if self.custom_text_position == 'top-left':
            return (self.margin + safety_margin, self.margin + safety_margin)
        elif self.custom_text_position == 'top-right':
            return (img_width - text_width - self.margin - safety_margin, self.margin + safety_margin)
        elif self.custom_text_position == 'bottom-left':
            return (self.margin + safety_margin, img_height - text_height - self.margin - safety_margin)
        elif self.custom_text_position == 'center':
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        elif self.custom_text_position == 'center-bottom':
            return ((img_width - text_width) // 2, img_height - text_height - self.margin - safety_margin)
        else:  # center-bottom (default)
            return ((img_width - text_width) // 2, img_height - text_height - self.margin - safety_margin)
    
    def _calculate_png_position(self, image: Image.Image, img_width: int, img_height: int, png_width: int, png_height: int) -> Tuple[int, int]:
        """Calculate PNG watermark position based on configuration."""
        if self.png_position == 'top-left':
            x_pos = self.margin + self.png_x_offset
            y_pos = self.margin + self.png_y_offset
            return (x_pos, y_pos)
        elif self.png_position == 'top-right':
            x_pos = img_width - png_width - self.margin + self.png_x_offset
            y_pos = self.margin + self.png_y_offset
            return (x_pos, y_pos)
        elif self.png_position == 'bottom-left':
            # For bottom-left, place exactly at bottom edge with offset support
            x_pos = self.margin + self.png_x_offset
            # Calculate Y position to place watermark exactly at bottom edge
            # img_height - png_height gives us the top edge of the watermark
            # We want it to sit exactly at the bottom, so no additional margin
            y_pos = img_height - png_height + self.png_y_offset
            return (x_pos, y_pos)
        elif self.png_position == 'center':
            x_pos = (img_width - png_width) // 2 + self.png_x_offset
            y_pos = (img_height - png_height) // 2 + self.png_y_offset
            return (x_pos, y_pos)
        elif self.png_position == 'center-bottom':
            # For center-bottom, use the margin value for bottom
            x_pos = (img_width - png_width) // 2 + self.png_x_offset
            y_pos = img_height - png_height - self.margin + self.png_y_offset
            return (x_pos, y_pos)
        else:  # center-bottom (default)
            # For center-bottom, use the margin value for bottom
            x_pos = (img_width - png_width) // 2 + self.png_x_offset
            y_pos = img_height - png_height - self.margin + self.png_y_offset
            return (x_pos, y_pos)
    
    def _resize_png_watermark(self, image: Image.Image) -> Image.Image:
        """Resize PNG watermark proportionally based on image size."""
        img_width, img_height = image.size
        
        # Calculate target size (increased from 20% to 30% of image width for bigger watermark)
        max_width = int(img_width * 0.3)  # Increased from 0.2 to 0.3
        max_height = int(img_height * 0.25)  # Increased from 0.15 to 0.25
        
        # Get current watermark dimensions
        wm_width, wm_height = self.png_watermark.size
        
        # Calculate scaling factor
        scale_x = max_width / wm_width
        scale_y = max_height / wm_height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        if scale < 1.0:
            new_width = int(wm_width * scale)
            new_height = int(wm_height * scale)
            return self.png_watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return self.png_watermark
    
    def _create_number_watermark(self, number: str, image: Image.Image) -> Image.Image:
        """Create number watermark with customizable drop shadow effect."""
        # Calculate font size based on image dimensions
        font_size = max(12, int(image.height * self.font_size_ratio))
        
        try:
            # Try to load font with calculated size
            if hasattr(self.font, 'font_variant'):
                font = ImageFont.truetype(self.font.path, font_size)
            else:
                # For default font, we'll scale the text differently
                font = self.font
        except:
            font = self.font
        
        # Get text dimensions for proper canvas sizing
        bbox = font.getbbox(number)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create canvas with proper dimensions - account for shadow offset AND blur
        # Blur effect extends the shadow beyond the offset - need more space for proper blur rendering
        # For small blur values, we need more padding to prevent cutting
        blur_extension = max(self.shadow_blur * 3, 20)  # Increased from 2x to 3x + minimum 20px
        # Increase padding significantly to prevent any cutting - especially for bottom shadows
        canvas_width = text_width + self.shadow_offset + blur_extension + 100
        canvas_height = text_height + self.shadow_offset + blur_extension + 120  # Extra height for bottom shadows
        text_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        # Convert colors to RGBA
        number_rgba = self._hex_to_rgba(self.number_color, self.number_opacity)
        shadow_rgba = self._hex_to_rgba(self.shadow_color, self.number_opacity)
        
        # Calculate center position for text within canvas
        text_x = (canvas_width - text_width) // 2
        text_y = (canvas_height - text_height) // 2
        
        # Apply blur to shadow if specified
        if self.shadow_blur > 0:
            # Create a separate shadow layer for blurring to prevent cutting
            shadow_layer = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)
            
            # Draw shadow with the specified shadow color
            shadow_x = text_x + self.shadow_offset
            shadow_y = text_y + self.shadow_offset
            shadow_draw.text((shadow_x, shadow_y), number, fill=shadow_rgba, font=font)
            
            # Apply blur to shadow layer
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=self.shadow_blur))
            
            # Composite the blurred shadow onto the main image
            text_img = Image.alpha_composite(text_img, shadow_layer)
            
            # Redraw the main text on top
            draw = ImageDraw.Draw(text_img)
        else:
            # No blur - draw simple shadow
            shadow_x = text_x + self.shadow_offset
            shadow_y = text_y + self.shadow_offset
            draw.text((shadow_x, shadow_y), number, fill=shadow_rgba, font=font)
        
        # Draw main text
        draw.text((text_x, text_y), number, fill=number_rgba, font=font)
        
        return text_img
    
    def _hex_to_rgba(self, color: str, opacity: float) -> Tuple[int, int, int, int]:
        """Convert hex color or color name to RGBA tuple."""
        try:
            # Handle hex colors
            if color.startswith('#'):
                color = color.lstrip('#')
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
                a = int(255 * opacity)
                return (r, g, b, a)
            
            # Handle named colors
            color_map = {
                'black': (0, 0, 0),
                'white': (255, 255, 255),
                'red': (255, 0, 0),
                'green': (0, 128, 0),
                'blue': (0, 0, 255),
                'yellow': (255, 255, 0),
                'cyan': (0, 255, 255),
                'magenta': (255, 0, 255),
                'gray': (128, 128, 128),
                'orange': (255, 165, 0),
                'purple': (128, 0, 128),
                'brown': (165, 42, 42)
            }
            
            if color.lower() in color_map:
                r, g, b = color_map[color.lower()]
                a = int(255 * opacity)
                return (r, g, b, a)
            
            # Default to black if color not recognized
            return (0, 0, 0, int(255 * opacity))
            
        except Exception as e:
            logger.warning(f"Invalid color '{color}', using black: {e}")
            return (0, 0, 0, int(255 * opacity))
    
    def _create_custom_text_watermark(self, text: str, image: Image.Image) -> Image.Image:
        """Create custom text watermark with customizable drop shadow effect."""
        # Calculate font size based on image dimensions
        font_size = max(16, int(image.height * self.custom_text_size_ratio))
        
        try:
            # Try to load font with calculated size
            if hasattr(self.font, 'font_variant'):
                font = ImageFont.truetype(self.font.path, font_size)
            else:
                # For default font, we'll scale the text differently
                font = self.font
        except:
            font = self.font
        
        # Get text dimensions for proper canvas sizing
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create canvas with proper dimensions - account for shadow offset AND blur
        # Blur effect extends the shadow beyond the offset - need more space for proper blur rendering
        # For small blur values, we need more padding to prevent cutting
        blur_extension = max(self.custom_text_shadow_blur * 3, 20)  # Increased from 2x to 3x + minimum 20px
        # Increase padding significantly to prevent any cutting - especially for bottom shadows
        canvas_width = text_width + self.custom_text_shadow_offset + blur_extension + 100
        canvas_height = text_height + self.custom_text_shadow_offset + blur_extension + 120  # Extra height for bottom shadows
        text_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        # Convert colors to RGBA
        text_rgba = self._hex_to_rgba(self.custom_text_color, self.custom_text_opacity)
        shadow_rgba = self._hex_to_rgba(self.custom_text_shadow_color, self.custom_text_shadow_opacity)
        
        # Calculate center position for text within canvas
        text_x = (canvas_width - text_width) // 2
        text_y = (canvas_height - text_height) // 2
        
        # Apply blur to shadow if specified
        if self.custom_text_shadow_blur > 0:
            # Create a separate shadow layer for blurring to prevent cutting
            shadow_layer = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)
            
            # Draw shadow with the specified shadow color
            shadow_x = text_x + self.custom_text_shadow_offset
            shadow_y = text_y + self.custom_text_shadow_offset
            shadow_draw.text((shadow_x, shadow_y), text, fill=shadow_rgba, font=font)
            
            # Apply blur to shadow layer
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=self.custom_text_shadow_blur))
            
            # Composite the blurred shadow onto the main image
            text_img = Image.alpha_composite(text_img, shadow_layer)
            
            # Redraw the main text on top
            draw = ImageDraw.Draw(text_img)
        else:
            # No blur - draw simple shadow
            shadow_x = text_x + self.custom_text_shadow_offset
            shadow_y = text_y + self.custom_text_shadow_offset
            draw.text((shadow_x, shadow_y), text, fill=shadow_rgba, font=font)
        
        # Draw main text
        draw.text((text_x, text_y), text, fill=text_rgba, font=font)
        
        return text_img
    
    def process_image(self, input_path: str, output_path: str) -> bool:
        """
        Process a single image with watermarks.
        
        Args:
            input_path: Path to input image
            output_path: Path to save watermarked image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open and convert image to RGBA
            with Image.open(input_path) as img:
                # Convert to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Create a copy for watermarking
                watermarked = img.copy()
                
                # Extract number from filename
                number = self._extract_number_from_filename(Path(input_path).name)
                
                # Calculate watermark positions
                png_pos, number_pos = self._calculate_watermark_positions(watermarked)
                
                # Apply PNG watermark or custom text watermark
                if self.png_watermark:
                    resized_png = self._resize_png_watermark(watermarked)
                    
                    # Create a copy of PNG watermark with proper alpha handling
                    # Instead of overwriting alpha with putalpha(), we'll blend the alpha properly
                    png_with_opacity = resized_png.copy()
                    
                    # Get the original alpha channel
                    original_alpha = png_with_opacity.split()[-1]  # Get alpha channel
                    
                    # Apply opacity to the alpha channel while preserving transparency
                    if self.png_opacity != 1.0:
                        # Create new alpha channel with adjusted opacity
                        new_alpha = original_alpha.point(lambda x: int(x * self.png_opacity))
                        png_with_opacity.putalpha(new_alpha)
                    
                    # Paste PNG watermark
                    watermarked.paste(png_with_opacity, png_pos, png_with_opacity)
                elif self.custom_text:
                    # Create and apply custom text watermark
                    custom_text_watermark = self._create_custom_text_watermark(self.custom_text, watermarked)
                    
                    # Paste custom text watermark
                    watermarked.paste(custom_text_watermark, png_pos, custom_text_watermark)
                
                # Apply number watermark
                if number and self.enable_numbering:
                    number_watermark = self._create_number_watermark(number, watermarked)
                    
                    # Get the dimensions of the number watermark
                    bbox = number_watermark.getbbox()
                    number_width = bbox[2] - bbox[0]
                    number_height = bbox[3] - bbox[1]
                    
                    # Calculate the position for the number watermark
                    # The number_pos was calculated earlier and includes the number_x_offset and number_y_offset
                    number_x, number_y = self._calculate_number_position(watermarked, watermarked.width, watermarked.height, number_width, number_height)
                    
                    watermarked.paste(number_watermark, (number_x, number_y), number_watermark)
                
                # Save watermarked image
                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Convert back to original mode for saving
                if img.mode != 'RGBA':
                    watermarked = watermarked.convert(img.mode)
                
                # Save with original quality - no optimization or quality reduction
                if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                    # For JPEG, ensure we're in RGB mode
                    if watermarked.mode == 'RGBA':
                        watermarked = watermarked.convert('RGB')
                    # Save with maximum quality, no optimization to preserve original quality
                    watermarked.save(output_path, 'JPEG', quality=100, optimize=False)
                else:
                    # For other formats, save as is with no optimization
                    watermarked.save(output_path, optimize=False)
                
                logger.info(f"Successfully processed: {input_path} -> {output_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to process {input_path}: {e}")
            return False

def validate_inputs(input_folder: str, output_folder: str, png_watermark: str = None, custom_text: str = None) -> bool:
    """Validate input parameters."""
    # Check input folder
    if not os.path.isdir(input_folder):
        logger.error(f"Input folder does not exist: {input_folder}")
        return False
    
    # Check that either PNG watermark or custom text is provided
    if not png_watermark and not custom_text:
        logger.error("Either PNG watermark file or custom text must be provided")
        return False
    
    # Check PNG watermark if provided
    if png_watermark:
        if not os.path.isfile(png_watermark):
            logger.error(f"PNG watermark file does not exist: {png_watermark}")
            return False
        
        # Check if PNG watermark is actually a PNG
        try:
            with Image.open(png_watermark) as img:
                if img.format != 'PNG':
                    logger.error(f"Watermark file is not a PNG: {png_watermark}")
                    return False
        except Exception as e:
            logger.error(f"Cannot open watermark file: {e}")
            return False
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    return True

def get_image_files(input_folder: str) -> list:
    """Get list of image files from input folder."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp'}
    image_files = []
    
    for file_path in Path(input_folder).rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(str(file_path))
    
    return sorted(image_files)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Bulk image watermark script with PNG and number watermarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="""
 Examples:
   # PNG watermark with numbering
   %(prog)s --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering
   
   # Custom text watermark with numbering
   %(prog)s --input-folder "./photos" --output-folder "./watermarked" --custom-text "mypage.com" --enable-numbering
   
   # Custom text with styling
   %(prog)s --input-folder "./photos" --output-folder "./watermarked" --custom-text "@mytaghere" --custom-text-color "#FF0000" --custom-text-position "top-right" --enable-numbering
   
   # PNG watermark with custom settings
   %(prog)s --input-folder "./photos" --output-folder "./watermarked" --png-watermark "./logo.png" --enable-numbering --png-opacity 0.5 --font-size-ratio 0.04 --margin 30
        """
    )
    
    # Required arguments
    parser.add_argument('--input-folder', required=True,
                       help='Source directory containing images to process')
    parser.add_argument('--output-folder', required=True,
                       help='Destination directory for watermarked images')
    parser.add_argument('--png-watermark', required=False,
                       help='Path to PNG watermark file (optional if using custom text)')
    parser.add_argument('--enable-numbering', action='store_true',
                       help='Enable automatic number watermark extraction from filenames')
    
    # Optional arguments
    parser.add_argument('--png-opacity', type=float, default=0.7,
                       help='PNG watermark transparency (0.1-1.0, default: 0.7)')
    parser.add_argument('--number-opacity', type=float, default=0.8,
                       help='Number watermark transparency (default: 0.8)')
    parser.add_argument('--font-size-ratio', type=float, default=0.03,
                       help='Number font size as ratio of image height (default: 0.03)')
    parser.add_argument('--margin', type=int, default=20,
                       help='Margin from edges in pixels (default: 20)')
    parser.add_argument('--number-pattern', default=r'\d+',
                       help='Regex pattern for number extraction (default: r\'\\d+\')')
    parser.add_argument('--number-position', choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                       default='bottom-right', help='Position of number watermark (default: bottom-right)')
    parser.add_argument('--number-color', default='#000000',
                       help='Color of number text (hex color or color name, default: #000000)')
    parser.add_argument('--shadow-color', default='#FFFFFF',
                       help='Color of drop shadow (hex color or color name, default: #FFFFFF)')
    parser.add_argument('--shadow-offset', type=int, default=3,
                       help='Offset of drop shadow in pixels (default: 3)')
    parser.add_argument('--shadow-blur', type=int, default=1,
                       help='Blur radius of drop shadow (default: 1)')
    parser.add_argument('--shadow-opacity', type=float, default=0.8,
                       help='Number watermark shadow transparency (0.1-1.0, default: 0.8)')
    parser.add_argument('--custom-font', default=None,
                       help='Path to custom font file (.ttf, .otf)')
    parser.add_argument('--google-font', default=None,
                       help='Google Font name to download and use')
    parser.add_argument('--custom-text', default=None,
                       help='Custom text watermark (e.g., "mypage.com", "@mytaghere")')
    parser.add_argument('--custom-text-position', choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center', 'center-bottom'],
                       default='center-bottom', help='Position of custom text watermark (default: center-bottom)')
    parser.add_argument('--custom-text-color', default='#000000',
                       help='Color of custom text (hex color or color name, default: #000000)')
    parser.add_argument('--custom-text-shadow-color', default='#FFFFFF',
                       help='Color of custom text drop shadow (hex color or color name, default: #FFFFFF)')
    parser.add_argument('--custom-text-shadow-offset', type=int, default=3,
                       help='Offset of custom text drop shadow in pixels (default: 3)')
    parser.add_argument('--custom-text-shadow-blur', type=int, default=1,
                       help='Blur radius of custom text drop shadow (default: 1)')
    parser.add_argument('--custom-text-shadow-opacity', type=float, default=0.8,
                       help='Custom text shadow transparency (0.1-1.0, default: 0.8)')
    parser.add_argument('--custom-text-size-ratio', type=float, default=0.04,
                       help='Custom text font size as ratio of image height (default: 0.04)')
    parser.add_argument('--custom-text-opacity', type=float, default=0.8,
                       help='Custom text transparency (0.1-1.0, default: 0.8)')
    parser.add_argument('--png-position', choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center', 'center-bottom'],
                       default='center-bottom', help='Position of PNG watermark (default: center-bottom)')
    parser.add_argument('--png-x-offset', type=int, default=0,
                       help='X offset for PNG watermark position (can be negative, default: 0)')
    parser.add_argument('--png-y-offset', type=int, default=0,
                       help='Y offset for PNG watermark position (can be negative, default: 0)')
    parser.add_argument('--number-x-offset', type=int, default=0,
                       help='X offset for number watermark position (can be negative, default: 0)')
    parser.add_argument('--number-y-offset', type=int, default=0,
                       help='Y offset for number watermark position (can be negative, default: 0)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without actually processing')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not validate_inputs(args.input_folder, args.output_folder, args.png_watermark, args.custom_text):
        sys.exit(1)
    
    # Initialize watermark processor
    processor = WatermarkProcessor(
        png_watermark_path=args.png_watermark,
        enable_numbering=args.enable_numbering,
        png_opacity=args.png_opacity,
        number_opacity=args.number_opacity,
        font_size_ratio=args.font_size_ratio,
        margin=args.margin,
        number_pattern=args.number_pattern,
        number_position=args.number_position,
        number_color=args.number_color,
        shadow_color=args.shadow_color,
        shadow_offset=args.shadow_offset,
        shadow_blur=args.shadow_blur,
        shadow_opacity=args.shadow_opacity,
        custom_font_path=args.custom_font,
        google_font_name=args.google_font,
        custom_text=args.custom_text,
        custom_text_position=args.custom_text_position,
        custom_text_color=args.custom_text_color,
        custom_text_shadow_color=args.custom_text_shadow_color,
        custom_text_shadow_offset=args.custom_text_shadow_offset,
        custom_text_shadow_blur=args.custom_text_shadow_blur,
        custom_text_shadow_opacity=args.custom_text_shadow_opacity,
        custom_text_size_ratio=args.custom_text_size_ratio,
        custom_text_opacity=args.custom_text_opacity,
        png_position=args.png_position,
        png_x_offset=args.png_x_offset,
        png_y_offset=args.png_y_offset,
        number_x_offset=args.number_x_offset,
        number_y_offset=args.number_y_offset
    )
    
    # Get list of image files
    image_files = get_image_files(args.input_folder)
    
    if not image_files:
        logger.warning(f"No image files found in: {args.input_folder}")
        return
    
    logger.info(f"Found {len(image_files)} image files to process")
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be processed")
        for img_file in image_files:
            output_file = os.path.join(args.output_folder, Path(img_file).name)
            logger.info(f"Would process: {img_file} -> {output_file}")
        return
    
    # Process images
    successful = 0
    failed = 0
    
    for i, img_file in enumerate(image_files, 1):
        logger.info(f"Processing {i}/{len(image_files)}: {Path(img_file).name}")
        
        # Create output path
        output_file = os.path.join(args.output_folder, Path(img_file).name)
        
        # Process image
        if processor.process_image(img_file, output_file):
            successful += 1
        else:
            failed += 1
    
    # Summary
    logger.info(f"Processing complete!")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Total: {len(image_files)}")

if __name__ == "__main__":
    main()
