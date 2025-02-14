#!/usr/bin/env python3
import sys
from pathlib import Path
from PIL import Image
import os

def resize_gif(gif_path, target_width=711, target_height=400):
    """
    Resize GIF to specified dimensions and remove black borders
    
    Args:
        gif_path: Path to input GIF
        target_width: Target width
        target_height: Target height
    """
    try:
        # Open GIF file
        gif = Image.open(gif_path)
        
        # Get all frames of the GIF
        frames = []
        try:
            while True:
                # Copy current frame
                frame = gif.copy()
                
                # Resize while maintaining aspect ratio
                aspect_ratio = frame.width / frame.height
                new_height = int(target_width / aspect_ratio)
                
                # First resize to target width
                resized_frame = frame.resize((target_width, new_height), Image.Resampling.LANCZOS)
                
                # If height exceeds target height, perform center crop
                if new_height > target_height:
                    # Calculate top and bottom margins to crop
                    excess_height = new_height - target_height
                    crop_top = excess_height // 2
                    
                    # Crop the image
                    resized_frame = resized_frame.crop((0, crop_top, target_width, crop_top + target_height))
                
                frames.append(resized_frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass  # Reached end of GIF
        
        # Build output file path
        gif_path = Path(gif_path)
        output_filename = f"{gif_path.stem}-{target_width}x{target_height}.gif"
        output_path = gif_path.parent / output_filename
        
        print(f"Processing GIF: {gif_path}")
        print(f"Output will be saved to: {output_path}")
        
        # Save the resized GIF
        frames[0].save(
            str(output_path),
            save_all=True,
            append_images=frames[1:],
            duration=gif.info.get('duration', 100),  # Keep original frame rate
            loop=0,  # 0 means infinite loop
            optimize=True  # Optimize file size
        )
        
        print(f"Processing complete! New GIF saved to: {output_path}")
        print(f"File size: {output_path.stat().st_size / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error occurred during processing: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gif_resize.py <gif_file_path>", file=sys.stderr)
        sys.exit(1)
    
    gif_path = sys.argv[1]
    resize_gif(gif_path) 