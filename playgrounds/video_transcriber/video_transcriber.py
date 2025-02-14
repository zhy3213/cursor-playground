#!/usr/bin/env python3
import argparse
import json
import time
import sys
import requests
from typing import Optional, Dict, Any

class VideoTranscriber:
    def __init__(self, base_url: str = "https://yage.ai/caption"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def submit_job(self, video_url: str) -> str:
        """Submit video transcription job"""
        response = self.session.post(
            f"{self.base_url}/submit_job/",
            json={"url": video_url}
        )
        response.raise_for_status()
        return response.json()["job_id"]

    def check_status(self, job_id: str) -> str:
        """Check job status"""
        response = self.session.get(f"{self.base_url}/check_status/{job_id}")
        response.raise_for_status()
        return response.json()["status"]

    def get_results(self, job_id: str) -> Dict[str, str]:
        """Get transcription results"""
        response = self.session.get(f"{self.base_url}/get_results/{job_id}")
        response.raise_for_status()
        return response.json()

    def process_video(self, video_url: str, check_interval: float = 2.0) -> Dict[str, Any]:
        """Process video and wait for results"""
        print(f"Submitting video URL: {video_url}", file=sys.stderr)
        job_id = self.submit_job(video_url)
        print(f"Job ID: {job_id}", file=sys.stderr)

        while True:
            status = self.check_status(job_id)
            print(f"Current status: {status}", file=sys.stderr)
            
            if status == "Completed":
                results = self.get_results(job_id)
                return results
            elif status == "Failed":
                raise Exception("Transcription job failed")
            
            time.sleep(check_interval)

def main():
    parser = argparse.ArgumentParser(description="Video Transcription Tool")
    parser.add_argument("url", help="Video URL (currently supports Bilibili links)")
    parser.add_argument("--output", "-o", help="Output file path (defaults to stdout)")
    parser.add_argument("--raw-only", action="store_true", help="Output raw transcription only")
    args = parser.parse_args()

    try:
        transcriber = VideoTranscriber()
        results = transcriber.process_video(args.url)
        
        output = {
            "raw_transcript": results["transcript"],
        }
        if not args.raw_only:
            output["paraphrased_transcript"] = results["paraphrased_transcript"]

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 