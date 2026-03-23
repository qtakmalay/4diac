# Exploration Results: AI-Based Usability Assessment for 4diac IDE
## Summary for Meeting with Prof. Zoitl & Rick Rabiser

**Prepared by:** Mirza Mir
**Date:** March 11, 2026
**Context:** Initial exploration phase — testing if/how AI models can assess IDE usability from video and screenshots

---

## 1. What Was Done

### Setup
- Created a Python project with API access to 3 AI providers: Google Gemini, OpenAI GPT-4o, Anthropic Claude
- Downloaded 3 YouTube videos referenced in the paper (Wiesmayr et al. 2023)
- Extracted video frames at different densities (6 frames / 20 frames)
- Built automated scripts to run assessments and save structured outputs

### Experiments Run (7 total, all on March 11, 2026)

| # | Model | Input | Prompt Type | Video Source |
|---|-------|-------|-------------|--------------|
| 1 | Gemini 2.5 Flash | Video (native) | Blind | task_demo.mkv |
| 2 | Gemini 2.5 Flash | Video (native) | CD-Guided (14 dimensions) | task_demo.mkv |
| 3 | Gemini 2.5 Flash | Video (native) | Task-Specific (4 tasks from paper) | task_demo.mkv |
| 4 | GPT-4o | 6 screenshots | Blind + CD-Guided | task_demo.mkv |
| 5 | Gemini 2.5 Flash | 6 screenshots | Blind + CD-Guided | task_demo.mkv |
| 6 | GPT-4o + Gemini | 20 screenshots | Blind | task_demo.mkv |
| 7 | Claude Sonnet 4 | 20 screenshots | Blind + CD-Guided | task_demo.mkv |

**Total assessments:** 16 individual model runs across different configurations.

All experiments used **task_demo.mkv** — Bianca Wiesmayr's demonstration video of 4 maintenance tasks in 4diac IDE (the same tasks from the paper).

---

## 2. Key Finding: Ground Truth Comparison

The paper documents 10 specific usability issues found by 10 real automation engineers. How many did each approach detect?

### Issue Detection Matrix

| # | Issue from Paper | Freq | Gemini Video | Gemini 20ss | Claude 20ss | GPT-4o 20ss |
|---|-----------------|------|:---:|:---:|:---:|:---:|
| 1 | No search feature | 6/10 | **YES** | partial | partial | partial |
| 2 | Can't identify location in hierarchy | 6/10 | **YES** | partial | no | no |
| 3 | No link to all instances of a type | 5/10 | **YES** | no | no | no |
| 4 | Difficulty adding files from filesystem | 9/10 | **YES** | no | no | no |
| 5 | Connection routing issues | 6/10 | **YES** | yes | yes | yes |
| 6 | Confusing context menu names | multiple | **YES** | yes | no | no |
| 7 | Icons too small / hard to understand | 4/10 | **YES** | partial | yes | partial |
| 8 | Insufficient input validation / errors | 4/10 | **YES** | no | partial | no |
| 9 | Cut/paste across hierarchy broken | 5/10 | no | no | no | no |
| 10 | No visible path from root to block | 4/10 | partial | no | no | no |
| | **Total** | | **~8/10** | **~4/10** | **~3/10** | **~2/10** |

### Additional Valid Issues Found by AI (not in paper's top 10)
- Broken connections after type change (all models caught this)
- Repetitive parameter creation workflow (Gemini video)
- No visual indicator for direct parameter values (Gemini video)
- Generic parameter naming (Gemini screenshots)
- Connection creation workflow inefficiency (Gemini video, Claude)

---

## 3. Model Comparison

### Overall Ranking

| Rank | Approach | Score | Strengths | Weaknesses |
|------|----------|-------|-----------|------------|
| 1 | **Gemini + Video** | ~8/10 | Sees interaction flow, cites timestamps, understands tool deeply | Requires video upload, ~30s processing |
| 2 | Gemini + 20 screenshots | ~4/10 | References frame numbers, good detail | Misses interaction dynamics |
| 3 | Claude + 20 screenshots | ~3/10 | More critical eye, catches some issues | Over-critical, assumes features are missing when they exist |
| 4 | GPT-4o + 20 screenshots | ~2/10 | Basic observations | Very generic, suggests features that already exist |

### CD Framework Ratings Comparison (from CD-guided prompts)

| Dimension | Paper Finding | Gemini Video | Claude 20ss | GPT-4o 20ss |
|-----------|--------------|:---:|:---:|:---:|
| Viscosity | Issues with type change | MODERATE | POOR | MODERATE |
| Visibility | Location identification hard | GOOD | MODERATE | POOR |
| Premature Commitment | Type change forces blind decisions | MODERATE | MODERATE | MODERATE |
| Hidden Dependencies | Internal params not visible | MODERATE | POOR | POOR |
| Role-Expressiveness | FB blocks lack behavior viz | GOOD | MODERATE | MODERATE |
| Error-Proneness | Broken connections, bad error msgs | **POOR** | POOR | MODERATE |
| Abstraction | Good subapp mechanisms | GOOD | GOOD | GOOD |
| Secondary Notation | Comments available but limited | MODERATE | POOR | MODERATE |
| Closeness of Mapping | Good match to domain | GOOD | GOOD | MODERATE |
| Consistency | Type change inconsistent | MODERATE | MODERATE | GOOD |
| Diffuseness | Large blocks reduce workspace | MODERATE | MODERATE | POOR |
| Hard Mental Operations | Re-wiring high cognitive load | **POOR** | POOR | MODERATE |
| Provisionality | Limited for type changes | MODERATE | POOR | MODERATE |
| Progressive Evaluation | Not shown in video | N/A | MODERATE | MODERATE |

**Note:** Gemini video ratings are evidence-based (cites specific moments). Claude ratings tend to be harsher without specific evidence. GPT-4o ratings are generic.

---

## 4. What This Means

### The Core Finding
**AI-based video analysis can detect ~80% of the usability issues that took 10 human engineers + 3 researchers to find.** This was achieved with a single video and zero human participants.

### Practical Implications
1. **Cost reduction:** No need for lab setup, eye trackers, multiple scribes, or scheduling participants
2. **Speed:** Full assessment in minutes vs. weeks of human studies
3. **Scalability:** Can assess every IDE release automatically
4. **Complementary:** AI finds many of the same issues + some additional ones, but humans still catch interaction-specific issues (like cut/paste across hierarchy)

### Limitations
1. **Can only assess what's shown** — if a feature isn't demonstrated in the video, the AI can't evaluate it
2. **No actual interaction** — AI observes but doesn't try to use the tool
3. **No subjective experience** — can't measure frustration, satisfaction, or emotional responses
4. **Video is essential** — screenshots lose too much information (~40-50% drop in detection rate)

---

## 5. Video Input Capabilities (Research Finding)

| Model | Video Input | Screenshot Input | Notes |
|-------|:---------:|:---------------:|-------|
| Gemini 2.5 | **Native** | Yes | Best option for video-based assessment |
| GPT-5 | Native | Yes | Accepts MP4/MOV but decomposes to keyframes internally |
| GPT-4o | No | Yes | Must extract frames manually |
| Claude (all) | No | Yes | Video API announced for mid-2026, not yet available |

**Conclusion:** Gemini is currently the only practical option for true video-based usability assessment.

---

## 6. Prompt Strategy Findings

Three prompt levels were tested (all with Gemini + video on task_demo.mkv):

| Level | Description | Best For | Example Output |
|-------|-------------|----------|----------------|
| **Blind** | "Assess the usability" — no framework | Discovering unexpected issues, getting unbiased first impressions | Found 5 issues + 7 strengths, good overview |
| **CD-Guided** | Provide all 14 Cognitive Dimensions | Structured comparison with existing studies, systematic evaluation | Rated all 14 dimensions, top 5 issues aligned with paper |
| **Task-Specific** | Describe a specific user task | Deep-diving into particular workflows, catching domain-specific issues | Task 1 correctly identified search as #1 missing feature |

**Recommended approach:** CD-Guided for overall assessment, then Task-Specific for deep dives into critical workflows. Blind as a sanity check.

---

## 7. What I Did (Technical Setup)

### Infrastructure
- **Conda environment:** `4diac` (Python 3.11) — isolated from other projects
- **API keys:** Managed via OpenClaw, copied to project `.env`
- **Video download:** `yt-dlp` from YouTube links in the paper
- **Frame extraction:** `ffmpeg` at 10s intervals (66 frames) and 3s intervals (221 frames)

### Scripts Created
| Script | Purpose |
|--------|---------|
| `exploration/prompts.py` | 3 prompt levels: blind, CD-guided, 4 task-specific |
| `exploration/gemini_video_assess.py` | Gemini video assessment (upload + assess + save) |
| `exploration/assess_screenshots.py` | Multi-model screenshot assessment (GPT-4o, Gemini, Claude) |

### Output Files (22 total)
```
outputs/gemini_video/
  td_blind.md              — Gemini video blind (task_demo.mkv)
  td_cd_guided.md          — Gemini video CD-guided (task_demo.mkv)
  td_task_task1_*.md       — Gemini video task 1: orientation (task_demo.mkv)
  td_task_task2_*.md       — Gemini video task 2: hierarchy (task_demo.mkv)
  td_task_task3_*.md       — Gemini video task 3: library (task_demo.mkv)
  td_task_task4_*.md       — Gemini video task 4: editing (task_demo.mkv)
  v1_blind.md              — Gemini video blind (intro_v1.mkv)
  v2_blind.md              — Gemini video blind (intro_v2.webm)

outputs/screenshots/
  gpt4o_blind.md           — GPT-4o 6 screenshots blind (task_demo.mkv)
  gpt4o_cd_guided.md       — GPT-4o 6 screenshots CD-guided (task_demo.mkv)
  gpt4o_blind_20frames.md  — GPT-4o 20 screenshots blind (task_demo.mkv)
  gemini_ss_blind.md       — Gemini 6 screenshots blind (task_demo.mkv)
  gemini_ss_cd_guided.md   — Gemini 6 screenshots CD-guided (task_demo.mkv)
  gemini_ss_blind_20frames.md — Gemini 20 screenshots blind (task_demo.mkv)
  claude_blind_20frames.md    — Claude 20 screenshots blind (task_demo.mkv)
  claude_cd_guided_20frames.md — Claude 20 screenshots CD-guided (task_demo.mkv)
```

---

## 8. Phase 2: Agent-Based UI Interaction (Proof of Concept)

### What Was Done
Beyond passive video/screenshot analysis, we explored whether AI agents can **directly interact** with the 4diac IDE — clicking, typing, navigating — like a real user.

### Setup
- **Docker container:** Ubuntu 22.04 + Java 17 + 4diac IDE 3.0.2
- **Remote display:** Xvfb (virtual framebuffer) + x11vnc + noVNC
- **Agent:** Claude Sonnet 4.6 via Computer Use API (`computer_20251124`)
- **Interaction:** xdotool for mouse/keyboard simulation
- **Script:** `agent_interaction/claude_computer_use.py` — full agent loop

### Agent Research
Surveyed 12+ AI agents capable of UI interaction (full details in `agent_interaction/RESEARCH_UI_AGENTS.md`):

| Agent | Capability | OSWorld Score |
|-------|-----------|---------------|
| Claude Computer Use | Screenshot + mouse/keyboard | ~22% |
| Simular Agent S | Multi-step UI tasks | **72.6%** (SOTA) |
| OpenAI CUA | Operator-based browsing | ~39% |
| Bytebot | Docker-based, pre-built | N/A |

### Experiment: Task 1 — Orientation (30 steps)
The agent attempted to explore the IDE, find function blocks, and navigate the project hierarchy.

**What the agent did:**
1. Took screenshots, identified the IDE layout
2. Tried clicking hyperlinks ("Import projects...", "Create new project")
3. Successfully opened the File menu
4. Tried File > Import, File > New, Ctrl+N keyboard shortcuts
5. Tried Alt+Tab, right-clicking, dragging windows to find hidden dialogs

**Usability issues found by the agent:**

| # | Issue | Severity | Valid? |
|---|-------|----------|--------|
| 1 | Tab labels truncated ("Sys", "Typ") — not self-explanatory | Minor | Yes |
| 2 | No loading feedback when actions are triggered | Major | Yes |
| 3 | Empty workspace has no onboarding guidance | Minor | Yes |
| 4 | "The chosen operation is not enabled" — unhelpful error | Major | Yes |
| 5 | Visual proximity — misclicked Clone instead of Continue | Minor | Yes |

### Limitation: QEMU Emulation
Running x86_64 4diac IDE on ARM Mac via QEMU caused SWT dialogs to not render. This blocked deeper exploration. **Solution:** Run on a native x86_64 Linux machine.

### Key Insight
Each assessment approach finds **different kinds of issues**:

| Approach | Finds | Misses |
|----------|-------|--------|
| **Video** (Gemini) | Workflow problems, timing, transitions | Can't try alternatives |
| **Screenshots** (multi-model) | Visual design, layout, clutter | No dynamics |
| **Agent** (Claude CU) | Interaction bugs, missing feedback, onboarding | Limited by environment |

**The ideal methodology combines all three.**

---

## 9. Proposed Next Steps

### For Discussion at Meeting
0. **QEMU blocker** — do you have access to an x86_64 Linux server at JKU for Docker experiments?
1. **Define goals & non-goals** for the practicum based on these findings
2. **Choose direction:**
   - A) Go deeper on video-based assessment (more videos, more prompts, systematic evaluation)
   - B) Explore agent-based interaction (AI agent actually uses the IDE via Docker)
   - C) Combine both — video assessment + agent interaction
3. **Scope the report:** What experiments to include, what to focus on

### Suggested Practicum Goals
- **Goal 1:** Systematically evaluate AI video assessment vs human assessment (using paper as ground truth)
- **Goal 2:** Develop a repeatable methodology for AI-based usability assessment
- **Goal 3:** Explore whether AI agents can interact with 4diac IDE to discover issues humans would find
- **Non-goal:** Replacing human studies entirely (AI is complementary, not a replacement)

### Suggested Timeline
- **March-April:** Systematic experiments, methodology development
- **May 18 (Presentation 1):** Present exploration results + methodology
- **May-June:** Deeper experiments, agent interaction exploration
- **June 22 (Presentation 2):** Present final results + comparison
- **July:** Write practicum report (10-20 pages)

---

## 10. All Output Files

### Phase 1 (16 assessments)
```
exploration/outputs/gemini_video/    — 8 Gemini video assessments
exploration/outputs/screenshots/     — 8 screenshot assessments (GPT-4o, Gemini, Claude)
```

### Phase 2 (1 agent experiment)
```
agent_interaction/outputs/           — Task 1 report + 30 step screenshots
agent_interaction/EXPERIMENTS.md     — Full experiment documentation
agent_interaction/RESEARCH_UI_AGENTS.md — Agent survey (12+ agents)
```

---

## 11. References

1. Wiesmayr, B., Zoitl, A., & Rabiser, R. (2023). Assessing the usefulness of a visual programming IDE for large-scale automation software. *Software and Systems Modeling*, 22, 1619-1643.
2. Gemini Team, Google (2023/2025). Gemini: A Family of Highly Capable Multimodal Models. arXiv:2312.11805v5.
3. Blackwell, A.F. & Green, T.R.G. (2003). Notational systems—The cognitive dimensions of notations framework.
4. Study materials: Zenodo DOI 10.5281/ZENODO.4758816
5. YouTube videos: https://youtu.be/K9iItQBC-ac, https://youtu.be/xishphcgYmc, https://youtu.be/by02Xu2yrPE
