# AI-Powered Adaptive Learning Platform

## Screen Specification & User Flow (v1.0)

**Status:** Pre-development specification\
**Based on:** `PROJECT_BLUEPRINT.md`, `UI_DESIGN_SYSTEM.md`, and
`TECH_STACK.md`\
**Purpose:** Define every important screen, its purpose, content,
states, actions, navigation, and API/data needs before frontend
implementation.

------------------------------------------------------------------------

# 1. How to Use This Document

This document is the screen-level source of truth for frontend
implementation.

It answers:

-   What screens exist?
-   Who can access them?
-   What does each screen contain?
-   What can the user do?
-   What happens after each action?
-   What loading, error, empty, and success states exist?
-   What data does each screen need?
-   Which backend capability will eventually power it?

It does **not** define database tables or detailed API contracts. Those
belong in `DATABASE_SCHEMA.md` and `API_SPECIFICATION.md`.

All screens must follow `UI_DESIGN_SYSTEM.md`.

------------------------------------------------------------------------

# 2. MVP Scope

The first working student experience should prioritize the core
adaptive-learning loop:

``` text
Landing
  ↓
Register / Login
  ↓
Onboarding
  ↓
Select Subject
  ↓
Choose Learning Goal
  ↓
Learner Profile
  ↓
Adaptive Assessment
  ↓
Concept Analysis
  ↓
Knowledge Graph
  ↓
Personalized Learning Path
  ↓
Recommended Resource
  ↓
Smart Video / Lesson
  ↓
AI Tutor / Practice
  ↓
Adaptive Quiz
  ↓
Knowledge Graph Update
  ↓
Analytics
  ↓
Next Concept OR Revision
```

Instructor and admin capabilities are designed in this document but can
be implemented after the student MVP is functional.

------------------------------------------------------------------------

# 3. Navigation Architecture

## 3.1 Public Navigation

Desktop:

``` text
Logo | Product | How It Works | Features | About | Login | Get Started
```

Mobile:

``` text
Logo | Menu
```

Primary CTA:

``` text
Get Started
```

------------------------------------------------------------------------

## 3.2 Student Application Navigation

Desktop sidebar:

``` text
Dashboard
My Learning
Learning Path
Knowledge Graph
Practice
AI Tutor
Analytics
Planner
Achievements
Certificates
────────────────
Profile
Settings
Help
```

Mobile:

``` text
Home
Learn
Practice
Tutor
Profile
```

Use a "More" destination for secondary pages when needed.

------------------------------------------------------------------------

## 3.3 Instructor Navigation

``` text
Overview
Courses
Content
Video Segments
Assessments
Students
Analytics
Discussions
Profile
Settings
```

------------------------------------------------------------------------

## 3.4 Admin Navigation

``` text
Overview
Users
Subjects & Taxonomy
Content Moderation
AI Configuration
Analytics
Subscriptions
Audit Logs
Settings
```

------------------------------------------------------------------------

# 4. Global Application Rules

Every authenticated screen must support:

-   loading state
-   error state
-   empty state where applicable
-   responsive layout
-   keyboard accessibility
-   visible focus states
-   consistent navigation
-   consistent AI identity

AI-generated content must be visually distinguishable from
user-created/system content.

Destructive actions require explicit confirmation.

------------------------------------------------------------------------

# 5. Public Screens

## 5.1 Landing Page

### Purpose

Explain the product and convert visitors into learners.

### Sections

1.  Navigation
2.  Hero
3.  Problem statement
4.  How adaptive learning works
5.  AI assessment demonstration
6.  Concept mastery / knowledge graph demonstration
7.  Smart video auto-skip demonstration
8.  Analytics demonstration
9.  AI Tutor demonstration
10. Feature grid
11. Testimonials / proof area
12. Pricing placeholder if billing is enabled
13. FAQ
14. Final CTA
15. Footer

### Hero message direction

Communicate the core value:

> Learn what you don't know. Skip what you already do.

Do not use exaggerated claims such as "learn anything instantly."

### Primary CTA

`Start Learning`

### Secondary CTA

`See How It Works`

### Key visual

A simplified animated flow:

``` text
Assessment → Diagnose → Learn → Re-assess
```

### States

Mostly static; animations should respect reduced-motion preferences.

------------------------------------------------------------------------

# 6. Authentication Screens

## 6.1 Login

### Content

-   Email
-   Password
-   Show/hide password
-   Remember session
-   Forgot password
-   Login
-   Create account

### Optional future

-   Continue with Google
-   Continue with GitHub

### Errors

-   invalid credentials
-   account not verified
-   server unavailable
-   rate limited

### Success

Redirect to intended destination or Dashboard.

------------------------------------------------------------------------

## 6.2 Register

Fields:

-   Name
-   Email
-   Password
-   Confirm password
-   Terms acceptance

CTA:

`Create Account`

After registration:

``` text
Register
↓
Email Verification
↓
Onboarding
```

------------------------------------------------------------------------

## 6.3 Email Verification

Show:

-   verification status
-   resend email
-   change email
-   continue after verification

------------------------------------------------------------------------

## 6.4 Forgot Password

Fields:

-   Email

Success:

> If an account exists for this email, a reset link has been sent.

Do not reveal whether an email is registered.

------------------------------------------------------------------------

## 6.5 Reset Password

Fields:

-   New password
-   Confirm password

Success:

Redirect to Login.

------------------------------------------------------------------------

# 7. Student Onboarding

## 7.1 Welcome

Purpose:

Introduce the adaptive process.

Show:

``` text
We first understand what you know.
Then we build what you need to learn.
```

CTA:

`Set Up My Learning`

------------------------------------------------------------------------

## 7.2 Learner Profile

Collect:

### Learning style

-   Visual / Video-first
-   Reading / Text-first
-   Practice-first
-   Mixed

### Learning speed

-   Fast
-   Moderate
-   Slow

### Preferred session duration

-   15 min
-   30 min
-   45--60 min
-   60+ min

### Preferred study time

-   Morning
-   Afternoon
-   Evening
-   Late night

Explain that these preferences can later be inferred/refined from
behavior.

CTA:

`Continue`

------------------------------------------------------------------------

## 7.3 Subject Selection

Search and browse subjects.

Example:

``` text
Python
Data Structures
Machine Learning
Web Development
```

Actions:

-   search
-   select
-   view subject details

CTA:

`Continue`

------------------------------------------------------------------------

## 7.4 Learning Goal

Per selected subject:

-   Interview Preparation
-   College Exams
-   Build Projects
-   Learn from Scratch
-   Revision
-   Advanced Mastery

Show a short explanation of how the goal changes recommendations.

CTA:

`Start Assessment`

------------------------------------------------------------------------

# 8. Adaptive Assessment

## 8.1 Assessment Introduction

Explain:

-   approximate duration
-   adaptive nature
-   no need to prepare
-   questions will change based on answers
-   final result will be concept-level, not just one score

CTA:

`Begin Assessment`

------------------------------------------------------------------------

## 8.2 Assessment Question

### Layout

Desktop:

``` text
Progress / question context
---------------------------
Concept area

Question

Answer options / editor

Confidence control (if enabled)

[Previous]             [Submit]
```

### Important

Do not display a traditional score after every question.

Show subtle progress information.

Difficulty should be controlled by the system, not manually exposed as a
game mechanic.

### States

-   question loading
-   question ready
-   submitting
-   answer accepted
-   generation failure
-   network failure

### AI generation

If a new question is being generated, use the AI loading language from
the Design System:

``` text
Generating your next question...
```

------------------------------------------------------------------------

## 8.3 Assessment Completion

Show:

-   completion message
-   total concepts assessed
-   assessment confidence / coverage
-   continue CTA

Do not immediately overwhelm the learner with a giant analytics
dashboard.

CTA:

`See My Learning Analysis`

------------------------------------------------------------------------

# 9. Concept-Level Analysis

## Purpose

Show the learner what they know before recommending learning.

### Main sections

#### Overall summary

Not just one percentage.

Example:

``` text
Strong: 6 concepts
Partial: 4 concepts
Weak: 3 concepts
Unknown: 2 concepts
```

#### Concept mastery

``` text
Variables       96%  Mastered
Loops           91%  Mastered
Functions       64%  Partial
OOP             37%  Weak
Recursion       12%  Weak
Decorators       0%  Unknown
```

#### Knowledge graph preview

Show a simplified graph.

CTA:

`View Full Knowledge Graph`

CTA:

`Build My Learning Path`

------------------------------------------------------------------------

# 10. Knowledge Graph

## Purpose

Make concept-level knowledge visible.

### Main controls

-   subject selector
-   search concept
-   filter by mastery state
-   zoom
-   reset view

### Node states

-   Mastered
-   Partial
-   Weak
-   Unknown

### Node interaction

Selecting a concept opens a detail panel containing:

-   mastery percentage
-   confidence
-   attempts
-   last assessed
-   last revised
-   prerequisites
-   dependent concepts
-   recommended next action

### Actions

`Learn This`

`Practice This`

`Ask AI Tutor`

### Empty state

If no assessment exists:

> Complete an assessment to build your knowledge graph.

CTA:

`Start Assessment`

------------------------------------------------------------------------

# 11. Personalized Learning Path

## Purpose

Turn graph analysis into an actionable roadmap.

### Header

Show:

-   Subject
-   Learning goal
-   Estimated remaining time
-   Progress

### Path structure

``` text
1. Functions
   ├── Video
   ├── Practice
   └── Quiz

2. OOP
   ├── Video
   ├── Notes
   └── Practice

3. Recursion
   ├── Video
   ├── Tutor
   └── Quiz
```

### Each path step shows

-   concept
-   mastery
-   prerequisites
-   estimated time
-   recommended resources
-   status

### Statuses

-   Locked
-   Ready
-   In Progress
-   Mastered
-   Needs Revision

### Locked concept

Explain why:

> Complete Functions first because it is a prerequisite for this
> concept.

CTA:

`Go to Prerequisite`

------------------------------------------------------------------------

# 12. Student Dashboard

## Purpose

Give the learner one clear place to continue learning.

### Top area

``` text
Good morning, [Name]
Continue where you left off.
```

### Primary CTA

`Continue Learning`

### Widgets

1.  Current learning path
2.  Current concept
3.  Overall mastery
4.  Learning streak
5.  Study time
6.  Time saved
7.  Weak concepts
8.  AI recommendation
9.  Recent activity
10. Upcoming revision

### AI insight

Example:

> You have strong fundamentals in loops and variables. Your current
> bottleneck is functions. Completing the next two lessons should unlock
> three dependent concepts.

------------------------------------------------------------------------

# 13. Resource Recommendation Screen

## Purpose

Present the best resources for a specific concept.

### Resource types

-   Video
-   Notes
-   Documentation
-   Coding exercise
-   Project
-   Flashcard
-   Article

### Resource card

Show:

-   title
-   type
-   estimated time
-   concept
-   difficulty
-   reason recommended

Example:

> Recommended because you prefer practice-first learning and this
> concept is currently weak.

### Filters

-   type
-   duration
-   difficulty

------------------------------------------------------------------------

# 14. Smart Video Player

## Purpose

Deliver only relevant video content.

### Layout

``` text
┌─────────────────────────────┐
│                             │
│         VIDEO               │
│                             │
└─────────────────────────────┘

Concept timeline
─────────────────────────────

Current concept

Transcript / Chapters

Notes | Bookmark | Ask AI
```

### Timeline

Use Mastery Fill:

``` text
[Mastered][Mastered][Partial][Weak][Unknown]
```

### Auto-skip

When a mastered segment is encountered:

``` text
You already know Loops.
Skipping to Functions...
[Watch Anyway]
```

### User controls

-   watch skipped section
-   disable auto-skip
-   jump to concept
-   bookmark
-   take notes
-   ask AI

### Trust requirement

Always explain why a segment was skipped.

Example:

> Skipped because your Functions mastery is 38%.

------------------------------------------------------------------------

# 15. Transcript / Chapter Panel

Show:

-   chapter title
-   concept
-   start timestamp
-   end timestamp
-   mastery state

Clicking a chapter seeks the player.

------------------------------------------------------------------------

# 16. AI Tutor

## Purpose

Provide context-aware help.

### Layout

``` text
Current Concept
----------------
Conversation
----------------
Message input
```

### Context shown to learner

Small indicator:

``` text
Learning context: Recursion
Your mastery: 22%
```

### Actions

-   explain simply
-   give example
-   give practice question
-   summarize
-   show mistake
-   ask follow-up

### AI identity

Use the AI visual identity from the design system.

Do not use a robot mascot.

### AI loading

Examples:

``` text
Thinking about your current concept...
Looking at your learning history...
Preparing an explanation...
```

------------------------------------------------------------------------

# 17. Practice Screen

## Purpose

Allow targeted practice without running the full assessment.

### Options

-   Practice weak concepts
-   Practice current concept
-   Practice prerequisites
-   Challenge mode

### Question flow

Similar to adaptive assessment but focused on a selected concept.

------------------------------------------------------------------------

# 18. Quiz Completion / Mastery Decision

After a quiz:

Show:

-   concept performance
-   mastery change
-   mistakes
-   explanation
-   next recommendation

Example:

``` text
Functions

Before: 64%
After: 78%

Status: Partial
```

### Decision

If threshold reached:

``` text
Concept mastered
↓
Next concept unlocked
```

Otherwise:

``` text
Mastery threshold not reached
↓
Revision recommendation
```

Do not shame the learner.

------------------------------------------------------------------------

# 19. Analytics Dashboard

## Purpose

Show progress over time and explain what is changing.

### Top metrics

-   Overall mastery
-   Concepts mastered
-   Study hours
-   Learning streak
-   Time saved

### Charts

1.  Mastery over time
2.  Quiz accuracy
3.  Study time
4.  Concept distribution
5.  Weekly activity
6.  Learning speed
7.  Video time saved

### Concept analysis

-   strongest concepts
-   weakest concepts
-   most improved
-   concepts at risk of decay

### AI insights

Example:

> Your accuracy improved 14% this week, but your study consistency
> dropped on weekends.

### Time Saved

Make this a prominent product metric.

``` text
12h 40m
saved by skipping concepts you already know
```

------------------------------------------------------------------------

# 20. Study Planner

## Purpose

Schedule learning around learner preferences.

### Calendar

-   day
-   week
-   month

### Session cards

Show:

-   concept
-   activity
-   duration
-   priority
-   reason

### Auto-plan

Use:

-   preferred study time
-   preferred session duration
-   remaining path
-   revision due dates

CTA:

`Generate My Study Plan`

------------------------------------------------------------------------

# 21. Achievements

## Sections

-   XP
-   Streak
-   Badges
-   Milestones

Keep visuals restrained.

Examples:

``` text
First Assessment
5 Concepts Mastered
7 Day Streak
10 Hours Saved
First Project Completed
```

------------------------------------------------------------------------

# 22. Certificates

### Certificate list

Show:

-   subject/path
-   completion date
-   mastery
-   certificate status

### Certificate detail

Show a professional certificate preview.

Actions:

`Download`

`Share`

------------------------------------------------------------------------

# 23. Profile

Sections:

-   personal information
-   learner profile
-   learning goals
-   preferences
-   subjects
-   achievements

Allow profile changes without deleting mastery history.

------------------------------------------------------------------------

# 24. Settings

Sections:

### Account

-   email
-   password
-   sessions

### Learning

-   learning style
-   speed
-   session duration
-   preferred study time

### Video

-   auto-skip on/off
-   confirmation before skip
-   playback speed

### Notifications

-   email
-   in-app
-   revision reminders
-   streak reminders

### Privacy

-   data export
-   account deletion

------------------------------------------------------------------------

# 25. Instructor Screens

## 25.1 Instructor Overview

Widgets:

-   active learners
-   course completion
-   average mastery
-   weak concepts
-   content performance

------------------------------------------------------------------------

## 25.2 Course Management

Actions:

-   create course
-   edit course
-   publish/unpublish
-   upload resources
-   organize concepts

------------------------------------------------------------------------

## 25.3 Video Upload

Flow:

``` text
Select video
↓
Upload
↓
Processing
↓
Transcription
↓
AI segmentation
↓
Concept tagging
↓
Review
↓
Publish
```

Show processing status.

------------------------------------------------------------------------

## 25.4 AI Segment Review

Show:

``` text
Video
Timeline
AI segments
Concept tags
Confidence
```

Instructor can:

-   edit timestamp
-   change concept
-   merge segments
-   split segment
-   delete segment
-   approve
-   reject

Approval is required before learner auto-skip is enabled.

------------------------------------------------------------------------

## 25.5 Question Review

Instructor sees:

-   generated question
-   concept
-   difficulty
-   answer
-   explanation
-   AI metadata

Actions:

-   approve
-   edit
-   reject
-   regenerate

------------------------------------------------------------------------

## 25.6 Class Analytics

Show:

-   mastery heatmap
-   weak concepts
-   student progress
-   assessment performance
-   resource performance

Instructor can drill down from class → student → concept.

------------------------------------------------------------------------

# 26. Admin Screens

## 26.1 Admin Overview

Metrics:

-   users
-   active learners
-   content
-   assessments
-   AI usage
-   retention
-   platform health

------------------------------------------------------------------------

## 26.2 User Management

Actions:

-   search
-   filter
-   view
-   suspend
-   change role
-   reset access

------------------------------------------------------------------------

## 26.3 Subject & Taxonomy Management

Manage:

``` text
Subject
↓
Topic
↓
Concept
↓
Sub-concept
```

Manage prerequisite relationships.

------------------------------------------------------------------------

## 26.4 Content Moderation

Queue:

-   pending videos
-   AI segments
-   AI questions
-   flagged content

------------------------------------------------------------------------

## 26.5 AI Configuration

Admin-only.

Show:

-   model configuration
-   prompt versions
-   AI usage
-   cost
-   evaluation status

Never expose API secrets.

------------------------------------------------------------------------

## 26.6 Platform Analytics

Show:

-   acquisition
-   engagement
-   retention
-   learning outcomes
-   content performance
-   AI usage
-   revenue when billing exists

------------------------------------------------------------------------

## 26.7 Audit Logs

Track:

-   user role changes
-   content approvals
-   AI configuration changes
-   billing changes
-   moderation actions

------------------------------------------------------------------------

# 27. Shared UI States

## Loading

Use skeletons for known page structures.

Use AI Thinking Animation for AI operations.

Never show an unexplained spinner when the user is waiting for AI.

------------------------------------------------------------------------

## Error

Every error must:

1.  explain what happened
2.  avoid technical jargon
3.  offer one recovery action

Example:

> We couldn't generate your next question.

CTA:

`Try Again`

------------------------------------------------------------------------

## Empty

Every empty state should:

1.  explain why
2.  explain what to do next
3.  contain one clear CTA

Example:

> Your knowledge graph is empty because you haven't completed an
> assessment yet.

CTA:

`Start Assessment`

------------------------------------------------------------------------

## Offline / Network Failure

Show:

> Your connection was interrupted. Your completed work is safe. We'll
> reconnect when possible.

Do not claim data was saved unless the system actually confirmed it.

------------------------------------------------------------------------

# 28. Critical User Flows

## Flow A --- New Learner

``` text
Landing
↓
Register
↓
Verify Email
↓
Welcome
↓
Learner Profile
↓
Subject
↓
Learning Goal
↓
Adaptive Assessment
↓
Concept Analysis
↓
Knowledge Graph
↓
Learning Path
↓
First Resource
```

------------------------------------------------------------------------

## Flow B --- Returning Learner

``` text
Login
↓
Dashboard
↓
Continue Learning
↓
Current Concept
↓
Resource
↓
Practice
↓
Knowledge Graph Update
↓
Next Concept / Revision
```

------------------------------------------------------------------------

## Flow C --- Smart Video

``` text
Learning Path
↓
Recommended Video
↓
Load learner mastery
↓
Identify mastered segments
↓
Start at first relevant segment
↓
Show skip explanation
↓
Continue learning
↓
Record watch/skip events
```

------------------------------------------------------------------------

## Flow D --- Adaptive Quiz

``` text
Select Concept
↓
Determine current mastery
↓
Generate question
↓
Answer
↓
Score
↓
Select next question
↓
Repeat
↓
Recalculate mastery
↓
Mastery threshold?
├── Yes → Unlock next concept
└── No → Revision loop
```

------------------------------------------------------------------------

## Flow E --- Instructor Video

``` text
Instructor uploads video
↓
Processing
↓
Transcript
↓
AI segmentation
↓
AI concept tags
↓
Instructor review
├── Edit
├── Reject
└── Approve
↓
Publish
↓
Learners can use smart skip
```

------------------------------------------------------------------------

# 29. Screen-to-Data Dependencies

  Screen              Main data needed
  ------------------- --------------------------------------------------
  Dashboard           learner profile, mastery summary, path, activity
  Subject Selection   subjects, taxonomy metadata
  Assessment          concepts, assessment state, generated questions
  Analysis            concept mastery, confidence, assessment summary
  Knowledge Graph     concepts, prerequisites, mastery
  Learning Path       path steps, concepts, prerequisites, resources
  Video Player        video metadata, segments, mastery, transcript
  AI Tutor            conversation, graph state, content retrieval
  Practice            concept mastery, generated questions
  Analytics           events, mastery snapshots, study sessions
  Planner             profile, path, revisions, sessions
  Achievements        XP, badges, streaks
  Certificates        completed paths, certificate metadata
  Instructor          courses, content, learners, analytics
  Admin               users, taxonomy, moderation, platform metrics

------------------------------------------------------------------------

# 30. API Boundary Rules

The frontend must not directly access:

-   PostgreSQL
-   Redis
-   OpenAI
-   object-storage secret credentials
-   internal worker services

The frontend communicates through the FastAPI API.

Conceptual boundary:

``` text
Browser
  ↓
Next.js
  ↓
FastAPI REST API
  ↓
Domain modules
  ↓
PostgreSQL / Redis / Storage / AI
```

------------------------------------------------------------------------

# 31. Responsive Rules

All screens must support:

### Desktop

Primary layout.

### Tablet

Collapsed navigation and responsive grids.

### Mobile

Single-column learning experience.

Important learning screens such as:

-   assessment
-   video
-   tutor

must remain usable without horizontal scrolling.

The Smart Video Player must prioritize video, current concept, and
controls on small screens.

------------------------------------------------------------------------

# 32. Accessibility Rules

Every screen must support:

-   keyboard navigation
-   visible focus
-   semantic HTML
-   accessible labels
-   sufficient contrast
-   reduced motion
-   screen-reader-compatible controls

Do not communicate mastery using color alone. Use text, icons, labels,
or patterns as appropriate.

------------------------------------------------------------------------

# 33. Screen Implementation Priority

## Priority 1 --- Core Student MVP

1.  Landing
2.  Register/Login
3.  Onboarding
4.  Subject Selection
5.  Learning Goal
6.  Adaptive Assessment
7.  Concept Analysis
8.  Dashboard
9.  Learning Path
10. Knowledge Graph
11. Resource Detail
12. Smart Video Player
13. Practice/Quiz
14. Analytics

## Priority 2

15. AI Tutor
16. Planner
17. Profile
18. Settings
19. Achievements
20. Certificates

## Priority 3

21. Instructor Dashboard
22. Course Management
23. Video Upload
24. Segment Review
25. Question Review
26. Class Analytics

## Priority 4

27. Admin Dashboard
28. Taxonomy Management
29. Moderation
30. AI Configuration
31. Platform Analytics
32. Audit Logs
33. Billing

------------------------------------------------------------------------

# 34. Definition of Done for a Screen

A screen is not considered complete until:

-   layout matches `UI_DESIGN_SYSTEM.md`
-   responsive behavior is implemented
-   loading state exists
-   error state exists
-   empty state exists where applicable
-   primary CTA works
-   navigation works
-   accessibility basics are implemented
-   API dependency is documented
-   no hard-coded fake production data remains unless explicitly marked
    as seed/demo data
-   frontend tests exist for important interactions

------------------------------------------------------------------------

# 35. Frontend Implementation Rule for AI Coding Tools

Every frontend coding prompt must instruct the AI to read:

``` text
docs/PROJECT_BLUEPRINT.md
docs/UI_DESIGN_SYSTEM.md
docs/TECH_STACK.md
docs/SCREEN_SPECIFICATION.md
```

before modifying the frontend.

The AI must:

-   reuse existing components
-   reuse existing tokens
-   avoid inventing new UI patterns
-   avoid changing architecture
-   avoid changing API contracts without explicit instruction
-   explain dependencies before adding new packages

------------------------------------------------------------------------

# 36. Final Product Navigation Map

``` text
PUBLIC
│
├── Landing
├── Login
├── Register
├── Verify Email
└── Password Reset

STUDENT
│
├── Dashboard
├── My Learning
│   ├── Learning Path
│   ├── Concept
│   ├── Resource
│   └── Video Player
│
├── Assessment
│   ├── Introduction
│   ├── Questions
│   └── Analysis
│
├── Knowledge Graph
├── Practice
├── AI Tutor
├── Analytics
├── Planner
├── Achievements
├── Certificates
├── Profile
└── Settings

INSTRUCTOR
│
├── Overview
├── Courses
├── Content
├── Video Upload
├── Segment Review
├── Assessment Review
├── Students
├── Analytics
└── Discussions

ADMIN
│
├── Overview
├── Users
├── Taxonomy
├── Content Moderation
├── AI Configuration
├── Analytics
├── Subscriptions
└── Audit Logs
```

------------------------------------------------------------------------

# 37. Final Core Experience

The entire interface must make this loop obvious:

``` text
                    ┌───────────────┐
                    │ Select Goal   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Assess      │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Diagnose    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Knowledge     │
                    │    Graph      │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Learning Path │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    Teach      │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    Practice   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  Re-assess    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Update Graph  │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Analytics   │
                    └───────┬───────┘
                            ↓
                  ┌─────────┴─────────┐
                  │                   │
             Mastered             Not Mastered
                  │                   │
                  ↓                   ↓
            Next Concept         Revision Loop
```

**End of SCREEN_SPECIFICATION.md**
