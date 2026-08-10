# AI-Powered Personalized Learning Platform
## Complete Project Blueprint (v1.0)

**Prepared by:** Senior Software Architect
**Document type:** Pre-development architecture & product blueprint
**Audience:** Engineering, Product, AI/ML, DevOps, QA teams

---

## Table of Contents

1. Project Vision
2. Problem Statement
3. Target Audience
4. Goals
5. Unique Selling Points (USP)
6. User Roles
7. Complete Feature List
8. Complete User Journey
9. AI Adaptive Learning Workflow
10. Functional Requirements
11. Non-Functional Requirements
12. High-Level System Architecture
13. Technology Stack Recommendations
14. Folder Structure Recommendation
15. Database Overview
16. Backend Overview
17. Frontend Overview
18. AI Modules Overview
19. Analytics Overview
20. Security Overview
21. Deployment Overview
22. Scalability Plan
23. Future Roadmap
24. Risks and Challenges
25. Suggested Development Milestones

---

## 1. Project Vision

Build an AI-native learning platform where **no learner ever watches or reads content they already know**. The system continuously measures what a learner knows at the *concept level*, not the course level, and dynamically assembles the shortest possible path to mastery — reusing existing high-quality video/text content but re-sequencing and re-cutting it around the learner's actual knowledge gaps.

The long-term vision is a **"knowledge operating system"**: a concept graph that sits underneath any subject, any content library, and any learner, and that gets smarter with every interaction (assessment, video watch, quiz, tutor chat).

---

## 2. Problem Statement

- Traditional e-learning platforms deliver content **linearly and identically** to every learner, regardless of prior knowledge.
- Learners re-watch material they already understand, causing **fatigue, drop-off, and wasted time**.
- Assessments are usually static quizzes that produce a single overall score, giving no insight into *which specific concepts* are weak.
- Video content is treated as an atomic, non-searchable block — there is no way to jump to "the part I don't know."
- Instructors have no visibility into concept-level class performance, only completion percentages.
- There is no continuously updated model of "what does this learner know right now" that all other features (videos, quizzes, tutor, planner) can share.

**Core problem to solve:** *Teach only what is not yet known, prove it with adaptive assessment, and prune everything else — automatically, continuously, and at the concept level.*

---

## 3. Target Audience

| Segment | Description |
|---|---|
| Self-taught learners | Individuals learning programming, data science, math, etc. outside formal institutions |
| University/college students | Supplementing coursework, exam prep, filling specific gaps |
| Bootcamp learners | Fast-paced, need efficient gap-filling rather than full re-teaching |
| Working professionals (upskilling) | Time-constrained, need to skip known basics and reach advanced topics fast |
| Instructors / content creators | Want analytics on concept-level class performance, not just video views |
| Corporate L&D teams | Need to certify employee skill levels efficiently at scale |
| Educational institutions (B2B) | White-labeled adaptive learning for their own course catalogs |

---

## 4. Goals

1. Reduce average time-to-mastery per subject by dynamically skipping known content.
2. Provide concept-level (not course-level) diagnostic accuracy for every learner.
3. Maintain a continuously updated, explainable knowledge graph per learner per subject.
4. Automatically segment any uploaded video into concept-tagged, timestamped chapters.
5. Deliver a closed adaptive loop: **Assess → Diagnose → Teach → Re-assess → Update**.
6. Give instructors and admins actionable, concept-level analytics.
7. Keep the system content-agnostic — it should work across subjects (STEM, languages, business, etc.).
8. Build an architecture that supports scaling to millions of learners and large video libraries.

---

## 5. Unique Selling Points (USP)

| # | USP | Why It Matters |
|---|---|---|
| 1 | **AI Video Segmentation & Auto-Skip** | Learners jump straight to the exact timestamp of the concept they don't know; no other mainstream LMS does this at concept-granularity |
| 2 | **Dynamic Adaptive Assessment Engine** | Questions are generated in real time by AI and difficulty adapts per answer — not a static question bank |
| 3 | **Concept-Level Knowledge Graph** | Every learner has a live graph of mastered / partial / weak concepts, not a single score |
| 4 | **Closed-Loop Personalization** | Every learner action (quiz, video, tutor chat) feeds back into the graph and re-personalizes what comes next |
| 5 | **Time-Saved Metric** | The platform explicitly measures and shows learners how much time AI skipping saved them — a tangible, marketable value proposition |
| 6 | **AI Tutor Grounded in the Knowledge Graph** | The tutor knows exactly what the learner has and hasn't mastered, so explanations are targeted, not generic |
| 7 | **Subject-Agnostic Graph Engine** | Same core engine powers Python, DSA, ML, or any other domain via a pluggable concept-taxonomy layer |

---

## 6. User Roles

| Role | Description | Key Permissions |
|---|---|---|
| **Student / Learner** | Primary end user consuming personalized paths | Take assessments, view knowledge graph, watch segmented videos, use AI tutor, track progress |
| **Instructor / Content Creator** | Uploads courses/videos, defines concept taxonomies (or approves AI-suggested ones) | Upload content, view class-level concept analytics, edit AI-generated segments, respond to flagged content |
| **Admin** | Platform operator | User management, content moderation, subscription/billing, system configuration, global analytics |
| **Content Reviewer (optional, Phase 2)** | QA for AI-generated segments/questions | Approve/reject AI-generated video segments and assessment items |
| **Super Admin / Org Owner (B2B)** | Manages an institutional tenant | Manage instructors, cohorts, branding, org-level reporting |
| **System (AI Agents)** | Non-human actor | Assessment generation, video segmentation, knowledge graph updates, tutoring, recommendation |

### 6.1 Learner Profile

To move personalization beyond pure concept mastery, every learner has a **Learner Profile** captured during onboarding and refined continuously from behavior. The Recommendation Service (Section 18) and Learning Path Service both read this profile — it does not change *what* a learner must learn (that's the knowledge graph's job), but it changes *how* content is selected, sequenced, and paced.

| Attribute | Description | Example Values |
|---|---|---|
| **Learning style** | Preferred content modality | Visual (video-first), Reading/Text (notes/docs-first), Practice-first (exercises-first), Mixed |
| **Learning speed** | Observed and self-reported pace | Fast, Moderate, Slow — also inferred from time-to-mastery history |
| **Preferred study duration** | Typical session length the learner wants to commit to | 15 min, 30 min, 45–60 min, 60+ min |
| **Preferred study time** | Time of day the learner is most active/available | Morning, Afternoon, Evening, Late night |

- Captured initially via a short onboarding questionnaire (not the adaptive assessment — that measures *knowledge*, not *preference*).
- Refined over time from engagement signals (e.g., actual session lengths, skip/re-watch behavior, time-of-day activity) via the Analytics Service, feeding back into the profile.
- Consumed by the Recommendation Service to prefer, e.g., video over text for a Visual learner, or to size a recommended resource bundle to fit a 30-minute session.
- Consumed by the Study Planner (Section 7.3) to auto-schedule sessions at the learner's preferred time and duration.

### 6.2 Learning Goals

At subject selection, the learner also selects a **Learning Goal**, which shapes how the Learning Path Service weights, sequences, and scopes concepts (in addition to what the knowledge graph says is unmastered).

| Goal | Path Adaptation |
|---|---|
| **Interview Preparation** | Prioritizes high-frequency interview topics and problem-solving practice; emphasizes coding exercises and timed quizzes over long-form video |
| **College Exams** | Aligns path to a syllabus/curriculum taxonomy; emphasizes notes, past-paper-style questions, and revision/flashcards |
| **Build Projects** | De-prioritizes theory depth on mastered fundamentals; fast-tracks toward project-applicable concepts; emphasizes project resources and documentation |
| **Learn from Scratch** | Full breadth-first path through the concept graph from foundational nodes, minimal skipping even for adjacent quick wins |
| **Revision** | Skips teaching entirely for mastered/partial concepts; path consists mainly of adaptive quizzes and flashcards to refresh and re-validate mastery |
| **Advanced Mastery** | Extends the path beyond the base taxonomy into advanced/edge-case concepts and projects, raises the mastery threshold required to mark a concept "complete" |

The selected goal is stored alongside the Learner Profile and is re-selectable per subject (a learner can pursue "Learn from Scratch" in one subject and "Interview Preparation" in another).

---

## 7. Complete Feature List

### 7.1 Core Features
- User authentication & profile management (student/instructor/admin)
- Subject/skill catalog and selection
- Concept taxonomy management (per subject, hierarchical: Subject → Topic → Concept → Sub-concept)
- Knowledge graph engine (per learner, per subject)
- **Learner Profile capture & management** (learning style, learning speed, preferred study duration, preferred study time — see Section 6.1)
- **Learning Goal selection** (Interview Preparation, College Exams, Build Projects, Learn from Scratch, Revision, Advanced Mastery — see Section 6.2)
- **Prerequisite validation engine** (verifies prerequisite concepts are satisfied before a concept is added to a learning path — see Section 9.1 and 10)
- Personalized learning path generator (adapted by knowledge graph + Learner Profile + Learning Goal)
- Content library management (videos, notes, documentation, coding exercises, projects, flashcards, articles)
- Progress tracking engine
- Notification system (email/push/in-app)
- Subscription & billing (B2C/B2B)

### 7.2 AI Features
- AI Adaptive Assessment Engine (dynamic question generation + IRT-style difficulty adaptation)
- Concept-Level Diagnostic Analyzer (post-assessment mastery scoring per concept)
- Knowledge Graph Builder & Updater
- AI Video Segmentation Engine (concept detection + timestamping)
- **Prerequisite Validation module** (graph traversal check prior to path generation, prevents out-of-order teaching)
- **Multi-format AI recommendation engine** — recommends, per concept: videos, notes, documentation, coding exercises, projects, flashcards, and articles, weighted by the learner's Learning Style, Learning Speed, and Learning Goal (see Section 6.1, 6.2, 18)
- AI Tutor (conversational, context-aware of learner's knowledge graph)
- AI-generated quiz questions (post-lesson, revision, spaced repetition)
- AI-generated insights (weak/strong concept summaries, predicted mastery, ETA to completion)
- Retention/forgetting-curve prediction model
- Auto-tagging of new content into taxonomy via NLP/embeddings

### 7.3 Student Features
- **Learner Profile setup** (learning style, learning speed, preferred study duration/time)
- **Learning Goal selection per subject** (Interview Prep, College Exams, Build Projects, Learn from Scratch, Revision, Advanced Mastery)
- Adaptive onboarding assessment
- Personal knowledge graph visualization
- Personalized learning path / roadmap view (goal- and profile-adapted)
- Smart video player with auto-skip and chapter markers
- AI Tutor chat (text; voice optional in later phase)
- **Multi-format resource recommendations** per concept: videos, notes, documentation, coding exercises, projects, flashcards, articles
- Practice question sets per concept
- Revision scheduler (spaced repetition)
- Study planner & calendar integration (auto-scheduled around preferred study time/duration)
- Progress dashboard (concept mastery, streaks, time saved)
- Gamification (XP, badges, streaks, leaderboards)
- Bookmarks/notes on videos
- Downloadable certificates on path completion

### 7.4 Instructor Features
- Course/video upload & management
- Review/edit AI-generated video segments and concept tags
- Review/edit AI-generated assessment questions
- Class-level concept mastery analytics (heatmaps)
- Student progress drill-down
- Content performance analytics (which segments are most skipped/re-watched)
- Discussion/Q&A moderation

### 7.5 Admin Features
- User & role management
- Subject/taxonomy management (global concept graph templates)
- Content moderation & approval workflows
- Billing & subscription management
- Platform-wide analytics (engagement, retention, revenue)
- AI model configuration/version management (prompt/model versioning, feature flags)
- System health & audit logs

### 7.6 Future Features
- Voice-based AI tutor
- Mobile offline mode with sync
- Peer-to-peer study groups matched by complementary knowledge gaps
- AI-generated original video/animation content for weak concepts
- Multi-language content generation & dubbing
- Employer/institution skill-certification API
- AR/VR immersive concept simulations
- Marketplace for third-party concept taxonomies and content packs

### 7.7 Feature Release Versioning (MVP / V2 / V3)

The features above are organized by *type* (Core/AI/Student/Instructor/Admin/Future). The table below organizes the same features by **release version**, so engineering can scope sprints and milestones (see Section 25) against a concrete cut line. This mapping is additive — it does not remove or alter any feature listed in 7.1–7.6.

| Version | Scope | Included Features |
|---|---|---|
| **MVP (Version 1)** | The closed adaptive loop, single-user, single-tenant, minimum viable personalization | User auth & profile management · Subject selection · Learner Profile capture (style, speed, duration, time) · Learning Goal selection (all six goals, basic weighting) · Concept taxonomy (1–2 pilot subjects) · Knowledge graph engine (core CRUD + mastery scoring) · Prerequisite validation engine · AI Adaptive Assessment Engine · Concept-Level Diagnostic Analyzer · Personalized learning path generator · AI Video Segmentation Engine (basic, instructor-reviewed) · Smart video player with auto-skip · Multi-format recommendation engine (videos + notes + practice questions only, at MVP) · AI Tutor (text, basic RAG) · Adaptive quiz + revision loop · Progress dashboard (core metrics: overall mastery, concept mastery, study hours, quiz performance) · Instructor upload & AI-segment review tools · Basic admin user/content management |
| **Version 2** | Depth, engagement, and instructor/admin maturity | Full multi-format recommendations (add documentation, coding exercises, projects, flashcards, articles) · Revision scheduler with spaced repetition & mastery decay · Study planner/calendar auto-scheduling by preferred time/duration · Gamification (XP, badges, streaks, leaderboards) · Full analytics dashboard (retention score, time saved, predicted mastery, ETA, AI-generated insights) · Instructor class-level concept heatmaps & content performance analytics · Admin platform-wide analytics, taxonomy management, AI model/prompt version control · Notification system · Billing/subscription management · Content Reviewer role & approval workflows · Auto-tagging of new content via NLP/embeddings · Multi-subject taxonomy support |
| **Version 3** | Scale, ecosystem, and advanced experience | Voice-based AI tutor · Mobile offline mode with sync · Peer-to-peer study groups matched by complementary gaps · AI-generated original video/animation content for weak concepts · Multi-language content generation & dubbing · Employer/institution skill-certification API · AR/VR immersive concept simulations · Marketplace for third-party taxonomies/content packs · Multi-tenant B2B (Super Admin/Org Owner role, institutional SSO, org-level reporting) |

---

## 8. Complete User Journey

**From signup to course/path completion:**

1. **Sign Up / Login** — Student registers (email, OAuth, or SSO for B2B).
2. **Learner Profile Setup** — On first use, learner sets learning style, learning speed (or leaves it to be inferred), preferred study duration, and preferred study time (see Section 6.1).
3. **Select Subject/Skill** — e.g., "Python."
4. **Select Learning Goal** — Interview Preparation, College Exams, Build Projects, Learn from Scratch, Revision, or Advanced Mastery (see Section 6.2).
5. **AI Adaptive Assessment Begins** — AI dynamically generates the first question at medium difficulty.
6. **Adaptive Question Loop** — Each answer adjusts the next question's difficulty and concept focus (branching, not fixed order) until the engine reaches statistical confidence per concept or a max question/time budget.
7. **Concept-Level Analysis Generated** — System computes a mastery percentage per concept (e.g., Variables 100%, Recursion 15%).
8. **Knowledge Graph Constructed** — Concepts are nodes; prerequisite relationships are edges; each node is tagged Mastered / Partial / Weak / Unknown.
9. **Prerequisite Validation** — Before path generation, the system verifies that every candidate concept's prerequisites are already mastered (or explicitly included earlier in the path); unmet prerequisites are auto-inserted ahead of the dependent concept (see Section 9.1, 10).
10. **Personalized Learning Path Generated** — Topological sort over the graph, filtered to non-mastered concepts, respecting validated prerequisite order, and adapted to the learner's Profile and Learning Goal.
11. **Resource Recommendation** — For each concept in the path, the system attaches the best-matching resources — videos, notes, documentation, coding exercises, projects, flashcards, and articles — weighted by the learner's Profile and Goal.
12. **Video Playback with Auto-Skip** — Player loads the recommended video, auto-seeks to the first unmastered concept's timestamp, and visually marks mastered sections as "skipped — you know this."
13. **AI Tutor & Notes** — Learner can ask the AI Tutor questions at any point; tutor responses are grounded in the current concept and the learner's known gaps.
14. **Post-Concept Adaptive Quiz** — Short quiz targeting the just-taught concept, again dynamically generated.
15. **Knowledge Graph Updated** — Node mastery score recalculated using latest quiz + video-engagement signals.
16. **Decision Point:**
    - If mastery ≥ threshold (e.g., 80%): concept marked mastered → next concept unlocked.
    - Else: system recommends revision resources (alternate video/notes/flashcards) and issues another adaptive quiz.
17. **Repeat Steps 12–16** for each concept in the path.
18. **Analytics Dashboard Updates Continuously** — streaks, study hours, time saved, retention score, predicted mastery.
19. **Path Completion** — When all concepts in the subject reach threshold, learner receives a completion certificate and a final mastery report.
20. **Retention Loop** — Spaced-repetition engine schedules periodic micro-quizzes to prevent forgetting; knowledge graph decays scores over time using a forgetting-curve model, prompting re-engagement.

---

## 9. AI Adaptive Learning Workflow

This section formalizes the closed adaptive loop introduced conceptually in Section 8 into a **named, reusable system workflow**. Every architecture decision in this document (services, events, data model) exists to support this cycle running efficiently and repeatedly for every learner, on every concept.

### 9.1 Workflow Diagram

```
 Subject Selection
        │
        ▼
 Adaptive Assessment ──────────► (AI dynamically generates questions;
        │                         difficulty adapts per answer)
        ▼
 Concept-Level Analysis ───────► (Per-concept mastery %, not one score)
        │
        ▼
 Knowledge Graph (Build/Update) ► (Nodes: concepts; Edges: prerequisites;
        │                         Status: Mastered/Partial/Weak/Unknown)
        ▼
 Prerequisite Validation ──────► (Confirms path only introduces concepts
        │                         whose prerequisites are satisfied)
        ▼
 Personalized Learning Path ───► (Filtered to non-mastered concepts,
        │                         adapted to Learner Profile + Learning Goal)
        ▼
 AI-Recommended Resources ─────► (Video segments, notes, docs, exercises,
        │                         projects, flashcards, articles)
        ▼
 AI Tutor + Guided Practice ───► (Context-aware help grounded in the
        │                         learner's current graph state)
        ▼
 Adaptive Quiz ─────────────────► (Concept-targeted, dynamically generated)
        │
        ▼
 Knowledge Graph Update ───────► (Recomputes mastery from quiz + engagement
        │                         signals; feeds Analytics)
        ▼
 Analytics Dashboard Update ───► (Mastery, streaks, time saved, insights)
        │
        ▼
   Mastery ≥ Threshold? ────────────────────────┐
        │                                          │
       Yes                                        No
        │                                          │
        ▼                                          ▼
 Unlock Next Concept                    Revision Loop:
 (re-enter Path at next node)           recommend alternate resources →
                                          Adaptive Quiz → Knowledge Graph
                                          Update (repeat until threshold met)
```

### 9.2 Workflow Stage Ownership

| Stage | Owning Service (from Section 16) | Primary Data Touched |
|---|---|---|
| Subject Selection | Content Service | `Subject`, `LearningGoal` (Section 6.2), `LearnerProfile` (Section 6.1) |
| Adaptive Assessment | Assessment Service | `AssessmentItem`, `Event: question_answered` |
| Concept-Level Analysis | Assessment Service → Knowledge Graph Service | `ConceptMastery` (initial) |
| Knowledge Graph Build/Update | Knowledge Graph Service | `Concept`, `PREREQUISITE_OF`, `LearnerConceptMastery` |
| Prerequisite Validation | Learning Path Service (reads Knowledge Graph Service) | Graph traversal over `PREREQUISITE_OF` edges |
| Personalized Learning Path | Learning Path Service | `LearningPath`, `PathStep`, filtered by `LearnerProfile` + `LearningGoal` |
| AI-Recommended Resources | Recommendation Service | `Resource` (video/notes/docs/exercise/project/flashcard/article) |
| AI Tutor + Guided Practice | AI Tutor Service | RAG context (graph state + content chunks) |
| Adaptive Quiz | Assessment Service | `AssessmentItem`, `Event: quiz_submitted` |
| Knowledge Graph Update | Knowledge Graph Service | `LearnerConceptMastery` (recomputed) |
| Analytics Dashboard Update | Analytics Service | Aggregated metrics (Section 19) |
| Unlock / Revision Decision | Learning Path Service | Threshold comparison, re-entry point into path |

### 9.3 Design Implication

Because this cycle repeats **per concept, continuously**, the Knowledge Graph Service must treat every stage's output as an event, not a direct database write from another service (see Section 12's event-driven principle). This keeps the workflow restart-safe: if a learner abandons a session mid-quiz, the graph simply reflects the last completed event, and the workflow naturally resumes from the correct stage on return.

---

## 10. Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | System shall allow learners to select a subject and begin an adaptive assessment |
| FR-2 | System shall generate assessment questions dynamically via AI, not from a static bank alone |
| FR-3 | System shall adjust question difficulty based on the learner's previous answers in real time |
| FR-4 | System shall compute and persist per-concept mastery scores after assessment |
| FR-5 | System shall construct/update a knowledge graph per learner per subject |
| FR-6 | System shall generate a personalized learning path from the knowledge graph, respecting concept prerequisites |
| FR-6a | System shall capture and persist a Learner Profile (learning style, learning speed, preferred study duration, preferred study time) and use it to influence resource selection and path pacing |
| FR-6b | System shall allow the learner to select a Learning Goal per subject (Interview Preparation, College Exams, Build Projects, Learn from Scratch, Revision, Advanced Mastery) and shall adapt path scope/sequencing/threshold accordingly |
| FR-6c | System shall validate that every concept's prerequisites are satisfied (mastered or already scheduled earlier in the path) before adding that concept to a learning path, and shall auto-insert any unmet prerequisite concepts |
| FR-7 | System shall recommend resources per concept across multiple formats: videos, notes, documentation, coding exercises, projects, flashcards, and articles |
| FR-8 | System shall segment uploaded videos into concept-based, timestamped chapters via AI |
| FR-9 | Video player shall auto-skip to the first unmastered segment based on the learner's knowledge graph |
| FR-10 | System shall update the knowledge graph after every quiz, video watch, and tutor interaction |
| FR-11 | System shall provide an AI Tutor that is context-aware of the learner's current concept and mastery state |
| FR-12 | System shall provide an analytics dashboard with the metrics listed in Section 19 |
| FR-13 | System shall support instructor upload/review workflows for videos and AI-generated segments/questions |
| FR-14 | System shall support admin management of users, content, taxonomy, and billing |
| FR-15 | System shall issue completion certificates when all path concepts reach mastery threshold |
| FR-16 | System shall support spaced-repetition scheduling and mastery decay over time |
| FR-17 | System shall support gamification elements (XP, streaks, badges, leaderboards) |
| FR-18 | System shall log all AI-generated content (questions, segments, insights) with versioning for auditability |

---

## 11. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Assessment question generation response time < 2s (p95); video segmentation is async/background |
| Scalability | Support horizontal scaling to 1M+ concurrent learners; knowledge graph service must scale independently |
| Availability | 99.9% uptime SLA for core learning services |
| Reliability | Knowledge graph updates must be idempotent and eventually consistent within 5s |
| Security | End-to-end encryption in transit (TLS 1.3); encryption at rest for PII and assessment data |
| Privacy | GDPR/FERPA/COPPA-aware design; configurable data residency for B2B tenants |
| Maintainability | AI prompts/models versioned and swappable without redeploying core services |
| Observability | Full tracing across assessment → graph update → recommendation pipeline |
| Cost Efficiency | Cache AI outputs (segments, generated questions) to avoid redundant model calls |
| Accessibility | WCAG 2.1 AA compliance for all learner-facing UI |
| Portability | Subject/taxonomy engine must be content- and domain-agnostic (works beyond programming) |
| Internationalization | UI and AI-generated content support multi-language from Phase 2 |

---

## 12. High-Level System Architecture

**Architectural style:** Microservices, event-driven, with a shared **Knowledge Graph Service** acting as the system's source of truth for "what does this learner know."

```
                                ┌─────────────────────────┐
                                │        Client Apps        │
                                │ Web (React) / Mobile (RN) │
                                └───────────┬────────────┘
                                                │  GraphQL/REST via API Gateway
                                ┌───────────▼────────────┐
                                │        API Gateway / BFF   │
                                └───────────┬────────────┘
        ┌──────────────┬──────────────┼──────────────┬───────────────┬──────────────┐
        ▼              ▼              ▼              ▼               ▼              ▼
 ┌─────────────┐┌──────────────┐┌──────────────┐┌──────────────┐┌─────────────┐┌─────────────┐
 │   Auth &     ││  Assessment   ││  Knowledge    ││   Learning    ││    Video     ││   AI Tutor   │
 │   User Svc   ││   Engine Svc  ││  Graph Svc    ││   Path Svc    ││ Intelligence ││    Service   │
 └─────────────┘└──────────────┘└──────────────┘└──────────────┘└─────────────┘└─────────────┘
        │              │              │              │               │              │
        └──────────────┴──────────────┴──────┬───────┴───────────────┴──────────────┘
                                                             │
                                          ┌────────────▼────────────┐
                                          │     Event Bus (Kafka/       │
                                          │  Pub/Sub) - domain events   │
                                          └────────────┬────────────┘
                                                             │
                    ┌───────────────────────────┼───────────────────────────┐
                    ▼                                    ▼                                    ▼
        ┌─────────────────┐           ┌─────────────────┐              ┌─────────────────┐
        │  Analytics &         │           │  Notification &      │              │  Content/Media       │
        │  Insights Svc         │           │  Gamification Svc     │              │  Storage (CDN/S3)   │
        └─────────────────┘           └─────────────────┘              └─────────────────┘

                                          ┌────────────────────────┐
                                          │  AI Orchestration Layer   │
                                          │ (LLM calls, embeddings,   │
                                          │  video ML pipeline)        │
                                          └────────────────────────┘
```

**Key architectural principles:**
- The **Knowledge Graph Service** is the single source of truth; all other services read from it and publish events that update it — never write directly to each other's data.
- All learner actions (quiz submitted, video watched, tutor question asked) emit **domain events** on an event bus; the Knowledge Graph Service consumes these to recompute mastery asynchronously.
- The **AI Orchestration Layer** abstracts all LLM/ML calls (question generation, video segmentation, tutoring, insight generation) behind a single internal API so model/provider swaps don't ripple through the codebase.
- Video segmentation runs as an **async pipeline** (upload → transcribe → segment → tag → review) decoupled from the request/response path.

---

## 13. Technology Stack Recommendations

| Layer | Recommendation | Notes |
|---|---|---|
| Frontend (Web) | React + TypeScript, Next.js | SSR for SEO on marketing/course pages, CSR for app |
| Frontend (Mobile) | React Native | Code-sharing with web where practical |
| State Management | Redux Toolkit / React Query | React Query for server-state (graph, path, analytics) |
| API Layer | GraphQL (Apollo/Gateway) + REST for webhooks | GraphQL fits well for nested knowledge-graph queries |
| Backend Services | Node.js (NestJS) or Python (FastAPI) per service | Python favored for AI-heavy services (Assessment, Video Intelligence, Tutor) |
| AI/LLM Orchestration | LangChain/LlamaIndex-style orchestration or custom, backed by Claude models via Anthropic API | Model-agnostic abstraction layer required |
| Video Processing | FFmpeg + Whisper-class ASR for transcription + custom concept-segmentation ML/LLM pipeline | Async worker pool (Celery/RQ or Temporal) |
| Databases | PostgreSQL (relational core), Neo4j or a graph-capable store (or PostgreSQL + AGE) for knowledge graph, Redis (cache/session), Elasticsearch/OpenSearch (search) | See Section 15 for rationale |
| Vector Store | pgvector / Pinecone / Weaviate | Embeddings for content-to-concept matching, semantic search |
| Event Bus | Apache Kafka or Google Pub/Sub | Domain events for graph updates, analytics |
| Object/Media Storage | AWS S3 / GCS + CDN (CloudFront) | Video, notes, certificates |
| Auth | OAuth2/OIDC via Auth0, Cognito, or custom | SSO support for B2B tenants |
| Background Jobs | Temporal.io or Celery/BullMQ | Video pipeline, spaced-repetition scheduler |
| Infra/Orchestration | Kubernetes (EKS/GKE) + Docker | Independent scaling per microservice |
| CI/CD | GitHub Actions + ArgoCD | GitOps deployment |
| Monitoring | Prometheus + Grafana, OpenTelemetry, Sentry | Distributed tracing across AI pipeline |
| Analytics | Segment/Amplitude (product analytics) + custom warehouse (BigQuery/Snowflake) | Feeds instructor/admin dashboards |

---

## 14. Folder Structure Recommendation

```
learning-platform/
├── apps/
│   ├── web/                      # Next.js student/instructor/admin web app
│   └── mobile/                   # React Native app
│
├── services/
│   ├── auth-service/
│   ├── user-service/
│   ├── assessment-service/       # Adaptive question generation + scoring
│   ├── knowledge-graph-service/  # Graph storage, mastery computation, decay
│   ├── learning-path-service/    # Path generation, prerequisite resolution
│   ├── video-intelligence-service/ # Transcription, segmentation, tagging
│   ├── content-service/          # Course/video/notes/practice CRUD
│   ├── ai-tutor-service/         # Conversational tutor, grounded in graph
│   ├── recommendation-service/   # Resource matching per concept
│   ├── analytics-service/        # Metrics aggregation, insights
│   ├── gamification-service/     # XP, badges, streaks, leaderboards
│   ├── notification-service/
│   └── billing-service/
│
├── ai-orchestration/
│   ├── prompts/                  # Versioned prompt templates
│   ├── pipelines/                # Assessment-gen, segmentation, tutoring pipelines
│   ├── model-adapters/           # Provider abstraction (Anthropic, etc.)
│   └── evaluation/               # AI output quality eval harness
│
├── shared/
│   ├── proto/ or graphql-schema/ # Shared API contracts
│   ├── event-schemas/            # Domain event definitions
│   ├── ui-components/            # Shared design system
│   └── utils/
│
├── infra/
│   ├── terraform/
│   ├── k8s/
│   └── ci-cd/
│
├── data/
│   ├── taxonomy-seeds/           # Initial concept taxonomies per subject
│   └── migrations/
│
└── docs/
    ├── architecture/
    ├── api-specs/
    └── runbooks/
```

---

## 15. Database Overview

A **polyglot persistence** approach is recommended — no single database fits all needs.

| Store | Purpose | Key Entities |
|---|---|---|
| **PostgreSQL** (primary OLTP) | Users, subjects, courses, content metadata, assessments, transactions | `users`, `learner_profiles`, `learning_goals`, `subjects`, `courses`, `videos`, `resources`, `questions`, `subscriptions` |
| **Graph DB (Neo4j / PostgreSQL+AGE)** | Knowledge graph: concepts as nodes, prerequisite/related-to edges, per-learner mastery edges | `Concept`, `PREREQUISITE_OF`, `LearnerConceptMastery` |
| **Redis** | Session cache, hot-path caching of active learning-path/graph reads, rate limiting | Session tokens, cached graph snapshots |
| **Elasticsearch/OpenSearch** | Full-text/content search, instructor content discovery | Indexed course/video/note text |
| **Vector DB (pgvector/Pinecone)** | Embeddings for content-to-concept matching, semantic tutor retrieval | Content embeddings, concept embeddings |
| **Object Storage (S3/GCS)** | Raw video files, transcripts, generated segment metadata, certificates | Blob references |
| **Data Warehouse (BigQuery/Snowflake)** | Analytics aggregation, instructor/admin reporting, ML training data | Event history, mastery snapshots over time |

**Core conceptual schema (simplified):**

- `Subject (1) — (N) Concept` (hierarchical: Topic → Concept → Sub-concept)
- `Concept (N) — (N) Concept` via `PREREQUISITE_OF` edges (the graph structure)
- `Learner (1) — (1) LearnerProfile` (learning style, learning speed, preferred study duration, preferred study time — Section 6.1)
- `Learner (1) — (N) LearnerLearningGoal` (per subject: Interview Prep / College Exams / Build Projects / Learn from Scratch / Revision / Advanced Mastery — Section 6.2)
- `Learner (1) — (N) ConceptMastery` (per learner, per concept: score, status, last_updated, confidence)
- `Video (1) — (N) VideoSegment` (each segment tagged to 1..N `Concept`)
- `Resource (N) — (N) Concept` (polymorphic resource types: `video_segment`, `note`, `documentation`, `coding_exercise`, `project`, `flashcard`, `article` — each tagged to 1..N `Concept`, with metadata for Learner Profile matching, e.g. `format`, `estimated_duration_minutes`)
- `Assessment (1) — (N) AssessmentItem` (dynamically generated, linked to `Concept`)
- `LearningPath (1) — (N) PathStep` (ordered, each step referencing a `Concept` + recommended `Resource` set; path generation reads `PrerequisiteValidationResult` before persisting)
- `Event` (append-only log: `quiz_submitted`, `video_watched`, `tutor_interaction`, `segment_skipped`, `profile_updated`, `goal_selected`) — feeds both the Knowledge Graph Service and Analytics.

---

## 16. Backend Overview

**Pattern:** Domain-driven microservices, each owning its own datastore, communicating via well-defined APIs (sync, GraphQL/REST) and domain events (async, Kafka).

| Service | Responsibility |
|---|---|
| Auth/User Service | Identity, roles, profiles, SSO |
| **Learner Profile Service** *(or module within Auth/User Service)* | Owns Learner Profile (style, speed, duration, time — Section 6.1) and per-subject Learning Goal selection (Section 6.2); exposes read API to Learning Path and Recommendation Services |
| Assessment Service | Generates adaptive questions via AI orchestration, scores responses, emits `ConceptScored` events |
| Knowledge Graph Service | Owns the graph; consumes events; recomputes mastery, applies forgetting-curve decay; exposes graph queries |
| Learning Path Service | Reads graph, runs **prerequisite validation** over the candidate concept set, applies topological sort over prerequisites, then re-weights/scopes the ordered path using Learner Profile + Learning Goal before producing the final path |
| Video Intelligence Service | Async pipeline: transcribe → segment → tag concepts → generate timestamps; exposes segment metadata API |
| Recommendation Service | Matches concepts to best-fit resources — videos, notes, documentation, coding exercises, projects, flashcards, articles — using embeddings + heuristics, weighted by Learner Profile and Learning Goal |
| AI Tutor Service | Conversational endpoint; retrieves learner's graph state + relevant content chunks (RAG) before responding |
| Content Service | CRUD for courses/videos/notes/documentation/coding exercises/projects/flashcards/articles; instructor upload workflows |
| Analytics Service | Aggregates events into dashboard metrics; generates AI insights (weak/strong concepts, predictions) |
| Gamification Service | XP, streaks, badges, leaderboard computation |
| Notification Service | Email/push/in-app triggers (streak reminders, revision due, mastery achieved) |
| Billing Service | Subscription management, payment provider integration |

**Communication:** GraphQL BFF aggregates data for the frontend; internal service-to-service calls use gRPC/REST; all mastery-affecting actions are events, not direct writes, to keep the Knowledge Graph Service the single writer of mastery state.

---

## 17. Frontend Overview

| App | Key Screens |
|---|---|
| **Student Web/Mobile App** | Onboarding assessment flow, Knowledge Graph visualization, Learning Path/roadmap, Smart Video Player (with skip markers), AI Tutor chat, Practice/Quiz screens, Study Planner/Calendar, Analytics Dashboard, Gamification (badges/streaks/leaderboard), Certificates |
| **Instructor Dashboard** | Content upload & management, AI segment review/edit tool, class concept-mastery heatmap, student drill-down, content performance analytics |
| **Admin Dashboard** | User/role management, taxonomy editor, content moderation queue, billing/subscriptions, platform-wide analytics, AI model/prompt version control, audit logs |

**Notable UI components requiring special design attention:**
- **Knowledge Graph Visualizer** — interactive node-graph (color-coded by mastery: mastered/partial/weak/unknown), zoomable, filterable by topic.
- **Smart Video Player** — chapter markers derived from AI segments, "skip known section" overlay, progress bar shaded by mastered vs. unmastered regions.
- **Adaptive Assessment UI** — single-question-at-a-time flow with a subtle difficulty/confidence indicator, no visible "score" until concept-level report at the end.
- **Analytics Dashboard** — modular widget grid (see Section 19 for exact metrics).

---

## 18. AI Modules Overview

| Module | Function | Technique |
|---|---|---|
| **Adaptive Assessment Generator** | Dynamically generates next question + adjusts difficulty | LLM-based item generation + Item Response Theory (IRT)-style adaptive selection logic; concept-targeted sampling |
| **Concept-Level Diagnostic Analyzer** | Converts raw answers into per-concept mastery percentages | Bayesian/IRT scoring per concept, weighted by question difficulty and confidence |
| **Knowledge Graph Builder/Updater** | Maintains node states (mastered/partial/weak) and edges (prerequisites) | Graph algorithms + event-driven recomputation; forgetting-curve decay model |
| **Prerequisite Validator** | Confirms every concept in a candidate path has its prerequisites satisfied before inclusion | Graph traversal (DFS/BFS) over `PREREQUISITE_OF` edges; auto-inserts unmet prerequisite concepts ahead of dependents |
| **Learning Path Generator** | Produces ordered concept sequence | Topological sort over prerequisite DAG, filtered to non-mastered nodes, re-weighted/scoped by Learner Profile and Learning Goal (Section 6.1, 6.2) |
| **Video Segmentation Engine** | Splits video into concept-tagged, timestamped chapters | ASR transcription → semantic chunking (embeddings) → LLM concept classification → timestamp alignment |
| **Recommendation Engine** | Matches concepts to best resources across **videos, notes, documentation, coding exercises, projects, flashcards, and articles** | Embedding similarity (concept ↔ content) + engagement/quality signals + Learner Profile weighting (style/speed/duration/time) + Learning Goal weighting |
| **AI Tutor** | Context-aware conversational help | RAG: retrieves learner's graph state + relevant content chunks, grounds LLM responses in current concept |
| **Insight Generator** | Produces natural-language summaries (weak areas, predicted mastery, ETA) | LLM summarization over structured analytics data |
| **Retention/Forgetting Model** | Predicts mastery decay over time, schedules revision | Spaced-repetition algorithm (e.g., SM-2/Leitner-inspired) combined with per-concept decay curves |

**Governance:** All AI outputs (questions, segments, insights) are versioned and logged for auditability; instructors can review/override AI-generated video segments and questions before they go live (human-in-the-loop for quality control in early phases).

---

## 19. Analytics Overview

**Student-facing Analytics Dashboard metrics:**

| Metric | Description |
|---|---|
| Overall mastery | Weighted average mastery across all concepts in a subject |
| Concept mastery | Per-concept mastery breakdown (bar/graph view) |
| Learning streak | Consecutive days of activity |
| Study hours | Total and per-session time spent |
| Quiz performance | Accuracy trends over time, per concept |
| Learning speed | Concepts mastered per hour/week vs. platform average |
| Retention score | Estimated long-term recall likelihood, derived from forgetting-curve model |
| Time saved (AI video skipping) | Minutes/hours skipped due to already-mastered segments |
| Weak concepts | Ranked list, with recommended next actions |
| Strong concepts | Ranked list, for confidence/reinforcement |
| AI-generated insights | Natural-language summary of trends and recommendations |
| Predicted mastery | Forecast of mastery trajectory if current pace continues |
| Estimated completion time | Projected date/hours to reach subject-level mastery |

**Instructor Analytics:** class-level concept heatmaps, content engagement (watch/skip/re-watch per segment), question difficulty calibration, cohort comparison.

**Admin Analytics:** platform engagement (DAU/MAU), retention/churn, revenue, AI cost/usage, content pipeline throughput, taxonomy coverage gaps.

---

## 20. Security Overview

- **Authentication:** OAuth2/OIDC, MFA support, short-lived JWT access tokens + refresh token rotation.
- **Authorization:** Role-based access control (RBAC) enforced at the API Gateway and per-service; row-level security for multi-tenant B2B data.
- **Data protection:** TLS 1.3 in transit; AES-256 at rest for PII and assessment records; field-level encryption for sensitive fields (e.g., minors' data where applicable).
- **Compliance:** Design with GDPR (right to erasure/export), FERPA (educational records), and COPPA (if serving under-13 users) in mind; data residency options for institutional tenants.
- **AI-specific security:** Prompt-injection defenses in the AI Tutor and Assessment services; output filtering before any AI-generated content reaches learners; rate limiting on AI endpoints to control cost and abuse.
- **Content security:** Signed, time-limited URLs for video delivery via CDN; DRM consideration for premium content in later phases.
- **Audit & monitoring:** Immutable audit logs for admin/instructor actions and AI content approvals; anomaly detection on account/billing activity.
- **Secrets management:** Centralized vault (e.g., HashiCorp Vault/Cloud Secrets Manager); no secrets in code or images.

---

## 21. Deployment Overview

- **Containerization:** Every service packaged as a Docker image; deployed on Kubernetes (EKS/GKE) for independent scaling.
- **Environments:** `dev → staging → production`, with feature flags for gradual AI feature rollout.
- **CI/CD:** GitHub Actions builds/tests/lints each service; ArgoCD (GitOps) handles progressive deployment with canary/blue-green strategies, especially for AI-orchestration changes.
- **Video pipeline deployment:** GPU-backed worker pool (autoscaled) separate from the main API cluster, since transcription/segmentation is compute-heavy and bursty.
- **CDN:** Video and static asset delivery via CloudFront/Cloudflare, edge-cached per region.
- **Infrastructure as Code:** Terraform for all cloud resources, reviewed via PR before apply.
- **Disaster recovery:** Multi-AZ database deployment; automated backups with point-in-time recovery; documented RTO/RPO targets per data tier (e.g., knowledge graph RPO < 5 min).

---

## 22. Scalability Plan

| Concern | Strategy |
|---|---|
| Knowledge Graph read/write load | Dedicated graph store, read replicas, Redis caching of hot learner-graph snapshots |
| AI inference cost/latency | Cache deterministic AI outputs (video segments, taxonomy tags); batch/async processing for non-real-time tasks; model-tiering (cheaper model for simple tasks, stronger model for tutoring/assessment) |
| Video processing throughput | Autoscaled async worker pool, queue-based backpressure (Temporal/Celery + Kafka) |
| Traffic spikes (cohort launches, exam season) | Horizontal pod autoscaling per service; stateless services behind load balancers |
| Multi-tenant B2B growth | Tenant-aware partitioning in Postgres (schema-per-tenant or row-level `tenant_id`), isolated resource quotas |
| Global expansion | Multi-region deployment with regional CDN + data residency compliance |
| Event bus growth | Kafka topic partitioning by learner/subject shard key to preserve ordering where needed while enabling parallelism |

---

## 23. Future Roadmap

| Phase | Focus |
|---|---|
| Phase 1 (MVP) | Core loop: assessment → graph → path → video skip → quiz → dashboard, for 1–2 pilot subjects |
| Phase 2 | Instructor tools, admin dashboard, gamification, spaced repetition, multi-subject taxonomy support |
| Phase 3 | AI Tutor voice mode, mobile offline mode, advanced analytics/predictive insights |
| Phase 4 | B2B multi-tenant offering, institutional SSO, certification APIs |
| Phase 5 | Marketplace for taxonomies/content packs, AI-generated original content for gap-filling, peer study matching |
| Phase 6 | AR/VR concept simulations, multi-language content generation & dubbing |

---

## 24. Risks and Challenges

| Risk | Impact | Mitigation |
|---|---|---|
| AI-generated video segments are inaccurate | Learners skip content they don't actually know | Human-in-the-loop instructor review before publishing; confidence thresholds; learner feedback loop to flag bad skips |
| Adaptive assessment difficulty miscalibration | Inaccurate mastery scores, broken personalization | Continuous calibration using response data (IRT parameter estimation); A/B test against fixed-form baseline |
| Knowledge graph drift/staleness | Personalization becomes inaccurate over time | Forgetting-curve decay + periodic re-assessment prompts |
| AI cost overrun at scale | Unsustainable unit economics | Aggressive caching, model tiering, async batching for non-interactive AI tasks |
| Content licensing/copyright (segmenting third-party videos) | Legal exposure | Restrict segmentation to owned/licensed content initially; clear ToS for instructor-uploaded content |
| Cold-start problem (new subject with no taxonomy/content) | Poor personalization for new domains | Taxonomy templates + AI-assisted taxonomy bootstrapping reviewed by instructors |
| Learner trust in "skip" decisions | Learners may distrust or override AI skips, reducing value | Transparent explanations ("You skipped this because you scored 92% on Loops"), easy manual override |
| Data privacy for minors (K-12 use case) | Regulatory risk (COPPA) | Age-gating, parental consent flows, restricted data collection for minors |
| Multi-tenant data isolation (B2B) | Data leakage between institutions | Strict tenant partitioning, automated isolation testing |

---

## 25. Suggested Development Milestones

| Milestone | Deliverables | Target Outcome |
|---|---|---|
| **M0: Foundations** | Repo/infra scaffolding, auth service, base CI/CD, core DB schemas | Deployable skeleton system |
| **M1: Taxonomy & Graph Core** | Concept taxonomy model, Knowledge Graph Service (CRUD + mastery model), seed taxonomy for 1 pilot subject | Graph can be queried/updated manually |
| **M2: Adaptive Assessment MVP** | Assessment Service with AI question generation, difficulty adaptation, concept-level scoring | End-to-end: student takes assessment → concept scores produced |
| **M3: Learning Path & Recommendations** | Learning Path Service, Recommendation Service, basic content library | Personalized path with resource links generated from graph |
| **M4: Video Intelligence MVP** | Transcription + segmentation pipeline, segment review UI for instructors | Uploaded video auto-splits into concept chapters |
| **M5: Smart Video Player & Skip Logic** | Player integration with graph-based auto-skip | Learner sees personalized skip behavior end-to-end |
| **M6: AI Tutor MVP** | RAG-based tutor grounded in graph + content | Learner can ask contextual questions during a concept |
| **M7: Analytics Dashboard v1** | Core student metrics (mastery, streak, time saved, etc.) | Learner-facing dashboard live |
| **M8: Adaptive Quiz Loop Closure** | Post-concept quizzes, mastery threshold gating, revision loop | Full closed adaptive loop operational |
| **M9: Gamification & Study Planner** | XP/badges/streaks, calendar/planner, spaced repetition scheduling | Engagement & retention features live |
| **M10: Instructor Dashboard** | Upload workflows, class analytics, content review tools | Instructors can manage content and see class insights |
| **M11: Admin Dashboard & Billing** | User/content moderation, subscription/billing, platform analytics | Platform ready for commercial pilot |
| **M12: Hardening & Scale Prep** | Load testing, security audit, multi-region readiness, cost optimization | Production-grade launch readiness |

---

*End of Blueprint. This document should be treated as a living artifact — updated as architectural decisions evolve during implementation.*