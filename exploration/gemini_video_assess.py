"""
Step 1: Gemini Video-Based Usability Assessment of 4diac IDE
Sends video directly to Gemini and evaluates with 3 prompt levels.
Uses the new google-genai SDK.
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import BLIND_PROMPT, CD_GUIDED_PROMPT, TASK_SPECIFIC_PROMPTS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("ERROR: GOOGLE_API_KEY not found in .env")
    sys.exit(1)

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL = "gemini-2.5-flash"

VIDEOS_DIR = Path(__file__).parent.parent / "videos"
OUTPUT_DIR = Path(__file__).parent / "outputs" / "gemini_video"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_FILES = {
    "td": VIDEOS_DIR / "task_demo.mkv",
    "v1": VIDEOS_DIR / "intro_v1.mkv",
    "v2": VIDEOS_DIR / "intro_v2.webm",
    "new_a": VIDEOS_DIR / "2026-03-19 21-25-12.mkv",  # New version video A (~12 min)
    "new_b": VIDEOS_DIR / "2026-03-19 21-39-08.mkv",  # New version video B (~5 min)
}


def upload_video(video_path: Path):
    """Upload video to Gemini API and wait for processing."""
    print(f"Uploading {video_path.name}...")
    video_file = client.files.upload(file=str(video_path))
    print(f"Upload complete. Waiting for processing...")

    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)
        print(f"  State: {video_file.state.name}")

    if video_file.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {video_file.state.name}")

    print(f"Video ready: {video_file.uri}")
    return video_file


def assess_video(video_file, prompt: str) -> str:
    """Send video + prompt to Gemini and get assessment."""
    print(f"Sending to {MODEL}...")
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(file_uri=video_file.uri, mime_type=video_file.mime_type),
                    types.Part.from_text(text=prompt),
                ],
            )
        ],
    )
    return response.text


def run_assessment(video_key: str = "task_demo", prompt_level: str = "all"):
    """Run usability assessment on a video with specified prompt level(s)."""
    video_path = VIDEO_FILES[video_key]
    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}")
        sys.exit(1)

    video_file = upload_video(video_path)

    prompts_to_run = {}
    if prompt_level in ("all", "blind"):
        prompts_to_run["blind"] = BLIND_PROMPT
    if prompt_level in ("all", "cd_guided"):
        prompts_to_run["cd_guided"] = CD_GUIDED_PROMPT
    if prompt_level in ("all", "task_specific"):
        for task_name, task_prompt in TASK_SPECIFIC_PROMPTS.items():
            prompts_to_run[f"task_{task_name}"] = task_prompt

    results = {}
    for name, prompt in prompts_to_run.items():
        print(f"\n{'='*60}")
        print(f"Running assessment: {name}")
        print(f"{'='*60}")

        try:
            response = assess_video(video_file, prompt)
            results[name] = {
                "prompt_level": name,
                "model": MODEL,
                "video": video_key,
                "response": response,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            output_file = OUTPUT_DIR / f"{video_key}_{name}.md"
            with open(output_file, "w") as f:
                f.write(f"# Gemini Assessment: {name}\n")
                f.write(f"**Video:** {video_path.name}\n")
                f.write(f"**Model:** {MODEL}\n")
                f.write(f"**Timestamp:** {results[name]['timestamp']}\n\n")
                f.write(f"---\n\n")
                f.write(response)

            print(f"\nSaved to: {output_file}")
            print(f"\nResponse preview:\n{response[:500]}...")

        except Exception as e:
            print(f"ERROR on {name}: {e}")
            results[name] = {"error": str(e)}

        if len(prompts_to_run) > 1:
            print("\nWaiting 5s (rate limit)...")
            time.sleep(5)

    combined_file = OUTPUT_DIR / f"{video_key}_all_results.json"
    with open(combined_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nAll results saved to: {combined_file}")

    try:
        client.files.delete(name=video_file.name)
        print("Uploaded video cleaned up.")
    except Exception:
        pass

    return results


if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "task_demo"
    level = sys.argv[2] if len(sys.argv) > 2 else "all"

    print(f"Starting Gemini video assessment")
    print(f"Video: {video}")
    print(f"Prompt level: {level}")
    print(f"Model: {MODEL}")
    print()

    results = run_assessment(video, level)

    print(f"\n{'='*60}")
    print(f"DONE — {len([r for r in results.values() if 'error' not in r])} successful assessments")
    print(f"{'='*60}")
