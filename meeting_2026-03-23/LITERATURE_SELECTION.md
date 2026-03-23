# Literature Selection — Most Relevant Papers for Video-Based Usability Assessment

## Selection Criteria

Priority: **Video as primary input** for AI-based usability assessment. The core workflow is:
1. A user (expert or beginner) records themselves using the IDE
2. AI model watches the video and produces a usability report
3. Results are compared against human study ground truth

Secondary: Agent-based interaction (Phase 2) and general LLM-as-evaluator methodology.

---

## Tier 1: MUST READ — Directly matches your video-first methodology

### 1. UXAgent (2025)
**"UXAgent: A System for Simulating Usability Testing of Web Design with LLM Agents"**
- arXiv / industry paper, 2025

**Why it's essential:**
This is the closest existing system to what you built. UXAgent simulates usability testing with LLM agents AND includes a **Video Replay interface** for reviewing agent sessions — nearly identical to your Phase 1 (video review) + Phase 2 (agent interaction) combination.

**What to cite it for:**
- Justifying the "simulated user + video review" methodology
- Their persona generator approach (you could extend: test with "novice automation engineer" vs "expert" personas)
- Their qualitative/quantitative log format matches your action log + report output

---

### 2. UXCascade (2026)
**"UXCascade: Scalable Usability Testing with Simulated User Agents"**
- arXiv, 2026

**Why it's essential:**
Extends UXAgent with a multi-level analysis workflow: aggregate agent traces → link reasoning to issues → support iterative improvements. This is exactly the "many agent runs → structured findings" pipeline you need for scaling.

**What to cite it for:**
- How to structure analysis when you have multiple agent runs / multiple videos
- Their aggregation methodology (pattern detection across runs)
- Justifying scalability claims ("run assessment on every IDE release")

---

### 3. LLM-powered Multimodal Insight Summarization for UX Testing (2024)
**ACM, 2024**

**Why it's essential:**
Directly addresses your core task: using LLMs to generate insights from **multimodal UX testing data** — connecting what users **did** (actions) with what they **said** (think-aloud). Your new_a and new_b videos have both visual actions AND verbal commentary.

**What to cite it for:**
- Theoretical grounding for "video + audio → usability insights" pipeline
- Their evidence-linking methodology (connecting observed behavior to issues)
- Bridging the gap between session recording and actionable findings

---

### 4. VideoWebArena (2025)
**"VideoWebArena: Evaluating Long-Context Multimodal Agents with Video Understanding Web Tasks"**
- ICLR, 2025

**Why it's essential:**
The strongest benchmark proof that **temporal context in video materially changes AI performance**. Your core finding (video >> screenshots) is directly supported by this paper's results.

**What to cite it for:**
- Academic backing for your key result: "video input dramatically outperforms screenshots"
- Their "skill retention" and "factual retention" metrics for video understanding
- Methodology for evaluating long-context video comprehension

---

### 5. SoSyM 2023 — Wiesmayr, Zoitl, Rabiser
**"Assessing the usefulness of a visual programming IDE for large-scale automation software"**
- Software and Systems Modeling, 2023

**Why it's essential:**
Your ground truth. Everything compares against this paper's 10 issues, 14 CD dimensions, and 4 tasks.

**What to cite it for:**
- Ground truth methodology (CD walkthrough + user study + reassessment)
- The specific usability issues you're trying to detect
- Framing your work as "automating what they did manually"

---

### 6. Cognitive Dimensions of Notations Framework (2003)
**Blackwell & Green — Book chapter (public PDF)**

**Why it's essential:**
Your entire CD-guided prompting strategy is a direct operationalization of this framework. It's what makes your prompts theory-driven rather than ad-hoc.

**What to cite it for:**
- Theoretical foundation for structured prompting
- Why CD produces better results than blind prompts (your own experiments prove this)
- The trade-off reasoning that prevents generic "add feature X" suggestions

---

## Tier 2: SHOULD READ — Supports specific claims in your report

### 7. CHI 2024 — "Generating Automatic Feedback on UI Mockups with Large Language Models"
**Why:** Closest "LLM as heuristic evaluator" paper. Shows LLMs can produce useful UI feedback but with limitations (generic critiques, decreasing usefulness over iterations). Your experiments confirm the same pattern — screenshot-based models suggest features that already exist.

**Cite for:** LLM critique quality discussion, comparison of your approach vs static mockup evaluation.

---

### 8. UICrit (2024, UIST)
**"UICrit: Enhancing Automated Design Evaluation with a UI Critique Dataset"**
- 3,059 critiques on 983 mobile UIs

**Why:** Shows that LLM critique quality can be **improved systematically** through better prompting and few-shot strategies. Your CD-guided vs blind comparison is exactly this kind of improvement.

**Cite for:** How structured prompting improves critique quality (your CD-guided results are evidence of this).

---

### 9. SeeAct (2024)
**"GPT-4V is a Generalist Web Agent, if Grounded"**

**Why:** Their central finding — "performance is high under oracle grounding, but grounding is the bottleneck" — directly explains your Phase 2 agent results. The agent "knows" what to click but struggles to land on the correct pixel.

**Cite for:** Explaining the coordinate calibration issue in your Windows experiments (menu misclicks), framing grounding as the key challenge for agent-based assessment.

---

### 10. OSWorld (2024, NeurIPS)
**369 real desktop tasks with execution-based evaluation**

**Why:** The closest desktop agent benchmark to your Phase 2. Provides methodology for how to evaluate agent task completion on real desktop applications.

**Cite for:** Framing your Docker + 4diac IDE setup as an "IDE-specific OSWorld-style benchmark," justifying step budgets, reporting success/failure rates.

---

### 11. WorldGUI (2025)
**"Tests desktop GUI automation from any starting point"**

**Why:** Directly addresses your biggest Phase 2 validity threat: **starting state matters**. Your QEMU issues, Welcome tab blocking, and empty workspace are all instances of initial-state sensitivity.

**Cite for:** Framing your QEMU/environment issues as a recognized research problem (not just an engineering bug), justifying state-variation testing.

---

### 12. Online-Mind2Web / "An Illusion of Progress?" (2025)
**"Assessing the Current State of Web Agents"**

**Why:** Critiques over-optimistic agent evaluation results. Their LLM-as-judge reaches ~85% agreement with humans. Directly relevant to: "how do we know the AI's usability assessment is accurate?"

**Cite for:** Evaluation validity, why naive metrics mislead, how to use LLM-as-judge responsibly.

---

## Tier 3: NICE TO HAVE — For bachelor thesis depth

| # | Paper | Why |
|---|-------|-----|
| 13 | **Windows Agent Arena** (2024) | Reports human 74.5% vs best agent 19.5% — proves desktop agents are still fragile |
| 14 | **ScreenAI** (2024) | UI-specialized vision model — could improve screenshot parsing |
| 15 | **Qwen2.5-VL** (open model) | Open-source video-capable model — reproducibility baseline |
| 16 | **GUI-360** (2025) | Separates perception quality from planning quality — useful framework |
| 17 | **WebArena** (2023) | Reproducible web agent evaluation — methodology template |
| 18 | **Mind2Web** (2023) | Task collection from real interfaces — precedent for your task design |

---

## How to Use This in Your Report

### For Practicum (10-20 pages)
Cite: **Papers 1-6** (Tier 1) + **Papers 7, 10** from Tier 2
- Position your work as: "We implement the first video-first, CD-guided AI usability assessment for an industrial IDE, validated against a published human study"

### For Seminar Presentation (5 min)
Cite: **Papers 1, 4, 5, 6** only
- Key message: "UXAgent showed simulated testing works for web; VideoWebArena proved video > screenshots; we applied this to a real industrial IDE using CD framework"

### For Bachelor Thesis (30-50 pages)
Cite: **All 18 papers**
- Add the full benchmark landscape (Tier 3) for a comprehensive related work section
- Position contribution as: bridging LLM UI critique + simulated usability testing + desktop agent benchmarks, applied to industrial automation IDEs

---

## Reading Order

1. **SoSyM 2023** (you've read it) — refresh the methodology sections
2. **UXAgent** — most similar system, understand their architecture
3. **VideoWebArena** — backs your "video >> screenshots" finding
4. **LLM Multimodal Insight Summarization** — theoretical grounding for video analysis
5. **UXCascade** — scaling methodology
6. **CD Framework chapter** — re-read the trade-off reasoning sections
7. **CHI 2024 UI Mockup Feedback** — understand LLM critique limitations
8. **SeeAct** — grounding problem framing
9. **OSWorld** — agent evaluation methodology
10. **Online-Mind2Web** — evaluation validity concerns
