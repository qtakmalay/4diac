"""
Step 3: Multi-model screenshot assessment of 4diac IDE.
Sends the same frames to GPT-4o and Gemini for comparison.
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

OUTPUT_DIR = Path(__file__).parent / "outputs" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Frame sets — different densities for comparison
FRAME_SETS = {
    "6frames": {
        "dir": Path(__file__).parent / "frames" / "td",
        "frames": [
            "frame_0005.jpg", "frame_0010.jpg", "frame_0020.jpg",
            "frame_0035.jpg", "frame_0050.jpg", "frame_0060.jpg",
        ],
    },
    "20frames": {
        "dir": Path(__file__).parent / "frames" / "td_3s",
        "frames": [f"frame_{i:04d}.jpg" for i in range(2, 221, 11)],  # every 11th from 3s set = ~every 33s
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

    print("Sending to GPT-4o...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=4096,
    )
    return response.choices[0].message.content


def assess_gemini_screenshots(images: list[Path], prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    parts = []
    for img in images:
        img_bytes = img.read_bytes()
        parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))
    parts.append(types.Part.from_text(text=prompt))

    print("Sending to Gemini (screenshots)...")
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

    print("Sending to Claude...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text


def run(prompt_level: str = "blind", models: str = "all", frame_set: str = "6frames"):
    prompt = BLIND_PROMPT if prompt_level == "blind" else CD_GUIDED_PROMPT

    fset = FRAME_SETS[frame_set]
    images = [fset["dir"] / f for f in fset["frames"]]
    # Filter to only existing frames
    images = [img for img in images if img.exists()]
    for img in images:
        if not img.exists():
            print(f"ERROR: Frame not found: {img}")
            sys.exit(1)

    video_name = "task_demo.mkv"
    print(f"Using {len(images)} frames from {video_name}, prompt: {prompt_level}")
    results = {}

    # GPT-4o
    if models in ("all", "gpt4o"):
        try:
            resp = assess_gpt4o(images, prompt)
            results["gpt4o"] = {
                "model": "gpt-4o",
                "prompt_level": prompt_level,
                "response": resp,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            out = OUTPUT_DIR / f"gpt4o_{prompt_level}_{frame_set}.md"
            with open(out, "w") as f:
                f.write(f"# GPT-4o Assessment: {prompt_level} ({frame_set})\n")
                f.write(f"**Frames:** {len(images)} screenshots from {video_name}\n")
                f.write(f"**Model:** gpt-4o\n")
                f.write(f"**Timestamp:** {results['gpt4o']['timestamp']}\n\n---\n\n")
                f.write(resp)
            print(f"GPT-4o saved to: {out}")
            print(f"Preview: {resp[:300]}...")
        except Exception as e:
            print(f"GPT-4o ERROR: {e}")
            results["gpt4o"] = {"error": str(e)}

    if models in ("all", "gpt4o") and models in ("all", "gemini"):
        time.sleep(3)

    # Gemini (screenshots for comparison with video)
    if models in ("all", "gemini"):
        try:
            resp = assess_gemini_screenshots(images, prompt)
            results["gemini_ss"] = {
                "model": "gemini-2.5-flash (screenshots)",
                "prompt_level": prompt_level,
                "response": resp,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            out = OUTPUT_DIR / f"gemini_ss_{prompt_level}_{frame_set}.md"
            with open(out, "w") as f:
                f.write(f"# Gemini Screenshot Assessment: {prompt_level} ({frame_set})\n")
                f.write(f"**Frames:** {len(images)} screenshots from {video_name}\n")
                f.write(f"**Model:** gemini-2.5-flash\n")
                f.write(f"**Timestamp:** {results['gemini_ss']['timestamp']}\n\n---\n\n")
                f.write(resp)
            print(f"Gemini screenshots saved to: {out}")
            print(f"Preview: {resp[:300]}...")
        except Exception as e:
            print(f"Gemini screenshots ERROR: {e}")
            results["gemini_ss"] = {"error": str(e)}

    # Claude
    if models in ("all", "claude"):
        if models == "all":
            time.sleep(3)
        try:
            resp = assess_claude(images, prompt)
            results["claude"] = {
                "model": "claude-sonnet-4",
                "prompt_level": prompt_level,
                "response": resp,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            out = OUTPUT_DIR / f"claude_{prompt_level}_{frame_set}.md"
            with open(out, "w") as f:
                f.write(f"# Claude Assessment: {prompt_level} ({frame_set})\n")
                f.write(f"**Frames:** {len(images)} screenshots from {video_name}\n")
                f.write(f"**Model:** claude-sonnet-4\n")
                f.write(f"**Timestamp:** {results['claude']['timestamp']}\n\n---\n\n")
                f.write(resp)
            print(f"Claude saved to: {out}")
            print(f"Preview: {resp[:300]}...")
        except Exception as e:
            print(f"Claude ERROR: {e}")
            results["claude"] = {"error": str(e)}

    # Save combined
    combined = OUTPUT_DIR / f"all_{prompt_level}_{frame_set}.json"
    with open(combined, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nAll results: {combined}")
    return results


if __name__ == "__main__":
    level = sys.argv[1] if len(sys.argv) > 1 else "blind"
    mdls = sys.argv[2] if len(sys.argv) > 2 else "all"
    fset = sys.argv[3] if len(sys.argv) > 3 else "6frames"
    print(f"Screenshot assessment — prompt: {level}, models: {mdls}, frames: {fset}\n")
    run(level, mdls, fset)
