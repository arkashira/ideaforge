# Roadmap for **ideaforge**
*AI‑powered idea generation & validation platform for indie hackers & creators*  

---

## 📅 Overview

| Phase | Timeline | Goal |
|-------|----------|------|
| **MVP** | **Q3 2026** (12 weeks) | Deliver a usable, self‑contained web app that can generate software ideas, run a quick market‑validation loop, and export a concise PRD. |
| **v1.0** | Q4 2026 – Q1 2027 | Expand validation depth, add collaboration, and integrate with Axentx’s knowledge base for richer suggestions. |
| **v2.0** | Q2 2027 – Q4 2027 | Introduce automated prototyping, monetization insights, and marketplace integration. |

> **MVP‑critical items** are marked with **⚡**.

---

## 🚀 MVP (Launch‑Ready)

| # | Feature | Description | Owner | Acceptance Criteria |
|---|---------|-------------|-------|----------------------|
| **⚡1** | **Idea Generator UI** | Simple React SPA where users input a brief problem statement or keywords and receive 3‑5 AI‑crafted software ideas. | Front‑end Lead | - Input box + “Generate” button.<br>- Results displayed with title, tagline, and one‑sentence value prop.<br>- Generation latency < 5 s. |
| **⚡2** | **Prompt Engine** | Server‑side service that builds a structured prompt for the LLM (vLLM) using the “SGLang” structured‑generation framework. | AI Engineer | - Prompt template versioned in repo.<br>- Uses Axentx’s **instr‑resp** dataset for idea phrasing.<br>- Passes unit tests for deterministic output shape. |
| **⚡3** | **Quick Validation Loop** | After idea display, user can click “Validate” → system runs a 3‑question market survey (problem severity, willingness‑to‑pay, competition) using a pre‑trained LLM classifier. | Data Scientist | - Survey shown in modal.<br>- Validation score (0‑100) returned.<br>- Score ≥ 60 flagged as “Promising”. |
| **⚡4** | **Export PRD** | One‑click download of a markdown PRD containing idea summary, validation score, target persona, and basic feature list. | Backend Lead | - File named `IDEA_<slug>.md`.<br>- Contains all MVP fields, passes schema validation. |
| **⚡5** | **User Accounts (OAuth)** | Minimal auth (Google/GitHub) to persist ideas and validation history. | DevOps | - Secure JWT session.<br>- Data stored in PostgreSQL (hosted on Axentx infra). |
| **⚡6** | **CI/CD & Deployment** | Automated pipeline (GitHub Actions) building Docker image, running unit/integration tests, and deploying to Axentx staging environment. | SRE | - 100 % test pass on merge.<br>- Zero‑downtime rollout. |
| **⚡7** | **Observability** | Basic logging, error tracking (Sentry), and usage metrics (Prometheus). | SRE | - Dashboard shows daily active users, generation latency, validation success rate. |

### MVP Success Metrics
- **≥ 2 000** registered users within 30 days of launch.  
- **≥ 70 %** of generated ideas receive a validation score ≥ 60.  
- **≤ 5 s** average end‑to‑end latency (input → results).  

---

## 🌟 v1.0 – “Collaboration & Depth”

| Theme | Feature | Description | Owner | Target Release |
|-------|---------|-------------|-------|----------------|
| **Collaboration** | Team Workspaces | Multi‑user spaces where a team can share, comment, and vote on ideas. | Front‑end Lead | Q4 2026 |
| | Real‑time Editing | WebSocket‑based live editing of idea descriptions & validation notes. | Backend Lead | Q4 2026 |
| **Validation Depth** | Competitive Landscape Scan | Automated web‑scrape + LLM summarization of existing solutions. | Data Scientist | Q1 2027 |
| | Pricing & TAM Modeling | Generate rough TAM (Total Addressable Market) and price‑point suggestions using Axentx’s **query‑resp** dataset. | AI Engineer | Q1 2027 |
| **Knowledge Integration** | Axentx Knowledge Graph Hook | Pull relevant prior projects (e.g., iceoryx2, other Axentx products) to enrich idea context. | Architect | Q1 2027 |
| **Productivity** | Idea Templates | Library of industry‑specific templates (SaaS, mobile, dev‑tools). | PM | Q4 2026 |
| **UX** | Dark Mode & Accessibility | WCAG‑2.1 AA compliance. | Front‑end Lead | Q4 2026 |

### v1 Success Metrics
- **≥ 30 %** of ideas receive a competitive scan report.  
- **≥ 1 000** active team workspaces.  
- **≥ 80 %** of users rate validation depth as “Helpful” (survey).  

---

## 🚀 v2.0 – “From Idea to Prototype”

| Theme | Feature | Description | Owner | Target Release |
|-------|---------|-------------|-------|----------------|
| **Automated Prototyping** | Code Skeleton Generator | Convert validated idea into a starter repo (frontend + backend) using Axentx’s **vLLM** inference templates. | Dev Lead | Q2 2027 |
| | UI Mockup AI | Generate low‑fidelity wireframes (Figma JSON) from idea description. | AI Engineer | Q2 2027 |
| **Monetization Insights** | Revenue Model Advisor | Suggest subscription tiers, freemium vs. paid features, and churn predictors. | Data Scientist | Q3 2027 |
| **Marketplace** | Publish to Ideaforge Marketplace | Allow creators to list validated ideas for sale or partnership. | PM | Q3 2027 |
| **Advanced Analytics** | Cohort Tracking | Follow idea performance over time (validation score changes, user engagement). | SRE | Q4 2027 |
| **Enterprise Ready** | SSO & RBAC | Integration with SAML / Azure AD for corporate teams. | DevOps | Q4 2027 |

### v2 Success Metrics
- **≥ 15 %** of validated ideas result in a generated code skeleton.  
- **≥ 500** marketplace listings within 6 months of launch.  
- **≥ 90 %** of enterprise trial users convert to paid plans.  

---

## 📌 Milestone Tracking & Governance

| Milestone | Owner | Review Cadence | Exit Criteria |
|-----------|-------|----------------|---------------|
| **MVP Sprint 0 – Setup** | Lead Engineer | Weekly | Repo scaffolded, CI pipeline live. |
| **MVP Sprint 1 – Core Generation** | AI Engineer | Bi‑weekly | Prompt engine passes integration tests. |
| **MVP Sprint 2 – Validation Loop** | Data Scientist | Bi‑weekly | Validation classifier ≥ 85 % accuracy on held‑out set. |
| **MVP Sprint 3 – Auth & Export** | Backend Lead | Weekly | OAuth flow secure, PRD export verified. |
| **MVP Release** | PM | End of Sprint 4 | All MVP‑critical items ✅, metrics plan approved. |
| **v1 Planning** | Product Council | Monthly | Feature backlog prioritized, resources allocated. |
| **v2 Go‑to‑Market** | GTM Lead | Quarterly | Marketplace pricing model defined, sales enablement ready. |

---

## 📚 References & Assets

- **Repo:** `github.com/arkashira/ideaforge` (main branch)  
- **Frameworks:** `vLLM` (inference), `SGLang` (structured generation)  
- **Datasets:** `instr-resp`, `query-resp` (used for prompt engineering & validation)  
- **Runbook:** AXENTX RUNBOOK + LOCATIONS (2026‑05‑23) – deployment standards, security guidelines.  

---  

*Prepared by the Ideaforge senior product/engineering lead, aligned with Axentx’s revenue‑validated product pipeline.*
