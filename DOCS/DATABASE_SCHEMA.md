# AI-Powered Adaptive Learning Platform

## Database Schema Specification (v1.0)

**Status:** Pre-development schema baseline\
**Based on:** `PROJECT_BLUEPRINT.md`, `UI_DESIGN_SYSTEM.md`,
`TECH_STACK.md`, and `SCREEN_SPECIFICATION.md`

------------------------------------------------------------------------

# 1. Purpose

This document defines the PostgreSQL data model for the MVP.

The database must support the platform's central loop:

``` text
Assess
  ↓
Diagnose
  ↓
Knowledge Graph
  ↓
Personalized Learning Path
  ↓
Teach
  ↓
Practice
  ↓
Re-assess
  ↓
Update Knowledge Graph
  ↓
Analytics
  ↓
Repeat
```

The schema is designed around a **modular monolith with PostgreSQL as
the source of truth**.

The project blueprint describes a concept-level knowledge graph, learner
profiles, learning goals, adaptive assessment, prerequisite validation,
multi-format resources, AI video segmentation, tutor interactions,
analytics, spaced repetition, gamification, certificates, instructor
workflows, and admin controls. These requirements drive the schema
below.

------------------------------------------------------------------------

# 2. Database Principles

1.  PostgreSQL is the authoritative source of truth for application
    data.
2.  Use UUIDs for externally exposed entity identifiers.
3.  Use `created_at` and `updated_at` on mutable entities.
4.  Use soft deletion only where recovery/audit value exists; do not
    blindly soft-delete every table.
5.  Foreign keys must enforce referential integrity.
6.  Use database constraints for data that must always be valid.
7.  Use UTC timestamps with `TIMESTAMPTZ`.
8.  Store percentages as numeric values from `0` to `100`.
9.  Store durations in seconds unless a field is explicitly a date/time.
10. Store AI model/prompt metadata with AI-generated artifacts.
11. Keep event records append-only.
12. Never store large video binaries in PostgreSQL.
13. Store object-storage keys/URLs as metadata.
14. Keep learner mastery as a first-class entity.
15. Keep prerequisite relationships acyclic at the application
    validation layer.
16. Avoid storing derived analytics when they can be safely recomputed;
    cache/aggregate only when useful for performance.
17. Do not create a separate graph database for MVP.

------------------------------------------------------------------------

# 3. Logical Domains

``` text
IDENTITY
  users
  roles
  user_roles
  learner_profiles

LEARNING TAXONOMY
  subjects
  topics
  concepts
  concept_prerequisites
  learning_goals

CONTENT
  courses
  course_modules
  lessons
  resources
  videos
  video_segments
  resource_concepts
  video_segment_concepts

ASSESSMENT
  assessments
  assessment_items
  questions
  question_options
  assessment_attempts
  assessment_responses

KNOWLEDGE GRAPH
  learner_subjects
  learner_concept_mastery
  mastery_history
  mastery_events

PERSONALIZATION
  learning_paths
  learning_path_steps
  recommendations
  recommendation_feedback

ACTIVITY
  study_sessions
  video_watch_events
  bookmarks
  notes
  revision_schedule

AI
  ai_conversations
  ai_messages
  ai_generations
  ai_prompt_versions

ANALYTICS
  analytics_events
  daily_learning_metrics
  concept_analytics_snapshots

GAMIFICATION
  achievements
  user_achievements
  xp_transactions
  streaks

COMMUNICATION
  notifications

CERTIFICATION
  certificates

INSTRUCTOR
  enrollments
  cohorts
  cohort_members

ADMIN / GOVERNANCE
  content_reviews
  audit_logs

BILLING (future / Phase 5)
  plans
  subscriptions
  payment_transactions
```

------------------------------------------------------------------------

# 4. Entity Relationship Overview

``` text
User
 │
 ├── LearnerProfile
 ├── UserRoles
 ├── LearnerSubjects
 │       │
 │       ├── LearnerConceptMastery
 │       ├── LearningPaths
 │       ├── Assessments / Attempts
 │       └── StudySessions
 │
 ├── AIConversations
 ├── Notifications
 ├── Achievements
 ├── Certificates
 └── Enrollments

Subject
 │
 ├── Topics
 │    └── Concepts
 │         ├── Prerequisites
 │         ├── Resources
 │         └── LearnerConceptMastery
 │
 └── Courses
      └── Modules
           └── Lessons
                └── Resources
                     └── Videos
                          └── VideoSegments

Assessment
 ├── AssessmentItems
 │    └── Questions
 │         └── Options
 └── Attempts
      └── Responses
           └── Mastery Events
                ↓
         LearnerConceptMastery
                ↓
         LearningPath
                ↓
         Recommendations
```

------------------------------------------------------------------------

# 5. Identity Schema

## 5.1 users

Stores account-level identity.

  Column              Type           Constraints
  ------------------- -------------- ----------------------------------
  id                  UUID           PK
  email               CITEXT         UNIQUE, NOT NULL
  password_hash       TEXT           nullable for OAuth-only accounts
  full_name           VARCHAR(120)   NOT NULL
  avatar_url          TEXT           nullable
  email_verified_at   TIMESTAMPTZ    nullable
  is_active           BOOLEAN        NOT NULL DEFAULT true
  last_login_at       TIMESTAMPTZ    nullable
  created_at          TIMESTAMPTZ    NOT NULL
  updated_at          TIMESTAMPTZ    NOT NULL

Indexes:

``` text
users_email_unique
users_active_idx
```

Never store plaintext passwords.

------------------------------------------------------------------------

## 5.2 roles

  Column        Type
  ------------- --------------------
  id            UUID PK
  code          VARCHAR(30) UNIQUE
  name          VARCHAR(60)
  description   TEXT

Initial roles:

``` text
student
instructor
admin
```

Future:

``` text
content_reviewer
org_owner
super_admin
```

------------------------------------------------------------------------

## 5.3 user_roles

Many-to-many user/role mapping.

  Column       Type
  ------------ ------------------
  user_id      UUID FK users.id
  role_id      UUID FK roles.id
  created_at   TIMESTAMPTZ

Primary key:

``` text
(user_id, role_id)
```

------------------------------------------------------------------------

# 6. Learner Profile

## 6.1 learner_profiles

Stores personalization preferences captured during onboarding and
refined over time.

  Column                      Type
  --------------------------- -------------------------
  id                          UUID PK
  user_id                     UUID FK users.id UNIQUE
  learning_style              VARCHAR(30)
  learning_speed              VARCHAR(20)
  preferred_session_minutes   INTEGER
  preferred_study_period      VARCHAR(30)
  timezone                    VARCHAR(80)
  onboarding_completed_at     TIMESTAMPTZ
  created_at                  TIMESTAMPTZ
  updated_at                  TIMESTAMPTZ

Allowed learning styles:

``` text
visual
reading
practice
mixed
```

Learning speed:

``` text
fast
moderate
slow
```

Study period:

``` text
morning
afternoon
evening
late_night
```

Do not hard-code these values in multiple application modules.
Centralize them as enums or validated constants.

------------------------------------------------------------------------

# 7. Learning Taxonomy

## 7.1 subjects

Top-level learning domain.

Examples:

``` text
Python
Data Structures
Machine Learning
```

  Column         Type
  -------------- ---------------------------
  id             UUID PK
  name           VARCHAR(150)
  slug           VARCHAR(180) UNIQUE
  description    TEXT
  icon_url       TEXT
  is_published   BOOLEAN
  created_by     UUID FK users.id nullable
  created_at     TIMESTAMPTZ
  updated_at     TIMESTAMPTZ

------------------------------------------------------------------------

## 7.2 topics

  Column            Type
  ----------------- ----------------------------
  id                UUID PK
  subject_id        UUID FK subjects.id
  parent_topic_id   UUID FK topics.id nullable
  name              VARCHAR(150)
  slug              VARCHAR(180)
  description       TEXT
  sort_order        INTEGER
  created_at        TIMESTAMPTZ
  updated_at        TIMESTAMPTZ

Unique:

``` text
(subject_id, slug)
```

------------------------------------------------------------------------

## 7.3 concepts

The most important taxonomy entity.

  Column                Type
  --------------------- ------------------------------
  id                    UUID PK
  subject_id            UUID FK subjects.id
  topic_id              UUID FK topics.id
  parent_concept_id     UUID FK concepts.id nullable
  name                  VARCHAR(180)
  slug                  VARCHAR(220)
  description           TEXT
  difficulty_baseline   NUMERIC(5,2)
  is_active             BOOLEAN
  created_at            TIMESTAMPTZ
  updated_at            TIMESTAMPTZ

A concept belongs to exactly one subject.

A concept may have a parent concept.

------------------------------------------------------------------------

## 7.4 concept_prerequisites

Represents the knowledge graph's prerequisite edges.

  Column                    Type
  ------------------------- ---------------------
  concept_id                UUID FK concepts.id
  prerequisite_concept_id   UUID FK concepts.id
  strength                  NUMERIC(5,2)
  created_at                TIMESTAMPTZ

Primary key:

``` text
(concept_id, prerequisite_concept_id)
```

Constraint:

``` text
concept_id != prerequisite_concept_id
```

The application must reject cycles before inserting a prerequisite edge.

------------------------------------------------------------------------

# 8. Learning Goals

## 8.1 learning_goals

System-level goal types.

  Column                      Type
  --------------------------- --------------------
  id                          UUID PK
  code                        VARCHAR(50) UNIQUE
  name                        VARCHAR(100)
  description                 TEXT
  default_mastery_threshold   NUMERIC(5,2)
  created_at                  TIMESTAMPTZ

Initial goals:

``` text
interview_preparation
college_exams
build_projects
learn_from_scratch
revision
advanced_mastery
```

------------------------------------------------------------------------

## 8.2 learner_subjects

Tracks the learner's relationship with a subject.

  Column             Type
  ------------------ ---------------------------
  id                 UUID PK
  user_id            UUID FK users.id
  subject_id         UUID FK subjects.id
  learning_goal_id   UUID FK learning_goals.id
  target_mastery     NUMERIC(5,2)
  started_at         TIMESTAMPTZ
  completed_at       TIMESTAMPTZ nullable
  status             VARCHAR(30)
  created_at         TIMESTAMPTZ
  updated_at         TIMESTAMPTZ

Statuses:

``` text
active
paused
completed
archived
```

Unique:

``` text
(user_id, subject_id, status active)
```

A learner may later study the same subject again with a different goal;
do not make `(user_id, subject_id)` universally unique.

------------------------------------------------------------------------

# 9. Courses and Lessons

## 9.1 courses

  Column              Type
  ------------------- ----------------------
  id                  UUID PK
  subject_id          UUID FK subjects.id
  instructor_id       UUID FK users.id
  title               VARCHAR(250)
  slug                VARCHAR(280)
  description         TEXT
  thumbnail_url       TEXT
  difficulty          VARCHAR(30)
  estimated_minutes   INTEGER
  status              VARCHAR(30)
  published_at        TIMESTAMPTZ nullable
  created_at          TIMESTAMPTZ
  updated_at          TIMESTAMPTZ

Statuses:

``` text
draft
processing
review
published
archived
```

------------------------------------------------------------------------

## 9.2 course_modules

  Column        Type
  ------------- --------------------
  id            UUID PK
  course_id     UUID FK courses.id
  title         VARCHAR(250)
  description   TEXT
  sort_order    INTEGER
  created_at    TIMESTAMPTZ
  updated_at    TIMESTAMPTZ

------------------------------------------------------------------------

## 9.3 lessons

  Column              Type
  ------------------- ---------------------------
  id                  UUID PK
  module_id           UUID FK course_modules.id
  title               VARCHAR(250)
  description         TEXT
  sort_order          INTEGER
  estimated_minutes   INTEGER
  created_at          TIMESTAMPTZ
  updated_at          TIMESTAMPTZ

------------------------------------------------------------------------

# 10. Resources

The recommendation engine must support multiple formats.

## 10.1 resources

  Column              Type
  ------------------- -----------------------------
  id                  UUID PK
  lesson_id           UUID FK lessons.id nullable
  subject_id          UUID FK subjects.id
  resource_type       VARCHAR(40)
  title               VARCHAR(250)
  description         TEXT
  url                 TEXT nullable
  storage_key         TEXT nullable
  thumbnail_url       TEXT nullable
  estimated_minutes   INTEGER
  difficulty          VARCHAR(30)
  language            VARCHAR(20)
  status              VARCHAR(30)
  quality_score       NUMERIC(5,2) nullable
  created_by          UUID FK users.id
  created_at          TIMESTAMPTZ
  updated_at          TIMESTAMPTZ

Resource types:

``` text
video
notes
documentation
coding_exercise
project
flashcard
article
```

------------------------------------------------------------------------

## 10.2 resource_concepts

Many-to-many mapping.

  Column            Type
  ----------------- ----------------------
  resource_id       UUID FK resources.id
  concept_id        UUID FK concepts.id
  relevance_score   NUMERIC(5,2)
  created_at        TIMESTAMPTZ

Primary key:

``` text
(resource_id, concept_id)
```

------------------------------------------------------------------------

# 11. Video Intelligence

## 11.1 videos

One resource may reference one video asset.

  Column                Type
  --------------------- -----------------------------
  id                    UUID PK
  resource_id           UUID FK resources.id UNIQUE
  storage_key           TEXT
  duration_seconds      INTEGER
  width                 INTEGER
  height                INTEGER
  format                VARCHAR(30)
  transcript_status     VARCHAR(30)
  segmentation_status   VARCHAR(30)
  processing_error      TEXT nullable
  created_at            TIMESTAMPTZ
  updated_at            TIMESTAMPTZ

Statuses:

``` text
pending
processing
completed
failed
```

------------------------------------------------------------------------

## 11.2 video_segments

AI-generated or instructor-edited concept chapters.

  Column            Type
  ----------------- ---------------------------
  id                UUID PK
  video_id          UUID FK videos.id
  title             VARCHAR(250)
  start_seconds     NUMERIC(12,3)
  end_seconds       NUMERIC(12,3)
  transcript_text   TEXT
  ai_confidence     NUMERIC(5,2)
  source            VARCHAR(30)
  review_status     VARCHAR(30)
  reviewed_by       UUID FK users.id nullable
  reviewed_at       TIMESTAMPTZ nullable
  created_at        TIMESTAMPTZ
  updated_at        TIMESTAMPTZ

Source:

``` text
ai
instructor
hybrid
```

Review status:

``` text
pending
approved
rejected
edited
```

Constraint:

``` text
end_seconds > start_seconds
```

------------------------------------------------------------------------

## 11.3 video_segment_concepts

  Column       Type
  ------------ ---------------------------
  segment_id   UUID FK video_segments.id
  concept_id   UUID FK concepts.id
  confidence   NUMERIC(5,2)
  is_primary   BOOLEAN
  created_at   TIMESTAMPTZ

Primary key:

``` text
(segment_id, concept_id)
```

Only approved segments may be used for automatic learner skipping.

------------------------------------------------------------------------

# 12. Assessments

## 12.1 assessments

Represents an assessment definition/session type.

  Column               Type
  -------------------- -----------------------------
  id                   UUID PK
  learner_subject_id   UUID FK learner_subjects.id
  assessment_type      VARCHAR(40)
  status               VARCHAR(30)
  target_concepts      JSONB nullable
  started_at           TIMESTAMPTZ nullable
  completed_at         TIMESTAMPTZ nullable
  created_at           TIMESTAMPTZ
  updated_at           TIMESTAMPTZ

Assessment types:

``` text
diagnostic
adaptive_quiz
revision
practice
final
```

------------------------------------------------------------------------

## 12.2 questions

Stores reusable/generated question records.

  Column             Type
  ------------------ ------------------------------------
  id                 UUID PK
  concept_id         UUID FK concepts.id
  question_type      VARCHAR(40)
  prompt             TEXT
  explanation        TEXT nullable
  difficulty         NUMERIC(5,2)
  answer_data        JSONB
  source             VARCHAR(30)
  ai_generation_id   UUID FK ai_generations.id nullable
  status             VARCHAR(30)
  created_at         TIMESTAMPTZ
  updated_at         TIMESTAMPTZ

Question types:

``` text
mcq
true_false
short_answer
coding
multiple_select
```

------------------------------------------------------------------------

## 12.3 question_options

For MCQ-style questions.

  Column        Type
  ------------- ----------------------
  id            UUID PK
  question_id   UUID FK questions.id
  option_text   TEXT
  option_key    VARCHAR(20)
  sort_order    INTEGER
  is_correct    BOOLEAN

Do not expose `is_correct` to the learner-facing API.

------------------------------------------------------------------------

## 12.4 assessment_items

Maps questions into a particular assessment and stores the AI-selected
difficulty context.

  Column                Type
  --------------------- ------------------------
  id                    UUID PK
  assessment_id         UUID FK assessments.id
  question_id           UUID FK questions.id
  concept_id            UUID FK concepts.id
  sequence_number       INTEGER
  selected_difficulty   NUMERIC(5,2)
  generated_at          TIMESTAMPTZ
  created_at            TIMESTAMPTZ

------------------------------------------------------------------------

# 13. Assessment Attempts and Responses

## 13.1 assessment_attempts

A learner's actual attempt.

  Column           Type
  ---------------- ------------------------
  id               UUID PK
  assessment_id    UUID FK assessments.id
  user_id          UUID FK users.id
  status           VARCHAR(30)
  started_at       TIMESTAMPTZ
  completed_at     TIMESTAMPTZ nullable
  total_items      INTEGER
  answered_items   INTEGER
  created_at       TIMESTAMPTZ
  updated_at       TIMESTAMPTZ

Statuses:

``` text
in_progress
completed
abandoned
expired
```

------------------------------------------------------------------------

## 13.2 assessment_responses

One answer submission.

  Column               Type
  -------------------- --------------------------------
  id                   UUID PK
  attempt_id           UUID FK assessment_attempts.id
  assessment_item_id   UUID FK assessment_items.id
  answer_data          JSONB
  is_correct           BOOLEAN
  score                NUMERIC(6,3)
  response_time_ms     INTEGER
  confidence_rating    INTEGER nullable
  answered_at          TIMESTAMPTZ
  created_at           TIMESTAMPTZ

If confidence is collected, use a defined scale such as `1–5`.

------------------------------------------------------------------------

# 14. Learner Knowledge Graph

This is the central personalization state.

## 14.1 learner_concept_mastery

One row per learner/subject/concept.

  Column              Type
  ------------------- -----------------------
  id                  UUID PK
  user_id             UUID FK users.id
  subject_id          UUID FK subjects.id
  concept_id          UUID FK concepts.id
  mastery_score       NUMERIC(5,2)
  confidence_score    NUMERIC(5,2)
  mastery_state       VARCHAR(20)
  attempts            INTEGER
  correct_attempts    INTEGER
  last_assessed_at    TIMESTAMPTZ nullable
  last_practiced_at   TIMESTAMPTZ nullable
  last_revised_at     TIMESTAMPTZ nullable
  next_review_at      TIMESTAMPTZ nullable
  decay_score         NUMERIC(5,2) nullable
  created_at          TIMESTAMPTZ
  updated_at          TIMESTAMPTZ

States:

``` text
unknown
weak
partial
mastered
```

Unique:

``` text
(user_id, concept_id)
```

A concept belongs to one subject, so subject can be validated against
concept.subject_id.

------------------------------------------------------------------------

## 14.2 mastery_history

Historical snapshots.

  Column                       Type
  ---------------------------- ------------------------------------
  id                           UUID PK
  learner_concept_mastery_id   UUID FK learner_concept_mastery.id
  previous_score               NUMERIC(5,2)
  new_score                    NUMERIC(5,2)
  previous_state               VARCHAR(20)
  new_state                    VARCHAR(20)
  reason                       VARCHAR(50)
  source_event_id              UUID nullable
  created_at                   TIMESTAMPTZ

Reasons:

``` text
assessment
quiz
practice
video_watch
tutor_interaction
decay
manual_review
```

This table supports the Analytics Dashboard's mastery-over-time graph.

------------------------------------------------------------------------

## 14.3 mastery_events

Domain events that cause or request mastery updates.

  Column            Type
  ----------------- ----------------------
  id                UUID PK
  user_id           UUID FK users.id
  subject_id        UUID FK subjects.id
  concept_id        UUID FK concepts.id
  event_type        VARCHAR(50)
  source_type       VARCHAR(50)
  source_id         UUID nullable
  payload           JSONB
  idempotency_key   VARCHAR(180) UNIQUE
  occurred_at       TIMESTAMPTZ
  processed_at      TIMESTAMPTZ nullable

Event types:

``` text
assessment_answered
quiz_submitted
practice_completed
video_watched
tutor_interaction
revision_completed
mastery_decay
```

The Knowledge Graph module is the authoritative writer of mastery state.

------------------------------------------------------------------------

# 15. Personalized Learning Paths

## 15.1 learning_paths

  Column                           Type
  -------------------------------- -----------------------------
  id                               UUID PK
  learner_subject_id               UUID FK learner_subjects.id
  generated_from_mastery_version   UUID nullable
  status                           VARCHAR(30)
  estimated_minutes                INTEGER
  progress_percent                 NUMERIC(5,2)
  generated_at                     TIMESTAMPTZ
  completed_at                     TIMESTAMPTZ nullable
  created_at                       TIMESTAMPTZ
  updated_at                       TIMESTAMPTZ

Statuses:

``` text
draft
active
paused
completed
superseded
```

------------------------------------------------------------------------

## 15.2 learning_path_steps

  Column                Type
  --------------------- ---------------------------
  id                    UUID PK
  learning_path_id      UUID FK learning_paths.id
  concept_id            UUID FK concepts.id
  sequence_number       INTEGER
  status                VARCHAR(30)
  mastery_threshold     NUMERIC(5,2)
  estimated_minutes     INTEGER
  prerequisite_status   VARCHAR(30)
  started_at            TIMESTAMPTZ nullable
  completed_at          TIMESTAMPTZ nullable
  created_at            TIMESTAMPTZ
  updated_at            TIMESTAMPTZ

Statuses:

``` text
locked
ready
in_progress
mastered
needs_revision
```

Prerequisite status:

``` text
satisfied
scheduled_before
blocked
```

------------------------------------------------------------------------

# 16. Recommendations

## 16.1 recommendations

  Column                Type
  --------------------- -------------------------------
  id                    UUID PK
  user_id               UUID FK users.id
  concept_id            UUID FK concepts.id
  resource_id           UUID FK resources.id nullable
  recommendation_type   VARCHAR(40)
  score                 NUMERIC(8,4)
  reason                TEXT
  generated_by          VARCHAR(40)
  expires_at            TIMESTAMPTZ nullable
  created_at            TIMESTAMPTZ

Types:

``` text
learn
practice
revision
video
reading
project
```

The reason should be explainable to the learner.

------------------------------------------------------------------------

## 16.2 recommendation_feedback

  Column              Type
  ------------------- ----------------------------
  id                  UUID PK
  recommendation_id   UUID FK recommendations.id
  user_id             UUID FK users.id
  feedback            VARCHAR(30)
  reason              TEXT nullable
  created_at          TIMESTAMPTZ

Feedback:

``` text
helpful
not_helpful
dismissed
completed
```

------------------------------------------------------------------------

# 17. Study Activity

## 17.1 study_sessions

  Column             Type
  ------------------ ----------------------
  id                 UUID PK
  user_id            UUID FK users.id
  subject_id         UUID FK subjects.id
  started_at         TIMESTAMPTZ
  ended_at           TIMESTAMPTZ nullable
  duration_seconds   INTEGER
  activity_type      VARCHAR(40)
  created_at         TIMESTAMPTZ

Activity types:

``` text
assessment
lesson
video
practice
tutor
revision
project
```

------------------------------------------------------------------------

## 17.2 video_watch_events

Append-only video interaction events.

  Column             Type
  ------------------ ------------------------------------
  id                 UUID PK
  user_id            UUID FK users.id
  video_id           UUID FK videos.id
  segment_id         UUID FK video_segments.id nullable
  event_type         VARCHAR(30)
  position_seconds   NUMERIC(12,3)
  duration_seconds   NUMERIC(12,3) nullable
  session_id         UUID FK study_sessions.id nullable
  occurred_at        TIMESTAMPTZ

Event types:

``` text
started
played
paused
completed
seeked
skipped
rewatched
```

This supports the time-saved metric.

------------------------------------------------------------------------

# 18. Notes and Bookmarks

## 18.1 bookmarks

  Column             Type
  ------------------ ------------------------------------
  id                 UUID PK
  user_id            UUID FK users.id
  resource_id        UUID FK resources.id nullable
  video_id           UUID FK videos.id nullable
  segment_id         UUID FK video_segments.id nullable
  position_seconds   NUMERIC(12,3) nullable
  title              VARCHAR(200) nullable
  created_at         TIMESTAMPTZ
  updated_at         TIMESTAMPTZ

------------------------------------------------------------------------

## 18.2 notes

  Column             Type
  ------------------ ------------------------------------
  id                 UUID PK
  user_id            UUID FK users.id
  resource_id        UUID FK resources.id nullable
  video_id           UUID FK videos.id nullable
  segment_id         UUID FK video_segments.id nullable
  content            TEXT
  position_seconds   NUMERIC(12,3) nullable
  created_at         TIMESTAMPTZ
  updated_at         TIMESTAMPTZ

------------------------------------------------------------------------

# 19. Revision / Spaced Repetition

## 19.1 revision_schedule

  Column             Type
  ------------------ ------------------------------------
  id                 UUID PK
  user_id            UUID FK users.id
  concept_id         UUID FK concepts.id
  mastery_id         UUID FK learner_concept_mastery.id
  due_at             TIMESTAMPTZ
  interval_days      NUMERIC(8,2)
  ease_factor        NUMERIC(6,3)
  repetition_count   INTEGER
  last_result        VARCHAR(30) nullable
  status             VARCHAR(20)
  created_at         TIMESTAMPTZ
  updated_at         TIMESTAMPTZ

Statuses:

``` text
scheduled
completed
skipped
overdue
```

The exact forgetting-curve algorithm should live in application logic,
not in database triggers.

------------------------------------------------------------------------

# 20. AI Tutor

## 20.1 ai_conversations

  Column       Type
  ------------ ------------------------------
  id           UUID PK
  user_id      UUID FK users.id
  subject_id   UUID FK subjects.id nullable
  concept_id   UUID FK concepts.id nullable
  title        VARCHAR(200) nullable
  created_at   TIMESTAMPTZ
  updated_at   TIMESTAMPTZ

------------------------------------------------------------------------

## 20.2 ai_messages

  Column            Type
  ----------------- -----------------------------
  id                UUID PK
  conversation_id   UUID FK ai_conversations.id
  role              VARCHAR(20)
  content           TEXT
  token_count       INTEGER nullable
  created_at        TIMESTAMPTZ

Roles:

``` text
system
user
assistant
tool
```

Do not expose system messages to learners.

------------------------------------------------------------------------

# 21. AI Governance

## 21.1 ai_prompt_versions

  Column       Type
  ------------ ---------------------------
  id           UUID PK
  prompt_key   VARCHAR(100)
  version      VARCHAR(30)
  template     TEXT
  status       VARCHAR(20)
  created_by   UUID FK users.id nullable
  created_at   TIMESTAMPTZ

Statuses:

``` text
draft
active
retired
```

Unique:

``` text
(prompt_key, version)
```

------------------------------------------------------------------------

## 21.2 ai_generations

Stores metadata for AI-generated artifacts.

  Column              Type
  ------------------- -------------------------------
  id                  UUID PK
  provider            VARCHAR(50)
  model               VARCHAR(100)
  prompt_version_id   UUID FK ai_prompt_versions.id
  generation_type     VARCHAR(50)
  input_hash          VARCHAR(128) nullable
  output_data         JSONB
  status              VARCHAR(30)
  latency_ms          INTEGER nullable
  input_tokens        INTEGER nullable
  output_tokens       INTEGER nullable
  estimated_cost      NUMERIC(12,6) nullable
  created_at          TIMESTAMPTZ

Generation types:

``` text
assessment_question
quiz_question
video_segmentation
recommendation
tutor_response
insight
summary
taxonomy_tagging
```

This directly supports the blueprint requirement that AI-generated
content be versioned and auditable.

------------------------------------------------------------------------

# 22. Analytics

## 22.1 analytics_events

Append-only product event log.

  Column        Type
  ------------- ------------------------------
  id            UUID PK
  user_id       UUID FK users.id nullable
  subject_id    UUID FK subjects.id nullable
  event_name    VARCHAR(80)
  entity_type   VARCHAR(50) nullable
  entity_id     UUID nullable
  properties    JSONB
  occurred_at   TIMESTAMPTZ
  session_id    UUID nullable

Examples:

``` text
login
assessment_started
question_answered
assessment_completed
learning_path_started
lesson_started
video_started
video_segment_skipped
video_completed
tutor_message_sent
quiz_submitted
revision_completed
certificate_issued
```

Use indexes on:

``` text
(user_id, occurred_at)
(event_name, occurred_at)
(subject_id, occurred_at)
```

Partitioning can be introduced later if event volume becomes large.

------------------------------------------------------------------------

## 22.2 daily_learning_metrics

Pre-aggregated student daily metrics.

  Column                  Type
  ----------------------- ---------------------
  id                      UUID PK
  user_id                 UUID FK users.id
  subject_id              UUID FK subjects.id
  metric_date             DATE
  study_seconds           INTEGER
  concepts_practiced      INTEGER
  concepts_mastered       INTEGER
  quiz_attempts           INTEGER
  correct_answers         INTEGER
  video_seconds_watched   INTEGER
  video_seconds_skipped   INTEGER
  tutor_interactions      INTEGER
  time_saved_seconds      INTEGER
  streak_day              INTEGER
  created_at              TIMESTAMPTZ
  updated_at              TIMESTAMPTZ

Unique:

``` text
(user_id, subject_id, metric_date)
```

------------------------------------------------------------------------

## 22.3 concept_analytics_snapshots

  Column             Type
  ------------------ ---------------------
  id                 UUID PK
  user_id            UUID FK users.id
  concept_id         UUID FK concepts.id
  snapshot_date      DATE
  mastery_score      NUMERIC(5,2)
  confidence_score   NUMERIC(5,2)
  attempts           INTEGER
  accuracy           NUMERIC(5,2)
  study_seconds      INTEGER
  video_seconds      INTEGER
  revision_count     INTEGER
  created_at         TIMESTAMPTZ

This supports mastery trend charts without scanning every event.

------------------------------------------------------------------------

# 23. Achievements and Gamification

## 23.1 achievements

  Column        Type
  ------------- --------------------
  id            UUID PK
  code          VARCHAR(80) UNIQUE
  name          VARCHAR(120)
  description   TEXT
  icon_url      TEXT
  xp_reward     INTEGER
  criteria      JSONB
  created_at    TIMESTAMPTZ

------------------------------------------------------------------------

## 23.2 user_achievements

  Column           Type
  ---------------- -------------------------
  id               UUID PK
  user_id          UUID FK users.id
  achievement_id   UUID FK achievements.id
  earned_at        TIMESTAMPTZ
  metadata         JSONB

Unique:

``` text
(user_id, achievement_id)
```

------------------------------------------------------------------------

## 23.3 xp_transactions

  Column        Type
  ------------- ----------------------
  id            UUID PK
  user_id       UUID FK users.id
  amount        INTEGER
  reason        VARCHAR(60)
  source_type   VARCHAR(50) nullable
  source_id     UUID nullable
  created_at    TIMESTAMPTZ

Never store only a mutable total XP value. The transaction log is
authoritative.

------------------------------------------------------------------------

## 23.4 streaks

  Column               Type
  -------------------- -------------------------
  id                   UUID PK
  user_id              UUID FK users.id UNIQUE
  current_streak       INTEGER
  longest_streak       INTEGER
  last_activity_date   DATE nullable
  updated_at           TIMESTAMPTZ

------------------------------------------------------------------------

# 24. Certificates

## 24.1 certificates

  Column               Type
  -------------------- -----------------------------
  id                   UUID PK
  user_id              UUID FK users.id
  learner_subject_id   UUID FK learner_subjects.id
  certificate_number   VARCHAR(100) UNIQUE
  title                VARCHAR(200)
  mastery_score        NUMERIC(5,2)
  issued_at            TIMESTAMPTZ
  storage_key          TEXT
  verification_token   VARCHAR(120) UNIQUE
  created_at           TIMESTAMPTZ

------------------------------------------------------------------------

# 25. Instructor / Cohort Data

## 25.1 cohorts

  Column          Type
  --------------- ---------------------
  id              UUID PK
  name            VARCHAR(200)
  instructor_id   UUID FK users.id
  subject_id      UUID FK subjects.id
  start_date      DATE nullable
  end_date        DATE nullable
  created_at      TIMESTAMPTZ
  updated_at      TIMESTAMPTZ

------------------------------------------------------------------------

## 25.2 cohort_members

  Column      Type
  ----------- --------------------
  cohort_id   UUID FK cohorts.id
  user_id     UUID FK users.id
  joined_at   TIMESTAMPTZ

Primary key:

``` text
(cohort_id, user_id)
```

------------------------------------------------------------------------

## 25.3 enrollments

General course enrollment.

  Column         Type
  -------------- ----------------------
  id             UUID PK
  user_id        UUID FK users.id
  course_id      UUID FK courses.id
  status         VARCHAR(30)
  enrolled_at    TIMESTAMPTZ
  completed_at   TIMESTAMPTZ nullable

Unique:

``` text
(user_id, course_id)
```

------------------------------------------------------------------------

# 26. Content Review

## 26.1 content_reviews

Supports instructor/reviewer approval of AI-generated content.

  Column        Type
  ------------- ------------------
  id            UUID PK
  reviewer_id   UUID FK users.id
  entity_type   VARCHAR(50)
  entity_id     UUID
  review_type   VARCHAR(40)
  status        VARCHAR(30)
  comments      TEXT nullable
  created_at    TIMESTAMPTZ
  updated_at    TIMESTAMPTZ

Review types:

``` text
video_segment
assessment_question
resource
taxonomy
```

Statuses:

``` text
pending
approved
rejected
changes_requested
```

------------------------------------------------------------------------

# 27. Notifications

## 27.1 notifications

  Column       Type
  ------------ ----------------------
  id           UUID PK
  user_id      UUID FK users.id
  type         VARCHAR(50)
  title        VARCHAR(200)
  body         TEXT
  action_url   TEXT nullable
  read_at      TIMESTAMPTZ nullable
  created_at   TIMESTAMPTZ

Types:

``` text
revision_due
mastery_achieved
streak
assessment
learning_path
system
```

------------------------------------------------------------------------

# 28. Audit Logs

## 28.1 audit_logs

  Column          Type
  --------------- ---------------------------
  id              UUID PK
  actor_user_id   UUID FK users.id nullable
  action          VARCHAR(100)
  entity_type     VARCHAR(50)
  entity_id       UUID nullable
  before_data     JSONB nullable
  after_data      JSONB nullable
  ip_address      INET nullable
  user_agent      TEXT nullable
  created_at      TIMESTAMPTZ

Use for:

-   role changes
-   content approval
-   AI configuration changes
-   taxonomy changes
-   billing administration
-   account actions

------------------------------------------------------------------------

# 29. Billing --- Future Phase

These tables should exist in the design but do not block the learning
MVP.

## 29.1 plans

  Column             Type
  ------------------ --------------------
  id                 UUID PK
  code               VARCHAR(50) UNIQUE
  name               VARCHAR(100)
  price_minor        INTEGER
  currency           CHAR(3)
  billing_interval   VARCHAR(20)
  features           JSONB
  active             BOOLEAN
  created_at         TIMESTAMPTZ
  updated_at         TIMESTAMPTZ

Store monetary amounts in minor currency units.

------------------------------------------------------------------------

## 29.2 subscriptions

  Column                     Type
  -------------------------- ---------------------
  id                         UUID PK
  user_id                    UUID FK users.id
  plan_id                    UUID FK plans.id
  provider_subscription_id   VARCHAR(200) UNIQUE
  status                     VARCHAR(30)
  current_period_start       TIMESTAMPTZ
  current_period_end         TIMESTAMPTZ
  created_at                 TIMESTAMPTZ
  updated_at                 TIMESTAMPTZ

------------------------------------------------------------------------

## 29.3 payment_transactions

  Column                    Type
  ------------------------- -----------------------------------
  id                        UUID PK
  user_id                   UUID FK users.id
  subscription_id           UUID FK subscriptions.id nullable
  provider_transaction_id   VARCHAR(200) UNIQUE
  amount_minor              INTEGER
  currency                  CHAR(3)
  status                    VARCHAR(30)
  created_at                TIMESTAMPTZ

------------------------------------------------------------------------

# 30. Index Strategy

## High-priority indexes

### Users

``` text
users(email)
users(is_active)
```

### Concepts

``` text
concepts(subject_id)
concepts(topic_id)
concepts(parent_concept_id)
```

### Prerequisites

``` text
concept_prerequisites(concept_id)
concept_prerequisites(prerequisite_concept_id)
```

### Mastery

``` text
learner_concept_mastery(user_id, subject_id)
learner_concept_mastery(user_id, concept_id)
learner_concept_mastery(user_id, mastery_state)
```

### Assessment

``` text
assessment_attempts(user_id, status)
assessment_responses(attempt_id)
assessment_items(assessment_id, sequence_number)
```

### Paths

``` text
learning_paths(learner_subject_id, status)
learning_path_steps(learning_path_id, sequence_number)
```

### Video

``` text
video_segments(video_id, start_seconds)
video_segment_concepts(concept_id)
```

### Analytics

``` text
analytics_events(user_id, occurred_at)
analytics_events(event_name, occurred_at)
daily_learning_metrics(user_id, metric_date)
concept_analytics_snapshots(user_id, concept_id, snapshot_date)
```

------------------------------------------------------------------------

# 31. Constraints and Integrity Rules

The application and database must enforce:

1.  mastery score is between `0` and `100`.
2.  confidence score is between `0` and `100`.
3.  difficulty score is within the defined range.
4.  video segment end time is greater than start time.
5.  assessment response belongs to the assessment attempt's assessment.
6.  question concept belongs to the relevant subject.
7.  learning path concept belongs to the learner subject's subject.
8.  prerequisite concept cannot equal dependent concept.
9.  prerequisite cycles must be rejected.
10. certificate can only be issued once per learner subject completion.
11. XP transactions are append-only.
12. analytics events are append-only.
13. mastery events are idempotent using `idempotency_key`.
14. only approved video segments can become learner auto-skip
    candidates.

------------------------------------------------------------------------

# 32. Data Lifecycle

## User deletion

When a learner requests deletion:

``` text
Account deletion request
↓
Verify identity
↓
Deactivate account
↓
Delete/anonymize personal data according to policy
↓
Retain only legally required audit/financial records
```

Do not blindly cascade-delete all historical analytics if retention
policy requires anonymization instead.

------------------------------------------------------------------------

# 33. Data Ownership Rules

### Knowledge Graph module owns

``` text
learner_concept_mastery
mastery_history
```

### Assessment module owns

``` text
assessments
assessment_items
assessment_attempts
assessment_responses
```

### Content module owns

``` text
courses
course_modules
lessons
resources
videos
video_segments
```

### Analytics module owns

``` text
analytics_events
daily_learning_metrics
concept_analytics_snapshots
```

Other modules read these through application services rather than
modifying another module's data directly.

------------------------------------------------------------------------

# 34. Event-to-Database Mapping

``` text
Assessment Answer
    ↓
assessment_responses
    ↓
mastery_events
    ↓
learner_concept_mastery
    ↓
mastery_history
    ↓
analytics_events
```

``` text
Video Skip
    ↓
video_watch_events
    ↓
analytics_events
    ↓
daily_learning_metrics
    ↓
time_saved_seconds
```

``` text
Tutor Interaction
    ↓
ai_messages
    ↓
analytics_events
    ↓
optional mastery_event
```

Tutor interaction must only change mastery when the system has a
defined, validated learning signal. A chat message by itself should not
automatically increase mastery.

------------------------------------------------------------------------

# 35. Derived Metrics

Do not store every metric as an independent mutable field.

## Overall mastery

Weighted aggregation of learner concept mastery.

## Time saved

``` text
sum(skipped segment duration)
```

Only count an automatic skip once.

## Learning streak

Derived from activity dates and cached in `streaks`.

## Learning speed

Concepts reaching the mastery threshold divided by relevant study time.

## Retention score

Produced by the retention model from:

-   mastery
-   time since review
-   prior performance
-   revision history

## Estimated completion time

Based on:

-   remaining concepts
-   current mastery
-   observed learning speed
-   resource duration
-   learning goal

------------------------------------------------------------------------

# 36. Database Migration Order

Create migrations in this order:

``` text
001_users_roles
002_learner_profiles
003_subjects_topics_concepts
004_concept_prerequisites
005_learning_goals_learner_subjects
006_courses_modules_lessons
007_resources_resource_concepts
008_videos_segments
009_assessments_questions
010_assessment_attempts_responses
011_learner_concept_mastery
012_mastery_events_history
013_learning_paths
014_recommendations
015_study_sessions_video_events
016_notes_bookmarks
017_revision_schedule
018_ai_conversations
019_ai_prompt_versions_generations
020_analytics_events_metrics
021_gamification
022_certificates
023_cohorts_enrollments
024_content_reviews
025_notifications
026_audit_logs
027_billing
```

Migrations should be small and reversible where practical.

------------------------------------------------------------------------

# 37. MVP Seed Data

The database should include seed data for **one pilot subject** first.

Recommended pilot:

``` text
Python
```

Example taxonomy:

``` text
Python
├── Fundamentals
│   ├── Variables
│   ├── Data Types
│   ├── Operators
│   └── Input/Output
│
├── Control Flow
│   ├── Conditions
│   ├── Loops
│   └── Loop Control
│
├── Functions
│   ├── Function Definition
│   ├── Parameters
│   ├── Return Values
│   └── Scope
│
├── Data Structures
│   ├── Lists
│   ├── Tuples
│   ├── Sets
│   └── Dictionaries
│
└── OOP
    ├── Classes
    ├── Objects
    ├── Inheritance
    └── Polymorphism
```

Add prerequisite edges such as:

``` text
Variables → Conditions
Conditions → Loops
Functions → OOP
Data Types → Lists
Data Types → Dictionaries
```

The pilot taxonomy is intentionally small. Do not create thousands of
concepts before the adaptive loop works.

------------------------------------------------------------------------

# 38. What Is NOT in the MVP Database

Do not create infrastructure-specific tables for:

-   Kubernetes
-   Kafka
-   Terraform
-   service discovery
-   microservice registries
-   graph database synchronization
-   warehouse pipelines

These are deployment/scale concerns, not core learner data.

------------------------------------------------------------------------

# 39. Schema Validation Checklist

Before implementation begins, verify:

-   [ ] Every screen's data requirements have a corresponding entity.
-   [ ] Every core functional requirement maps to one or more tables.
-   [ ] Learner Profile is persisted.
-   [ ] Learning Goal is persisted per subject.
-   [ ] Prerequisites are represented.
-   [ ] Concept mastery is persisted per learner.
-   [ ] Mastery history is preserved.
-   [ ] Adaptive questions and responses are stored.
-   [ ] Video segments have timestamps.
-   [ ] Segment-to-concept mapping exists.
-   [ ] AI generation metadata is auditable.
-   [ ] Learning paths are versionable.
-   [ ] Recommendations are explainable.
-   [ ] Video skip events support time-saved analytics.
-   [ ] Tutor conversations are persisted.
-   [ ] Revision schedules exist.
-   [ ] Analytics events are append-only.
-   [ ] Gamification is represented.
-   [ ] Certificates are represented.
-   [ ] Instructor review is represented.
-   [ ] Admin audit logs exist.
-   [ ] Billing can be added without redesigning learner data.
-   [ ] Indexes cover core access patterns.
-   [ ] Constraints protect invalid mastery and graph data.

------------------------------------------------------------------------

# 40. Final Architecture

``` text
                         PostgreSQL
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
   Identity               Taxonomy               Content
       │                      │                      │
       ▼                      ▼                      ▼
    Users               Concepts/Edges       Courses/Resources
       │                      │                      │
       └──────────────┬───────┘                      │
                      │                              │
                      ▼                              ▼
              Learner Mastery                 Video Segments
                      │                              │
                      ├──────────────┐               │
                      ▼              ▼               ▼
               Assessments     Learning Paths   Watch Events
                      │              │               │
                      └──────┬───────┘               │
                             ▼                       │
                      Recommendations               │
                             │                       │
                             ▼                       │
                         AI Tutor ◄──── Content ─────┘
                             │
                             ▼
                       AI Generations
                             │
                             ▼
                    Analytics Events
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       Daily Metrics                 Concept Snapshots
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    Analytics Dashboard
```

------------------------------------------------------------------------

# 41. Final Rule

The database exists to support the adaptive learning loop.

The most important records are not users, courses, or certificates.

They are:

``` text
Concept
   ↓
Prerequisite
   ↓
Learner Concept Mastery
   ↓
Assessment Evidence
   ↓
Learning Path
   ↓
Resource / Video Segment
   ↓
New Learning Evidence
   ↓
Updated Mastery
```

If this chain is reliable, the rest of the product can be built around
it.

**End of DATABASE_SCHEMA.md**
