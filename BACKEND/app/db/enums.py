"""Centralized domain values used by model constraints and application code."""

LEARNING_STYLES = ("visual", "reading", "practice", "mixed")
LEARNING_SPEEDS = ("fast", "moderate", "slow")
STUDY_PERIODS = ("morning", "afternoon", "evening", "late_night")
LEARNER_SUBJECT_STATUSES = ("active", "paused", "completed", "archived")
COURSE_STATUSES = ("draft", "processing", "review", "published", "archived")
RESOURCE_TYPES = (
    "video",
    "notes",
    "documentation",
    "coding_exercise",
    "project",
    "flashcard",
    "article",
)
PROCESSING_STATUSES = ("pending", "processing", "completed", "failed")
VIDEO_SEGMENT_SOURCES = ("ai", "instructor", "hybrid")
REVIEW_STATUSES = ("pending", "approved", "rejected", "edited")
ASSESSMENT_TYPES = ("diagnostic", "adaptive_quiz", "revision", "practice", "final")
ASSESSMENT_STATUSES = ("draft", "in_progress", "completed", "abandoned")
QUESTION_TYPES = (
    "mcq",
    "true_false",
    "short_answer",
    "coding",
    "multiple_select",
)
ATTEMPT_STATUSES = ("in_progress", "completed", "abandoned", "expired")
MASTERY_STATES = ("unknown", "weak", "partial", "mastered")
MASTERY_REASONS = (
    "assessment",
    "quiz",
    "practice",
    "video_watch",
    "tutor_interaction",
    "decay",
    "manual_review",
)
MASTERY_EVENT_TYPES = (
    "assessment_answered",
    "quiz_submitted",
    "practice_completed",
    "video_watched",
    "tutor_interaction",
    "revision_completed",
    "mastery_decay",
)
PATH_STATUSES = ("draft", "active", "paused", "completed", "superseded")
PATH_STEP_STATUSES = ("locked", "ready", "in_progress", "mastered", "needs_revision")
PREREQUISITE_STATUSES = ("satisfied", "scheduled_before", "blocked")
RECOMMENDATION_TYPES = ("learn", "practice", "revision", "video", "reading", "project")
RECOMMENDATION_FEEDBACK = (
    "helpful",
    "not_helpful",
    "dismissed",
    "completed",
)
ACTIVITY_TYPES = (
    "assessment",
    "lesson",
    "video",
    "practice",
    "tutor",
    "revision",
    "project",
)
VIDEO_EVENT_TYPES = (
    "started",
    "played",
    "paused",
    "completed",
    "seeked",
    "skipped",
    "rewatched",
)
AI_MESSAGE_ROLES = ("system", "user", "assistant", "tool")
PROMPT_STATUSES = ("draft", "active", "retired")
GENERATION_TYPES = (
    "assessment_question",
    "quiz_question",
    "video_segmentation",
    "recommendation",
    "tutor_response",
    "insight",
    "summary",
    "taxonomy_tagging",
)
GENERATION_STATUSES = ("pending", "completed", "failed")
ACHIEVEMENT_FEEDBACK = ("helpful", "not_helpful", "dismissed", "completed")
CONTENT_REVIEW_TYPES = (
    "video_segment",
    "assessment_question",
    "resource",
    "taxonomy",
)
CONTENT_REVIEW_STATUSES = ("pending", "approved", "rejected", "changes_requested")
NOTIFICATION_TYPES = (
    "revision_due",
    "mastery_achieved",
    "streak",
    "assessment",
    "learning_path",
    "system",
)
