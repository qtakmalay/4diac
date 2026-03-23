# New vs Old Version Usability Comparison
# AI-Based Usability Assessment of Eclipse 4diac IDE

**Date:** 2026-03-23
**Author:** Azat Vakhitov (with Claude Opus 4.6 as assistant)
**Purpose:** Compare usability findings between old 4diac version (task_demo.mkv, intro_v1/v2) and new version (2026-03-19 videos) to identify which issues persist, which are resolved, and what new issues emerged.

---

## Table of Contents

1. [Experiment Setup](#1-experiment-setup)
2. [Videos Assessed](#2-videos-assessed)
3. [Assessment Methods Used](#3-assessment-methods-used)
4. [Commands to Replicate](#4-commands-to-replicate)
5. [New Version Findings Summary](#5-new-version-findings-summary)
6. [Old vs New Comparison Table](#6-old-vs-new-comparison-table)
7. [Issues Still Present in New Version](#7-issues-still-present-in-new-version)
8. [Issues Resolved in New Version](#8-issues-resolved-in-new-version)
9. [New Issues Found in New Version](#9-new-issues-found-in-new-version)
10. [Cognitive Dimensions Comparison](#10-cognitive-dimensions-comparison)
11. [Conclusions](#11-conclusions)

---

## 1. Experiment Setup

**Machine:** Windows 11 Home (10.0.22631), x86_64
**Python:** 3.11.15 (conda env: `4diac`)
**Models Used:**
- Gemini 2.5 Flash (video + screenshots)
- GPT-4o (screenshots)
- Claude Sonnet 4 (screenshots)

**Docker:** 28.1.1 with WSL2 (native x86_64, no QEMU)

---

## 2. Videos Assessed

### Old Version (Previous Experiments)
| Video | File | Duration | Content |
|-------|------|----------|---------|
| task_demo | `task_demo.mkv` | ~11 min | Full task demonstration (orientation, hierarchy, library, editing) |
| intro_v1 | `intro_v1.mkv` | ~5 min | Introduction to 4diac IDE v1 |
| intro_v2 | `intro_v2.webm` | ~8 min | Introduction to 4diac IDE v2 |

### New Version (This Experiment)
| Video | File | Duration | Content |
|-------|------|----------|---------|
| new_a | `2026-03-19 21-25-12.mkv` | 704s (~12 min) | Project creation, FB type creation, palette usage, connections |
| new_b | `2026-03-19 21-39-08.mkv` | 320s (~5 min) | FB insertion, ECC discovery, data/event connections |

---

## 3. Assessment Methods Used

### A. Gemini Video Assessment (full video upload)
- **Blind prompt**: Open-ended usability assessment
- **CD-guided prompt**: Cognitive Dimensions of Notations framework (14 dimensions rated)
- Script: `exploration/gemini_video_assess.py`

### B. Multi-Model Screenshot Assessment (6 frames per video)
- Frames extracted at 1 frame per 10 seconds, then 6 evenly-spaced frames selected
- Script: `exploration/assess_new_videos.py`
- Models: GPT-4o, Gemini 2.5 Flash, Claude Sonnet 4

### C. Agent Interaction (Docker + Claude Computer Use)
- Claude controls the IDE via xdotool in Docker container
- Takes screenshots at each step, reports usability issues encountered
- Script: `agent_interaction/claude_computer_use.py`

---

## 4. Commands to Replicate

```bash
# Prerequisites
conda create -n 4diac python=3.11 -y
conda run -n 4diac pip install google-genai openai anthropic python-dotenv Pillow yt-dlp

# Set API keys in .env file at project root
# GOOGLE_API_KEY=...
# OPENAI_API_KEY=...
# ANTHROPIC_API_KEY=...

# Step 1: Extract frames from new videos (1 per 10 seconds)
mkdir -p exploration/frames/new_a exploration/frames/new_b
ffmpeg -i "videos/2026-03-19 21-25-12.mkv" -vf "fps=1/10" -q:v 2 exploration/frames/new_a/frame_%04d.jpg
ffmpeg -i "videos/2026-03-19 21-39-08.mkv" -vf "fps=1/10" -q:v 2 exploration/frames/new_b/frame_%04d.jpg
# Result: 70 frames (video A), 32 frames (video B)

# Step 2: Run Gemini video assessments (blind + CD-guided on each video)
cd exploration
conda run -n 4diac python gemini_video_assess.py new_a blind
conda run -n 4diac python gemini_video_assess.py new_a cd_guided
conda run -n 4diac python gemini_video_assess.py new_b blind
conda run -n 4diac python gemini_video_assess.py new_b cd_guided
# Output: exploration/outputs/gemini_video/new_a_blind.md, new_a_cd_guided.md, new_b_blind.md, new_b_cd_guided.md

# Step 3: Run multi-model screenshot assessments
conda run -n 4diac python assess_new_videos.py new_a all blind
conda run -n 4diac python assess_new_videos.py new_b all blind
# Output: exploration/outputs/new_version/new_a_gpt4o_blind.md, new_a_gemini_blind.md, new_a_claude_blind.md, etc.

# Step 4: Run agent interaction (requires Docker)
cd ../agent_interaction
docker compose up --build -d
# Wait 10 seconds for IDE to load, then:
conda run -n 4diac python claude_computer_use.py
# Output: agent_interaction/outputs/task*_report.md, task*_step*.png
```

---

## 5. New Version Findings Summary

### Video A (12 min) — Key Issues Found Across All Models

| # | Issue | Severity | Found By |
|---|-------|----------|----------|
| 1 | **Empty Palette on new project** — users must manually click "Add Standard Libraries" | HIGH | Gemini-video, Gemini-ss |
| 2 | **Vague connection error feedback** — red X with no explanation of why connection failed | MEDIUM | Gemini-video, Claude-ss |
| 3 | **Unclear multiple event input handling** — no visual indication of OR-ing event sources | MEDIUM | Gemini-video |
| 4 | **Viscosity — connections break/require multiple attempts** to snap correctly | HIGH | Gemini-CD |
| 5 | **Diffuseness — too many panels** reduce canvas working area | MEDIUM | Gemini-CD, Claude-ss, GPT4o-ss |
| 6 | **Poor role-expressiveness** — cryptic FB names (E_SWITCH, E_CYCLE, E_SR) | MEDIUM | Gemini-CD, GPT4o-ss |
| 7 | **Intrusive white bar** at bottom of TutorialApp editor, unclear purpose | LOW | Gemini-ss |
| 8 | **Truncated descriptions** in New Type dialog | LOW | Gemini-ss |
| 9 | **No snap-to-grid or alignment aids** | LOW | Gemini-ss, Claude-ss |
| 10 | **Grayed-out Package field** without explanation | LOW | Gemini-ss |

### Video B (5 min) — Key Issues Found Across All Models

| # | Issue | Severity | Found By |
|---|-------|----------|----------|
| 1 | **ECC editor undiscoverable** — hidden tab only appears when FB selected, no right-click option | CRITICAL | Gemini-video, Gemini-CD |
| 2 | **Documentation-UI discrepancy** — help says "tab at bottom" but tab not visible | HIGH | Gemini-video |
| 3 | **Data pin connection difficulty** — repeated fumbling, unclear interaction model | HIGH | Gemini-video, Gemini-CD |
| 4 | **Inconsistent FB insertion methods** — palette drag, right-click menu, global search all work differently | MEDIUM | Gemini-video, Gemini-CD |
| 5 | **Empty canvas gives no guidance** — no prompt on how to add first FB | MEDIUM | Gemini-ss |
| 6 | **Abstract port labels** — EDO, EI, EO0, SI, Q require prior IEC 61499 knowledge | MEDIUM | Gemini-ss |
| 7 | **"Properties not available" shown frequently** — frustrating empty state | LOW | Claude-ss |

---

## 6. Old vs New Comparison Table

| Issue Category | Old Version (task_demo) | New Version (2026-03-19) | Status |
|----------------|------------------------|--------------------------|--------|
| **Connection loss on type change** | CRITICAL — all connections break when changing sub-app type | NOT TESTED in new videos (different tasks shown) | UNKNOWN — needs agent verification |
| **Misleading error messages** | "Param2 has already an input connection" when Param2 unconnected | Vague red X with no explanation on invalid connections | PERSISTS (different manifestation) |
| **Manual reconnection burden** | HIGH — tedious re-wiring after type changes | NOT TESTED | UNKNOWN |
| **Visual clutter / diffuseness** | MODERATE — many panels reduce canvas area | PERSISTS — all 3 models flag this in new version | PERSISTS |
| **Lack of global search** | No way to search for block instances across project | Global search exists but returns irrelevant results (e.g., "FB Debug" view) | PARTIALLY IMPROVED |
| **Truncated block names** | Block names truncated on canvas | Description column truncated in New Type dialog | PERSISTS (different location) |
| **No visual differentiation for block types** | All blocks look like similar rectangles | Still similar rectangles, terse names | PERSISTS |
| **Hierarchical navigation** | EXCELLENT — toggle sub-app, follow connection, drill-down | Not demonstrated in new videos | ASSUMED STABLE |
| **Follow Connection feature** | EXCELLENT — right-click to trace connections | Not demonstrated | ASSUMED STABLE |
| **Type system for reusability** | Strong but undermined by connection loss | Not demonstrated | ASSUMED STABLE |
| **Standard IDE familiarity** | Good — Eclipse-based layout recognized | Good — all models note familiar layout | STABLE |
| **Visual programming paradigm** | Strong — intuitive block-and-wire approach | Strong — all models praise drag-and-drop | STABLE |
| **Dark theme** | Not noted (light theme in old videos?) | All models note dark theme positively | NEW/IMPROVED |
| **Empty Palette on new project** | Not noted (palette pre-populated?) | CRITICAL — empty palette, non-obvious "Add Libraries" button | NEW ISSUE or newly visible |
| **ECC editor discoverability** | Not tested (tasks didn't require ECC) | CRITICAL — hidden, undiscoverable | NEW ISSUE |
| **Data pin connection difficulty** | Connection drawing generally worked | Repeated fumbling, unclear feedback | NEW ISSUE or worsened |
| **Inconsistent FB insertion** | Not tested | Multiple methods work differently | NEW ISSUE |
| **Onboarding for empty canvas** | Welcome screen present with clear options | Empty canvas has no guidance prompt | MIXED — welcome page good, but per-canvas guidance missing |

---

## 7. Issues Still Present in New Version

These issues were found in the old version AND confirmed in the new version:

1. **Visual density / screen real estate** — Too many panels (System Explorer, Type Navigator, Outline, Properties, Problems, Palette) competing for space. The canvas area is too small for complex diagrams.
   - Old: 3/5 models flagged this
   - New: 5/5 assessments flag this (all models + both CD-guided)

2. **Poor role-expressiveness of FB names** — Cryptic abbreviations (E_SWITCH, E_CYCLE, E_CTU, SEND_RECV_1_1) require domain expertise.
   - Old: Noted in screenshot assessments
   - New: Gemini-CD rates Role-Expressiveness as POOR

3. **Error message quality** — Error messages are vague, misleading, or don't explain the root cause.
   - Old: "Param2 has already an input connection" when Param2 is unconnected
   - New: Red X for invalid connections with no explanation

4. **Lack of contextual tooltips/help** — UI elements don't explain themselves on hover.
   - Old: Noted across models
   - New: All 3 screenshot models flag this

5. **Truncation issues** — Important text is cut off without easy way to read full content.
   - Old: Block names on canvas
   - New: Description column in New Type dialog

---

## 8. Issues Resolved in New Version

1. **Dark theme** — The new version uses a dark theme by default, which all models note positively. Old version appeared to use a light theme.

2. **Welcome screen / getting started** — The new version has a clear welcome screen with project creation options that all models praise (though empty canvas within a project still lacks guidance).

3. **Template descriptions in New Type dialog** — The new version shows descriptions for each template type (Basic FB, Composite FB, etc.), helping users choose correctly.

---

## 9. New Issues Found in New Version

These issues were NOT found in old version assessments but appear in the new version:

1. **CRITICAL: ECC Editor Discoverability** — The Execution Control Chart tab only appears when a specific FB is selected, and is not accessible via right-click or any obvious UI path. Users must consult help documentation to find it. This was not tested in old videos (different task focus).

2. **HIGH: Empty Palette Problem** — New projects start with an empty Palette, requiring users to find and click a small "Add Standard Libraries" button. This is a major first-use barrier.

3. **HIGH: Data Pin Connection Difficulty** — Connecting data pins requires repeated fumbling. The interaction model differs from event connections without clear indication.

4. **MEDIUM: Inconsistent FB Insertion Methods** — Multiple methods exist (palette drag, right-click > Insert FB, global search) but work differently and aren't clearly hierarchized.

5. **MEDIUM: Global Search Returns Irrelevant Results** — Searching "FB" returns "FB Debug" view instead of FB insertion, misleading users.

6. **LOW: Mysterious White Bar** — A large white bar at the bottom of the TutorialApp editor has unclear purpose and wastes space.

---

## 10. Cognitive Dimensions Comparison

### Old Version (task_demo, CD-guided)
| Dimension | Rating |
|-----------|--------|
| Viscosity | MODERATE |
| Visibility | GOOD |
| Premature Commitment | MODERATE |
| Hidden Dependencies | MODERATE |
| Role-Expressiveness | MODERATE |
| Error-Proneness | POOR |
| Abstraction | GOOD |
| Consistency | MODERATE |
| Hard Mental Operations | POOR |

### New Version — Video A (CD-guided)
| Dimension | Rating |
|-----------|--------|
| Viscosity | **POOR** (worsened) |
| Visibility | **MODERATE-POOR** (worsened) |
| Premature Commitment | MODERATE (stable) |
| Hidden Dependencies | MODERATE (stable) |
| Role-Expressiveness | **POOR** (worsened) |
| Error-Proneness | **MODERATE-POOR** (stable-ish) |
| Abstraction | GOOD (stable) |
| Secondary Notation | MODERATE |
| Closeness of Mapping | GOOD |
| Consistency | GOOD (improved) |
| Diffuseness | **POOR** (worsened) |
| Hard Mental Operations | **MODERATE-POOR** (stable) |
| Provisionality | MODERATE |
| Progressive Evaluation | MODERATE |

### New Version — Video B (CD-guided)
| Dimension | Rating |
|-----------|--------|
| Viscosity | **POOR** |
| Visibility | **POOR** |
| Premature Commitment | MODERATE |
| Hidden Dependencies | **POOR** (worsened — ECC hidden) |
| Role-Expressiveness | **POOR** |
| Error-Proneness | **POOR** |
| Abstraction | MODERATE |
| Secondary Notation | MODERATE |
| Closeness of Mapping | MODERATE |
| Consistency | **POOR** (worsened — inconsistent FB insertion) |
| Diffuseness | MODERATE |
| Hard Mental Operations | **POOR** |
| Provisionality | MODERATE |
| Progressive Evaluation | **POOR** |

### Key Dimension Changes
- **Viscosity**: MODERATE → POOR (connections harder to make in new version)
- **Hidden Dependencies**: MODERATE → POOR (ECC tab completely hidden)
- **Role-Expressiveness**: MODERATE → POOR (still cryptic names, no improvement)
- **Consistency**: Mixed — GOOD in video A but POOR in video B (different tasks reveal different inconsistencies)

---

## 11. Conclusions

### Overall Assessment
The new version of 4diac IDE shows **some improvements** (dark theme, better welcome screen, template descriptions) but **introduces new usability issues** and **fails to resolve most existing ones**.

### Key Takeaways

1. **Persistent core issues dominate**: Visual density, cryptic naming, poor error messages, and lack of contextual help remain across both versions. These are systemic issues that require design-level changes.

2. **New version introduces regression in learnability**: The empty Palette problem and undiscoverable ECC editor create significant first-use barriers that didn't exist (or weren't visible) in the old version.

3. **Connection interaction has worsened**: Multiple models report connection difficulty in the new version, with Viscosity rated POOR vs MODERATE in the old version.

4. **Strengths remain stable**: The visual programming paradigm, hierarchical navigation, type system, and familiar IDE layout continue to be praised across all assessments.

5. **Critical unknown**: Whether the old version's most severe issue — connection loss on type change — has been fixed in the new version was not testable from the new videos. The new videos focus on project creation and basic FB wiring rather than advanced type management tasks.

### Recommendations for 4diac IDE Team
1. **Fix ECC discoverability** — Add right-click > "Edit ECC" on function blocks
2. **Auto-populate Palette** for new projects with Standard Libraries
3. **Improve connection feedback** — show compatible ports, explain why connections fail
4. **Add contextual tooltips** for all UI elements, especially FB port labels
5. **Reduce default panel count** — collapse non-essential panels by default
6. **Verify and fix connection preservation** on type changes (if still broken)

---

## Output Files Generated

### Gemini Video Assessments
- `exploration/outputs/gemini_video/new_a_blind.md`
- `exploration/outputs/gemini_video/new_a_cd_guided.md`
- `exploration/outputs/gemini_video/new_b_blind.md`
- `exploration/outputs/gemini_video/new_b_cd_guided.md`

### Multi-Model Screenshot Assessments
- `exploration/outputs/new_version/new_a_gpt4o_blind.md`
- `exploration/outputs/new_version/new_a_gemini_blind.md`
- `exploration/outputs/new_version/new_a_claude_blind.md`
- `exploration/outputs/new_version/new_b_gpt4o_blind.md`
- `exploration/outputs/new_version/new_b_gemini_blind.md`
- `exploration/outputs/new_version/new_b_claude_blind.md`

### Combined JSON Results
- `exploration/outputs/new_version/new_a_all_blind.json`
- `exploration/outputs/new_version/new_b_all_blind.json`
- `exploration/outputs/gemini_video/new_a_all_results.json`
- `exploration/outputs/gemini_video/new_b_all_results.json`
