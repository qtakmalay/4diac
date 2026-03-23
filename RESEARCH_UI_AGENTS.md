# Research: AI Agents for UI Interaction & Usability Testing

**Date:** March 11, 2026
**Purpose:** Evaluate which AI agents can interact with desktop UIs to perform automated usability assessment of Eclipse 4diac IDE

---

## 1. The Question

Can an AI agent **actually use** the 4diac IDE (click, type, navigate) and report usability issues from first-hand experience — instead of just observing a video?

**Answer: Yes.** Multiple production-ready agents exist. Below is the full landscape.

---

## 2. Major Provider Agents

### Claude Computer Use (Anthropic) — RECOMMENDED
- **Status:** Production-ready (2025+, improved with Opus 4.6 Feb 2026)
- **How it works:** Takes screenshots → reasons about UI → sends mouse/keyboard actions
- **Desktop apps:** Full support
- **Docker/VM:** Yes — designed for containerized environments
- **Benchmark:** 61.4% on OSWorld (up from <15% in late 2024)
- **Cost:** Via Anthropic API (we have the key)
- **Key advantage:** Best documented API, we already have access
- **Acquisition:** Anthropic acquired Vercept (computer use startup, $50M) in Feb 2026

### OpenAI Operator
- **Status:** DEPRECATED (launched Jan 2025, shut down Aug 2025)
- **Replaced by:** ChatGPT "agent mode" — web-focused only
- **Desktop apps:** Limited, primarily web
- **Verdict:** Not viable for our use case

### Google Project Mariner
- **Status:** Limited availability (May 2025+)
- **Access:** Requires Google AI Ultra subscription ($249.99/month)
- **Architecture:** Chrome extension + cloud VM
- **Desktop apps:** Primarily web-based
- **Verdict:** Too expensive, web-focused, not suitable

---

## 3. Open-Source GUI Agents

### Simular Agent S — HIGHEST PERFORMANCE
- **GitHub:** https://github.com/simular-ai/Agent-S
- **Benchmark:** 72.6% on OSWorld — **first agent to exceed human performance** (72.36%)
- **Versions:** Agent S → S2 (March 2025) → S3 (Dec 2025)
- **Innovation:** Behavior Best-of-N (bBoN) — multiple agents vote on best action
- **Desktop apps:** Full support
- **Docker/VM:** Yes
- **Funding:** $21.5M raised
- **Verdict:** Best performance, but more complex to set up than Claude

### UFO2 (Microsoft) — BEST FOR WINDOWS
- **GitHub:** https://github.com/microsoft/UFO
- **Versions:** UFO (Feb 2024) → UFO2 AgentOS (April 2025) → UFO3 Galaxy (Nov 2025)
- **Architecture:** Dual-agent (HostAgent + AppAgents), native OS API integration
- **Desktop apps:** Windows-focused, multi-app workflows
- **Key feature:** Picture-in-Picture for isolated automation
- **License:** MIT (open source)
- **Verdict:** Excellent but Windows-only — our Docker setup is Linux

### CogAgent — OPEN-SOURCE VISION MODEL
- **GitHub:** https://github.com/zai-org/CogAgent
- **Model:** 9B parameter visual language model
- **Resolution:** 1120x1120 (recognizes tiny UI elements)
- **Desktop apps:** Full support
- **Docker/VM:** Yes
- **Product:** GLM-PC desktop agent (Zhipu, launched Jan 2025)
- **Verdict:** Good alternative if we want to run the model locally

### OpenAdapt — LEARNS FROM DEMOS
- **GitHub:** https://github.com/OpenAdaptAI/OpenAdapt
- **Approach:** Records human demonstrations → learns → replays with adaptation
- **Performance:** 100% first-action accuracy on macOS System Settings (vs 46.7% zero-shot)
- **Desktop apps:** Full cross-platform
- **Privacy:** Built-in PII/PHI scrubbing
- **Verdict:** Interesting for learning from existing user study videos

### ShowUI (CVPR 2025) — LIGHTWEIGHT
- **GitHub:** https://github.com/showlab/ShowUI
- **Model:** 2B parameters — very efficient
- **Innovation:** UI-guided visual token selection (33% fewer tokens)
- **Accuracy:** 75.1% zero-shot screenshot grounding
- **Verdict:** Good for resource-constrained setups

---

## 4. Docker-Native Platforms

### Bytebot — EASIEST SETUP
- **GitHub:** https://github.com/bytebot-ai/bytebot
- **Setup:** 2-minute docker-compose start
- **Architecture:** Containerized Linux desktop, each task in isolated container
- **AI backends:** Supports Claude, GPT, Gemini APIs
- **License:** Apache 2.0
- **Verdict:** Great backup option — pre-built Docker environment

### ScreenEnv (HuggingFace) — NEWEST
- **GitHub:** https://github.com/huggingface/screenenv
- **Architecture:** Docker-native Ubuntu desktops
- **Setup:** pip-installable Python library, <10 second deployment
- **Features:** Built-in MCP support, session recording
- **Platforms:** AMD64 and ARM64
- **Verdict:** Modern, well-maintained, good for CI/CD

### AskUI — ENTERPRISE QA
- **Website:** https://www.askui.com/
- **Approach:** Vision-based (no XPath/CSS selectors)
- **SDK:** Node.js (open-source)
- **Enterprise users:** Deutsche Bahn, Intel
- **Verdict:** Purpose-built for QA testing, enterprise-grade

---

## 5. Benchmark Environments

### OSWorld (NeurIPS 2024)
- **GitHub:** https://github.com/xlang-ai/OSWorld
- **Tasks:** 369 real-world scenarios across Ubuntu, Windows, macOS
- **Apps:** LibreOffice, VS Code, Chromium, GIMP, Thunderbird, VLC
- **Human baseline:** 72.36%
- **Best agent:** Simular Agent S3 at 72.6%
- **Relevance:** Provides evaluation methodology we can adapt

### WindowsAgentArena (Microsoft)
- 154 tasks on Windows OS
- Best agent: 19.5% (vs human 74.5%) — still a gap on Windows

### AndroidWorld
- Dynamic mobile benchmarks, agents now >90% success rate
- Not relevant for desktop IDE testing

---

## 6. Our Approach — Step by Step

### Infrastructure: 4diac IDE in Docker + VNC

**Why Docker + VNC:**
- Reproducible environment (same setup every time)
- AI agent connects via VNC screenshots
- Safe sandbox (agent can't break anything outside container)
- 4diac has official Docker support for FORTE runtime

**Components:**
```
┌─────────────────────────────┐
│  Docker Container           │
│  ┌───────────────────────┐  │
│  │  Ubuntu 22.04         │  │
│  │  + Java 17            │  │
│  │  + Xvfb (virtual X)   │  │
│  │  + fluxbox (WM)       │  │
│  │  + x11vnc (VNC)       │  │
│  │  + noVNC (web client) │  │
│  │  + 4diac IDE 3.0.2    │  │
│  └───────────────────────┘  │
│                             │
│  Ports: 5900 (VNC)          │
│         6080 (noVNC/web)    │
└─────────────────────────────┘
         ↕ screenshots + actions
┌─────────────────────────────┐
│  Python Script (host)       │
│  + Anthropic API            │
│  + Claude Computer Use      │
│  + Task definitions         │
│  + Result logging           │
└─────────────────────────────┘
```

### Step 1: Build & Start Docker Container
```bash
cd agent_interaction/
docker compose up --build -d
```
Then verify: open http://localhost:6080/vnc.html → should see 4diac IDE running.

### Step 2: Claude Computer Use Script
The script will:
1. Connect to the Docker container via VNC/screenshots
2. Take a screenshot of the current state
3. Send screenshot + task description to Claude API with computer_use tool
4. Execute the action Claude returns (mouse click, keyboard input)
5. Repeat until task is complete or max steps reached
6. Log all screenshots, actions, and observations

### Step 3: Define the 4 Tasks (from the paper)
Same tasks the 10 human engineers performed:

**Task 1 — Orientation:** "Find the motor function block in an unknown industrial application. Explore the IDE to understand the project structure."

**Task 2 — Hierarchy:** "Navigate the application hierarchy. Find a specific function block nested 3 levels deep in a subapplication."

**Task 3 — Library:** "Add a new function block from the library to an existing subapplication. Connect it to existing blocks."

**Task 4 — Editing:** "Change the type of an existing function block. Fix any broken connections that result from the type change."

### Step 4: Run & Collect
- Run each task 2-3 times (for consistency)
- Record: screenshots at each step, actions taken, time per task, errors
- Ask Claude to provide usability observations after each task

### Step 5: Compare with Phase 1
Create 3-way matrix:
- Human engineers (paper) — 10 issues found
- AI video assessment (Gemini) — 8/10 issues detected
- AI agent interaction (Claude CU) — TBD

---

## 7. Why Claude Computer Use First

| Factor | Claude CU | Agent S | Bytebot | ScreenEnv |
|--------|:---------:|:-------:|:-------:|:---------:|
| We have API key | ✅ | ❌ need setup | ✅ uses our keys | ✅ uses our keys |
| Documentation | Excellent | Good | Good | Good |
| Setup complexity | Low | High | Very low | Low |
| Performance (OSWorld) | 61.4% | 72.6% | Depends on backend | Depends on backend |
| Can reason about UX | ✅ (LLM-native) | ✅ | ✅ | ✅ |
| Active maintenance | ✅ Anthropic | ✅ | ✅ | ✅ HuggingFace |

**Decision:** Start with Claude Computer Use. If it struggles, try Bytebot (uses same APIs but pre-built environment). Agent S as stretch goal for best performance comparison.

---

## 8. Key Papers & Sources

1. Anthropic Computer Use Docs — https://docs.anthropic.com/en/docs/agents-and-tools/computer-use
2. OSWorld Benchmark — https://os-world.github.io/
3. Simular Agent S — https://github.com/simular-ai/Agent-S
4. UFO2 Microsoft — https://github.com/microsoft/UFO
5. Bytebot — https://github.com/bytebot-ai/bytebot
6. ScreenEnv — https://github.com/huggingface/screenenv
7. CogAgent — https://github.com/zai-org/CogAgent
8. OpenAdapt — https://github.com/OpenAdaptAI/OpenAdapt
9. ShowUI — https://github.com/showlab/ShowUI
10. AskUI — https://www.askui.com/
11. Screen2AX (Accessibility) — https://arxiv.org/abs/2507.16704

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 4diac IDE doesn't start in Docker | Blocks everything | Use Bytebot as pre-built alternative |
| Claude CU can't handle IDE complexity | Poor task completion | Try with simpler tasks first, then escalate |
| VNC latency causes action errors | Incorrect interactions | Add delays between actions, increase screenshot quality |
| API costs too high | Budget concern | Use smaller resolution, limit max steps per task |
| Agent gets stuck in loops | Wasted API calls | Set max step limit (e.g., 50), add loop detection |
