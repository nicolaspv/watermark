#!/usr/bin/env python3
"""
Helper script to create a sample PNG watermark for testing.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_watermark():
    """Create a sample PNG watermark."""
    # Create a transparent image
    width, height = 200, 100
    watermark = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Get drawing context
    draw = ImageDraw.Draw(watermark)
    
    # Try to use a nice font
    try:
        # Try common font paths
        font_paths = [
            "arial.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/System/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 24)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Draw text with outline effect
    text = "SAMPLE"
    
    # Draw outline (white)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((50 + dx, 35 + dy), text, fill=(255, 255, 255, 200), font=font)
    
    # Draw main text (blue)
    draw.text((50, 35), text, fill=(0, 100, 200, 255), font=font)
    
    # Add a simple border
    draw.rectangle([0, 0, width-1, height-1], outline=(0, 100, 200, 150), width=2)
    
    # Save as PNG
    watermark.save('sample_watermark.png', 'PNG')
    print("Created sample_watermark.png")

if __name__ == "__main__":
    create_sample_watermark()
