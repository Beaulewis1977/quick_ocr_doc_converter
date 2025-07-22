#!/usr/bin/env python3
"""
Create Windows Icon File for Quick Document Convertor
Generates a professional-looking .ico file for the application
"""

from PIL import Image, ImageDraw
from pathlib import Path
import sys

def create_icon_image(size: int = 256) -> Image.Image:
    """Create a professional icon image"""
    # Create image with transparent background
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Scale factors based on size
    scale = size / 64
    
    # Colors
    doc_color = (70, 130, 180, 255)  # Steel blue
    doc_outline = (25, 25, 112, 255)  # Midnight blue
    fold_color = (135, 206, 235, 255)  # Sky blue
    line_color = (255, 255, 255, 200)  # White with transparency
    arrow_color = (255, 215, 0, 255)  # Gold
    
    # Document body
    doc_left = int(12 * scale)
    doc_top = int(8 * scale)
    doc_right = int(52 * scale)
    doc_bottom = int(56 * scale)
    
    draw.rectangle([doc_left, doc_top, doc_right, doc_bottom], 
                  fill=doc_color, outline=doc_outline, width=max(1, int(2 * scale)))
    
    # Document fold corner
    fold_size = int(10 * scale)
    fold_points = [
        (doc_right - fold_size, doc_top),
        (doc_right, doc_top),
        (doc_right, doc_top + fold_size),
        (doc_right - fold_size, doc_top)
    ]
    draw.polygon(fold_points, fill=fold_color)
    
    # Fold lines
    draw.line([
        (doc_right - fold_size, doc_top),
        (doc_right - fold_size, doc_top + fold_size),
        (doc_right, doc_top + fold_size)
    ], fill=doc_outline, width=max(1, int(1 * scale)))
    
    # Document lines (text representation)
    line_start_x = int(18 * scale)
    line_end_x = int(46 * scale)
    line_start_y = int(20 * scale)
    line_spacing = int(6 * scale)
    
    for i in range(3):
        y = line_start_y + i * line_spacing
        draw.line([(line_start_x, y), (line_end_x, y)], 
                 fill=line_color, width=max(1, int(2 * scale)))
    
    # Conversion arrow
    arrow_center_x = int(32 * scale)
    arrow_top_y = int(42 * scale)
    arrow_bottom_y = int(48 * scale)
    arrow_width = int(4 * scale)
    
    arrow_points = [
        (arrow_center_x - arrow_width, arrow_top_y),
        (arrow_center_x + arrow_width, arrow_top_y),
        (arrow_center_x, arrow_bottom_y)
    ]
    draw.polygon(arrow_points, fill=arrow_color)
    
    return image

def create_ico_file(output_path: Path):
    """Create a multi-resolution .ico file"""
    # Common icon sizes for Windows
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Create images for each size
    images = []
    for size in sizes:
        img = create_icon_image(size)
        images.append(img)
    
    # Save as ICO file with multiple resolutions
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print(f"✅ Created icon file: {output_path}")
    print(f"📏 Resolutions: {', '.join(f'{s}x{s}' for s in sizes)}")

def main():
    """Main function"""
    print("🎨 Creating Windows Icon File...")
    print("=" * 40)
    
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("❌ PIL (Pillow) not available")
        print("Install with: pip install pillow")
        sys.exit(1)
    
    # Create icon file
    output_path = Path(__file__).parent / "icon.ico"
    
    try:
        create_ico_file(output_path)
        print(f"\n🎉 Icon created successfully!")
        print(f"📁 Location: {output_path}")
        print(f"📏 Size: {output_path.stat().st_size} bytes")
        
    except Exception as e:
        print(f"❌ Failed to create icon: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 