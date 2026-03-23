"""Claude Computer Use agent for 4diac IDE usability assessment.

Connects to 4diac IDE running in Docker via VNC, performs tasks,
and reports usability issues found during interaction.
"""

import sys
import io

# Fix Windows cp1252 encoding issues — force UTF-8 for stdout/stderr
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import anthropic
import base64
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from tasks import TASKS, SYSTEM_PROMPT

# Load API key
load_dotenv(Path(__file__).parent.parent / "exploration" / ".env")

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
CONTAINER_NAME = "agent_interaction-4diac-ide-1"
OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def take_screenshot() -> str:
    """Take screenshot from Docker container, return base64-encoded PNG."""
    # Take screenshot inside container
    subprocess.run(
        ["docker", "exec", CONTAINER_NAME, "bash", "-c",
         "DISPLAY=:1 scrot -o /tmp/screen.png"],
        check=True, capture_output=True
    )
    # Copy to host
    tmp_path = "/tmp/4diac_screen.png"
    subprocess.run(
        ["docker", "cp", f"{CONTAINER_NAME}:/tmp/screen.png", tmp_path],
        check=True, capture_output=True
    )
    with open(tmp_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def _focus_window():
    """Focus the 4diac IDE window before any action."""
    subprocess.run(
        ["docker", "exec", CONTAINER_NAME, "bash", "-c",
         "DISPLAY=:1 WID=$(xdotool search --name '4diac' | tail -1) && "
         "DISPLAY=:1 xdotool windowfocus --sync $WID && "
         "DISPLAY=:1 xdotool windowactivate --sync $WID"],
        capture_output=True, timeout=5
    )


def execute_action(action: dict) -> str:
    """Execute a computer use action in the Docker container."""
    action_type = action.get("action")
    coord = action.get("coordinate")
    text = action.get("text")

    if action_type == "screenshot":
        return "screenshot_requested"

    # Always focus window first
    _focus_window()

    cmd_parts = []
    post_delay = 1.0  # QEMU is slow, need longer delays

    if action_type == "mouse_move" and coord:
        cmd_parts = [f"DISPLAY=:1 xdotool mousemove {coord[0]} {coord[1]}"]

    elif action_type == "left_click" and coord:
        cmd_parts = [
            f"DISPLAY=:1 xdotool mousemove {coord[0]} {coord[1]}",
            "sleep 0.3",
            "DISPLAY=:1 xdotool click 1"
        ]

    elif action_type == "right_click" and coord:
        cmd_parts = [
            f"DISPLAY=:1 xdotool mousemove {coord[0]} {coord[1]}",
            "sleep 0.3",
            "DISPLAY=:1 xdotool click 3"
        ]

    elif action_type == "double_click" and coord:
        cmd_parts = [
            f"DISPLAY=:1 xdotool mousemove {coord[0]} {coord[1]}",
            "sleep 0.3",
            "DISPLAY=:1 xdotool click --repeat 2 --delay 200 1"
        ]

    elif action_type == "triple_click" and coord:
        cmd_parts = [
            f"DISPLAY=:1 xdotool mousemove {coord[0]} {coord[1]}",
            "sleep 0.3",
            "DISPLAY=:1 xdotool click --repeat 3 --delay 200 1"
        ]

    elif action_type == "left_click_drag" and coord:
        start = action.get("start_coordinate", [0, 0])
        cmd_parts = [
            f"DISPLAY=:1 xdotool mousemove {start[0]} {start[1]}",
            "sleep 0.3",
            "DISPLAY=:1 xdotool mousedown 1",
            "sleep 0.2",
            f"DISPLAY=:1 xdotool mousemove --delay 100 {coord[0]} {coord[1]}",
            "sleep 0.2",
            "DISPLAY=:1 xdotool mouseup 1"
        ]

    elif action_type == "type" and text:
        escaped = text.replace("'", "'\\''")
        cmd_parts = [f"DISPLAY=:1 xdotool type --clearmodifiers --delay 80 '{escaped}'"]

    elif action_type == "key" and text:
        key = text.replace("Return", "Return").replace("Tab", "Tab")
        cmd_parts = [f"DISPLAY=:1 xdotool key --clearmodifiers {key}"]

    elif action_type == "scroll" and coord:
        direction = action.get("delta_y", 0)
        button = 5 if direction > 0 else 4
        clicks = abs(direction) // 50 or 1
        cmd_parts = [
            f"DISPLAY=:1 xdotool mousemove {coord[0]} {coord[1]}",
            "sleep 0.3",
            f"DISPLAY=:1 xdotool click --repeat {clicks} {button}"
        ]

    elif action_type == "wait":
        time.sleep(action.get("duration", 2))
        return "waited"

    elif action_type == "cursor_position":
        result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "bash", "-c",
             "DISPLAY=:1 xdotool getmouselocation"],
            capture_output=True, text=True
        )
        return result.stdout.strip()

    if cmd_parts:
        full_cmd = " && ".join(cmd_parts)
        subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "bash", "-c", full_cmd],
            capture_output=True, timeout=15
        )
        time.sleep(post_delay)  # QEMU needs longer delays
        return f"executed: {action_type}"

    return f"unknown action: {action_type}"


def run_task(task_key: str) -> dict:
    """Run a single usability assessment task."""
    task = TASKS[task_key]
    print(f"\n{'='*60}")
    print(f"Starting: {task['name']}")
    print(f"{'='*60}\n")

    client = anthropic.Anthropic()

    tools = [
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": DISPLAY_WIDTH,
            "display_height_px": DISPLAY_HEIGHT,
            "display_number": 1,
        }
    ]

    # Take initial screenshot
    print("Taking initial screenshot...")
    initial_ss = take_screenshot()

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": task["description"]},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": initial_ss,
                    },
                },
            ],
        }
    ]

    # Tracking
    steps = []
    step_num = 0
    max_steps = task["max_steps"]
    final_text = ""

    while step_num < max_steps:
        step_num += 1
        print(f"\n--- Step {step_num}/{max_steps} ---")

        try:
            response = client.beta.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=tools,
                messages=messages,
                betas=["computer-use-2025-11-24"],
            )
        except Exception as e:
            print(f"API error: {e}")
            break

        # Collect text responses
        for block in response.content:
            if hasattr(block, "text"):
                print(f"Claude: {block.text[:200]}")
                final_text += block.text + "\n"

        # Check if done
        if response.stop_reason == "end_turn":
            print("Task completed (end_turn)")
            break

        # Process tool uses
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    action = block.input
                    action_type = action.get("action", "unknown")
                    print(f"  Action: {action_type} {action.get('coordinate', '')}")

                    step_record = {
                        "step": step_num,
                        "action": action_type,
                        "coordinate": action.get("coordinate"),
                        "text": action.get("text"),
                        "timestamp": datetime.now().isoformat(),
                    }
                    steps.append(step_record)

                    if action_type == "screenshot":
                        ss_data = take_screenshot()
                        # Save screenshot
                        ss_path = OUTPUT_DIR / f"{task_key}_step{step_num:02d}.png"
                        with open(ss_path, "wb") as f:
                            f.write(base64.b64decode(ss_data))

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": ss_data,
                                    },
                                }
                            ],
                        })
                    else:
                        result = execute_action(action)
                        # Take screenshot after action for logging
                        ss_data = take_screenshot()
                        ss_path = OUTPUT_DIR / f"{task_key}_step{step_num:02d}.png"
                        with open(ss_path, "wb") as f:
                            f.write(base64.b64decode(ss_data))

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

            messages.append({"role": "user", "content": tool_results})
        else:
            print(f"Unexpected stop_reason: {response.stop_reason}")
            break

    # Save results
    result = {
        "task": task["name"],
        "task_key": task_key,
        "total_steps": step_num,
        "max_steps": max_steps,
        "steps": steps,
        "final_report": final_text,
        "timestamp": datetime.now().isoformat(),
    }

    # Save JSON
    json_path = OUTPUT_DIR / f"{task_key}_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Save markdown report
    md_path = OUTPUT_DIR / f"{task_key}_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {task['name']} — Claude Computer Use Assessment\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Model:** claude-sonnet-4-6\n")
        f.write(f"**Steps taken:** {step_num}/{max_steps}\n\n")
        f.write("## Agent's Report\n\n")
        f.write(final_text)
        f.write("\n\n## Action Log\n\n")
        f.write("| Step | Action | Coordinate | Text |\n")
        f.write("|------|--------|------------|------|\n")
        for s in steps:
            text_val = s.get('text') or ''
            f.write(f"| {s['step']} | {s['action']} | {s.get('coordinate', '')} | {text_val[:50]} |\n")

    print(f"\nResults saved to {json_path} and {md_path}")
    return result


def main():
    """Run all tasks or a specific one."""
    import sys

    # Install xdotool in container if not present
    print("Ensuring xdotool is installed in container...")
    subprocess.run(
        ["docker", "exec", CONTAINER_NAME, "bash", "-c",
         "which xdotool || (apt-get update -qq && apt-get install -y -qq xdotool)"],
        capture_output=True
    )

    if len(sys.argv) > 1:
        task_key = sys.argv[1]
        if task_key in TASKS:
            run_task(task_key)
        else:
            print(f"Unknown task: {task_key}")
            print(f"Available: {', '.join(TASKS.keys())}")
    else:
        # Run all tasks
        for task_key in TASKS:
            run_task(task_key)
            print("\nWaiting 5s before next task...")
            time.sleep(5)


if __name__ == "__main__":
    main()
