# AI-Powered Adaptive Learning Platform

## API Specification (v1.0)

**Status:** Pre-development API contract\
**Based on:** `PROJECT_BLUEPRINT.md`, `UI_DESIGN_SYSTEM.md`,
`TECH_STACK.md`, `SCREEN_SPECIFICATION.md`, and `DATABASE_SCHEMA.md`

------------------------------------------------------------------------

# 1. Purpose

This document defines the REST API contract for the MVP.

The API is the boundary between:

``` text
Next.js Frontend
        ↓
FastAPI REST API
        ↓
Domain Modules
        ↓
PostgreSQL / Redis / Object Storage / AI Workers
```

The API must support the core product loop:

``` text
Assess
↓
Diagnose
↓
Update Knowledge Graph
↓
Generate Learning Path
↓
Recommend Content
↓
Teach
↓
Practice
↓
Re-assess
↓
Update Mastery
↓
Analytics
```

------------------------------------------------------------------------

# 2. API Principles

1.  Use REST for MVP.
2.  Prefix all application endpoints with `/api/v1`.
3.  JSON is the default request/response format.
4.  Use UUIDs for resource identifiers.
5.  Use ISO 8601 timestamps in UTC.
6.  Use Pydantic schemas for request and response validation.
7.  Never expose database models directly.
8.  Never expose secrets.
9.  Never expose question answer keys through learner endpoints.
10. Return consistent error structures.
11. Use pagination for potentially large collections.
12. Use idempotency keys for operations that may be retried.
13. Keep AI calls behind backend endpoints.
14. The frontend never calls OpenAI directly.
15. Background operations return a job/resource status rather than
    blocking unnecessarily.
16. API behavior must match the database and screen specifications.

------------------------------------------------------------------------

# 3. Base URL

Development:

``` text
http://localhost:8000/api/v1
```

Production:

``` text
https://api.<domain>/api/v1
```

The frontend must read the base URL from:

``` text
NEXT_PUBLIC_API_BASE_URL
```

------------------------------------------------------------------------

# 4. Authentication

## 4.1 Access Token

Use JWT access tokens.

Typical flow:

``` text
Login
↓
Access Token + Refresh Token
↓
Frontend stores session securely
↓
Access token sent to protected API
```

Preferred production approach:

-   secure, HttpOnly refresh-token cookie
-   short-lived access token
-   refresh-token rotation

Exact token storage implementation must avoid exposing long-lived
secrets to JavaScript.

------------------------------------------------------------------------

## 4.2 Authorization

Roles:

``` text
student
instructor
admin
```

Authorization is enforced server-side.

Never rely on frontend route hiding for security.

------------------------------------------------------------------------

# 5. Standard Response Format

## Success

For single resources:

``` json
{
  "data": {
    "id": "uuid",
    "..."
  }
}
```

For collections:

``` json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

For actions:

``` json
{
  "data": {
    "status": "completed"
  }
}
```

------------------------------------------------------------------------

# 6. Standard Error Format

All errors should follow:

``` json
{
  "error": {
    "code": "ASSESSMENT_NOT_FOUND",
    "message": "The assessment could not be found.",
    "details": {},
    "request_id": "uuid"
  }
}
```

Do not expose:

-   stack traces
-   SQL errors
-   API keys
-   internal infrastructure details
-   prompt secrets

in production responses.

------------------------------------------------------------------------

# 7. HTTP Status Codes

Use:

``` text
200 OK
201 Created
202 Accepted
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
429 Too Many Requests
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
```

------------------------------------------------------------------------

# 8. Health Endpoints

## GET `/health`

Public/simple liveness check.

Response:

``` json
{
  "status": "ok"
}
```

## GET `/ready`

Checks required dependencies.

Response:

``` json
{
  "status": "ready",
  "dependencies": {
    "database": "ok",
    "redis": "ok"
  }
}
```

------------------------------------------------------------------------

# 9. Authentication API

## POST `/auth/register`

Create learner account.

Request:

``` json
{
  "full_name": "Manasvi",
  "email": "user@example.com",
  "password": "********",
  "accept_terms": true
}
```

Response:

``` text
201 Created
```

``` json
{
  "data": {
    "user": {
      "id": "uuid",
      "full_name": "Manasvi",
      "email": "user@example.com",
      "email_verified": false
    }
  }
}
```

------------------------------------------------------------------------

## POST `/auth/login`

Request:

``` json
{
  "email": "user@example.com",
  "password": "********"
}
```

Response contains authenticated session information.

Do not return password data.

------------------------------------------------------------------------

## POST `/auth/refresh`

Refresh access token.

------------------------------------------------------------------------

## POST `/auth/logout`

Invalidate current refresh session.

Response:

``` text
204 No Content
```

------------------------------------------------------------------------

## POST `/auth/verify-email`

Verify email using a verification token.

------------------------------------------------------------------------

## POST `/auth/resend-verification`

Request a new verification email.

------------------------------------------------------------------------

## POST `/auth/forgot-password`

Request password reset.

Always return a generic success message to avoid account enumeration.

------------------------------------------------------------------------

## POST `/auth/reset-password`

Request:

``` json
{
  "token": "reset-token",
  "new_password": "********"
}
```

------------------------------------------------------------------------

# 10. Current User

## GET `/me`

Return authenticated user's basic profile.

Response:

``` json
{
  "data": {
    "id": "uuid",
    "full_name": "Manasvi",
    "email": "user@example.com",
    "roles": ["student"],
    "email_verified": true
  }
}
```

------------------------------------------------------------------------

## PATCH `/me`

Update basic profile.

Allowed:

-   name
-   avatar
-   timezone

------------------------------------------------------------------------

# 11. Learner Profile API

## GET `/me/learner-profile`

Returns learning preferences.

## PUT `/me/learner-profile`

Request:

``` json
{
  "learning_style": "mixed",
  "learning_speed": "moderate",
  "preferred_session_minutes": 30,
  "preferred_study_period": "evening",
  "timezone": "Asia/Kolkata"
}
```

------------------------------------------------------------------------

# 12. Subjects

## GET `/subjects`

List published subjects.

Query:

``` text
?page=1&page_size=20&search=python
```

------------------------------------------------------------------------

## GET `/subjects/{subject_id}`

Return subject details.

------------------------------------------------------------------------

## GET `/subjects/{subject_id}/topics`

Return topic hierarchy.

------------------------------------------------------------------------

## GET `/subjects/{subject_id}/concepts`

Query:

``` text
?topic_id=uuid&search=functions
```

------------------------------------------------------------------------

# 13. Learning Goals

## GET `/learning-goals`

Return available goals.

Example response:

``` json
{
  "data": [
    {
      "id": "uuid",
      "code": "learn_from_scratch",
      "name": "Learn from Scratch",
      "description": "Build foundational understanding."
    }
  ]
}
```

------------------------------------------------------------------------

# 14. Learner Subjects

## GET `/me/subjects`

Return subjects the learner is studying.

------------------------------------------------------------------------

## POST `/me/subjects`

Request:

``` json
{
  "subject_id": "uuid",
  "learning_goal_id": "uuid",
  "target_mastery": 85
}
```

------------------------------------------------------------------------

## GET `/me/subjects/{learner_subject_id}`

Return learner-subject status.

------------------------------------------------------------------------

## PATCH `/me/subjects/{learner_subject_id}`

Update:

-   target mastery
-   status
-   learning goal

------------------------------------------------------------------------

# 15. Onboarding

## POST `/onboarding/complete`

Request:

``` json
{
  "learner_profile": {
    "learning_style": "mixed",
    "learning_speed": "moderate",
    "preferred_session_minutes": 30,
    "preferred_study_period": "evening",
    "timezone": "Asia/Kolkata"
  },
  "subject_id": "uuid",
  "learning_goal_id": "uuid"
}
```

Response:

``` json
{
  "data": {
    "onboarding_completed": true,
    "learner_subject_id": "uuid"
  }
}
```

------------------------------------------------------------------------

# 16. Adaptive Assessment

## POST `/assessments`

Create a diagnostic/adaptive assessment.

Request:

``` json
{
  "learner_subject_id": "uuid",
  "assessment_type": "diagnostic"
}
```

Response:

``` json
{
  "data": {
    "id": "uuid",
    "status": "ready",
    "assessment_type": "diagnostic"
  }
}
```

------------------------------------------------------------------------

## GET `/assessments/{assessment_id}`

Return assessment status.

Do not expose correct answers.

------------------------------------------------------------------------

## POST `/assessments/{assessment_id}/start`

Create an assessment attempt.

Response:

``` json
{
  "data": {
    "attempt_id": "uuid",
    "status": "in_progress"
  }
}
```

------------------------------------------------------------------------

## POST `/assessments/{assessment_id}/next-question`

Generate/select the next question based on:

-   learner mastery
-   concept prerequisites
-   previous answers
-   difficulty
-   assessment objective

Request:

``` json
{
  "attempt_id": "uuid"
}
```

Response:

``` json
{
  "data": {
    "assessment_item_id": "uuid",
    "question": {
      "id": "uuid",
      "type": "mcq",
      "concept": {
        "id": "uuid",
        "name": "Functions"
      },
      "prompt": "Which statement correctly defines..."
    },
    "position": 4
  }
}
```

The response must never contain the correct answer.

------------------------------------------------------------------------

## POST `/assessments/{assessment_id}/responses`

Submit an answer.

Request:

``` json
{
  "attempt_id": "uuid",
  "assessment_item_id": "uuid",
  "answer_data": {
    "selected_option": "B"
  },
  "confidence_rating": 4
}
```

Response:

``` json
{
  "data": {
    "is_correct": true,
    "score": 1,
    "concept": {
      "id": "uuid",
      "name": "Functions"
    },
    "mastery_update": {
      "previous_score": 62,
      "new_score": 69,
      "state": "partial"
    }
  }
}
```

The API may reveal whether the submitted answer was correct after
submission.

------------------------------------------------------------------------

## POST `/assessments/{assessment_id}/complete`

Complete the attempt.

Response:

``` json
{
  "data": {
    "attempt_id": "uuid",
    "status": "completed",
    "analysis_available": true
  }
}
```

------------------------------------------------------------------------

# 17. Assessment Analysis

## GET `/assessments/{assessment_id}/analysis`

Returns concept-level analysis.

Example:

``` json
{
  "data": {
    "summary": {
      "mastered": 6,
      "partial": 4,
      "weak": 3,
      "unknown": 2
    },
    "concepts": [
      {
        "concept_id": "uuid",
        "name": "Functions",
        "mastery_score": 64,
        "state": "partial",
        "confidence": 72
      }
    ]
  }
}
```

------------------------------------------------------------------------

# 18. Knowledge Graph API

## GET `/me/knowledge-graph`

Query:

``` text
?subject_id=uuid
```

Response:

``` json
{
  "data": {
    "subject_id": "uuid",
    "nodes": [
      {
        "concept_id": "uuid",
        "name": "Functions",
        "mastery_score": 64,
        "mastery_state": "partial"
      }
    ],
    "edges": [
      {
        "from": "uuid",
        "to": "uuid",
        "relationship": "prerequisite"
      }
    ]
  }
}
```

------------------------------------------------------------------------

## GET `/me/knowledge-graph/concepts/{concept_id}`

Return detailed concept state:

-   mastery
-   confidence
-   attempts
-   correct attempts
-   last assessed
-   last practiced
-   last revised
-   prerequisites
-   dependent concepts
-   next review

------------------------------------------------------------------------

## POST `/me/knowledge-graph/concepts/{concept_id}/practice`

Start targeted practice.

------------------------------------------------------------------------

# 19. Learning Paths

## POST `/me/learning-paths/generate`

Generate/update path from learner mastery.

Request:

``` json
{
  "learner_subject_id": "uuid"
}
```

Response:

``` json
{
  "data": {
    "learning_path_id": "uuid",
    "status": "active",
    "estimated_minutes": 420
  }
}
```

If generation is expensive, return `202 Accepted` with a job/status
reference.

------------------------------------------------------------------------

## GET `/me/learning-paths`

List paths.

------------------------------------------------------------------------

## GET `/me/learning-paths/{path_id}`

Return path and steps.

Response structure:

``` json
{
  "data": {
    "id": "uuid",
    "status": "active",
    "progress_percent": 42,
    "steps": [
      {
        "id": "uuid",
        "concept": {
          "id": "uuid",
          "name": "Functions"
        },
        "status": "ready",
        "estimated_minutes": 30,
        "mastery_score": 64
      }
    ]
  }
}
```

------------------------------------------------------------------------

## POST `/me/learning-paths/{path_id}/steps/{step_id}/start`

Start step.

------------------------------------------------------------------------

## POST `/me/learning-paths/{path_id}/steps/{step_id}/complete`

Complete step after the required learning evidence is recorded.

------------------------------------------------------------------------

# 20. Recommendations

## GET `/me/recommendations`

Query:

``` text
?concept_id=uuid&type=learn
```

Return ranked resources with explainable reasons.

------------------------------------------------------------------------

## POST `/recommendations/{recommendation_id}/feedback`

Request:

``` json
{
  "feedback": "helpful",
  "reason": "The explanation matched my level."
}
```

------------------------------------------------------------------------

# 21. Resources

## GET `/resources/{resource_id}`

Return resource details.

------------------------------------------------------------------------

## GET `/subjects/{subject_id}/resources`

Filters:

``` text
?concept_id=uuid
&type=video
&difficulty=beginner
&max_minutes=30
```

------------------------------------------------------------------------

# 22. Video API

## GET `/videos/{video_id}`

Return:

-   duration
-   processing status
-   transcript availability
-   segments

------------------------------------------------------------------------

## GET `/videos/{video_id}/segments`

Return only learner-eligible approved segments.

------------------------------------------------------------------------

## GET `/videos/{video_id}/playback-plan`

This is a critical endpoint.

It returns the personalized viewing plan.

Request query:

``` text
?subject_id=uuid
```

Response:

``` json
{
  "data": {
    "video_id": "uuid",
    "auto_skip_enabled": true,
    "segments": [
      {
        "segment_id": "uuid",
        "start_seconds": 0,
        "end_seconds": 120,
        "concept_ids": ["uuid"],
        "mastery_state": "mastered",
        "action": "skip",
        "reason": "You have already demonstrated mastery of this concept."
      },
      {
        "segment_id": "uuid",
        "start_seconds": 120,
        "end_seconds": 300,
        "concept_ids": ["uuid"],
        "mastery_state": "weak",
        "action": "watch",
        "reason": "This concept is currently weak."
      }
    ]
  }
}
```

The frontend uses this to implement smart video behavior.

------------------------------------------------------------------------

## POST `/videos/{video_id}/events`

Record playback events.

Request:

``` json
{
  "segment_id": "uuid",
  "event_type": "skipped",
  "position_seconds": 145.2,
  "duration_seconds": 85
}
```

------------------------------------------------------------------------

# 23. Video Processing --- Instructor

## POST `/instructor/videos`

Create/upload video metadata.

For large files, use a presigned object-storage upload rather than
sending the entire file through FastAPI.

------------------------------------------------------------------------

## POST `/instructor/videos/{video_id}/process`

Start asynchronous processing.

Response:

``` text
202 Accepted
```

``` json
{
  "data": {
    "video_id": "uuid",
    "status": "processing"
  }
}
```

------------------------------------------------------------------------

## GET `/instructor/videos/{video_id}/processing-status`

Return:

``` json
{
  "data": {
    "transcription": "completed",
    "segmentation": "processing",
    "concept_tagging": "pending"
  }
}
```

------------------------------------------------------------------------

# 24. Video Segment Review

## GET `/instructor/videos/{video_id}/segments`

Return all segments, including pending/rejected.

------------------------------------------------------------------------

## PATCH `/instructor/video-segments/{segment_id}`

Instructor can edit:

-   title
-   timestamps
-   transcript
-   concept mapping

------------------------------------------------------------------------

## POST `/instructor/video-segments/{segment_id}/approve`

Approve segment.

------------------------------------------------------------------------

## POST `/instructor/video-segments/{segment_id}/reject`

Reject segment.

------------------------------------------------------------------------

## POST `/instructor/video-segments/{segment_id}/request-changes`

Request changes.

------------------------------------------------------------------------

# 25. Practice

## POST `/practice/sessions`

Start targeted practice.

Request:

``` json
{
  "concept_id": "uuid",
  "question_count": 10
}
```

------------------------------------------------------------------------

## GET `/practice/sessions/{session_id}`

Return practice status.

------------------------------------------------------------------------

## POST `/practice/sessions/{session_id}/next-question`

Generate/select next question.

------------------------------------------------------------------------

## POST `/practice/sessions/{session_id}/responses`

Submit answer.

------------------------------------------------------------------------

## POST `/practice/sessions/{session_id}/complete`

Complete practice session.

------------------------------------------------------------------------

# 26. AI Tutor

## POST `/tutor/conversations`

Create conversation.

Request:

``` json
{
  "subject_id": "uuid",
  "concept_id": "uuid",
  "title": "Help with recursion"
}
```

------------------------------------------------------------------------

## GET `/tutor/conversations`

List learner conversations.

------------------------------------------------------------------------

## GET `/tutor/conversations/{conversation_id}`

Return conversation history.

------------------------------------------------------------------------

## POST `/tutor/conversations/{conversation_id}/messages`

Send learner message.

Request:

``` json
{
  "message": "Explain recursion using a simple example."
}
```

Response:

``` json
{
  "data": {
    "message_id": "uuid",
    "content": "..."
  }
}
```

The backend builds context from:

-   current concept
-   mastery
-   relevant resources
-   transcripts
-   learning goal
-   recent mistakes where appropriate

The browser never calls the LLM provider directly.

------------------------------------------------------------------------

# 27. Analytics

## GET `/me/analytics/overview`

Return:

-   overall mastery
-   concepts mastered
-   study hours
-   streak
-   time saved

------------------------------------------------------------------------

## GET `/me/analytics/mastery`

Query:

``` text
?subject_id=uuid&range=30d
```

Return mastery-over-time series.

------------------------------------------------------------------------

## GET `/me/analytics/study-time`

Return study-time series.

------------------------------------------------------------------------

## GET `/me/analytics/quiz-performance`

Return:

-   accuracy
-   attempts
-   trend
-   concept breakdown

------------------------------------------------------------------------

## GET `/me/analytics/concepts`

Return:

-   strongest concepts
-   weakest concepts
-   most improved
-   at-risk concepts

------------------------------------------------------------------------

## GET `/me/analytics/time-saved`

Return:

``` json
{
  "data": {
    "seconds_saved": 45600,
    "hours_saved": 12.67
  }
}
```

Time saved must be calculated from recorded eligible skip events, not
guessed.

------------------------------------------------------------------------

## GET `/me/analytics/insights`

Return AI-generated learning insights.

Example:

``` json
{
  "data": [
    {
      "type": "trend",
      "message": "Your quiz accuracy improved this week, but weekend study consistency decreased."
    }
  ]
}
```

AI insights must be based on actual learner data.

------------------------------------------------------------------------

# 28. Study Planner

## GET `/me/planner`

Query:

``` text
?start_date=2026-08-10&end_date=2026-08-16
```

------------------------------------------------------------------------

## POST `/me/planner/generate`

Generate a study plan based on:

-   learner preferences
-   path
-   revision schedule
-   available time

------------------------------------------------------------------------

## PATCH `/me/planner/sessions/{session_id}`

Update a planned session.

------------------------------------------------------------------------

# 29. Notes

## GET `/me/notes`

Filters:

``` text
?concept_id=uuid
&resource_id=uuid
```

------------------------------------------------------------------------

## POST `/me/notes`

Create note.

------------------------------------------------------------------------

## PATCH `/me/notes/{note_id}`

Update note.

------------------------------------------------------------------------

## DELETE `/me/notes/{note_id}`

Delete note.

------------------------------------------------------------------------

# 30. Bookmarks

## GET `/me/bookmarks`

------------------------------------------------------------------------

## POST `/me/bookmarks`

------------------------------------------------------------------------

## DELETE `/me/bookmarks/{bookmark_id}`

------------------------------------------------------------------------

# 31. Revision

## GET `/me/revision/due`

Return concepts currently due for review.

------------------------------------------------------------------------

## POST `/me/revision/sessions`

Start revision.

------------------------------------------------------------------------

## POST `/me/revision/sessions/{session_id}/complete`

Complete revision and update schedule.

------------------------------------------------------------------------

# 32. Achievements

## GET `/me/achievements`

Return:

-   earned
-   locked
-   progress

------------------------------------------------------------------------

## GET `/me/streak`

Return current and longest streak.

------------------------------------------------------------------------

# 33. Certificates

## GET `/me/certificates`

List certificates.

------------------------------------------------------------------------

## GET `/me/certificates/{certificate_id}`

Return certificate metadata.

------------------------------------------------------------------------

## GET `/me/certificates/{certificate_id}/download`

Return a secure download URL.

------------------------------------------------------------------------

# 34. Instructor APIs

All routes require `instructor` or `admin` role.

## GET `/instructor/overview`

Return:

-   active learners
-   course completion
-   average mastery
-   weak concepts
-   content performance

------------------------------------------------------------------------

## GET `/instructor/courses`

List instructor courses.

------------------------------------------------------------------------

## POST `/instructor/courses`

Create course.

------------------------------------------------------------------------

## PATCH `/instructor/courses/{course_id}`

Update course.

------------------------------------------------------------------------

## POST `/instructor/courses/{course_id}/publish`

Publish course.

------------------------------------------------------------------------

## POST `/instructor/courses/{course_id}/unpublish`

Unpublish course.

------------------------------------------------------------------------

## GET `/instructor/courses/{course_id}/analytics`

Return course analytics.

------------------------------------------------------------------------

# 35. Instructor Question Review

## GET `/instructor/questions/review-queue`

Return generated questions awaiting review.

------------------------------------------------------------------------

## GET `/instructor/questions/{question_id}`

Return question and AI metadata.

------------------------------------------------------------------------

## PATCH `/instructor/questions/{question_id}`

Edit question.

------------------------------------------------------------------------

## POST `/instructor/questions/{question_id}/approve`

Approve.

------------------------------------------------------------------------

## POST `/instructor/questions/{question_id}/reject`

Reject.

------------------------------------------------------------------------

## POST `/instructor/questions/{question_id}/regenerate`

Request AI regeneration.

------------------------------------------------------------------------

# 36. Instructor Student Analytics

## GET `/instructor/students`

Search/filter learners.

------------------------------------------------------------------------

## GET `/instructor/students/{user_id}/overview`

Return learner overview.

------------------------------------------------------------------------

## GET `/instructor/students/{user_id}/concepts`

Return concept-level mastery.

------------------------------------------------------------------------

## GET `/instructor/students/{user_id}/activity`

Return learning activity.

------------------------------------------------------------------------

# 37. Cohorts

## GET `/instructor/cohorts`

------------------------------------------------------------------------

## POST `/instructor/cohorts`

Create cohort.

------------------------------------------------------------------------

## POST `/instructor/cohorts/{cohort_id}/members`

Add learner.

------------------------------------------------------------------------

## DELETE `/instructor/cohorts/{cohort_id}/members/{user_id}`

Remove learner.

------------------------------------------------------------------------

## GET `/instructor/cohorts/{cohort_id}/analytics`

Return cohort analytics.

------------------------------------------------------------------------

# 38. Admin APIs

All routes require `admin`.

## GET `/admin/users`

Query:

``` text
?search=
&role=
&status=
&page=1
&page_size=50
```

------------------------------------------------------------------------

## GET `/admin/users/{user_id}`

------------------------------------------------------------------------

## PATCH `/admin/users/{user_id}/status`

Suspend/activate user.

------------------------------------------------------------------------

## PATCH `/admin/users/{user_id}/roles`

Change roles.

Every role change must create an audit log.

------------------------------------------------------------------------

# 39. Taxonomy Administration

## POST `/admin/subjects`

Create subject.

------------------------------------------------------------------------

## PATCH `/admin/subjects/{subject_id}`

Update subject.

------------------------------------------------------------------------

## POST `/admin/topics`

Create topic.

------------------------------------------------------------------------

## PATCH `/admin/topics/{topic_id}`

Update topic.

------------------------------------------------------------------------

## POST `/admin/concepts`

Create concept.

------------------------------------------------------------------------

## PATCH `/admin/concepts/{concept_id}`

Update concept.

------------------------------------------------------------------------

## POST `/admin/concepts/{concept_id}/prerequisites`

Create prerequisite edge.

The backend must detect and reject graph cycles.

------------------------------------------------------------------------

## DELETE `/admin/concepts/{concept_id}/prerequisites/{prerequisite_id}`

Remove prerequisite edge.

------------------------------------------------------------------------

# 40. Content Moderation

## GET `/admin/content/review-queue`

Return pending review items.

------------------------------------------------------------------------

## POST `/admin/content/{entity_type}/{entity_id}/approve`

Approve content.

------------------------------------------------------------------------

## POST `/admin/content/{entity_type}/{entity_id}/reject`

Reject content.

------------------------------------------------------------------------

# 41. AI Configuration

Admin-only.

## GET `/admin/ai/models`

Return configured model identifiers and providers without exposing
secrets.

------------------------------------------------------------------------

## GET `/admin/ai/prompts`

List prompt versions.

------------------------------------------------------------------------

## POST `/admin/ai/prompts`

Create prompt version.

------------------------------------------------------------------------

## POST `/admin/ai/prompts/{prompt_id}/activate`

Activate prompt version.

------------------------------------------------------------------------

## GET `/admin/ai/usage`

Return:

-   request count
-   token usage
-   estimated cost
-   failure rate
-   latency

------------------------------------------------------------------------

# 42. Audit Logs

## GET `/admin/audit-logs`

Filters:

``` text
?actor_user_id=
&action=
&entity_type=
&start_date=
&end_date=
```

Audit logs are read-only through the admin API.

------------------------------------------------------------------------

# 43. Billing --- Future

## GET `/billing/plans`

Public/learner-accessible plan list.

------------------------------------------------------------------------

## POST `/billing/checkout`

Create checkout session.

------------------------------------------------------------------------

## GET `/billing/subscription`

Return current subscription.

------------------------------------------------------------------------

## POST `/billing/webhook`

Provider webhook.

This endpoint must:

-   verify provider signature
-   be idempotent
-   never trust client-provided payment status

------------------------------------------------------------------------

# 44. Pagination

Default:

``` text
page=1
page_size=20
```

Maximum:

``` text
page_size=100
```

For high-volume analytics/event APIs, cursor pagination may be used
later.

------------------------------------------------------------------------

# 45. Filtering and Sorting

Use predictable query parameters.

Example:

``` text
?status=active
&sort=-created_at
&page=1
&page_size=20
```

Do not expose arbitrary SQL/order expressions.

Whitelist sortable fields.

------------------------------------------------------------------------

# 46. Idempotency

Required for:

-   payment operations
-   assessment response submission where retries could duplicate answers
-   mastery events
-   certificate generation
-   content approval actions
-   asynchronous job creation where applicable

Client may send:

``` text
Idempotency-Key: <unique-value>
```

The server must safely handle repeated requests.

------------------------------------------------------------------------

# 47. Background Jobs

The following endpoints may return `202 Accepted`:

``` text
POST /instructor/videos/{video_id}/process
POST /me/learning-paths/generate
POST /admin/ai/prompts/{prompt_id}/...
```

Recommended generic job status endpoint:

``` text
GET /jobs/{job_id}
```

Response:

``` json
{
  "data": {
    "id": "uuid",
    "type": "video_processing",
    "status": "processing",
    "progress": 64,
    "error": null
  }
}
```

Job statuses:

``` text
queued
processing
completed
failed
cancelled
```

------------------------------------------------------------------------

# 48. API and Knowledge Graph Rules

The API must preserve the rule:

> AI suggests; application logic decides.

For example:

``` text
AI
↓
suggests question
↓
backend validates
↓
learner answers
↓
deterministic scoring
↓
mastery service updates graph
```

Never allow:

``` text
LLM → directly writes mastery_score
```

------------------------------------------------------------------------

# 49. API and Video Rules

The smart video API must never blindly trust AI segmentation.

Required:

``` text
AI segmentation
↓
review status
↓
approved?
├── No → learner cannot auto-skip
└── Yes → eligible for personalized playback plan
```

A learner can always request:

``` text
Watch Anyway
```

even when the system recommends skipping.

------------------------------------------------------------------------

# 50. API and Analytics Rules

Analytics must be derived from actual events.

For example:

``` text
video segment skipped
↓
video_watch_event
↓
analytics_event
↓
daily metric aggregation
↓
time saved
```

Do not fabricate time-saved values from the UI.

------------------------------------------------------------------------

# 51. API Security Rules

1.  All protected routes require authentication.
2.  Role checks happen server-side.
3.  Object ownership must be verified.
4.  Instructors can only modify resources they are authorized to manage.
5.  Students cannot access another student's mastery data.
6.  Admin endpoints require admin role.
7.  Correct answers are never returned before submission.
8.  AI keys remain server-side.
9.  Rate limit authentication and AI-heavy endpoints.
10. Validate all request bodies.
11. Validate uploaded file types and sizes.
12. Generate signed URLs for private media.
13. Log security-sensitive administrative actions.

------------------------------------------------------------------------

# 52. Frontend API Mapping

  -----------------------------------------------------------------------
  Screen                              API endpoints
  ----------------------------------- -----------------------------------
  Login                               `/auth/login`

  Register                            `/auth/register`

  Onboarding                          `/onboarding/complete`,
                                      `/subjects`, `/learning-goals`

  Dashboard                           `/me`, `/me/subjects`,
                                      `/me/learning-paths`,
                                      `/me/analytics/overview`

  Assessment                          `/assessments`,
                                      `/assessments/{id}/start`,
                                      `/next-question`, `/responses`,
                                      `/complete`

  Analysis                            `/assessments/{id}/analysis`

  Knowledge Graph                     `/me/knowledge-graph`

  Learning Path                       `/me/learning-paths/{id}`

  Recommendations                     `/me/recommendations`

  Video                               `/videos/{id}`, `/playback-plan`,
                                      `/events`

  Practice                            `/practice/sessions/...`

  AI Tutor                            `/tutor/conversations/...`

  Analytics                           `/me/analytics/...`

  Planner                             `/me/planner...`

  Achievements                        `/me/achievements`, `/me/streak`

  Certificates                        `/me/certificates`

  Profile                             `/me`, `/me/learner-profile`

  Instructor                          `/instructor/...`

  Admin                               `/admin/...`
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 53. API Implementation Folder Structure

``` text
backend/app/
├── main.py
├── core/
│   ├── config.py
│   ├── security.py
│   ├── errors.py
│   └── logging.py
│
├── api/
│   ├── deps.py
│   └── router.py
│
├── modules/
│   ├── auth/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── models.py
│   │
│   ├── assessments/
│   ├── knowledge_graph/
│   ├── learning_paths/
│   ├── recommendations/
│   ├── videos/
│   ├── tutor/
│   ├── analytics/
│   ├── users/
│   ├── subjects/
│   ├── content/
│   ├── gamification/
│   ├── notifications/
│   └── admin/
│
├── ai/
│   ├── providers/
│   ├── prompts/
│   └── schemas/
│
├── workers/
│   └── tasks/
│
└── db/
    ├── session.py
    ├── base.py
    └── migrations/
```

Each module should separate:

``` text
router
schemas
service
repository/data access
models
```

Do not put all business logic inside FastAPI route functions.

------------------------------------------------------------------------

# 54. API Development Order

Implement in this order:

## Phase 1 --- Foundation

``` text
health
auth
users
learner profile
subjects
learning goals
```

## Phase 2 --- Core Adaptive Loop

``` text
assessments
questions
attempts
responses
mastery
knowledge graph
```

## Phase 3 --- Personalization

``` text
learning paths
recommendations
resources
```

## Phase 4 --- Learning Experience

``` text
videos
video segments
practice
revision
notes
bookmarks
```

## Phase 5 --- Intelligence

``` text
AI tutor
AI insights
AI generation metadata
```

## Phase 6 --- Analytics

``` text
events
metrics
mastery trends
time saved
```

## Phase 7 --- Engagement

``` text
achievements
streaks
certificates
notifications
```

## Phase 8 --- Instructor/Admin

``` text
courses
video review
question review
student analytics
taxonomy administration
audit logs
```

## Phase 9 --- Billing

``` text
plans
subscriptions
payments
```

Billing must not block the learning MVP.

------------------------------------------------------------------------

# 55. API Definition of Done

An endpoint is complete only when:

-   request schema exists
-   response schema exists
-   authorization is defined
-   validation exists
-   service logic is separated from route logic
-   database access is tested
-   error cases are tested
-   happy path is tested
-   OpenAPI documentation is accurate
-   frontend integration requirements are documented
-   idempotency is considered where relevant
-   logging exists for important operations

------------------------------------------------------------------------

# 56. Final API Architecture

``` text
                    Next.js
                       │
                       │ HTTPS / REST
                       ▼
                FastAPI API Layer
                       │
              ┌────────┴────────┐
              │                 │
         Auth / RBAC        Domain Services
                                │
       ┌────────────────────────┼─────────────────────┐
       │                        │                     │
       ▼                        ▼                     ▼
 Knowledge Graph          Assessment            Learning Path
       │                        │                     │
       └───────────────┬────────┴─────────────┬──────┘
                       │                      │
                       ▼                      ▼
                  PostgreSQL              Redis
                       │                      │
                       │                Background Jobs
                       │                      │
              ┌────────┴────────┐             ▼
              │                 │          AI / Video
              ▼                 ▼
          pgvector        Object Storage
              │                 │
              └────────┬────────┘
                       ▼
                    Analytics
```

------------------------------------------------------------------------

# 57. Non-Negotiable API Rules

1.  REST + OpenAPI is the MVP API architecture.
2.  `/api/v1` is mandatory for application endpoints.
3.  Frontend never calls OpenAI directly.
4.  Database models are never returned directly.
5.  Correct answers are never exposed before submission.
6.  LLM output never directly determines authoritative mastery.
7.  Only approved video segments can drive auto-skip.
8.  All learner data is protected by ownership checks.
9.  All admin actions are audited.
10. AI-heavy work can be asynchronous.
11. Analytics are based on real events.
12. API contracts must be updated before breaking frontend/backend
    changes.
13. New endpoints must be added to this specification.
14. Do not introduce GraphQL unless a measured product need exists.
15. Do not split the backend into microservices during MVP.

**End of API_SPECIFICATION.md**
