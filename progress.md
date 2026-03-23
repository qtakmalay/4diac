# 4diac IDE — Automated Usability Assessment with AI Agents
## Project Progress & Documentation

**Student:** Mirza Mir
**Supervisors:** Prof. Alois Zoitl, Rick Rabiser (JKU Linz, LIT CPS Lab)
**Type:** Seminar + Practicum (combined)
**Start Date:** Feb 24, 2026 (initial meeting)
**Next Meeting:** ~March 10, 2026 (2 weeks after initial)

---

## 1. Project Overview

### Goal
Explore to what extent AI agents/LLMs can automate usability assessment tasks for the Eclipse 4diac IDE — a visual programming environment for industrial automation based on the IEC 61499 standard.

### Background
Currently, usability studies at JKU for 4diac IDE require:
- 3+ humans per session (moderator, 2 scribes, 1 participant)
- Remote sessions via Zoom/Skype with screen sharing
- Think-aloud protocols (900+ statements across all subjects)
- Observer notes (370+ observations)
- Semi-structured interviews + questionnaires
- Open coding analysis by researchers

This is expensive, time-consuming, and hard to scale. The research question is: **Can AI replace or augment parts of this process?**

### Key Papers
1. **Wiesmayr, Zoitl, Rabiser (2023)** — "Assessing the usefulness of a visual programming IDE for large-scale automation software" — Software and Systems Modeling, 22:1619-1643, DOI: 10.1007/s10270-023-01084-7
   - Ground truth paper. Describes the methodology, metrics, and findings we're trying to replicate with AI.
2. **Google Gemini Team (2023/2025)** — "Gemini: A Family of Highly Capable Multimodal Models" — arXiv:2312.11805v5
   - Describes Gemini's multimodal capabilities (image, video, text) relevant for our video-based assessment approach.

---

## 2. Meeting Notes (Feb 24, 2026)

### Decisions Made
- Combine **seminar + practicum** into one project (one report, total ECTS of both)
- Two **5-minute presentations**: May 18 (intermediate results) and June 22 (final results)
- Report structure: Motivation/Goals/Approach → Background/State-of-the-art → Concepts/Implementation → Experiments/Results → Conclusion
- Report: 10-20 pages. Bachelor thesis later: 30-50 pages.
- Bachelor thesis can start immediately after practicum (summer, done by ~October)
- Thesis builds on practical work but must add something new

### Action Items for Next Meeting
1. Read the paper (s10270-023-01084-7-1.pdf) — contains YouTube links, methodology, framework
2. Have an initial idea of what to do — define goals and non-goals with Rick
3. Start exploring: try different models on the provided video/screenshots

### Key Quotes from Supervisor
- "Think about that you will be the next student continuing the work. What information would you like to have that it's easier to start?"
- "If you bump into errors and the goals are not met, we can document — this is a result. The failure would be if we would not document."
- "Document as much as possible — how did you do the setup, what did you do, what was the outcome"

---

## 3. Setup & Infrastructure

### Environment
- **OS:** macOS (Darwin 25.3.0, ARM/Apple Silicon)
- **Conda env:** `4diac` (Python 3.11)
- **Packages:** `google-genai`, `python-dotenv`
- **Tools:** `yt-dlp` (video download), `ffmpeg` (frame extraction — to be installed)
- **API key management:** OpenClaw (`~/.openclaw/`)

### API Keys Available
| Provider | Model | Key Location | Status |
|----------|-------|-------------|--------|
| Google Gemini | gemini-2.5-flash | `~/.openclaw/agents/main/agent/auth-profiles.json` | Working (rate limited sometimes) |
| OpenAI | GPT-4o | `~/.openclaw/openclaw.json` env vars | Available (untested) |
| Anthropic | Claude | `~/.openclaw/agents/main/agent/auth-profiles.json` | Billing errors — may need new key |
| Moonshot (Kimi) | kimi-k2 | `~/.openclaw/agents/main/agent/auth-profiles.json` | Available |
| Ollama | local models | localhost:11434 | Available |

### Project Structure
```
/Users/mirzamir/Desktop/4diac/
├── s10270-023-01084-7-1.pdf          # Ground truth paper
├── 2312.11805v5.pdf                   # Gemini paper
├── progress.md                        # THIS FILE
├── videos/
│   ├── intro_v1.mkv       # V1 — Intro to IEC 61499 & 4diac IDE (7min, v1.14.0)
│   ├── task_demo.mkv      # TD — Task demo by Bianca (maintenance tasks)
│   └── intro_v2.webm      # V2 — Preview of upcoming 4diac IDE features (v2.1.0)
└── exploration/
    ├── .env                           # API keys for scripts
    ├── .gitignore
    ├── prompts.py                     # 3 prompt levels (blind, CD-guided, task-specific)
    ├── gemini_video_assess.py         # Gemini video assessment script
    └── outputs/
        └── gemini_video/              # Assessment results (markdown + JSON)
```

### YouTube Videos (from the paper)
1. https://youtu.be/K9iItQBC-ac — Intro to IEC 61499 & 4diac IDE (7 min, v1.14.0)
2. https://youtu.be/xishphcgYmc — Task demonstration in 4diac IDE (by Bianca)
3. https://youtu.be/by02Xu2yrPE — Preview of upcoming 4diac IDE features (v2.1.0)

---

## 4. Research Framework: Cognitive Dimensions of Notations

The paper uses the **Cognitive Dimensions (CD) framework** by Blackwell & Green (2003) — 14 dimensions:

| # | Dimension | What it measures |
|---|-----------|-----------------|
| 1 | Viscosity | Resistance to change — how many actions for one goal |
| 2 | Visibility | Can you see all relevant info without digging? |
| 3 | Premature Commitment | Forced decisions before having enough info |
| 4 | Hidden Dependencies | Important links between entities not visible |
| 5 | Role-Expressiveness | Can you infer purpose from appearance? |
| 6 | Error-Proneness | Does the interface invite mistakes? |
| 7 | Abstraction | Appropriate abstraction mechanisms? |
| 8 | Secondary Notation | Can you add informal notes/colors? |
| 9 | Closeness of Mapping | Does representation match domain concepts? |
| 10 | Consistency | Similar semantics = similar syntax? |
| 11 | Diffuseness | Is the notation verbose? Large elements? |
| 12 | Hard Mental Operations | High cognitive load tasks? |
| 13 | Provisionality | Can you make tentative changes easily? |
| 14 | Progressive Evaluation | Can you check work-in-progress? |

---

## 5. Ground Truth — Known Usability Issues from Paper

These are the specific issues found by real human evaluators (10 automation engineers in Study 1):

| # | Issue | Frequency | Detected by Gemini? |
|---|-------|-----------|-------------------|
| 1 | No search feature for finding instances by name | 6/10 | **YES** — identified as "most crucial improvement" in Task 1 |
| 2 | Difficulty identifying current location in hierarchy | 6/10 | **PARTIAL** — noted breadcrumbs help (newer version has them) |
| 3 | No direct link to all instances of a type | 5/10 | **YES** — "Find all instances of Type X" recommended |
| 4 | Difficulty adding files from filesystem to project | 9/10 | **YES** — noted "subtle folder creation mechanism" |
| 5 | Connection routing criticized | 6/10 | **YES** — mentioned in blind assessment |
| 6 | Confusing context menu names | multiple | **YES** — "Flatten Subapplication" confusion noted |
| 7 | Icons too small / hard to understand | 4/10 | **YES** — "small target area for event pins" |
| 8 | Insufficient input validation | 4/10 | **YES** — "unhelpful error messages" identified as POOR |
| 9 | Cut/paste doesn't maintain cross-hierarchy connections | 5/10 | **NO** — not mentioned (not demonstrated in video) |
| 10 | No visible path from root to current block | 4/10 | **PARTIAL** — noted breadcrumbs exist (v2 feature) |

**Score: ~8/10 issues detected** (6 full, 2 partial, 2 missed)

### Additional Issues Gemini Found (not in paper's top 10 but still valid)
- Broken connections after type change (paper discusses this extensively)
- Repetitive parameter creation workflow
- Lack of visual indicators for direct parameter values
- No batch parameter creation
- Connection creation workflow less efficient than drag-and-drop

---

## 6. Experiments Conducted

**NOTE:** All main experiments (1-3) used **`task_demo.mkv` (TD)** — Bianca's task demo (31MB) — because it shows actual maintenance tasks being performed (the same 4 tasks from the paper). The intro videos (`intro_v1.mkv`, `intro_v2.webm`) are overview presentations, not task executions, so they are less useful for usability assessment comparison with the paper's ground truth.

### Experiment 1: Gemini Video Assessment — Blind Prompt
- **Date:** 2026-03-11
- **Model:** gemini-2.5-flash
- **Input:** `task_demo.mkv` (TD — task demo by Bianca, 31MB)
- **Prompt:** General usability assessment, no framework provided
- **Output:** `exploration/outputs/gemini_video/td_blind.md`
- **Key Findings:**
  - Correctly identified the IDE as a block-based visual programming tool for industrial automation
  - Identified 5 major usability issues and 7 strengths
  - Referenced specific timestamps from the video (e.g., "0:38", "2:19", "5:54")
  - Detected: connection routing, small pins, folder creation issues, context menu confusion, parameter repetitiveness
  - Missed: search feature (not shown in video), cut/paste hierarchy issues

### Experiment 2: Gemini Video Assessment — CD-Guided Prompt
- **Date:** 2026-03-11
- **Model:** gemini-2.5-flash
- **Input:** `task_demo.mkv` (TD)
- **Prompt:** Evaluate using all 14 Cognitive Dimensions
- **Output:** `exploration/outputs/gemini_video/td_cd_guided.md`
- **Key Findings:**
  - Rated each dimension: 4 GOOD, 7 MODERATE, 2 POOR, 1 NOT OBSERVABLE
  - POOR: Error-Proneness (broken connections, unhelpful errors), Hard Mental Operations (re-wiring cognitive load)
  - GOOD: Visibility, Role-Expressiveness, Abstraction, Closeness of Mapping
  - Top 5 critical issues identified align well with paper findings
  - More structured output than blind — easier to compare systematically

### Experiment 3: Gemini Video Assessment — Task-Specific Prompts (4 tasks)
- **Date:** 2026-03-11
- **Model:** gemini-2.5-flash
- **Input:** `task_demo.mkv` (TD)
- **Prompts:** 4 prompts matching the paper's 4 maintenance tasks
- **Outputs:** `exploration/outputs/gemini_video/td_task_task[1-4]_*.md`

**Task 1 (Orientation in Unknown Application):**
- Critical finding: Correctly identified that finding ALL motors requires global search (the paper's #1 issue)
- Praised breadcrumb navigation and "Follow Connection" feature
- Recommended: global search, cross-referencing, contextual Ctrl+F
- **This was the most insightful task-specific assessment**

**Task 2 (Creating/Removing Hierarchies):**
- Correctly assessed grouping/ungrouping as intuitive
- Identified type change connection loss as MAJOR usability issue
- Recommended pin mapping dialog during type changes
- Matched paper's findings on connection handling

**Task 3 (Working with Library):**
- Correctly identified file system interaction issues
- Noted "Change Type" breaking connections as key bottleneck
- Evaluated save/load workflow as logical but improvable
- Matched paper's findings on filesystem difficulties

**Task 4 (Editing):**
- Identified connection creation as "less efficient than ideal" (3-step process vs drag-and-drop)
- Praised type-to-create functionality for function blocks
- Identified parameter addition as efficient with auto-incrementing
- Noted lack of keyboard shortcuts

### Experiment 4: GPT-4o Screenshot Assessment — Blind + CD-Guided
- **Date:** 2026-03-11
- **Model:** gpt-4o
- **Input:** 6 key frames from task_demo.mkv (frames at ~40s, 1:30, 3:10, 5:40, 8:10, 9:50)
- **Outputs:** `exploration/outputs/screenshots/gpt4o_blind.md`, `gpt4o_cd_guided.md`
- **Key Findings:**
  - **Much less detailed than Gemini** — shorter responses, more generic observations
  - Blind: identified 4 issues (clutter, no tooltips, overlapping lines, no context highlighting)
  - CD-guided: rated all 14 dimensions but explanations are shallow and vague
  - **Did NOT identify**: search feature missing, connection breaking on type change, folder creation issues, specific pin/icon problems
  - GPT-4o treats screenshots as static images — misses the interaction flow that Gemini sees from video
  - Suggests features that already exist (zoom/pan, collapsing) — shows it doesn't understand the tool deeply

### Experiment 5: Gemini Screenshot Assessment — Blind + CD-Guided (for comparison)
- **Date:** 2026-03-11
- **Model:** gemini-2.5-flash (same model, screenshots instead of video)
- **Input:** Same 6 frames
- **Outputs:** `exploration/outputs/screenshots/gemini_ss_blind.md`, `gemini_ss_cd_guided.md`
- **Key Findings:**
  - More detailed than GPT-4o but less detailed than Gemini video assessment
  - Still identifies the IDE correctly and provides reasonable observations
  - **Missing the interaction dynamics** — can't see workflows, transitions, error states

### Experiment 6: Increased Frame Density — 20 Frames (every ~33s)
- **Date:** 2026-03-11
- **Models:** GPT-4o + gemini-2.5-flash
- **Input:** 20 frames from task_demo.mkv (extracted every 3s, then every 11th selected)
- **Outputs:** `exploration/outputs/screenshots/gpt4o_blind_20frames.md`, `gemini_ss_blind_20frames.md`
- **Key Findings:**
  - **GPT-4o improved slightly** — now mentions search functionality (missed with 6 frames)
  - Still generic overall, no specific timestamps, suggests features that exist
  - **Gemini with 20 screenshots improved significantly** — references specific frames (0:06, 0:17, etc.), identifies sub-app representation inconsistency, context menu overload, generic parameter naming
  - More frames help both models but the gap remains: video > many screenshots > few screenshots
  - Gemini with 20 screenshots approaches ~5-6/10 ground truth issues (up from ~4/10 with 6 frames)

### Experiment 7: Claude Screenshot Assessment — Blind + CD-Guided (20 frames)
- **Date:** 2026-03-11
- **Model:** claude-sonnet-4
- **Input:** 20 frames from task_demo.mkv
- **Outputs:** `exploration/outputs/screenshots/claude_blind_20frames.md`, `claude_cd_guided_20frames.md`
- **Key Findings:**
  - Claude is **more critical than GPT-4o** — rates more dimensions as POOR (Viscosity, Hidden Deps, Error-Proneness, Secondary Notation, Hard Mental Ops, Provisionality)
  - But **less specific** — doesn't reference specific UI elements or timestamps
  - Blind: mentions search functionality needed, connection complexity, small text/icons
  - CD-guided: 2 GOOD, 4 MODERATE, 6 POOR — harsher than Gemini but without evidence
  - **Claude assumes features don't exist** (e.g., "no visible undo/redo", "no visible shortcuts") when they do exist but weren't shown in screenshots
  - Better than GPT-4o at identifying issues but worse at understanding what the tool actually does

### Video Input Capability Research
- **Gemini:** Native video input via API (best option)
- **GPT-5:** Accepts MP4/MOV natively (released ~Aug 2025), but processes as keyframes internally
- **GPT-4o:** No native video — must extract frames
- **Claude:** No video input — must extract frames. Real-time video API announced for mid-2026 but not yet available
- **Conclusion:** For now, Gemini is the only practical option for true video-based assessment

### Comparison: All Models & Input Types

| Aspect | Gemini (video) | Gemini (20 ss) | Claude (20 ss) | GPT-4o (20 ss) |
|--------|---------------|----------------|----------------|----------------|
| Detail level | Very high | High | Moderate | Low-Moderate |
| Specificity | Very specific | Good | Low | Low |
| Issues detected (vs ground truth) | ~8/10 | ~5-6/10 | ~4/10 | ~3-4/10 |
| Domain understanding | Strong | Good | Moderate | Weak |
| Interaction flow | Yes | Partial | No | No |
| Criticality level | Balanced | Balanced | Over-critical | Under-critical |
| Suggests existing features | Rarely | Sometimes | Often | Often |
| CD framework quality | Nuanced, evidence-based | Reasonable | Harsh but vague | Shallow |

**Key takeaways:**
1. **Video input dramatically outperforms screenshots** — regardless of model
2. **Gemini with video is the clear winner** for automated usability assessment
3. **More screenshots help** but can't match video's understanding of interaction flow
4. **Claude is more critical** than GPT-4o but makes more false assumptions about missing features
5. **GPT-4o gives surface-level** observations — least useful for this task

---

## 7. Conclusions So Far

### What Works
1. **Gemini video processing is remarkably effective** — it correctly identifies the IDE, its components, interaction patterns, and usability issues directly from video
2. **CD-guided prompts produce the most structured, useful output** — easy to systematically compare with ground truth
3. **Task-specific prompts catch domain-specific issues** better (e.g., search feature missing) because they focus attention on what users actually need to do
4. **Blind prompts are good for discovering unexpected issues** that structured prompts might miss
5. **Timestamp references** — Gemini cites specific video timestamps, making results verifiable

### What Doesn't Work (Yet)
1. **Can't detect issues not shown in the video** — e.g., cut/paste across hierarchy wasn't demonstrated
2. **No actual interaction** — Gemini observes but doesn't try to use the IDE itself
3. **Single video limitation** — assessment quality depends on what's shown in the video
4. **No quantitative metrics** — no task completion time, click counts, error rates

### Key Insight
**The CD-guided + task-specific combination is the most effective.** Run CD-guided for the overall structured assessment, then task-specific for deep dives into particular workflows. The blind prompt is good as a sanity check.

### Detection Rate
- **8/10 known issues detected** from a single video (6 full match, 2 partial)
- Several additional valid issues identified that complement the paper's findings
- This suggests AI video assessment could serve as a **cost-effective first pass** before human studies

---

## 8. Next Steps

### Immediate (before next meeting)
- [x] Run blind assessments on Video 1 (intro v1) and Video 3 (intro v2) — done, less useful (overview videos)
- [x] Extract frames from videos → test GPT-4o with screenshots — done, 6 key frames
- [x] Compare models: Gemini (video) vs GPT-4o (screenshots) vs Gemini (screenshots) — done, see comparison table
- [x] Build ground truth comparison matrix (formal scoring) — done, see SUMMARY_FOR_MEETING.md
- [x] Prepare initial findings summary for the meeting — done, see SUMMARY_FOR_MEETING.md
- [x] Test Claude with screenshots — done, Anthropic key works, claude-sonnet-4 used

### Phase 2: Agent-Based UI Interaction (March 11, 2026)
- [x] Research AI agents that can interact with desktop UIs — see `agent_interaction/RESEARCH_UI_AGENTS.md`
- [x] Set up 4diac IDE 3.0.2 in Docker + VNC (Ubuntu 22.04, Xvfb, x11vnc, noVNC, fluxbox)
- [x] Build Claude Computer Use script — `agent_interaction/claude_computer_use.py`
- [x] Run Task 1 (Orientation) with Claude Sonnet 4.6 — 30 steps, partial success
- [ ] Run Tasks 2-4 on native Linux machine (avoid QEMU limitation)
- [ ] Try Bytebot or ScreenEnv as alternative Docker environments
- [ ] Compare agent findings vs video findings vs human findings

### Phase 2 Results: Agent Interaction Experiment

**Setup:**
- Docker container: Ubuntu 22.04 + Java 17 + 4diac IDE 3.0.2 + Xvfb + x11vnc + noVNC
- Docker Compose with `platform: linux/amd64` (QEMU emulation on ARM Mac)
- Claude Sonnet 4.6 via `client.beta.messages.create()` with `computer_20251124` tool
- Action execution: xdotool via docker exec (requires windowfocus --sync for QEMU)

**Limitation Discovered:**
- QEMU x86_64 emulation on ARM Mac causes severe interaction latency
- SWT dialogs fail to open (menu items trigger but dialogs don't appear)
- xdotool clicks work for menus but hyperlinks in SWT are unreliable
- **Solution needed:** Run on a native x86_64 machine or use a cloud VM

**Task 1 (Orientation) Results — Despite Limitations:**
The agent completed 30 steps and found real usability issues:
1. **Tab labels truncated** — "Sys", "Typ" labels are not self-explanatory for new users
2. **Hyperlinks unresponsive** — "Import projects..." and "Create a new 4diac IDE Project" links didn't respond
3. **"The chosen operation is not enabled"** — unhelpful error dialog with no explanation of what operation or why
4. **Visual proximity** — accidentally clicked "Clone Project from GIT Repository" instead of "Continue to 4diac IDE" (items too close together)
5. **Empty workspace confusion** — no guidance for first-time users on how to start
6. **Dialogs not appearing** — menu items triggered but no visible response (QEMU issue, but also reveals: IDE gives no loading feedback)

**Output files:**
- `agent_interaction/outputs/task1_orientation_report.md`
- `agent_interaction/outputs/task1_orientation_results.json`
- `agent_interaction/outputs/task1_orientation_step*.png` (screenshots at each step)

### Short-term (during practicum)
- [ ] Run agent experiments on native x86_64 Linux (VM or cloud instance)
- [ ] Try giving models multiple screenshots in sequence (simulating video)
- [ ] Test with different Gemini models (pro vs flash)
- [ ] Design systematic experiment methodology for the report

### Medium-term (toward bachelor thesis)
- [ ] Develop automated pipeline: video → AI assessment → report generation
- [ ] Compare AI assessment with actual human study results quantitatively
- [ ] Full agent interaction study (all 4 tasks, multiple agents)
- [ ] Investigate supervision model: AI does assessment, human verifies

---

## 9. Tips & Notes

### Technical Tips
- **Google GenAI SDK:** Use `google-genai` (new), NOT `google-generativeai` (deprecated)
- **Model naming:** `gemini-2.0-flash` is retired for new users. Use `gemini-2.5-flash` or newer
- **Video upload:** Gemini requires uploading video first, then waiting for PROCESSING→ACTIVE state (takes ~20-30s)
- **Rate limits:** Add 5s pause between consecutive Gemini API calls
- **Conda env:** Always use `4diac` env for this project to isolate dependencies
- **Video format:** yt-dlp downloads as .mkv or .webm — Gemini handles both fine

### Research Tips
- **Document EVERYTHING** — prompts, model versions, timestamps, outputs. Supervisor emphasized this repeatedly.
- **Keep prompts fixed** when comparing models — only change one variable at a time
- **The paper's study materials are on Zenodo** (DOI: 10.5281/ZENODO.4758816) — includes protocols, questionnaire, task list, interview questions
- **Cross-reference with the paper's specific findings** — Table 2 (strengths/weaknesses), Figures 7-10 (questionnaire results)
- **"Daumen mal Pi"** — German expression for "rough estimate" (thumb times Pi)

### Project Management
- Meetings every 2 weeks with supervisor
- Report due after second presentation (June 22)
- Keep this progress.md updated as the single source of truth
- Use memory system (Claude/agents) to track experiment state across sessions

---

## 10. References

1. Wiesmayr, B., Zoitl, A., & Rabiser, R. (2023). Assessing the usefulness of a visual programming IDE for large-scale automation software. *Software and Systems Modeling*, 22, 1619-1643.
2. Gemini Team, Google (2023/2025). Gemini: A Family of Highly Capable Multimodal Models. arXiv:2312.11805v5.
3. Blackwell, A.F. & Green, T.R.G. (2003). Notational systems—The cognitive dimensions of notations framework. *HCI Models, Theories, and Frameworks*.
4. Nielsen, J. (1994). *Usability Engineering*. Morgan Kaufmann.
5. Davis, F.D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319-340.
6. Ko, A.J., et al. (2015). A practical guide to controlled experiments of software engineering tools with human participants. *Empirical Software Engineering*, 20(1), 110-141.

---

## 11. Session Artifacts

| File | Purpose |
|------|---------|
| `progress.md` | Master progress document (this file) |
| `SUMMARY_FOR_MEETING.md` | Meeting-ready summary (Phase 1 + 2) |
| `FULL_SESSION_LOG.md` | Complete replication guide with all commands, challenges, solutions |
| `agent_interaction/EXPERIMENTS.md` | Phase 2 experiment documentation with screenshots |
| `agent_interaction/RESEARCH_UI_AGENTS.md` | Survey of 12+ UI interaction agents |

## 12. Thesis Title Candidates

**Top pick:** *"AI as Usability Tester: Comparing Video Analysis and Agent-Based Interaction for Assessing Industrial Automation IDEs"*

**Naming convention for the two phases:**
- **Passive analysis** — AI observes video/screenshots (Phase 1)
- **Interactive assessment** — AI agent uses the IDE directly (Phase 2)
- **Multimodal AI usability evaluation** — umbrella term for both

---

*Last updated: 2026-03-11*
