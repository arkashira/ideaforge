# ideaforge – Product Requirements Document (PRD)

**Document Version:** 1.0  
**Last Updated:** 2026‑06‑20  
**Author:** Senior Product/Engineering Lead, Axentx  

---  

## 1. Purpose & Vision  

**Problem Statement**  
Indie hackers, solo founders, and creator‑entrepreneurs repeatedly hit an *ideation bottleneck*: they have technical skill but struggle to surface high‑impact software ideas that are both novel and commercially viable. Existing brainstorming tools are generic, lack data‑driven validation, and require manual market research, leading to wasted time and resources.

**Vision**  
Create **ideaforge**, an AI‑powered “Idea Engine” that **generates, refines, and validates** software product concepts in a single, frictionless workflow. By leveraging Axentx’s proprietary data assets (22 M+ training pairs, market signal pipelines, and validation loops), ideaforge will become the go‑to ideation companion for indie creators, accelerating time‑to‑concept and increasing the probability of building revenue‑validated products.

---

## 2. Target Users & Personas  

| Persona | Core Traits | Pain Points | Desired Outcome |
|---------|-------------|-------------|-----------------|
| **Indie Hacker** | Solo developer, limited budget, rapid iteration mindset | No systematic way to discover market‑ready ideas; spends weeks on research | Quick, data‑backed idea list with clear problem‑solution fit |
| **Creator‑Entrepreneur** | Non‑technical founder, strong brand, wants a tech product | Lacks technical fluency to assess feasibility; fears building something nobody wants | High‑level concept + feasibility score + validation hints |
| **Product Scout (Early‑stage VC / Accelerator)** | Evaluates many founder pitches | Hard to triage ideas for market potential | Automated pre‑screening of ideas with market‑size estimate |
| **Community Mentor / Coach** | Guides multiple founders | Needs repeatable framework to help mentees generate ideas | Ready‑to‑use workshop tool that outputs vetted concepts |

---

## 3. Goals & Success Metrics  

| Goal | Metric | Target (12 mo) |
|------|--------|----------------|
| **Accelerate ideation** | Avg. time from user login to first validated idea | ≤ 5 min |
| **Increase idea quality** | % of generated ideas that pass a “validation gate” (WTP survey + market signal) | ≥ 30 % |
| **User adoption** | Monthly active users (MAU) | 5 k |
| **Retention** | 30‑day retention rate | ≥ 45 % |
| **Revenue potential** | % of ideas that later convert to paid Axentx services (e.g., custom dev, consulting) | ≥ 5 % |
| **Operational efficiency** | Avg. compute cost per idea generation | <$0.02 (leveraging vLLM inference) |

---

## 4. Scope  

### 4.1 In‑Scope (Must‑Have)

1. **AI‑Driven Idea Generation**  
   - Prompt‑based generation using **vLLM** (high‑throughput inference).  
   - Input fields: domain, target user, constraints (tech stack, budget).  

2. **Idea Refinement Loop**  
   - Structured generation via **SGLang** to produce:  
     - Problem statement  
     - Solution sketch (features, tech stack)  
     - Unique value proposition (UVP)  
     - Preliminary market sizing (based on internal signal dataset).  

3. **Validation Engine**  
   - Automated “soft validation” using:  
     - Historical market‑signal similarity (vector search against BRAIN).  
     - Quick WTP (Willingness‑to‑Pay) micro‑survey (optional email capture).  
   - Scorecard: **Feasibility (0‑10)**, **Market Fit (0‑10)**, **Novelty (0‑10)**.  

4. **User Interface**  
   - Web SPA (React + Vite) with:  
     - Dashboard of generated ideas.  
     - Inline editing of prompts.  
     - Export options (Markdown, PDF, CSV).  

5. **Data & Privacy**  
   - Store user prompts & generated ideas in encrypted DB (PostgreSQL).  
   - GDPR‑compliant opt‑out for data retention.  

6. **Analytics & Feedback Loop**  
   - Capture conversion events (idea saved, survey completed).  
   - Feed back into BRAIN to improve future generation quality.  

### 4.2 Out‑of‑Scope (Will Not Be Delivered in v1)

| Item | Reason |
|------|--------|
| Full market research (e.g., competitor analysis, SEO data) | Planned for v2 as a premium add‑on. |
| Integrated code scaffolding (auto‑generate starter repos) | Too early; focus on idea stage first. |
| Multi‑language support (non‑English) | Initial launch limited to English; later expansion. |
| Real‑time collaboration (multiple users editing same idea) | Requires sync layer; deferred to v2. |
| Direct integration with Axentx’s downstream product pipeline (dev, QA) | Separate downstream service; will expose API for future integration. |

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Prompt Builder** | Guided UI to capture domain, user persona, constraints. | Users can complete prompt in ≤ 3 steps; generated prompt matches schema. |
| **P1** | **Idea Generation Engine** | Calls vLLM with SGLang templates to output structured idea. | Returns all 4 sections (Problem, Solution, UVP, Market) within 2 s. |
| **P1** | **Validation Scorecard** | Computes feasibility, market fit, novelty scores. | Scores displayed with color coding; total ≥ 15 triggers “high‑potential” badge. |
| **P2** | **WTP Micro‑Survey** | Optional 1‑question survey (e.g., “Would you pay $X for this?”) sent via email. | Survey link generated; response recorded; score updates accordingly. |
| **P2** | **Export & Share** | Export idea as Markdown, PDF, or shareable link. | Export succeeds; link is view‑only and expires after 30 days. |
| **P3** | **Idea Library** | Personal library of saved ideas with tagging & search. | Users can save, tag, and retrieve ideas; search returns relevant results within 0.5 s. |
| **P3** | **Analytics Dashboard** | Shows user’s idea generation stats, conversion funnel. | Dashboard loads with correct metrics; data updates in real‑time. |
| **P4** | **API Endpoint** | Public REST endpoint for programmatic idea generation. | Authenticated request returns same payload as UI within SLA. |

---

## 6. Technical Architecture Overview  

- **Frontend**: React (TypeScript) + Vite, hosted on Axentx CDN.  
- **Backend**: FastAPI (Python) micro‑services:  
  - `generation_service` → vLLM inference (GPU‑accelerated).  
  - `validation_service` → vector similarity (pgvector) + scoring logic.  
  - `survey_service` → email dispatch (Postmark) + response webhook.  
- **Data Store**: PostgreSQL + pgvector for embeddings; Redis for request caching.  
- **Model Assets**:  
  - **vLLM** (latest LLM checkpoint, tuned on `instr-resp` & `query-resp` datasets).  
  - **SGLang** templates for structured output.  
- **Observability**: OpenTelemetry tracing, Grafana dashboards, Loki logs.  
- **CI/CD**: GitHub Actions → Docker images → Axentx Kubernetes cluster (auto‑scale).  

---

## 7. Milestones & Timeline  

| Milestone | Duration | Owner | Deliverable |
|-----------|----------|-------|-------------|
| **M1 – Discovery & Design** | 2 weeks | PM / UX | Wireframes, API spec, data schema |
| **M2 – Core Engine Prototype** | 3 weeks | ML Eng | vLLM + SGLang integration, basic prompt → idea flow |
| **M3 – Validation Layer** | 2 weeks | Data Eng | Vector similarity pipeline, scoring algorithm |
| **M4 – Frontend MVP** | 3 weeks | Frontend Eng | Prompt Builder UI, result view, export |
| **M5 – Beta Launch & Feedback** | 4 weeks | PM / QA | Closed beta (50 users), analytics collection |
| **M6 – Iteration & Scaling** | 3 weeks | All | Performance tuning, WTP survey, API endpoint |
| **M7 – Public Release (v1.0)** | 2 weeks | PM / Ops | Documentation, marketing assets, support handoff |

**Total Time to Market:** ~19 weeks (~4.5 months)

---

## 8. Risks & Mitigations  

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Model Hallucination** – generated ideas unrealistic or infeasible. | High (user trust) | Medium | Post‑generation validation via similarity scoring; human‑in‑the‑loop review for beta. |
| **Data Privacy** – storing user prompts could breach GDPR. | High | Low | Encrypt at rest, provide explicit opt‑out, purge after 90 days. |
| **Compute Cost Overrun** – high inference cost at scale. | Medium | Medium | Use vLLM’s batch inference, auto‑scale GPU nodes, monitor cost per idea. |
| **User Adoption** – niche market may not reach MAU target. | Medium | Medium | Early partnership with indie‑hacker communities (Product Hunt, Indie Hackers). |
| **Regulatory** – WTP survey may be considered marketing solicitation. | Low | Low | Keep surveys optional, clear consent flow. |

---

## 9. Acceptance Criteria (Definition of Done)

- All **P1** features implemented, passing unit & integration tests (≥ 90 % coverage).  
- End‑to‑end latency ≤ 5 seconds for idea generation + validation.  
- Security audit completed; no critical findings.  
- Documentation (README, API spec, user guide) published in repo.  
- Beta feedback loop shows ≥ 30 % of ideas achieving “high‑potential” score.  
- Deployment to production with zero‑downtime migration path.  

---

## 10. Appendices  

### A. Glossary  
- **WTP** – Willingness‑to‑Pay survey.  
- **UVP** – Unique Value Proposition.  
- **BRAIN** – Axentx’s pgvector knowledge store.  

### B. References  
- vLLM repo: https://github.com/vllm-project/vllm  
- SGLang repo: https://github.com/sgl-project/sglang  
- Axentx Runbook (2026‑05‑23) – internal documentation.  

---  

*End of Document*
