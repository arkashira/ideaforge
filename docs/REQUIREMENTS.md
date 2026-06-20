# Requirements Document  
**Project:** ideaforge  
**Owner:** Axentx – Product Engineering Lead  
**Date:** 2026‑06‑20  
**Version:** 1.0  

---  

## 1. Overview  

ideaforge is an AI‑powered SaaS tool that assists indie hackers, solo founders, and creators in generating, refining, and validating software product ideas. The system must surface high‑potential concepts, evaluate market pain, and estimate willingness‑to‑pay (WTP) before the user invests time or capital. It leverages Axentx’s existing data assets (auto, instr‑resp, messages, query‑resp) and inference frameworks (vLLM, SGLang) to deliver real‑time, structured outputs.

---  

## 2. Functional Requirements  

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| **FR‑1** | **User onboarding** – New users can sign‑up via email/password or OAuth (Google, GitHub). | • Account created and email verified within 5 min.<br>• OAuth flow completes without redirect errors. |
| **FR‑2** | **Idea generation** – Users submit a brief problem statement (≤ 200 chars) and receive **3–5** distinct software ideas. | • Each idea includes title, one‑sentence description, target persona, and core value proposition.<br>• Generation latency ≤ 3 s for average load (see NFR‑1). |
| **FR‑3** | **Idea refinement** – Users can request “expand”, “pivot”, or “simplify” on any generated idea. | • System returns an updated idea within 2 s, preserving original intent.<br>• At least one of the three refinement modes must be applied per request. |
| **FR‑4** | **Market validation** – For any idea, the system produces a **validation report** containing: <br>• Estimated market size (TAM) <br>• Pain severity score (1‑10) <br>• Willingness‑to‑pay estimate (USD/month) <br>• Primary competitor snapshot | • Scores derived from the **query‑resp** and **messages** datasets using prompt‑engineered LLM calls.<br>• Report rendered in a structured JSON payload and a human‑readable UI view. |
| **FR‑5** | **Idea ranking** – Users can sort generated ideas by any validation metric (e.g., WTP, pain score). | • Sorting operation completes instantly (≤ 200 ms) on the client side. |
| **FR‑6** | **Export & share** – Users can export an idea or validation report as PDF or Markdown and share via a unique public URL. | • Exported files match the on‑screen content exactly.<br>• Public URL is read‑only, expires after 30 days unless renewed. |
| **FR‑7** | **Feedback loop** – Users can rate each idea (thumbs up/down) and optionally provide free‑text feedback. | • Rating stored in the BRAIN vector store for future model fine‑tuning.<br>• Feedback visible in the admin dashboard. |
| **FR‑8** | **Admin dashboard** – Internal staff can view usage metrics, model performance, and flagged content. | • Dashboard updates every 5 min.<br>• Access restricted to admin role via RBAC. |
| **FR‑9** | **API access** – Expose a RESTful endpoint `/v1/ideas` that mirrors the UI generation flow for third‑party integrations. | • API follows OpenAPI 3.0 spec.<br>• Rate‑limited to 60 calls/min per API key. |
| **FR‑10** | **Data privacy compliance** – Allow users to delete their account and all associated data. | • Deletion completes within 24 h and is auditable. |

---  

## 3. Non‑Functional Requirements  

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | • 99th‑percentile response time ≤ 3 s for idea generation under 200 concurrent users.<br>• Backend inference served via **vLLM** with GPU autoscaling; target throughput ≥ 500 req/min. |
| **NFR‑2** | **Scalability** | • Horizontal scaling of stateless API containers (K8s Deployment).<br>• Vector store (pgvector) sharded to support up to 10 M stored feedback vectors. |
| **NFR‑3** | **Reliability** | • SLA 99.9 % uptime (excluding scheduled maintenance).<br>• Automatic failover to a warm standby replica for the inference service. |
| **NFR‑4** | **Security** | • All traffic TLS 1.3.<br>• Secrets managed via Vault; no hard‑coded credentials.<br>• OWASP Top 10 mitigations applied (SQLi, XSS, CSRF, etc.). |
| **NFR‑5** | **Observability** | • Structured logging (JSON) to centralized ELK stack.<br>• Metrics exported to Prometheus (latency, error rate, GPU utilization). |
| **NFR‑6** | **Data Governance** | • Use only licensed datasets (Apache‑2.0, MIT, CDLA‑Permissive‑2.0).<br>• No PII stored in model training data; user‑provided text is encrypted at rest. |
| **NFR‑7** | **Maintainability** | • Codebase follows Axentx’s Python style guide (flake8 ≤ 9, black).<br>• Unit test coverage ≥ 85 % for core modules.<br>• CI pipeline includes security scanning (Snyk) and performance regression tests. |
| **NFR‑8** | **Portability** | • Deployable on both AWS (EKS) and GCP (GKE) using Helm charts. |
| **NFR‑9** | **Accessibility** | • UI complies with WCAG 2.1 AA (contrast, keyboard navigation, ARIA labels). |
| **NFR‑10** | **Legal** | • Terms of Service and Privacy Policy must be presented on sign‑up; acceptance recorded. |

---  

## 4. Constraints  

1. **Technology stack** – Must use existing Axentx‑approved frameworks:  
   * Inference: **vLLM** (GPU‑accelerated) and **SGLang** for structured output.  
   * Vector store: **pgvector** (PostgreSQL 15).  
   * Backend: Python 3.11, FastAPI.  
   * Frontend: React 18 + TypeScript.  

2. **Data limits** – Training‑time data cannot exceed the current licensed corpus (≈ 38 M pairs). No external proprietary datasets may be introduced without legal review.  

3. **Budget** – Cloud GPU usage capped at $12,000 / month; inference must stay within this budget while meeting NFR‑1.  

4. **Release cadence** – MVP must be production‑ready within 8 weeks from project kickoff.  

---  

## 5. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Users have internet access and a modern browser (Chrome ≥ 108, Firefox ≥ 107). |
| **A‑2** | The underlying LLM (e.g., Llama‑2‑70B) is already fine‑tuned on Axentx’s datasets and hosted in‑house. |
| **A‑3** | Market validation heuristics (pain score, TAM, WTP) can be approximated via prompt‑engineered queries to the LLM without external APIs. |
| **A‑4** | The BRAIN vector store will be periodically refreshed (weekly) with new feedback embeddings for continuous improvement. |
| **A‑5** | Legal team has approved the use of user‑generated content for model fine‑tuning under the agreed consent flow. |
| **A‑6** | Third‑party OAuth providers (Google, GitHub) remain stable and their APIs unchanged for the project duration. |

---  

## 6. Acceptance Criteria Summary  

- All functional requirements FR‑1 – FR‑10 are demonstrably working in a staging environment.  
- Non‑functional targets NFR‑1 – NFR‑10 are met as verified by automated tests and monitoring dashboards.  
- No duplicate functionality with existing Axentx products (e.g., iceoryx2) is introduced.  
- Documentation (API spec, user guide, admin guide) is complete and version‑controlled in the repository.  

---  

*Prepared by the Ideaforge Product/Engineering Lead – Axentx*
