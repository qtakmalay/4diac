# 4diac IDE — AI-Based Usability Assessment

Automated usability assessment of [Eclipse 4diac IDE](https://eclipse.dev/4diac/) using multimodal AI models and agent-based interaction.

**Seminar + Practicum** at JKU Linz (LIT CPS Lab)
**Student:** Azat Vakhitov | **Supervisors:** Prof. Alois Zoitl, Rick Rabiser

---

## What This Is

Two approaches to automated usability evaluation:

1. **Passive Analysis** — Send IDE demo videos/screenshots to AI models (Gemini, GPT-4o, Claude) and ask them to identify usability issues
2. **Interactive Assessment** — An AI agent (Claude Computer Use) runs the IDE in Docker and interacts with it via mouse/keyboard, reporting issues from first-hand experience

Both are compared against ground truth from [Wiesmayr et al. (2023)](https://doi.org/10.1007/s10270-023-01084-7) — a human usability study with 10 automation engineers.

**Key result:** Gemini + video detected ~80% of known usability issues from a single video with zero human participants.

---

## Project Structure

```
├── progress.md                     # Master progress document
├── SUMMARY_FOR_MEETING.md          # Meeting-ready summary
├── FULL_SESSION_LOG.md             # Complete replication guide
│
├── exploration/                    # Phase 1: Video/Screenshot Assessment
│   ├── prompts.py                  # 3 prompt levels (blind, CD-guided, task-specific)
│   ├── gemini_video_assess.py      # Gemini video assessment script
│   ├── assess_screenshots.py       # Multi-model screenshot assessment
│   └── outputs/                    # All model outputs (16 assessments)
│       ├── gemini_video/           # 8 Gemini video assessments
│       └── screenshots/            # 8 screenshot assessments
│
└── agent_interaction/              # Phase 2: Agent-Based UI Interaction
    ├── Dockerfile                  # Ubuntu + Java + 4diac IDE + VNC
    ├── docker-compose.yml          # Container config
    ├── start.sh                    # Entrypoint script
    ├── tasks.py                    # 4 task definitions from the paper
    ├── claude_computer_use.py      # Claude Computer Use agent
    ├── EXPERIMENTS.md              # Experiment documentation
    ├── RESEARCH_UI_AGENTS.md       # Survey of 12+ UI agents
    └── outputs/                    # Agent results + step screenshots
```

---

## Setup (Windows)

### Prerequisites

1. **Python 3.11+** via [Miniconda](https://docs.anaconda.com/miniconda/)
2. **Docker Desktop** for Windows (with WSL2 backend)
3. **Git** for Windows
4. **ffmpeg** — `winget install ffmpeg` or download from https://ffmpeg.org
5. **yt-dlp** — `pip install yt-dlp`

### Step 1: Clone & Setup Environment

```powershell
git clone https://github.com/qtakmalay/4diac.git
cd 4diac

# Create conda environment
conda create -n 4diac python=3.11 -y
conda activate 4diac

# Install Python dependencies
pip install google-genai openai anthropic python-dotenv Pillow yt-dlp
```

### Step 2: API Keys

Create `exploration/.env`:

```env
GOOGLE_API_KEY=<your-google-gemini-api-key>
OPENAI_API_KEY=<your-openai-api-key>
ANTHROPIC_API_KEY=<your-anthropic-api-key>
```

Get keys from:
- Google: https://aistudio.google.com/apikey
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

### Step 3: Download Videos

```powershell
mkdir videos
yt-dlp -o "videos/task_demo.%(ext)s" "https://youtu.be/xishphcgYmc"
yt-dlp -o "videos/intro_v1.%(ext)s" "https://youtu.be/K9iItQBC-ac"
yt-dlp -o "videos/intro_v2.%(ext)s" "https://youtu.be/by02Xu2yrPE"
```

### Step 4: Download Papers (not in repo)

- Ground truth paper: https://doi.org/10.1007/s10270-023-01084-7 → save as `s10270-023-01084-7-1.pdf`
- Gemini paper: https://arxiv.org/abs/2312.11805 → save as `2312.11805v5.pdf`

---

## Running Phase 1: Video/Screenshot Assessment

```powershell
conda activate 4diac
cd exploration

# Gemini video assessments
python gemini_video_assess.py td blind
python gemini_video_assess.py td cd_guided
python gemini_video_assess.py td task_specific

# Extract frames for screenshot assessment
mkdir -p frames\td frames\td_3s
ffmpeg -i ..\videos\task_demo.mkv -vf "fps=1/10" -q:v 2 frames\td\frame_%04d.jpg
ffmpeg -i ..\videos\task_demo.mkv -vf "fps=1/3" -q:v 2 frames\td_3s\frame_%04d.jpg

# Screenshot assessments
python assess_screenshots.py blind all 6frames
python assess_screenshots.py cd_guided all 6frames
python assess_screenshots.py blind claude 20frames
python assess_screenshots.py cd_guided claude 20frames
```

---

## Running Phase 2: Agent Interaction (Docker)

**Windows advantage:** No QEMU emulation needed — Docker runs natively on x86_64.

```powershell
cd agent_interaction

# Build and start 4diac IDE container
docker compose up --build -d

# Verify IDE is running (should see Java process)
docker exec agent_interaction-4diac-ide-1 ps aux | findstr 4diac

# Install interaction tools
docker exec agent_interaction-4diac-ide-1 bash -c "apt-get update -qq && apt-get install -y -qq xdotool scrot"

# Take test screenshot
docker exec agent_interaction-4diac-ide-1 bash -c "DISPLAY=:1 scrot /tmp/screen.png"
docker cp agent_interaction-4diac-ide-1:/tmp/screen.png screen_check.png

# Open in browser to verify visually
start http://localhost:6080/vnc.html

# Run agent experiment (Task 1)
cd ..
python agent_interaction\claude_computer_use.py task1_orientation

# Run all 4 tasks
python agent_interaction\claude_computer_use.py

# Stop container
cd agent_interaction
docker compose down
```

### Windows-Specific Notes

- **No `platform: linux/amd64` needed** on x86_64 Windows — remove or comment out that line in `docker-compose.yml` if it causes issues
- **Docker Desktop WSL2 backend** is required (not Hyper-V)
- **VNC access:** Open `http://localhost:6080/vnc.html` in a browser to see the IDE visually
- **Path separators:** Use `\` in PowerShell or `/` in Git Bash

---

## Results Summary

| Approach | Model | Input | Issues Detected (out of 10) |
|----------|-------|-------|:---:|
| Video | Gemini 2.5 Flash | task_demo.mkv | **~8/10** |
| Screenshots (20) | Gemini 2.5 Flash | 20 frames | ~5/10 |
| Screenshots (20) | Claude Sonnet 4 | 20 frames | ~3/10 |
| Screenshots (20) | GPT-4o | 20 frames | ~2/10 |
| Agent | Claude Sonnet 4.6 (CU) | Live IDE | ~3/10 (QEMU-limited) |

---

## Documentation

| Document | Description |
|----------|-------------|
| [progress.md](progress.md) | Master progress — all phases, experiments, results |
| [SUMMARY_FOR_MEETING.md](SUMMARY_FOR_MEETING.md) | Meeting-ready summary for supervisors |
| [FULL_SESSION_LOG.md](FULL_SESSION_LOG.md) | Complete replication guide with every command |
| [agent_interaction/EXPERIMENTS.md](agent_interaction/EXPERIMENTS.md) | Phase 2 experiment details + screenshots |
| [agent_interaction/RESEARCH_UI_AGENTS.md](agent_interaction/RESEARCH_UI_AGENTS.md) | Survey of 12+ UI interaction agents |

---

## References

1. Wiesmayr, B., Zoitl, A., & Rabiser, R. (2023). *Assessing the usefulness of a visual programming IDE for large-scale automation software.* Software and Systems Modeling, 22, 1619-1643.
2. Blackwell, A.F. & Green, T.R.G. (2003). *Notational systems — The cognitive dimensions of notations framework.*
3. Study materials: [Zenodo DOI 10.5281/ZENODO.4758816](https://doi.org/10.5281/ZENODO.4758816)
