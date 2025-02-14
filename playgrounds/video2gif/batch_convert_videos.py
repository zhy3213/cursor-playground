#!/usr/bin/env python3
import sys
from pathlib import Path
from video_to_gif import convert_video_to_gif

def batch_convert_videos(videos_dir):
    """
    Batch convert all video files in the specified directory to GIF
    
    Args:
        videos_dir: Directory containing video files
    """
    videos_path = Path(videos_dir)
    if not videos_path.exists():
        print(f"Error: Directory {videos_dir} does not exist", file=sys.stderr)
        sys.exit(1)
        
    video_files = list(videos_path.glob("*.mp4"))
    if not video_files:
        print(f"Warning: No MP4 files found in {videos_dir}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(video_files)} video files, starting conversion...")
    
    for video_file in video_files:
        try:
            convert_video_to_gif(video_file)
        except Exception as e:
            print(f"Error converting {video_file.name}: {str(e)}", file=sys.stderr)
            continue
            
    print("All video conversions completed!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_convert_videos.py <videos_directory_path>", file=sys.stderr)
        sys.exit(1)
        
    videos_dir = sys.argv[1]
    batch_convert_videos(videos_dir) 