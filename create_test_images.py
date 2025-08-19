#!/usr/bin/env python3
"""
Helper script to create sample test images for watermark testing.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(filename, width=800, height=600, text="Test Image"):
    """Create a test image with the given filename."""
    # Create image with gradient background
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create a simple gradient background
    for y in range(height):
        r = int(100 + (y / height) * 100)
        g = int(150 + (y / height) * 50)
        b = int(200 + (y / height) * 55)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Try to use a nice font
    try:
        font_paths = [
            "arial.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/System/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 48)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with shadow
    draw.text((x + 3, y + 3), text, fill=(100, 100, 100), font=font)
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Save image
    image.save(filename)
    print(f"Created {filename}")

def create_test_images():
    """Create a set of test images with numbered filenames."""
    # Create test_images directory
    os.makedirs('test_images', exist_ok=True)
    
    # Create images with different names and numbers
    test_cases = [
        ("IMG_001.jpg", 800, 600, "Test Image 001"),
        ("photo_123_2024.png", 1024, 768, "Photo 123"),
        ("vacation_456.jpg", 1200, 800, "Vacation 456"),
        ("event_789.png", 900, 600, "Event 789"),
        ("sample_012.jpg", 750, 500, "Sample 012"),
        ("test_345.png", 1100, 700, "Test 345"),
        ("image_678.jpg", 850, 650, "Image 678"),
        ("photo_901.png", 950, 600, "Photo 901"),
        ("demo_234.jpg", 1000, 750, "Demo 234"),
        ("example_567.png", 800, 600, "Example 567")
    ]
    
    for filename, width, height, text in test_cases:
        filepath = os.path.join('test_images', filename)
        create_test_image(filepath, width, height, text)
    
    print(f"\nCreated {len(test_cases)} test images in 'test_images' folder")
    print("You can now test the watermark script with:")
    print("py watermark_script.py --input-folder './test_images' --output-folder './watermarked' --png-watermark './sample_watermark.png' --enable-numbering")

if __name__ == "__main__":
    create_test_images()
