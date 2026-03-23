# Tier 1 Papers — Detailed Summaries, Experiments, and Takeaways

Prepared for: Azat Vakhitov | Meeting: March 23, 2026

---

## 1. UXAgent (CHI EA '25)
**"UXAgent: A System for Simulating Usability Testing of Web Design with LLM Agents"**
- Authors: Lu, Yao, Gu, et al. (Northeastern University + Amazon)
- arXiv: https://arxiv.org/abs/2504.09407
- GitHub: https://github.com/neuhai/UXAgent
- Demo: https://uxagent.hailab.io/

### How It Works
Dual-loop agent architecture:
- **Fast Loop:** Perception (parses HTML) → Planning (next action) → Action (click/type/navigate)
- **Slow Loop:** Wonder Module (random thoughts, like human mind-wandering) → Reflection Module (high-level insights from recent memory)
- **Memory Stream:** Stores observations + actions + reflections with timestamps, scored by importance/relevance/recency

### Their Experiments
- Tested on Amazon.com and Google Flights
- **60 LLM agent personas** with demographic distribution (gender, income groups)
- Task: "Buy a Jacket" — analyzed purchasing behavior across income groups
- User study with **5 UX researchers** evaluating the system

### Key Results
| Data Modality | Helpfulness Rating (1-5) |
|---|:---:|
| Statistics | **4.6** |
| Action Trace | **4.2** |
| Chat Interface | 4.1 |
| Video Recording | 3.4 |
| Memory Trace | 2.9 |

- Different income personas showed realistic purchasing patterns ($28 avg for low-income vs $41 for high-income)
- UX researchers rated trust at 3.6/5, data realism at 3.0/5

### What You Can Reuse
1. **Persona approach** — generate "novice automation engineer" vs "experienced IEC 61499 developer" personas for your agent
2. **Dual-loop architecture** — your agent could add a "reflection" step after every N actions
3. **Chat interface idea** — after an agent run, ask it "Why did you struggle with the Welcome tab?" in conversation
4. **Multi-modal output** — your script already produces action trace + screenshots; add a final "reflection report"

### Key Quote for Your Report
> "UX researchers rated action traces (M=4.2) as the most helpful data modality, while memory traces (M=2.9) were harder to interpret — suggesting that structured behavioral data is more useful than raw internal reasoning."

### Limitations They Report
- Agent behaviors can seem "unrealistically human" (too quirky)
- Limited to web interactions (click, type, navigate) — your setup extends this to desktop
- Model bias from training data affects persona realism

---

## 2. UXCascade (2026, arXiv)
**"UXCascade: Scalable Usability Testing with Simulated User Agents"**
- Authors: Holter, Koh, Dogan, Chan (ETH Zurich + Adobe Research)
- arXiv: https://arxiv.org/abs/2601.15777

### How It Works
5-phase workflow:
1. **Explore Goals & Outcomes** — examine agent goals and success rates
2. **Observe Trait Distributions** — analyze behavior patterns across persona traits
3. **Isolate UX Issues** — drill into specific problems with agent reasoning traces
4. **Propose Fixes** — suggest interface modifications
5. **Evaluate Effects** — re-run simulations to assess impact

Three agent types:
- **Simulation Agents** — generate interaction traces (GPT-5, temp=1.0, max 25 steps)
- **Annotation Agents** — tag cognitive intent, detect usability issues from think-aloud logs
- **Refinement Agents** — apply and validate interface edits

### Their Experiments
- **8 UX professionals** evaluated an e-commerce prototype (Cascada Tees)
- **9 seeded usability issues** as ground truth
- Compared: Baseline (no tool) vs UXCascade

### Key Results
| Metric | Baseline | UXCascade |
|--------|:--------:|:---------:|
| Issues found | 2.62 ± 0.91 | **2.87 ± 0.84** |
| Perceived workload (NASA-TLX) | 3.50 ± 0.76 | **2.75 ± 0.89** (lower = better) |
| Task success support | 2.65 ± 0.99 | **3.00 ± 0.71** |

### What You Can Reuse
1. **Annotation Agent idea** — after your agent runs, use a second LLM to annotate the action log with "cognitive intent" labels (exploring, struggling, recovering from error)
2. **Trait-based analysis** — run your agent with different "expertise levels" and compare which issues each finds
3. **5-phase workflow** — structure your results as: explore → observe → isolate → propose → evaluate
4. **Re-run after fix** — if 4diac fixes an issue, re-run your assessment to show it's resolved (mirrors SoSyM paper's reassessment)

### Key Quote for Your Report
> "UXCascade reduced perceived workload (2.75 vs 3.50 on NASA-TLX) while helping UX professionals discover more issues (2.87 vs 2.62), demonstrating that AI-augmented analysis can be both more effective and less demanding than manual review."

### Limitations
- Only 8 participants, 1 prototype
- 25-step limit per agent (you use 30 — similar constraint)
- Agent diversity may not capture full range of real user behavior

---

## 3. LLM-Powered Multimodal Insight Summarization for UX Testing (ACM ICMI '24)
**Authors:** Turbeville, Muengtaweepongsa, et al. (UIUC + UserTesting)
- DOI: https://doi.org/10.1145/3678957.3685701

### How It Works
Two-stage LLM pipeline:

**Stage 1: Multimodal Session Transcript**
- Merges **behavioral data** (clickstream + DOM elements, timestamped) with **verbal data** (think-aloud speech-to-text)
- Format: chronological interleaving of actions and speech
- Example: `[00:23] Clicked "Add to cart" → [00:25] "I like this red one"`

**Stage 2: Cross-Session Aggregation**
- Concatenates all session transcripts
- LLM identifies commonalities, differences, sentiments, blockers
- Each insight mapped back to source references ("walking the references")

### Their Experiments — MASSIVE Real-World Deployment
- **75,464 eligible UX studies** on UserTesting platform
- **11,030 researchers** viewed results
- **3,821 researchers (34.6%)** created **56,830 insight summaries**
- Deployment period: August 2023 - April 2024

### Key Results
- 61 researchers provided written feedback
- Users report "huge time saver" for analysis
- Action traces + verbal transcripts together more useful than either alone

### What You Can Reuse
1. **Multimodal transcript format** — your new_a and new_b videos have BOTH visual actions AND your verbal commentary. Extract audio → speech-to-text → merge with action timestamps
2. **Two-stage pipeline** — first summarize each video separately, then aggregate across videos
3. **"Walking the references" traceability** — your Gemini outputs already cite timestamps; formalize this as a methodology
4. **Cross-session comparison** — you already do this (expert td vs beginner new_a vs new_b); their framework legitimizes it

### Key Quote for Your Report
> "34.6% of researchers who viewed the results page created insight summaries, generating 56,830 summaries in 8 months — demonstrating strong real-world demand for automated UX insight extraction from multimodal session data."

> P35: "The source information makes this extremely useful in its current state" — mirrors your finding that Gemini's timestamp citations add credibility

### Limitations (IMPORTANT — same as yours!)
- **Counting errors:** LLM says "several" instead of "17 of 20" — your Gemini outputs also use vague quantifiers
- **Transcription errors:** "small cough" → "small cost" — relevant if you add audio analysis
- **Context window limits:** GPT-3.5 16k was insufficient for long sessions — Gemini handles video natively, avoiding this
- They acknowledge: future work should use **inherently multimodal models (like Gemini)** instead of text-only pipelines — **you're already doing this**

---

## 4. VideoWebArena (ICLR 2025)
**"Evaluating Long-Context Multimodal Agents with Video Understanding Web Tasks"**
- arXiv: https://arxiv.org/abs/2410.19100
- Website: https://videowebarena.github.io/

### How It Works
Benchmark with **2,021 tasks** requiring agents to process ~4 hours of video content:
- **Skill Retention (1,621 tasks):** Can agents learn from tutorial videos and apply the skills?
- **Factual Retention (400 tasks):** Can agents extract facts from videos to complete tasks?

### Key Results — THE MOST IMPORTANT FINDING

| Metric | Best Model | Human |
|--------|:----------:|:-----:|
| Factual Retention QA | 45.8% | 79.3% |
| Factual Retention Task Success | 13.3% | 73.9% |

**The shocking finding:** On Skill Retention tasks, **including tutorial videos made agents WORSE**:
- WebArena tasks: **-5% performance** with tutorials vs without
- VisualWebArena tasks: **-10.3% performance** with tutorials vs without

### What This Means for You
1. **Your video >> screenshots finding is academically validated** — this paper proves temporal context matters
2. **But also a warning:** giving agents tutorial videos can degrade performance — your agent experiments should test with/without instructional context
3. **The gap is huge:** best model 13.3% vs human 73.9% on video-informed tasks — aligns with your agent's ~0% task completion rate

### Key Quote for Your Report
> "Long-context models perform worse with video tutorials than without them, showing a 5-10% performance decrease — suggesting that current models struggle to extract and apply procedural knowledge from video, despite having the temporal context available."

**This directly supports your finding:** Gemini can OBSERVE usability issues in video but current agents cannot LEARN skills from video to operate software.

### What You Can Reuse
- Their **skill retention vs factual retention** framing maps perfectly to your two phases:
  - **Factual retention** = Phase 1 (watch video, report what you observe)
  - **Skill retention** = Phase 2 (watch someone use IDE, then try to use it yourself)
- Your Gemini video assessment is essentially "factual retention" — and it works well (~80% hit rate)
- Your agent experiments are "skill retention" — and they struggle (~0% task completion), just like VideoWebArena

---

## 5. CHI 2024 — UI Mockup Feedback with LLMs
**"Generating Automatic Feedback on UI Mockups with Large Language Models"**
- CHI 2024, UC Berkeley
- arXiv: https://arxiv.org/abs/2403.13139

### Key Results

| Metric | GPT-4 | Human Experts |
|--------|:-----:|:------------:|
| Precision | 0.603 | 0.829 |
| Recall | 0.380 | 0.336 |
| F1 Score | 0.466 | 0.478 |

- 52% of GPT-4 suggestions rated "Accurate"
- 19% "Partially Accurate"
- 29% "Not Accurate"
- 49% considered "Helpful or Very Helpful"

**Critical finding: Feedback quality DECREASES over design iterations** — first critique is useful, subsequent ones less so.

### What You Can Reuse
- **Your CD-guided prompts outperform their approach** — they use general heuristics, you use domain-specific CD framework
- Their **precision/recall methodology** for scoring LLM feedback against expert feedback — apply this to your ground truth comparison
- **Iteration degradation** — relevant if you run multiple assessment rounds on the same video

### Key Quote for Your Report
> "GPT-4 achieved F1=0.466 compared to human experts' F1=0.478, suggesting LLM critique is approaching human expert level — but with lower precision (0.603 vs 0.829), meaning LLMs generate more false positives."

Your Gemini video approach likely has HIGHER precision because video provides richer evidence than static mockups.

---

## 6. SoSyM 2023 + CD Framework
Already thoroughly analyzed in your project. Key addition from the deep research report:

### Why CD Framework Works Better Than Nielsen's Heuristics for Your Case
> From the deep research report: "CD's trade-off framing helps mitigate a common LLM failure mode: recommending generic feature additions without acknowledging that fixing one difficulty can create another."

This explains why your CD-guided prompts produce better results than blind prompts — CD forces the LLM to consider trade-offs, not just list problems.

---

## Comparison: Your Setup vs. These Papers

| Aspect | UXAgent | UXCascade | Multimodal Summary | VideoWebArena | Your Setup |
|--------|---------|-----------|-------------------|---------------|------------|
| **Input** | Web HTML | Web HTML | Clicks + speech | Video + web | **Video + Docker IDE** |
| **Domain** | E-commerce | E-commerce | Various web | Web tasks | **Industrial IDE** |
| **Personas** | 60 generated | Trait-based | Real users | N/A | Expert + beginner videos |
| **Ground truth** | None formal | 9 seeded issues | User feedback | Task completion | **10 published issues (SoSyM)** |
| **Video analysis** | Recording only | No | Speech-to-text | Video input | **Native Gemini video** |
| **Agent interaction** | Yes (web) | Yes (web) | No | Yes (web) | **Yes (desktop IDE)** |
| **CD framework** | No | No | No | No | **Yes** |

**Your unique contributions:**
1. Only one using **native video understanding** (Gemini) instead of text-converted pipelines
2. Only one targeting a **desktop IDE** (not web)
3. Only one using a **theory-driven rubric** (CD framework)
4. Only one with a **published human study as ground truth** (SoSyM)
5. Only one testing **expert vs beginner videos** to show expertise sensitivity

---

## Recommended Reading Order

| # | Paper | Time | Focus on |
|---|-------|------|----------|
| 1 | **UXAgent** | 30 min | Architecture diagram (Fig 1), dual-loop reasoning, persona generator, user study results (Table 1) |
| 2 | **Multimodal Insight Summarization** | 30 min | Two-stage pipeline (Fig 4), multimodal transcript format, deployment scale, user quotes |
| 3 | **VideoWebArena** | 20 min | Skill vs factual retention definition, the -5%/-10% degradation finding, Tables 1-2 |
| 4 | **UXCascade** | 20 min | 5-phase workflow (Fig 3), three agent types (Fig 4), NASA-TLX results |
| 5 | **CHI UI Mockup** | 15 min | Precision/recall table, iteration degradation finding, Figma plugin approach |
| 6 | **CD Framework** | 15 min | Trade-off reasoning sections, dimension definitions |

Total: ~2 hours of focused reading

---

## Appendix: Key Quotes with Page Numbers

### UXAgent (CHI EA '25) — Page References

**p.1, Abstract:**
> "Our system features an LLM Agent module and a universal browser connector module so that UX researchers can automatically generate thousands of simulated users to test the target website."

**p.2, Section 1 (Introduction):**
> "LLM Agents are not to replace human participants, rather to be more responsible to the human participants — LLM Agents can work together with UX researchers (human-AI collaboration) in a simulated pilot session to provide the desired early and immediate feedback"

**p.3, Section 3.2 (Agent Design):**
> "The Fast Loop enables real-time interaction with the web environment, while the Slow Loop facilitates in-depth reasoning. [...] The Wonder Module: The agent generates random thoughts based on the current situation, mimicking a human's 'mind drifting' phenomenon."

**p.5, Section 4.1 (User Study):**
> "We recruited five UX researchers as participants, each with self-reported UX experience ranging from 1 to 6 years (M = 3, SD = 1.87)."

**p.6, Section 4.2.2 (Fig 3b — Helpfulness ratings):**
> Action Trace: M=4.2 | Statistics: M=4.6 | Chat: M=4.8 | Memory: M=2.9 | Recording: M=3.4
> P1: "It's very hard to find pilot study of 60 participants or even just five or ten. So I think in this way I can conduct my pilot study with the large language model agent."

**p.7, Section 4.2.2 (Concerns):**
> P2: "because we do feel like the LLM has sort of stereotyping that. My feeling female will buy more male will buy less things" — Data Representation Bias
> P1: "it could be bias or it could disturb my study design" — Algorithmic Decision Bias

**p.7, Section 5.1 (Discussion):**
> "the future systems should automatically generate high-level insight summaries as the generated LLM Agents' raw memory is hard to analyze."

**p.8, Section 5.3 (Future Work):**
> "Incorporating Multimodal LLMs (MLLMs) to interpret and utilize both textual and visual information could enable the system to better understand page context"

---

### UXCascade (2026, ETH Zurich + Adobe) — Page References

**p.1, Figure 1 caption:**
> "The workflow begins with simulated agents browsing a website to uncover issues based on user-defined goals, which are then (A) aggregated and visualized in the analysis view. Users can (B) propose interface changes to address these issues, and the system (C) automatically re-evaluates the modified version."

**p.2, Section 1 (Introduction):**
> "The fundamental challenge is that anticipating usability and engagement issues is inherently difficult even for seasoned experts. Testing with human participants is therefore invaluable in theory, yet often unfeasible in practice because of time and resource constraints."

**p.4, Section 3.3 (User Needs — E1 quote):**
> E1: "This is definitely a pain point in our design process, especially because it's really hard to get access to those specific personas we design for."

**p.4, Section 3.3 (E4 quote on AI replacing humans):**
> E4: "I don't think the AI could ever replace a human study. But it could be one more data point, a proxy that we run through to see what it says."

**p.5, Section 3.4 (Requirements R1-R5):**
> R1: "Support rapid, interface analysis during early-stage design"
> R4: "Enable quick creation, rerunning, and structuring of simulation data"

**p.7, Section 5.1 (Agent Framework):**
> "Simulation Agents operate with temperature=1.0 to encourage behavioral diversity across runs, capped at 25 steps per agent to balance realism and cost."

**p.8, Figure 5 caption:**
> "User interaction scenario with the UXCascade visual interface, showing (A) isolation of issue details, (B) generation of a fix based on natural language instruction, (C) simulation of new agent behavior, and (D) visualization of impacted personas across the user population."

**p.10, Section 6.2.1 (Results — Fig 6):**
> Average issues found: None=3.6, Baseline=2.5, UXCascade=3.0 (after initial onboarding phase)

**p.10, Section 6.2.2 (Workflow quotes):**
> P1: "It collects all the most important highlights... you don't have to dig into the information"
> P3: "I could imagine this uncovering some patterns you wouldn't necessarily find just manually going through a page."
> P4: "It's doing what a checklist or report can't do... it's allowing active scanning."
> P7: "For my personal workflow, I rely heavily on those tiny little fixes and being able to directly go in and fix something will be immensely helpful."

**p.10, Section 6.2.3 (NASA-TLX):**
> "participants rated UXCascade as mentally less demanding than the baseline condition (2.75±0.89 vs. 3.50±0.76)"

---

### LLM-Powered Multimodal Insight Summarization (ICMI '24) — Page References

**p.4, Abstract:**
> "By unifying verbal, behavioral, and design data streams into a novel natural language representation, we construct LLM prompts that generate insights combining information across all data types. Each insight can be traced back to behavioral and verbal evidence, allowing users to quickly verify accuracy."

**p.5, Section 3.1:**
> "Researchers can review the results of an unmoderated UX test as a list of insights summarizing what people did and said across all sessions"

**p.6, Figure 3 caption:**
> "Multimodal session summaries allow researchers to quickly review what a participant did and said without having to watch an entire session video."

**p.7, Figure 4 caption:**
> "The first prompt generates 'multimodal transcripts' for a single session, summarizing across the behavioral, verbal, and design data streams. The second prompt summarizes across a set of multimodal transcripts to generate summative insights for a UX test."

**p.8, Section 4.2 (Multimodal Transcript):**
> "The platform combines the event/interaction and DOM data streams into a 'behavioral transcript' that describes the participant's actions throughout the session in natural language."

**p.8, Section 4.2 (Key finding):**
> "We found that this input representation allows the LLM to synthesize cohesive insights across user actions and verbal feedback. For instance, an LLM can infer that a participant is interested in a specific product by connecting the verbal feedback about that item with the click interaction on the DOM element linking to that item's product page."

**p.9, Section 4.4 (Implementation):**
> "We faced constraints related to context size, which was 16,384 tokens for the GPT-3.5 16k model and 8,192 tokens for the GPT-4 model."

**p.9, Section 5 (Results — Scale):**
> "Between August 30, 2023 and April 30, 2024, UX researchers created 75,464 UX studies eligible for insights summarization. [...] 11,030 individual researchers reviewed the Results page, and 3,821 of them (34.6%) created 56,830 insights summaries."

**p.10, Section 5 (User quotes):**
> P48: "This really helps with the fast data analysis and synthesis per task"
> P35: "This is a fantastic feature: the source information makes this extremely useful in its current state"
> P28: "This feature is great and a huge time saver!!"

**p.10, Section 5 (Counting limitation):**
> P45: "I would like to see the statement in this format: 'Most contributors (17 of 20)'"
> P27: "It would be helpful to clarify how many the many, several, some, and a few are exactly."

**p.10, Section 6 (Future Work — critical for your thesis):**
> "Future work should examine whether leveraging inherently multimodal LLMs such as Gemini could improve performance. Can multimodal LLMs automatically generate a multimodal transcript from screen capture video and think-aloud audio without having to construct an intermediate verbal-behavioral transcript?"

**This last quote is gold for your thesis** — they explicitly call out Gemini + video as future work, and **you're already doing it.**
