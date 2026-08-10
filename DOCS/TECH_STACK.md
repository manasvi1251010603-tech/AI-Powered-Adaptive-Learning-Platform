# AI-Powered Adaptive Learning Platform

## Technical Stack Specification (v1.0)

**Status:** Approved MVP baseline\
**Based on:** `PROJECT_BLUEPRINT.md` v1.0 and `UI_DESIGN_SYSTEM.md` v1.0

## 1. Purpose

This is the technical source of truth for implementation. Every AI
coding assistant must read the Blueprint, UI Design System, and this
document before generating or modifying code.

The product is being built by a first-time full-stack developer using
AI. Therefore Version 1 uses a **modular monolith**, not a distributed
microservice architecture. The system must be modular enough to split
later, but MVP prioritizes understanding, debugging, low cost, and
reliable integration.

Do not introduce Kubernetes, Kafka, Terraform, multiple databases,
GraphQL federation, or microservices merely for architectural prestige.

## 2. Locked MVP Stack

  Layer             Choice
  ----------------- ----------------------------------------------------------
  Frontend          Next.js + React + TypeScript
  Styling           Tailwind CSS
  Components        shadcn/ui
  Animation         Motion for React
  Charts            Recharts
  Icons             Lucide React
  Forms             React Hook Form + Zod
  Backend           FastAPI + Python
  API schemas       Pydantic
  ORM               SQLAlchemy 2.x
  Migrations        Alembic
  Database          PostgreSQL
  Vector search     pgvector
  Cache/jobs        Redis
  Background jobs   Celery + Redis
  AI                OpenAI API through a provider abstraction
  Video             FFmpeg + asynchronous workers
  Storage           S3-compatible object storage
  API docs          FastAPI OpenAPI/Swagger
  Testing           Pytest, HTTPX, Vitest, React Testing Library, Playwright
  Quality           Ruff, Black, ESLint, Prettier
  Containers        Docker + Docker Compose
  CI                GitHub Actions
  Source control    Git + GitHub

## 3. Frontend

### Next.js + TypeScript

Use Next.js App Router. Next.js provides file-system routing, modern
React support, and a strong production ecosystem.
citeturn0search0turn0search6

Use strict TypeScript.

### Tailwind CSS

Implement the exact tokens from `UI_DESIGN_SYSTEM.md`. Do not invent new
colors, spacing, radii, or shadows without updating the design system.

### shadcn/ui

Use for accessible primitives such as dialogs, sheets, tabs, forms,
dropdowns, tooltips, and toasts. Adapt them to the project's tokens
instead of keeping default styling.

### Motion

Use for meaningful state changes and feedback only.

### Recharts

Use for mastery trends, study time, quiz performance, learning progress,
and time saved. The design system explicitly identifies Recharts as the
preferred chart library and Chart.js as fallback. fileciteturn6file4

Build the Knowledge Graph and Mastery Fill as custom SVG/React
components.

### Lucide

Use Lucide icons. The design system specifies outlined icons by default
and filled icons for active/completed states. fileciteturn6file5

### API client

Use native `fetch` behind a centralized typed API client. Do not scatter
API URLs through components.

### State

Start with React state/context and server data. Do not introduce Redux
unless real complexity requires it. Evaluate Zustand before Redux if
global client state becomes necessary.

## 4. Backend

### FastAPI + Python

Use FastAPI for the REST API. It provides typed validation, automatic
OpenAPI documentation, async support, testing utilities, and a Python
ecosystem suited to AI/ML. citeturn0search2turn0search3

Use Python 3.12+ unless a dependency requires another supported version.

### Architecture

Use a modular monolith:

``` text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── db/
│   ├── modules/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── subjects/
│   │   ├── taxonomy/
│   │   ├── assessments/
│   │   ├── knowledge_graph/
│   │   ├── learning_paths/
│   │   ├── recommendations/
│   │   ├── content/
│   │   ├── videos/
│   │   ├── tutor/
│   │   ├── analytics/
│   │   ├── gamification/
│   │   ├── notifications/
│   │   └── billing/
│   ├── ai/
│   │   ├── providers/
│   │   ├── prompts/
│   │   ├── schemas/
│   │   └── evaluation/
│   └── workers/
└── tests/
```

Keep module boundaries clear so services can be extracted later if
required.

### REST, not GraphQL, for MVP

Use:

``` text
/api/v1/auth
/api/v1/assessments
/api/v1/knowledge-graph
/api/v1/learning-paths
/api/v1/recommendations
/api/v1/videos
/api/v1/tutor
/api/v1/analytics
```

The original blueprint mentions a GraphQL BFF, but REST + OpenAPI is
deliberately selected for MVP because it is easier to learn, debug,
test, and integrate with FastAPI.

## 5. Database

### PostgreSQL

PostgreSQL is the single source of truth for MVP. Store users, roles,
subjects, concepts, prerequisites, learner profiles, assessments,
mastery, paths, content metadata, video segments, events, analytics,
achievements, notifications, certificates, and subscriptions.

The blueprint identifies PostgreSQL as the primary OLTP store.
fileciteturn6file10

### SQLAlchemy + Alembic

Use SQLAlchemy 2.x and Alembic migrations. Never manually modify
production schema.

### Knowledge graph

The blueprint allows Neo4j or PostgreSQL+AGE. For MVP, use PostgreSQL
tables for concepts, prerequisite relationships, and learner mastery.
fileciteturn6file10

Do not add Neo4j until measured graph complexity requires it.

### pgvector

Use PostgreSQL + pgvector for embeddings and semantic retrieval. Do not
add Pinecone in MVP.

### Redis

Use Redis for caching, rate limiting, temporary data, and Celery's
broker. Redis is never the source of truth.

## 6. AI

### OpenAI

Use OpenAI as the initial provider, accessed only from the backend. The
official SDK supports server-side API calls through the Responses API;
API keys must remain secret. citeturn1search1

Use AI for:

-   adaptive question generation
-   question explanations
-   concept analysis assistance
-   AI tutor
-   recommendations
-   video concept extraction
-   video segmentation assistance
-   summaries and notes
-   AI insights

### Provider abstraction

Use:

``` text
ai/
└── providers/
    ├── base.py
    └── openai_provider.py
```

Do not scatter provider-specific calls throughout the application.

Use environment variables for model selection:

``` text
OPENAI_MODEL_GENERAL=
OPENAI_MODEL_FAST=
OPENAI_MODEL_REASONING=
OPENAI_EMBEDDING_MODEL=
```

Verify model availability when implementation begins rather than
hard-coding a model name into architecture documentation. OpenAI
provides a model-list endpoint for current availability.
citeturn1search6

## 7. Adaptive Assessment

The LLM generates questions, but deterministic application logic
controls mastery.

``` text
Learner Profile
↓
Concept Taxonomy
↓
Current Mastery
↓
Select Concept + Difficulty
↓
LLM Generates Question
↓
Validate Output
↓
Learner Answers
↓
Score Answer
↓
Update Mastery
↓
Select Next Question
```

Never let an LLM directly become the authoritative source of learner
mastery.

The blueprint requires dynamic AI-generated questions, real-time
difficulty adjustment, concept-level scoring, and continuous graph
updates. fileciteturn6file11

## 8. Knowledge Graph

Represent:

``` text
Concept
├── mastery_score
├── mastery_state
├── confidence
├── attempts
├── correct_attempts
├── last_assessed
├── last_revised
└── decay_state
```

States:

-   unknown
-   weak
-   partial
-   mastered

Prerequisite relationships are first-class data.

The graph is the central personalization state.

## 9. AI Tutor / RAG

The tutor must be grounded in the learner's graph and approved learning
content.

Pipeline:

``` text
Question
↓
Current Concept
↓
Learner Graph State
↓
Retrieve Relevant Content
↓
Build Context
↓
LLM
↓
Validate
↓
Answer
```

Context may include learner mastery, relevant transcripts, notes,
documentation, exercises, learning goal, and recent mistakes.

## 10. Video Intelligence

Use FFmpeg for media processing.

Pipeline:

``` text
Upload
↓
Object Storage
↓
Background Job
↓
Extract Audio
↓
Speech-to-Text
↓
Transcript
↓
Concept Detection
↓
Timestamp Segmentation
↓
Confidence Check
↓
Instructor Review
↓
Publish
```

Video processing must be asynchronous.

The blueprint explicitly requires AI video segmentation, timestamped
concept chapters, and instructor review before publishing.
fileciteturn6file13

The learner must be able to override an AI skip.

## 11. Storage

Use S3-compatible object storage for:

-   videos
-   thumbnails
-   PDFs
-   certificates
-   transcripts
-   processed media

PostgreSQL stores metadata and object references, not large video
binaries.

## 12. Authentication

MVP:

-   email/password
-   password hashing
-   JWT access tokens
-   refresh tokens
-   email verification
-   password reset
-   role-based authorization

Roles:

``` text
student
instructor
admin
```

Future:

-   Google OAuth
-   GitHub OAuth
-   MFA
-   institutional SSO

Never store plaintext passwords or expose API keys to the browser.

## 13. Analytics

Use PostgreSQL for MVP analytics.

Record append-only events such as:

``` text
question_answered
assessment_completed
quiz_submitted
video_started
video_watched
segment_skipped
tutor_interaction
lesson_completed
revision_completed
path_completed
```

Calculate:

-   mastery
-   study hours
-   quiz accuracy
-   streak
-   time saved
-   weak concepts
-   strong concepts
-   video completion
-   retention
-   learning trends
-   predicted mastery

Do not add BigQuery/Snowflake until PostgreSQL analytics becomes a
measured bottleneck.

## 14. Notifications

MVP:

-   in-app notifications
-   email

Use for:

-   revision due
-   streak reminders
-   mastery achieved
-   assessment completion
-   learning-path updates

Push notifications are future scope.

## 15. Gamification

Store:

-   XP
-   streaks
-   badges
-   achievements
-   leaderboard data

Gamification remains secondary to learning mastery and follows the
restrained visual rules in the design system.

## 16. Testing

### Backend

-   Pytest
-   HTTPX
-   FastAPI test client

### Frontend

-   Vitest
-   React Testing Library

### End-to-end

-   Playwright

Critical flow:

``` text
Register
↓
Select Subject
↓
Choose Goal
↓
Adaptive Assessment
↓
Concept Analysis
↓
Learning Path
↓
Recommended Resource
↓
Quiz
↓
Updated Analytics
```

## 17. Code Quality

Python:

-   Ruff
-   Black
-   type hints

TypeScript:

-   ESLint
-   Prettier
-   strict TypeScript

Do not disable type checking simply to remove errors.

## 18. Docker

Use Docker Compose for local development.

MVP services:

``` text
frontend
backend
postgres
redis
```

Do not create a container for every conceptual module.

## 19. GitHub and CI

Use GitHub.

Recommended branches:

``` text
main
feature/...
fix/...
```

Commit prefixes:

``` text
feat:
fix:
docs:
refactor:
test:
chore:
```

Use GitHub Actions for:

``` text
install
↓
lint
↓
type-check
↓
tests
↓
frontend build
↓
backend build
```

Do not use Kubernetes, ArgoCD, or Terraform for MVP.

## 20. Deployment

### Frontend

Use Vercel or another managed Next.js-compatible host.

### Backend

Use a managed container platform.

### Database

Use managed PostgreSQL.

### Redis

Use managed Redis.

### Storage

Use S3-compatible object storage.

Exact providers will be chosen during deployment based on current
pricing, limits, and student-project needs.

## 21. Security

Required from the beginning:

-   HTTPS in production
-   password hashing
-   token expiration
-   refresh-token rotation
-   role checks
-   input validation
-   CORS
-   rate limiting
-   secure headers
-   secret management
-   audit logs

Never commit `.env` files containing secrets.

## 22. Environment Variables

``` text
DATABASE_URL=
REDIS_URL=
JWT_SECRET_KEY=
JWT_REFRESH_SECRET_KEY=

OPENAI_API_KEY=
OPENAI_MODEL_GENERAL=
OPENAI_MODEL_FAST=
OPENAI_MODEL_REASONING=
OPENAI_EMBEDDING_MODEL=

STORAGE_ENDPOINT=
STORAGE_BUCKET=
STORAGE_ACCESS_KEY=
STORAGE_SECRET_KEY=
STORAGE_REGION=

EMAIL_PROVIDER=
EMAIL_API_KEY=
EMAIL_FROM=

NEXT_PUBLIC_API_BASE_URL=

SENTRY_DSN=

PAYMENT_PROVIDER_KEY=
PAYMENT_WEBHOOK_SECRET=
```

No real values belong in GitHub.

## 23. AI Cost Control

Use:

1.  caching
2.  model tiering
3.  structured outputs
4.  batching
5.  deduplication
6.  token limits
7.  prompt versioning
8.  usage tracking

For large non-interactive workloads, OpenAI's Batch API can be
considered later. citeturn1search0

## 24. AI Evaluation

Maintain evaluation datasets for:

-   question quality
-   difficulty calibration
-   concept tagging
-   video segmentation
-   tutor correctness
-   recommendation relevance

Every AI feature should have measurable evaluation criteria rather than
relying only on subjective inspection.

## 25. Repository Structure

``` text
AI-Adaptive-Learning-Platform/
├── README.md
├── LICENSE
├── .gitignore
├── docker-compose.yml
├── docs/
│   ├── PROJECT_BLUEPRINT.md
│   ├── UI_DESIGN_SYSTEM.md
│   ├── TECH_STACK.md
│   ├── SCREEN_SPECIFICATION.md
│   ├── DATABASE_SCHEMA.md
│   ├── API_SPECIFICATION.md
│   ├── AI_ARCHITECTURE.md
│   ├── DEVELOPMENT_SETUP.md
│   ├── TESTING_STRATEGY.md
│   └── DEPLOYMENT.md
├── frontend/
├── backend/
├── database/
├── ai/
└── .github/
    └── workflows/
```

## 26. Technologies Explicitly Deferred

### Kubernetes

Not needed until traffic and service complexity justify it.

### Kafka

Not needed for MVP. Use application events and Celery/Redis first.

### Neo4j

Not needed until PostgreSQL graph traversal becomes a measured
bottleneck.

### Elasticsearch/OpenSearch

Not needed until PostgreSQL search becomes insufficient.

### Pinecone

Not needed while pgvector handles MVP semantic retrieval.

### BigQuery/Snowflake

Not needed until analytics volume requires a warehouse.

### GraphQL

Not needed while REST + OpenAPI is sufficient.

### Terraform

Not needed while deployment remains simple and managed.

### ArgoCD

Not needed while GitHub Actions plus managed deployment is sufficient.

### Microservices

Not needed for MVP. Use modular boundaries and extract services later if
measurement justifies it.

## 27. Scalability Strategy

### 100 users

``` text
Next.js
+
FastAPI
+
PostgreSQL
+
Redis
+
Object Storage
```

### 1,000 users

Add:

-   caching
-   background workers
-   indexes
-   monitoring
-   connection pooling

### 10,000 users

Evaluate:

-   multiple backend instances
-   dedicated workers
-   CDN
-   database read replicas
-   analytics aggregation

### 100,000+ users

Evaluate:

-   service extraction
-   event streaming
-   dedicated graph database
-   dedicated vector database
-   analytics warehouse
-   distributed video processing
-   regional deployment

Scale because measurements require it, not because the architecture
diagram looks impressive.

## 28. Non-Negotiable Rules

1.  Read the three core documents before generating code.
2.  Never invent a new technology without documenting why.
3.  Never expose secrets in frontend code.
4.  Never allow an LLM to directly decide authoritative mastery.
5.  Keep the Knowledge Graph as the central personalization state.
6.  Keep PostgreSQL as the MVP source of truth.
7.  Keep AI providers behind an abstraction layer.
8.  Keep video processing asynchronous.
9.  Human-review AI-generated video segmentation before publication.
10. Make mastery-changing actions traceable.
11. Version AI prompts/models and generated artifacts.
12. Do not over-engineer infrastructure before the need exists.
13. Test every major feature.
14. Document major architectural changes.
15. Update this file whenever a locked technology changes.

## 29. Relationship Between Core Documents

``` text
PROJECT_BLUEPRINT.md
        ↓ WHAT
UI_DESIGN_SYSTEM.md
        ↓ HOW IT LOOKS
TECH_STACK.md
        ↓ HOW IT IS BUILT
SCREEN_SPECIFICATION.md
        ↓ EACH SCREEN
DATABASE_SCHEMA.md
        ↓ DATA
API_SPECIFICATION.md
        ↓ COMMUNICATION
AI_ARCHITECTURE.md
        ↓ INTELLIGENCE
IMPLEMENTATION
```

## 30. Final Architecture

``` text
                    USER
                     │
                     ▼
             Next.js Frontend
                     │
                 REST API
                     │
                     ▼
              FastAPI Backend
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
 PostgreSQL        Redis       Object Storage
       │             │             │
       │             ▼             │
       │       Background Jobs     │
       │             │             │
       ▼             ▼             ▼
 Knowledge Graph   AI/Video      Media
       │           Workers
       │
       ├── Adaptive Assessment
       ├── Learning Paths
       ├── Recommendations
       ├── AI Tutor / RAG
       └── Analytics
                     │
                     ▼
                OpenAI API
```

The core product loop remains:

``` text
Assess
  ↓
Diagnose
  ↓
Knowledge Graph
  ↓
Personalized Path
  ↓
Teach
  ↓
Practice
  ↓
Re-assess
  ↓
Update Graph
  ↓
Analytics
  ↓
Repeat
```

**End of TECH_STACK.md**
