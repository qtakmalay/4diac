"""
New Version Video Assessment — Screenshot-based multi-model comparison.
Sends frames from the two new 4diac IDE videos (2026-03-19) to GPT-4o, Gemini, and Claude.

Usage:
    python assess_new_videos.py                    # Run all models on both videos
    python assess_new_videos.py new_a              # Run all models on video A only
    python assess_new_videos.py new_b gemini       # Run Gemini on video B only
"""

import os
import sys
import json
import time
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types
import anthropic

from prompts import BLIND_PROMPT, CD_GUIDED_PROMPT

load_dotenv()

FRAMES_DIR = Path(__file__).parent / "frames"
OUTPUT_DIR = Path(__file__).parent / "outputs" / "new_version"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# New version videos — select 6 evenly-spaced frames from each
VIDEO_FRAME_SETS = {
    "new_a": {
        "dir": FRAMES_DIR / "new_a",
        "total_frames": 70,
        "description": "Video A: 2026-03-19 21-25-12.mkv (~12 min, new 4diac version)",
        # Pick 6 evenly spaced: 1, 12, 24, 35, 47, 58
        "frames_6": [f"frame_{i:04d}.jpg" for i in [1, 12, 24, 35, 47, 58]],
        # Pick 15 evenly spaced for denser assessment
        "frames_15": [f"frame_{i:04d}.jpg" for i in range(1, 71, 5)],
    },
    "new_b": {
        "dir": FRAMES_DIR / "new_b",
        "total_frames": 32,
        "description": "Video B: 2026-03-19 21-39-08.mkv (~5 min, new 4diac version)",
        # Pick 6 evenly spaced: 1, 7, 13, 19, 25, 31
        "frames_6": [f"frame_{i:04d}.jpg" for i in [1, 7, 13, 19, 25, 31]],
        # All frames for denser assessment
        "frames_15": [f"frame_{i:04d}.jpg" for i in range(1, 33, 2)],
    },
}


def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def assess_gpt4o(images: list[Path], prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    content = []
    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encode_image(img)}", "detail": "high"}
        })
    content.append({"type": "text", "text": prompt})
    print("  Sending to GPT-4o...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=4096,
    )
    return response.choices[0].message.content


def assess_gemini(images: list[Path], prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    parts = []
    for img in images:
        parts.append(types.Part.from_bytes(data=img.read_bytes(), mime_type="image/jpeg"))
    parts.append(types.Part.from_text(text=prompt))
    print("  Sending to Gemini 2.5-flash...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=parts)],
    )
    return response.text


def assess_claude(images: list[Path], prompt: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    content = []
    for img in images:
        img_data = base64.b64encode(img.read_bytes()).decode("utf-8")
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": img_data}
        })
    content.append({"type": "text", "text": prompt})
    print("  Sending to Claude Sonnet 4...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text


MODEL_FNS = {
    "gpt4o": ("gpt-4o", assess_gpt4o),
    "gemini": ("gemini-2.5-flash", assess_gemini),
    "claude": ("claude-sonnet-4", assess_claude),
}


def run(video_key: str, model_key: str = "all", prompt_level: str = "blind", density: str = "6"):
    vset = VIDEO_FRAME_SETS[video_key]
    frame_list_key = f"frames_{density}" if f"frames_{density}" in vset else "frames_6"
    frame_names = vset[frame_list_key]
    images = [vset["dir"] / f for f in frame_names if (vset["dir"] / f).exists()]

    prompt = BLIND_PROMPT if prompt_level == "blind" else CD_GUIDED_PROMPT

    print(f"{'='*60}")
    print(f"Video: {vset['description']}")
    print(f"Frames: {len(images)} ({frame_list_key})")
    print(f"Prompt: {prompt_level}")
    print(f"{'='*60}\n")

    models_to_run = MODEL_FNS if model_key == "all" else {model_key: MODEL_FNS[model_key]}
    results = {}

    for mk, (model_name, fn) in models_to_run.items():
        print(f"\n--- {model_name} ---")
        try:
            resp = fn(images, prompt)
            results[mk] = {
                "model": model_name,
                "video": video_key,
                "prompt_level": prompt_level,
                "num_frames": len(images),
                "response": resp,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            out = OUTPUT_DIR / f"{video_key}_{mk}_{prompt_level}.md"
            with open(out, "w", encoding="utf-8") as f:
                f.write(f"# {model_name} Assessment: {prompt_level}\n")
                f.write(f"**Video:** {vset['description']}\n")
                f.write(f"**Frames:** {len(images)} screenshots\n")
                f.write(f"**Model:** {model_name}\n")
                f.write(f"**Timestamp:** {results[mk]['timestamp']}\n\n---\n\n")
                f.write(resp)
            print(f"  Saved: {out.name}")
            print(f"  Preview: {resp[:200]}...")
        except Exception as e:
            print(f"  ERROR: {e}")
            results[mk] = {"error": str(e)}

        if len(models_to_run) > 1:
            time.sleep(3)

    combined = OUTPUT_DIR / f"{video_key}_all_{prompt_level}.json"
    with open(combined, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nCombined results: {combined.name}")
    return results


if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "all"
    model = sys.argv[2] if len(sys.argv) > 2 else "all"
    level = sys.argv[3] if len(sys.argv) > 3 else "blind"

    videos = ["new_a", "new_b"] if video == "all" else [video]

    for v in videos:
        run(v, model, level)
        if len(videos) > 1:
            print("\n" + "=" * 60 + "\n")
