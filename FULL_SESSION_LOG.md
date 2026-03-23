# Complete Session Log — AI-Based Usability Assessment for 4diac IDE

**Date:** March 11, 2026
**Duration:** ~3 hours
**Author:** Mirza Mir (with Claude Opus 4.6 as assistant)
**Purpose:** Initial exploration — can AI assess IDE usability from video, screenshots, and direct interaction?

---

## Table of Contents

1. [Prerequisites & Environment Setup](#1-prerequisites--environment-setup)
2. [Phase 1A: Video Download & API Configuration](#2-phase-1a-video-download--api-configuration)
3. [Phase 1B: Gemini Video Assessments](#3-phase-1b-gemini-video-assessments)
4. [Phase 1C: Frame Extraction](#4-phase-1c-frame-extraction)
5. [Phase 1D: Screenshot Assessments (GPT-4o, Gemini, Claude)](#5-phase-1d-screenshot-assessments)
6. [Phase 1E: Results & Comparison](#6-phase-1e-results--comparison)
7. [Phase 2A: Agent Research](#7-phase-2a-agent-research)
8. [Phase 2B: Docker Environment Setup](#8-phase-2b-docker-environment-setup)
9. [Phase 2C: Claude Computer Use Script](#9-phase-2c-claude-computer-use-script)
10. [Phase 2D: Agent Experiment — Task 1](#10-phase-2d-agent-experiment--task-1)
11. [Challenges & Solutions](#11-challenges--solutions)
12. [All Code — Full Source](#12-all-code--full-source)
13. [How to Replicate](#13-how-to-replicate)

---

## 1. Prerequisites & Environment Setup

### Hardware
- macOS (Darwin 25.3.0), Apple Silicon (ARM)
- Docker Desktop installed

### Software Installation

```bash
# 1. Create isolated Python environment
conda create -n 4diac python=3.11 -y
conda activate 4diac

# 2. Install Python dependencies
pip install google-genai python-dotenv openai anthropic Pillow

# 3. Install system tools
brew install yt-dlp ffmpeg

# 4. Verify
python -c "from google import genai; print('google-genai OK')"
python -c "import openai; print('openai OK')"
python -c "import anthropic; print('anthropic OK')"
which yt-dlp && echo "yt-dlp OK"
which ffmpeg && echo "ffmpeg OK"
```

### API Keys
Keys were sourced from OpenClaw (`~/.openclaw/`) and saved to `exploration/.env`:

```env
GOOGLE_API_KEY=<your-google-api-key>
OPENAI_API_KEY=<your-openai-api-key>
ANTHROPIC_API_KEY=<your-anthropic-api-key>
```

**Challenge:** Initially tried `google-generativeai` SDK — it's deprecated. The correct SDK is `google-genai` (new).

**Challenge:** Initially used `gemini-2.0-flash` model — it's retired for new API users. Correct model: `gemini-2.5-flash`.

---

## 2. Phase 1A: Video Download & API Configuration

### Videos from the Paper
The paper (Wiesmayr et al. 2023) references 3 YouTube videos:

| Short Name | YouTube URL | Description | Size |
|-----------|-------------|-------------|------|
| `task_demo.mkv` | https://youtu.be/xishphcgYmc | Bianca's task demo (4 tasks) | 31MB |
| `intro_v1.mkv` | https://youtu.be/K9iItQBC-ac | Intro to IEC 61499 & 4diac (v1.14.0) | 17MB |
| `intro_v2.webm` | https://youtu.be/by02Xu2yrPE | Preview of new features (v2.1.0) | 32MB |

### Download Commands
```bash
mkdir -p videos/
yt-dlp -o "videos/task_demo.%(ext)s" "https://youtu.be/xishphcgYmc"
yt-dlp -o "videos/intro_v1.%(ext)s" "https://youtu.be/K9iItQBC-ac"
yt-dlp -o "videos/intro_v2.%(ext)s" "https://youtu.be/by02Xu2yrPE"
```

**Note:** yt-dlp chooses the best format automatically. Task demo downloads as `.mkv`, intro v2 as `.webm`. Both formats work with Gemini's API.

---

## 3. Phase 1B: Gemini Video Assessments

### Script: `exploration/gemini_video_assess.py`

**How it works:**
1. Uploads video file to Gemini via `client.files.upload()`
2. Waits for PROCESSING → ACTIVE (takes ~20-30 seconds)
3. Sends video + prompt to `gemini-2.5-flash`
4. Saves response as markdown + JSON
5. Cleans up uploaded file

### Three Prompt Levels
Defined in `exploration/prompts.py`:

1. **Blind** — "Assess the usability of this IDE" (no framework)
2. **CD-Guided** — "Evaluate using 14 Cognitive Dimensions" (full framework provided)
3. **Task-Specific** — 4 prompts matching the paper's 4 maintenance tasks

### Commands Run
```bash
conda activate 4diac
cd /Users/mirzamir/Desktop/4diac/exploration

# Experiment 1: Blind assessment on task demo
python gemini_video_assess.py td blind

# Experiment 2: CD-guided on task demo
python gemini_video_assess.py td cd_guided

# Experiment 3: All 4 task-specific prompts on task demo
python gemini_video_assess.py td task_specific

# Experiment 4: Blind on intro v1
python gemini_video_assess.py v1 blind

# Experiment 5: Blind on intro v2
python gemini_video_assess.py v2 blind
```

### Output Files
```
exploration/outputs/gemini_video/
├── td_blind.md                    (10KB) — Blind assessment
├── td_cd_guided.md                (13KB) — CD-guided assessment
├── td_task_task1_orientation.md   (9.3KB) — Task 1
├── td_task_task2_hierarchy.md     (8.0KB) — Task 2
├── td_task_task3_library.md       (7.5KB) — Task 3
├── td_task_task4_editing.md       (7.9KB) — Task 4
├── td_all_results.json            (33KB) — Combined JSON
├── v1_blind.md                    (9.0KB) — Intro v1 blind
├── v1_all_results.json            (9.1KB)
├── v2_blind.md                    (7.4KB) — Intro v2 blind
└── v2_all_results.json            (7.5KB)
```

### Key Results
- **Gemini correctly identified** the IDE, its purpose, all major UI components
- **Referenced specific timestamps** (e.g., "at 0:38", "around 2:19")
- **Detected 8/10 known usability issues** from the paper's ground truth
- **CD-guided produced the most structured output** — easy to compare
- **Task 1 correctly identified** search feature as #1 missing feature (matching 6/10 human subjects)

### Challenges
- **Rate limiting**: Added 5-second pause between API calls
- **Video processing time**: ~20-30 seconds per upload
- **Model naming**: `gemini-2.0-flash` was retired — had to discover `gemini-2.5-flash`

---

## 4. Phase 1C: Frame Extraction

Used `ffmpeg` to extract frames at different densities for screenshot-based assessment.

### Commands
```bash
# 6 key frames (every 10 seconds) — 66 total frames
mkdir -p exploration/frames/td
ffmpeg -i videos/task_demo.mkv -vf "fps=1/10" -q:v 2 exploration/frames/td/frame_%04d.jpg

# 20 frames (every 3 seconds) — 221 total frames
mkdir -p exploration/frames/td_3s
ffmpeg -i videos/task_demo.mkv -vf "fps=1/3" -q:v 2 exploration/frames/td_3s/frame_%04d.jpg
```

### Frame Selection for Assessment
- **6 frames**: Manually selected frames 5, 10, 20, 35, 50, 60 (skipping frame 1 which is JKU logo)
- **20 frames**: Every 11th frame from the 3-second set (`range(2, 221, 11)`) = ~every 33 seconds

**Note:** Frame 1 from 10-second extraction is just the JKU logo — not useful for assessment.

---

## 5. Phase 1D: Screenshot Assessments

### Script: `exploration/assess_screenshots.py`

**Supports 3 models:** GPT-4o, Gemini (screenshots), Claude Sonnet 4
**Two prompt levels:** Blind, CD-Guided
**Two frame sets:** 6 frames, 20 frames

### Commands Run
```bash
cd /Users/mirzamir/Desktop/4diac/exploration

# 6 frames — blind
python assess_screenshots.py blind all 6frames

# 6 frames — CD-guided
python assess_screenshots.py cd_guided all 6frames

# 20 frames — blind (GPT-4o + Gemini)
python assess_screenshots.py blind all 20frames

# 20 frames — Claude only (blind + CD-guided)
python assess_screenshots.py blind claude 20frames
python assess_screenshots.py cd_guided claude 20frames
```

### Output Files
```
exploration/outputs/screenshots/
├── gpt4o_blind.md                 — GPT-4o, 6 frames, blind
├── gpt4o_cd_guided.md             — GPT-4o, 6 frames, CD-guided
├── gpt4o_blind_20frames.md        — GPT-4o, 20 frames, blind
├── gemini_ss_blind.md             — Gemini, 6 frames, blind
├── gemini_ss_cd_guided.md         — Gemini, 6 frames, CD-guided
├── gemini_ss_blind_20frames.md    — Gemini, 20 frames, blind
├── claude_blind_20frames.md       — Claude, 20 frames, blind
├── claude_cd_guided_20frames.md   — Claude, 20 frames, CD-guided
└── all_*.json                     — Combined JSON results
```

### Challenges
- **OpenAI SDK**: Had to install separately (`pip install openai`)
- **Anthropic SDK**: Had to install separately (`pip install anthropic`)
- **Anthropic billing**: Initial key had billing issues — resolved with different key from OpenClaw
- **Image encoding**: GPT-4o uses `image_url` with base64 data URL; Claude uses `image` with separate `source` object; Gemini uses `Part.from_bytes()`

---

## 6. Phase 1E: Results & Comparison

### Ground Truth Detection Matrix

| # | Issue from Paper | Gemini Video | Gemini 20ss | Claude 20ss | GPT-4o 20ss |
|---|-----------------|:---:|:---:|:---:|:---:|
| 1 | No search feature (6/10) | **YES** | partial | partial | partial |
| 2 | Can't identify location (6/10) | **YES** | partial | no | no |
| 3 | No link to type instances (5/10) | **YES** | no | no | no |
| 4 | Difficulty adding files (9/10) | **YES** | no | no | no |
| 5 | Connection routing (6/10) | **YES** | yes | yes | yes |
| 6 | Confusing context menus (multiple) | **YES** | yes | no | no |
| 7 | Icons small/unclear (4/10) | **YES** | partial | yes | partial |
| 8 | Insufficient validation (4/10) | **YES** | no | partial | no |
| 9 | Cut/paste broken (5/10) | no | no | no | no |
| 10 | No path from root (4/10) | partial | no | no | no |
| | **Total** | **~8/10** | **~4/10** | **~3/10** | **~2/10** |

### Key Finding
**Video input dramatically outperforms screenshots regardless of model.** Gemini + video detected ~80% of known issues from a single video with zero human participants.

### Video Input Capability Research
| Model | Native Video | Screenshots | Notes |
|-------|:---------:|:---------:|-------|
| Gemini 2.5 | **Yes** | Yes | Only practical video option today |
| GPT-5 | Yes (new) | Yes | Accepts MP4/MOV, decomposes to keyframes |
| GPT-4o | No | Yes | Must extract frames manually |
| Claude (all) | No | Yes | Video API announced for mid-2026 |

---

## 7. Phase 2A: Agent Research

Researched 12+ AI agents that can interact with desktop UIs. Key findings saved to `agent_interaction/RESEARCH_UI_AGENTS.md`.

### Top Candidates

| Agent | OSWorld Score | Docker? | Desktop Apps? |
|-------|:---:|:---:|:---:|
| Claude Computer Use | ~22% (improving) | Yes | Yes |
| Simular Agent S | **72.6%** (exceeds human 72.36%) | Yes | Yes |
| Bytebot | N/A | Docker-native | Yes |
| ScreenEnv (HuggingFace) | N/A | Docker-native | Yes (Linux) |
| UFO2 (Microsoft) | N/A | Yes | Windows only |

**Decision:** Use Claude Computer Use first — we already have the API key, it's best documented, and production-ready.

---

## 8. Phase 2B: Docker Environment Setup

### Goal
Run 4diac IDE in a Docker container with remote display access so an AI agent can take screenshots and send mouse/keyboard commands.

### Architecture
```
┌─────────────────────────────────────────┐
│ Docker Container (linux/amd64)          │
│                                         │
│  Xvfb (:1)  →  4diac IDE (Java/SWT)    │
│     ↓                                   │
│  x11vnc     →  VNC on port 5900        │
│     ↓                                   │
│  websockify →  noVNC on port 6080      │
│                                         │
│  xdotool    →  mouse/keyboard control  │
│  scrot      →  screenshot capture      │
└─────────────────────────────────────────┘
         ↑
    Host Machine
    (claude_computer_use.py)
    - Takes screenshots via: docker exec ... scrot
    - Sends actions via: docker exec ... xdotool
    - Calls Claude API with screenshots
```

### Files Created

**`agent_interaction/Dockerfile`:**
```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV VNC_PORT=5900
ENV NOVNC_PORT=6080
ENV RESOLUTION=1920x1080x24

RUN apt-get update && apt-get install -y \
    openjdk-17-jre wget xvfb x11vnc fluxbox \
    novnc websockify dbus-x11 libgtk-3-0 \
    libswt-gtk-4-jni libwebkit2gtk-4.0-37 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q "https://www.eclipse.org/downloads/download.php?file=/4diac/releases/3.0/4diac-ide/4diac-ide_3.0.2-linux.gtk.x86_64.tar.gz&r=1" \
    -O /tmp/4diac-ide.tar.gz \
    && mkdir -p /opt/4diac \
    && tar -xzf /tmp/4diac-ide.tar.gz -C /opt/4diac --strip-components=1 \
    && rm /tmp/4diac-ide.tar.gz \
    && chmod +x /opt/4diac/4diac-ide

RUN mkdir -p /root/workspace

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5900 6080
CMD ["/start.sh"]
```

**`agent_interaction/start.sh`:**
```bash
#!/bin/bash
Xvfb $DISPLAY -screen 0 $RESOLUTION &
sleep 2
fluxbox &
sleep 1
x11vnc -display $DISPLAY -forever -nopw -shared -rfbport $VNC_PORT &
sleep 1
websockify --web /usr/share/novnc/ $NOVNC_PORT localhost:$VNC_PORT &
sleep 1
/opt/4diac/4diac-ide -data /root/workspace &
echo "=== 4diac IDE is running ==="
echo "VNC:    localhost:$VNC_PORT"
echo "noVNC:  http://localhost:$NOVNC_PORT/vnc.html"
wait
```

**`agent_interaction/docker-compose.yml`:**
```yaml
services:
  4diac-ide:
    build: .
    platform: linux/amd64
    ports:
      - "5900:5900"
      - "6080:6080"
    environment:
      - DISPLAY=:1
      - RESOLUTION=1920x1080x24
    volumes:
      - ./workspace:/root/workspace
    shm_size: '2gb'
```

### Build & Run Commands
```bash
cd agent_interaction/
docker compose up --build -d

# Verify IDE is running
docker logs agent_interaction-4diac-ide-1

# Check process
docker exec agent_interaction-4diac-ide-1 ps aux | grep 4diac

# Take test screenshot
docker exec agent_interaction-4diac-ide-1 bash -c "apt-get update -qq && apt-get install -y -qq scrot && DISPLAY=:1 scrot /tmp/screen.png"
docker cp agent_interaction-4diac-ide-1:/tmp/screen.png ./screen_check.png
```

### Challenges & Solutions

**Challenge 1: Rosetta error on ARM Mac**
- **Problem:** First build without `platform: linux/amd64` failed — 4diac binary is x86_64 only
- **Error:** `rosetta error: failed to open elf at /lib64/ld-linux-x86-64.so.2`
- **Solution:** Added `platform: linux/amd64` to docker-compose.yml — forces QEMU emulation

**Challenge 2: IDE window not responding to clicks**
- **Problem:** `xdotool click` on the IDE had no effect
- **Diagnosis:** Window didn't have focus under QEMU
- **Solution:** Must call `xdotool windowfocus --sync $WID && xdotool windowactivate --sync $WID` before any action

**Challenge 3: SWT hyperlinks not clickable**
- **Problem:** Hyperlinks in the System Explorer ("Create a new 4diac IDE Project", "Import projects...") didn't respond to xdotool clicks
- **Diagnosis:** SWT hyperlink widgets handle click events differently; QEMU emulation loses the event
- **Status:** Unresolved — needs native x86_64 machine

**Challenge 4: SWT dialogs not appearing**
- **Problem:** File > Import and File > New trigger but no dialog window appears
- **Diagnosis:** Confirmed with `wmctrl -l` that only 1 window exists — dialogs aren't being created
- **Root cause:** QEMU emulation of x86_64 Java/SWT is too slow for dialog rendering
- **Status:** Unresolved — needs native x86_64 machine

**Challenge 5: Keyboard shortcuts not working**
- **Problem:** `xdotool key ctrl+n` has no effect
- **Diagnosis:** Key events not being delivered properly under QEMU
- **Workaround:** Use `--clearmodifiers` flag, but still unreliable
- **Status:** Partially resolved

---

## 9. Phase 2C: Claude Computer Use Script

### Script: `agent_interaction/claude_computer_use.py`

**Architecture:**
1. **`take_screenshot()`** — Runs `scrot` in Docker, copies PNG to host, returns base64
2. **`_focus_window()`** — Focuses 4diac window (required for QEMU)
3. **`execute_action()`** — Translates Claude's actions to xdotool commands
4. **`run_task()`** — Main agent loop

**API Configuration:**
- Model: `claude-sonnet-4-6`
- Tool: `computer_20251124` (type name includes date)
- Beta: `computer-use-2025-11-24`
- Call: `client.beta.messages.create()` (NOT `client.messages.create()`)

### Challenges & Solutions

**Challenge: `betas` parameter not accepted**
- **Error:** `Messages.create() got an unexpected keyword argument 'betas'`
- **Root cause:** Anthropic SDK v0.84.0 moved computer use to `client.beta.messages.create()`
- **Solution:** Changed from `client.messages.create(..., betas=[...])` to `client.beta.messages.create(..., betas=[...])`

**Challenge: NoneType error in report generation**
- **Error:** `'NoneType' object is not subscriptable` on `s.get('text', '')[:50]`
- **Root cause:** Some steps have `text: null` (not empty string)
- **Solution:** Changed to `text_val = s.get('text') or ''`

### Task Definitions: `agent_interaction/tasks.py`
4 tasks matching the paper's methodology:
1. **Orientation** — Explore project structure, find function blocks
2. **Hierarchy** — Navigate nesting levels, understand location
3. **Library** — Find and add blocks from library
4. **Editing** — Edit blocks, change types, handle broken connections

---

## 10. Phase 2D: Agent Experiment — Task 1

### Configuration
- **Model:** Claude Sonnet 4.6
- **Max steps:** 30
- **Starting state:** 4diac IDE with empty workspace (no projects)
- **Task:** Orientation — explore project, find function blocks

### Run Command
```bash
conda activate 4diac
cd /Users/mirzamir/Desktop/4diac
python agent_interaction/claude_computer_use.py task1_orientation
```

### Step-by-Step Log

| Step | Action | Coordinate | Agent Reasoning |
|------|--------|-----------|-----------------|
| 1 | screenshot | — | "Take screenshot to assess current state" |
| 2 | left_click | [74, 229] | "Click Import projects..." |
| 3 | screenshot | — | Check result |
| 4 | left_click | [74, 229] | "Link not responding, try again" |
| 5 | screenshot | — | Check result |
| 6 | left_click | [15, 26] | "Try File menu instead" |
| 7 | screenshot | — | "File menu visible" |
| 8 | left_click | [57, 333] | "Click Import..." |
| 9 | screenshot | — | "Import dialog didn't open" |
| 10 | left_click | [15, 26] | "Open File menu again" |
| 11 | screenshot | — | "Menu visible, try Import again" |
| 12 | left_click | [57, 333] | "Click Import..." |
| 13 | screenshot | — | "Still no dialog" |
| 14 | wait | — | "Wait 2 seconds for slow dialog" |
| 15 | screenshot | — | "Nothing appeared" |
| 16 | left_click | [15, 26] | "Try File menu" |
| 17 | left_click | [33, 45] | "Click New submenu" |
| 18 | screenshot | — | "Menu still showing" |
| 19 | key | ctrl+n | "Try keyboard shortcut" |
| 20 | screenshot | — | "Nothing happened" |
| 21 | left_click | [81, 204] | "Try Create Project link" |
| 22 | wait | — | "Wait for response" |
| 23 | screenshot | — | "Nothing" |
| 24 | key | alt+Tab | "Check for hidden windows" |
| 25 | screenshot | — | "Only main window visible" |
| 26 | right_click | [900, 400] | "Try desktop context menu" |
| 27 | screenshot | — | "No menu appeared" |
| 28 | left_click_drag | [700, 100] | "Try moving window" |
| 29 | screenshot | — | "Window didn't move" |
| 30 | mouse_move | [74, 229] | "Hover over link" |

### Issues Found by Agent

| # | Issue | Severity | Notes |
|---|-------|----------|-------|
| 1 | Tab labels "Sys", "Typ" truncated | Minor | Not self-explanatory for new users |
| 2 | No loading feedback | Major | Actions trigger with no visual indicator |
| 3 | Empty workspace — no onboarding | Minor | New users see "no projects" without guidance |
| 4 | "Operation not enabled" error | Major | Unhelpful — doesn't explain what or why |
| 5 | Visual proximity misclick | Minor | Clicked Clone instead of Continue |

### Output Files
```
agent_interaction/outputs/
├── task1_orientation_report.md      — Agent's usability report
├── task1_orientation_results.json   — Full JSON with action log
└── task1_orientation_step01-30.png  — Screenshot at every step
```

---

## 11. Challenges & Solutions — Complete List

| # | Challenge | Phase | Root Cause | Solution | Status |
|---|-----------|-------|-----------|----------|--------|
| 1 | `google-generativeai` deprecated | 1B | SDK replaced | Use `google-genai` SDK | Resolved |
| 2 | `gemini-2.0-flash` retired | 1B | Model deprecated | Use `gemini-2.5-flash` | Resolved |
| 3 | Rate limiting on Gemini API | 1B | API quota | Add 5s pause between calls | Resolved |
| 4 | Video upload processing time | 1B | Expected behavior | Wait loop checking state | Resolved |
| 5 | Frame 1 is JKU logo | 1C | Video starts with intro | Skip frame 1, start from 2 | Resolved |
| 6 | Too many frames (221) for API | 1C | 3s extraction too dense | Select every 11th frame | Resolved |
| 7 | Anthropic billing error | 1D | Key issue | Used different key from OpenClaw | Resolved |
| 8 | Different image formats per API | 1D | API differences | Separate encode functions | Resolved |
| 9 | Rosetta error on ARM Mac | 2B | x86_64 binary on ARM | `platform: linux/amd64` in compose | Resolved |
| 10 | IDE window not responding | 2B | No window focus | `windowfocus --sync` before actions | Resolved |
| 11 | SWT hyperlinks not clickable | 2B | QEMU + SWT issue | **Unresolved** — need native x86_64 | Open |
| 12 | SWT dialogs not appearing | 2B | QEMU rendering | **Unresolved** — need native x86_64 | Open |
| 13 | Keyboard shortcuts fail | 2B | QEMU key delivery | `--clearmodifiers` partially helps | Partial |
| 14 | `betas` param not accepted | 2C | SDK API change | Use `client.beta.messages.create()` | Resolved |
| 15 | NoneType in report gen | 2C | null text values | `s.get('text') or ''` | Resolved |

---

## 12. All Code — Full Source

### File Structure
```
/Users/mirzamir/Desktop/4diac/
├── progress.md                        # Master progress document
├── SUMMARY_FOR_MEETING.md             # Meeting-ready summary
├── FULL_SESSION_LOG.md                # THIS FILE
├── s10270-023-01084-7-1.pdf           # Ground truth paper
├── 2312.11805v5.pdf                   # Gemini paper
│
├── videos/
│   ├── task_demo.mkv                  # Video 2 — Bianca's task demo (31MB)
│   ├── intro_v1.mkv                   # Video 1 — IEC 61499 intro (17MB)
│   └── intro_v2.webm                  # Video 3 — New features preview (32MB)
│
├── exploration/
│   ├── .env                           # API keys
│   ├── prompts.py                     # 3 prompt levels (blind, CD, task-specific)
│   ├── gemini_video_assess.py         # Gemini video assessment
│   ├── assess_screenshots.py          # Multi-model screenshot assessment
│   ├── frames/
│   │   ├── td/                        # 66 frames (every 10s)
│   │   └── td_3s/                     # 221 frames (every 3s)
│   └── outputs/
│       ├── gemini_video/              # 8 video assessments
│       └── screenshots/               # 8 screenshot assessments
│
└── agent_interaction/
    ├── Dockerfile                     # Ubuntu + Java + 4diac + VNC
    ├── docker-compose.yml             # Container config
    ├── start.sh                       # Entrypoint (Xvfb + VNC + IDE)
    ├── tasks.py                       # 4 task definitions
    ├── claude_computer_use.py         # Claude Computer Use agent
    ├── RESEARCH_UI_AGENTS.md          # Survey of 12+ agents
    ├── EXPERIMENTS.md                 # Experiment documentation
    ├── workspace/                     # Mounted in Docker
    └── outputs/                       # Agent results + 30 screenshots
```

---

## 13. How to Replicate

### Phase 1: Video/Screenshot Assessment

```bash
# Step 1: Setup
conda activate 4diac
cd /Users/mirzamir/Desktop/4diac

# Step 2: Download videos
yt-dlp -o "videos/task_demo.%(ext)s" "https://youtu.be/xishphcgYmc"
yt-dlp -o "videos/intro_v1.%(ext)s" "https://youtu.be/K9iItQBC-ac"
yt-dlp -o "videos/intro_v2.%(ext)s" "https://youtu.be/by02Xu2yrPE"

# Step 3: Run Gemini video assessments
cd exploration/
python gemini_video_assess.py td blind
python gemini_video_assess.py td cd_guided
python gemini_video_assess.py td task_specific
python gemini_video_assess.py v1 blind
python gemini_video_assess.py v2 blind

# Step 4: Extract frames
ffmpeg -i ../videos/task_demo.mkv -vf "fps=1/10" -q:v 2 frames/td/frame_%04d.jpg
ffmpeg -i ../videos/task_demo.mkv -vf "fps=1/3" -q:v 2 frames/td_3s/frame_%04d.jpg

# Step 5: Run screenshot assessments
python assess_screenshots.py blind all 6frames
python assess_screenshots.py cd_guided all 6frames
python assess_screenshots.py blind all 20frames
python assess_screenshots.py blind claude 20frames
python assess_screenshots.py cd_guided claude 20frames
```

### Phase 2: Agent Interaction

```bash
# Step 1: Build and start Docker container
cd agent_interaction/
docker compose up --build -d

# Step 2: Verify IDE is running
docker exec agent_interaction-4diac-ide-1 ps aux | grep 4diac

# Step 3: Install xdotool + scrot
docker exec agent_interaction-4diac-ide-1 bash -c "apt-get update -qq && apt-get install -y -qq xdotool scrot"

# Step 4: Take test screenshot
docker exec agent_interaction-4diac-ide-1 bash -c "DISPLAY=:1 scrot /tmp/screen.png"
docker cp agent_interaction-4diac-ide-1:/tmp/screen.png ./screen_check.png

# Step 5: Run agent task
cd ..
python agent_interaction/claude_computer_use.py task1_orientation

# Step 6: View results
cat agent_interaction/outputs/task1_orientation_report.md

# Step 7: Stop container when done
cd agent_interaction/
docker compose down
```

### Important Notes for Replication
1. **ARM Mac users:** The `platform: linux/amd64` line is required but causes QEMU performance issues. For full agent experiments, use a native x86_64 Linux machine.
2. **API keys:** All 3 providers require active accounts with billing enabled.
3. **Rate limits:** Gemini has per-minute limits — the 5-second pause between calls handles this.
4. **Conda env:** Always activate `4diac` env before running scripts.
5. **Video formats:** yt-dlp downloads vary — .mkv and .webm both work with Gemini.

---

---

## 14. Full Conversation Transcript

The complete conversation between the student and Claude (3149 lines) is saved in `dialog.txt`. It includes:

- Meeting notes review and corrections
- Questions about the meeting (goals, next steps, timeline)
- Paper analysis and ground truth extraction
- All experiment runs with live output
- Troubleshooting sessions (SDK issues, Docker issues, QEMU issues)
- Research discussions (video input capabilities, agent survey)
- Report generation and documentation
- Thesis title brainstorming

### Topics Discussed (chronological order)

| Topic | Lines (approx) | Summary |
|-------|:-----------:|---------|
| Meeting notes review | 1-80 | Reviewed and corrected meeting notes |
| Meeting summary & questions | 80-100 | What was discussed, action items, next meeting date |
| Paper analysis | 100-200 | Extracted methodology, metrics, tasks, CD framework, YouTube links |
| API key setup | 200-250 | Found keys in OpenClaw, configured .env |
| Video download | 250-300 | yt-dlp for 3 YouTube videos |
| Gemini video assessments | 300-700 | 8 experiments (blind, CD-guided, task-specific) |
| Frame extraction | 700-800 | ffmpeg at 10s and 3s intervals |
| Screenshot assessments | 800-1100 | GPT-4o, Gemini, Claude — 6 and 20 frames |
| Video input research | 1100-1200 | Which models accept video natively |
| Results comparison | 1200-1400 | Ground truth matrix, model ranking |
| SUMMARY_FOR_MEETING.md creation | 1400-1600 | Full meeting summary |
| Agent research | 1600-1900 | 12+ agents surveyed, Docker feasibility |
| Docker setup & debugging | 1900-2400 | Dockerfile, QEMU issues, xdotool fixes |
| Claude Computer Use script | 2400-2600 | API format, action execution, agent loop |
| Task 1 experiment | 2600-2800 | 30-step agent run, usability issues found |
| Documentation | 2800-3000 | progress.md, EXPERIMENTS.md, memory updates |
| Thesis titles | 3000-3149 | Title suggestions for practicum report and bachelor thesis |

### Suggested Thesis Titles (from discussion)

**Top pick:** *"AI as Usability Tester: Comparing Video Analysis and Agent-Based Interaction for Assessing Industrial Automation IDEs"*

**Two-phase naming convention:**
| Phase | Name |
|-------|------|
| Video/screenshot analysis | **Passive analysis** (AI as observer) |
| Agent clicking through IDE | **Interactive assessment** (AI as user) |
| Both combined | **Multimodal AI usability evaluation** |

---

*Generated: 2026-03-11 | Total experiments: 17 (16 Phase 1 + 1 Phase 2) | Dialog: 3149 lines*
