# TECH_SPEC.md – Ideaforge

**Document version:** 1.0  
**Last updated:** 2026‑06‑20  
**Author:** Senior Product/Engineering Lead, Axentx  

---  

## Table of Contents
1. [Overview](#1-overview)  
2. [Goals & Success Metrics](#2-goals--success-metrics)  
3. [Architecture Overview](#3-architecture-overview)  
4. [Core Components](#4-core-components)  
5. [Data Model](#5-data-model)  
6. [Key APIs & Interfaces](#6-key-apis--interfaces)  
7. [Technology Stack](#7-technology-stack)  
8. [External Dependencies](#8-external-dependencies)  
9. [Deployment & Operations](#9-deployment--operations)  
10. [Security & Compliance](#10-security--compliance)  
11. [Observability & Monitoring](#11-observability--monitoring)  
12. [Scalability & Performance](#12-scalability--performance)  
13. [Future Enhancements](#13-future-enhancements)  
14. [Appendix](#14-appendix)  

---  

## 1. Overview
Ideaforge is an AI‑powered SaaS tool that assists indie hackers, solo founders, and creators in **generating, refining, and validating software product ideas**. The system ingests market signals (search trends, Reddit posts, product‑hunt listings, etc.), runs structured generation pipelines, and returns a ranked list of ideas with:

* **Idea Summary** – concise description (≤ 2 sentences).  
* **Target Persona** – who benefits most.  
* **Problem Statement** – validated pain point.  
* **Solution Sketch** – high‑level feature set.  
* **Revenue Validation Score** – derived from willingness‑to‑pay signals (e.g., pre‑launch surveys, price‑sensitivity modeling).  

The product is delivered via a web UI and a public REST/GraphQL API for integration into other tools (e.g., no‑code builders, community bots).

---  

## 2. Goals & Success Metrics
| Goal | Metric | Target (12 mo) |
|------|--------|----------------|
| Idea generation quality | % of ideas rated “high relevance” by human reviewers | ≥ 85 % |
| Validation accuracy | Correlation between AI‑predicted revenue score and actual post‑launch sales (pilot) | r ≥ 0.7 |
| User activation | Daily active users (DAU) / Monthly active users (MAU) ratio | ≥ 30 % |
| Latency | 95th‑percentile response time for `/generate` endpoint | ≤ 800 ms |
| Reliability | Monthly uptime (excluding scheduled maintenance) | ≥ 99.9 % |
| Cost efficiency | Avg. compute cost per generated idea | ≤ $0.02 (using vLLM inference) |

---  

## 3. Architecture Overview
```
+-------------------+       +-------------------+       +-------------------+
|   Front‑end (SPA) | <---> |   API Gateway     | <---> |   Auth Service    |
+-------------------+       +-------------------+       +-------------------+
                                 |
                                 v
                         +-------------------+
                         |   Orchestrator    |  (Celery + Redis)
                         +-------------------+
                                 |
        +------------------------+------------------------+
        |                        |                        |
        v                        v                        v
+----------------+      +----------------+      +----------------+
| Idea Generator |      | Validator      |      | Analytics &    |
| (vLLM + SGLang)|      | (ML models)    |      | Reporting      |
+----------------+      +----------------+      +----------------+
        |                        |                        |
        v                        v                        v
+----------------+      +----------------+      +----------------+
| Vector Store   |      | Postgres DB    |      | PGVector (BRAIN)|
| (pgvector)     |      | (metadata)    |      | (embeddings)   |
+----------------+      +----------------+      +----------------+
```

* **Front‑end** – React + Vite, hosted on CloudFront (or equivalent).  
* **API Gateway** – FastAPI (Python) behind an NGINX reverse‑proxy, exposing REST & GraphQL.  
* **Auth Service** – OAuth2 / OpenID Connect (Auth0 or self‑hosted Keycloak).  
* **Orchestrator** – Celery workers (Python) coordinated via Redis; schedules generation & validation pipelines.  
* **Idea Generator** – Inference engine built on **vLLM** (production‑grade LLM serving) with **SGLang** for structured output.  
* **Validator** – Ensemble of lightweight models (price‑sensitivity, market‑size, competitor‑density) trained on the internal **auto**, **instr‑resp**, **messages**, **query‑resp** datasets.  
* **Vector Store** – PostgreSQL with **pgvector** extension (the company‑wide BRAIN) for semantic similarity search and caching of market‑signal embeddings.  
* **Analytics** – Click‑stream stored in ClickHouse; dashboards in Metabase.  

---  

## 4. Core Components  

| Component | Responsibility | Key Technologies | Public/Private |
|-----------|----------------|------------------|----------------|
| **Web UI** | Interactive idea generation, user feedback, dashboard | React, TypeScript, TailwindCSS | Public |
| **API Gateway** | Request routing, rate limiting, schema validation | FastAPI, Pydantic, Uvicorn, NGINX | Public |
| **Auth Service** | User identity, token issuance, RBAC | Auth0 (fallback Keycloak) | Private |
| **Orchestrator** | Job queue, retries, scheduling | Celery 5.x, Redis 7.x | Private |
| **Idea Generator** | Prompt engineering, LLM inference, structured output | vLLM, SGLang, OpenAI‑compatible model (e.g., Llama‑3‑70B) | Private |
| **Validator** | Scoring ideas on market fit & revenue potential | Scikit‑learn, XGBoost, PyTorch, custom feature pipelines | Private |
| **Vector Store (BRAIN)** | Semantic search of market signals, caching embeddings | PostgreSQL 15 + pgvector, pgvector‑hnsw index | Private |
| **Metadata DB** | Persist user sessions, idea records, audit logs | PostgreSQL 15 | Private |
| **Analytics** | Event ingestion, KPI reporting | ClickHouse, Metabase | Private |
| **CI/CD** | Automated testing, container builds, canary releases | GitHub Actions, Docker, Helm, ArgoCD | Private |

---  

## 5. Data Model  

### 5.1 Relational Tables (PostgreSQL)

| Table | Columns | Description |
|-------|---------|-------------|
| `users` | `id PK`, `email`, `hashed_pw`, `created_at`, `last_login`, `role` | User profile & RBAC |
| `ideas` | `id PK`, `user_id FK`, `title`, `summary`, `persona`, `problem`, `solution`, `generated_at`, `validation_score`, `status` | Core idea record |
| `validation_runs` | `id PK`, `idea_id FK`, `model_version`, `score`, `features_json`, `run_at` | Historical validation data |
| `market_signals` | `id PK`, `source`, `raw_text`, `embedding VECTOR(1536)`, `created_at` | Raw signals (news, Reddit, etc.) |
| `api_keys` | `id PK`, `user_id FK`, `key_hash`, `created_at`, `revoked_at` | For programmatic access |

### 5.2 Vector Store (pgvector)

* **Embedding dimension:** 1536 (OpenAI `text-embedding-3-large` compatible).  
* **Index:** `ivfflat` with 100 clusters + `hnsw` for re‑ranking.  
* **Use‑cases:**  
  * Find similar market signals for a generated idea (semantic relevance).  
  * Retrieve prior ideas for deduplication checks.

---  

## 6. Key APIs & Interfaces  

### 6.1 REST Endpoints (FastAPI)

| Method | Path | Auth | Description | Request Body | Response |
|--------|------|------|-------------|--------------|----------|
| POST | `/v1/ideas/generate` | Bearer token | Trigger generation pipeline | `{ "seed": "string (optional)", "tags": ["ai","product"] }` | `202 Accepted` + `{ "job_id": "uuid" }` |
| GET | `/v1/ideas/{job_id}` | Bearer token | Poll job status / retrieve result | – | `{ "status":"pending|success|failed", "idea": IdeaDTO? }` |
| POST | `/v1/ideas/{idea_id}/feedback` | Bearer token | Submit user rating (1‑5) | `{ "rating": int, "comment": "string?" }` | `200 OK` |
| GET | `/v1/analytics/summary` | Admin token | KPI snapshot | – | `{ "daily_requests": int, "avg_latency_ms": float, ... }` |
| POST | `/v1/webhook/market-signal` | API key | Ingest external market signal (internal use) | `{ "source":"string","text":"string" }` | `201 Created` |

### 6.2 GraphQL (optional)

* **Query:** `ideas(userId: ID, status: IdeaStatus, limit: Int): [Idea]`  
* **Mutation:** `submitFeedback(ideaId: ID!, rating: Int!, comment: String): FeedbackResult`  

### 6.3 Internal Interfaces  

| Interface | Producer | Consumer | Message Format |
|-----------|----------|----------|----------------|
| `generation_task` (Celery) | API Gateway | Idea Generator Worker | JSON payload with `seed`, `tags`, `user_id` |
| `validation_task` (Celery) | Idea Generator | Validator Worker | Idea ID + generated text |
| `embedding_update` (Kafka) | Market Signal Ingestor | Vector Store Updater | `{ id, source, embedding }` |

---  

## 7. Technology Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python 3.11 | Rich ML ecosystem, async support, aligns with vLLM & SGLang |
| **Web UI** | React 18 + Vite | Fast dev cycles, tree‑shaking, easy SSR fallback |
| **API** | FastAPI + Uvicorn | High performance, automatic OpenAPI docs |
| **LLM Serving** | vLLM (GPU‑accelerated) | Low‑latency inference, dynamic batching |
| **Structured Generation** | SGLang | Guarantees JSON‑compatible output, reduces post‑processing |
| **Task Queue** | Celery + Redis | Proven, easy scaling, supports retries |
| **Vector DB** | PostgreSQL + pgvector | Unified storage, leverages existing BRAIN, no extra infra |
| **Metadata DB** | PostgreSQL | ACID guarantees for user & audit data |
| **Observability** | OpenTelemetry, Prometheus, Grafana | Vendor‑agnostic tracing & metrics |
| **CI/CD** | GitHub Actions + Docker + Helm + ArgoCD | GitOps, zero‑downtime canary releases |
| **Hosting** | AWS (EKS for containers, RDS for Postgres, S3 for static assets) – can be abstracted to any K8s cloud | Scalability, managed services, cost predictability |

---  

## 8. External Dependencies  

| Dependency | Version | License | Usage |
|------------|---------|---------|-------|
| `vllm` | `0.5.0` | Apache‑2.0 | LLM inference engine |
| `sglang` | `0.2.1` | Apache‑2.0 | Structured generation |
| `pgvector` | `0.5.0` | PostgreSQL | Vector embeddings |
| `fastapi` | `0.115.0` | MIT | API layer |
| `celery` | `5.4.0` | BSD‑3 | Task orchestration |
| `redis-py` | `5.0.1` | MIT | Queue backend |
| `scikit-learn` | `1.5.0` | BSD‑3 | Validation models |
| `xgboost` | `2.1.0` | Apache‑2.0 | Gradient‑boosted scoring |
| `torch` | `2.4.0` | BSD‑3 | Optional GPU inference |
| `auth0-js` | `9.23.0` | MIT | Auth integration (fallback) |

All dependencies are vetted for security and are compatible with the company‑wide **license compliance policy**.

---  

## 9. Deployment & Operations  

### 9.1 Containerization  
* Each service (API, worker, validator, generator) is packaged as an **OCI‑compatible Docker image**.  
* Base image: `python:3.11-slim` + `nvidia/cuda:12.4-runtime` for GPU workers.  

### 9.2 Kubernetes Manifests (Helm Chart)  
* **Namespace:** `ideaforge`  
* **Deployments:**  
  * `api-gateway` – 3 replicas, HPA (CPU > 70 % → +1).  
  * `worker-generator` – GPU node pool, 2 replicas.  
  * `worker-validator` – CPU‑only, 4 replicas.  
  * `redis` – StatefulSet, 3‑node cluster.  
  * `postgres` – Managed RDS (multi‑AZ).  

* **Ingress:** AWS ALB with TLS (Let’s Encrypt).  

### 9.3 CI/CD Flow  
1. **Push** → GitHub Actions runs unit, integration, and security scans.  
2. **Docker Build** → Image pushed to ECR (versioned tag).  
3. **ArgoCD** detects new tag → Canary rollout (5 % traffic).  
4. **Automated smoke tests** → Promote to full rollout on success.  

### 9.4 Secrets Management  
* AWS Secrets Manager for DB credentials, API keys, JWT secret.  
* All pods mount secrets via **Kubernetes secrets** with **IAM role‑based access**.  

---  

## 10. Security & Compliance  

| Area | Controls |
|------|----------|
| **Authentication** | OAuth2 + PKCE, short‑lived JWT (15 min) + refresh token (7 days). |
| **Authorization** | RBAC (user, admin, service‑account). |
| **Data Encryption** | TLS 1.3 for all in‑flight traffic; at‑rest encryption via RDS & S3 SSE‑AES256. |
| **Input Validation** | Pydantic models; strict schema for all external payloads. |
| **Rate Limiting** | NGINX + FastAPI `slowapi` – 100 req/min per API key. |
| **Audit Logging** | Immutable logs stored in CloudWatch Logs; GDPR‑compliant retention (90 days). |
| **Vulnerability Scanning** | Trivy scan on every image; Dependabot alerts. |
| **Compliance** | Licenses verified against company whitelist; data usage limited to anonymized market signals. |

---  

## 11. Observability & Monitoring  

* **Metrics** – Prometheus exporters on each service (request latency, error rates, queue depth).  
* **Tracing** – OpenTelemetry (Jaeger backend) for end‑to‑end request flow (API → Celery → Generator → Validator).  
* **Logs** – Structured JSON logs shipped to Elastic Cloud via Fluent Bit.  
* **Dashboards** – Grafana panels for SLA (latency, uptime) and business KPIs (ideas generated per day, validation score distribution).  

---  

## 12. Scalability & Performance  

| Dimension | Strategy |
|-----------|----------|
| **Compute** | vLLM auto‑batching; horizontal GPU scaling via Kubernetes node‑pool autoscaler. |
| **Queue** | Redis cluster with sharding; Celery prefetch limit tuned to avoid worker overload. |
| **Storage** | PostgreSQL read replicas for analytics; pgvector HNSW index for sub‑millisecond similarity search. |
| **Cache** | In‑memory LRU cache (Python `cachetools`) for recent market‑signal embeddings. |
| **Cold‑start mitigation** | Warm‑up jobs scheduled every 5 min to keep at least one generator worker active. |
| **Cost control** | Spot instances for GPU workers; auto‑scale down to zero when idle (nightly). |

Performance benchmark (internal test, 2026‑05‑30):  

| Load (req/s) | 95th‑pct latency | CPU Util (API) | GPU Util (Generator) |
|--------------|------------------|----------------|----------------------|
| 10 | 210 ms | 30 % | 15 % |
| 50 | 460 ms | 70 % | 45 % |
| 100 | 780 ms | 95 % | 80 % |
| 200 | 1 420 ms (degraded) – triggers autoscale | 120 % (autoscaling) | 150 % (adds GPU node) |

---  

## 13. Future Enhancements  

1. **Multi‑modal signals** – ingest images & videos (e.g., TikTok trends) using CLIP embeddings.  
2. **User‑generated prompts** – UI for custom prompt engineering with live preview.  
3. **Marketplace integration** – one‑click export of validated ideas to product‑hunt or IndieHackers posts.  
4. **A/B testing of validation models** – MAB framework to continuously improve revenue‑score predictions.  
5. **Self‑serve API pricing tiers** – metered billing based on generated ideas count.  

---  

## 14. Appendix  

### 14.1 Sample Prompt (SGLang)  

```sglang
<system>
You are Ideaforge, an AI assistant that creates concise software product ideas.
Output must be a JSON object with the following fields:
title, summary, persona, problem, solution, tags.
All fields are required, strings no longer than 200 characters.
</system>

<user>
Generate 3 ideas for the niche "remote team productivity tools". Use recent Reddit trends about "async meetings".
</user>

<assistant>
{
  "ideas": [
    {
      "title": "Async Standup Bot",
      "summary": "A Slack/Discord bot that collects daily updates via voice notes and auto‑summarizes them.",
      "persona": "Remote team leads",
      "problem": "Synchronous standups waste time across time zones.",
      "solution": "Record, transcribe, and generate concise bullet‑point reports.",
      "tags": ["slack","ai","productivity"]
    },
    ...
  ]
}
```

### 14.2 Environment Variables (example)

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_URL` | SQLAlchemy connection string | `postgresql+psycopg2://user:pass@db:5432/ideaforge` |
| `REDIS_URL` | Celery broker | `redis://redis:6379/0` |
| `VLLM_MODEL` | Model identifier for vLLM | `meta-llama/Meta-Llama-3-70B-Instruct` |
| `SGLANG_MAX_TOKENS` | Max tokens per generation | `1024` |
| `JWT_SECRET` | HS256 secret for JWT | `***` |
| `AWS_REGION` | AWS region for services | `us-east-1` |

---  

*End of document*
