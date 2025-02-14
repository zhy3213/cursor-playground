#!/usr/bin/env python3
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip

def convert_video_to_gif(video_path, target_width=320, target_height=172, offset_y=0):
    """
    Convert video to GIF, maintaining horizontal width and center-cropping vertically
    
    Args:
        video_path: Path to input video
        target_width: Target width (default 320)
        target_height: Target height (default 172)
        offset_y: Vertical offset in pixels (0 means perfectly centered)
    """
    # Build output file path
    video_path = Path(video_path)
    output_filename = f"{video_path.stem}-{target_width}x{target_height}.gif"
    output_path = video_path.parent.parent / "gifs" / output_filename
    
    print(f"Processing video: {video_path}")
    print(f"Output GIF will be saved to: {output_path}")
    
    try:
        # Load video
        video_clip = VideoFileClip(str(video_path))
        
        # Calculate adjusted dimensions
        aspect_ratio = video_clip.w / video_clip.h
        new_height = int(target_width / aspect_ratio)
        
        # First resize to target width
        resized_clip = video_clip.resize(width=target_width)
        
        # If height exceeds target height, perform center crop
        if new_height > target_height:
            # Calculate top and bottom margins to crop
            excess_height = new_height - target_height
            crop_top = excess_height // 2
            
            # Adjust crop position upward
            crop_top = max(0, crop_top - offset_y)  # Ensure we don't crop outside the image
            crop_bottom = min(new_height, crop_top + target_height)  # Ensure we don't exceed the bottom
            
            # Apply cropping
            resized_clip = resized_clip.crop(y1=crop_top, y2=crop_bottom)
        
        # Convert to GIF
        print("Converting to GIF, please wait...")
        print(f"Final dimensions: {resized_clip.w}x{resized_clip.h}")
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        resized_clip.write_gif(
            str(output_path),
            fps=20,  # Moderate frame rate
            program='ffmpeg',  # Use ffmpeg as backend
            opt='OptimizePlus',  # Use optimized settings
        )
        
        # Clean up resources
        video_clip.close()
        resized_clip.close()
        
        print(f"Conversion complete! GIF saved to: {output_path}")
        print(f"File size: {output_path.stat().st_size / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error occurred during conversion: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_to_gif.py <video_file_path>", file=sys.stderr)
        sys.exit(1)
    
    video_path = sys.argv[1]
    convert_video_to_gif(video_path) 