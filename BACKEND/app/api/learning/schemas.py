from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================================
# SUBJECTS
# ============================================================

class SubjectResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None
    icon_url: str | None
    is_published: bool

    model_config = {"from_attributes": True}


# ============================================================
# LEARNING GOALS
# ============================================================

class LearningGoalResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    default_mastery_threshold: float

    model_config = {"from_attributes": True}


# ============================================================
# SUBJECT ENROLLMENT
# ============================================================

class EnrollSubjectRequest(BaseModel):
    subject_id: UUID
    learning_goal_id: UUID
    target_mastery: float = Field(
        default=80,
        ge=0,
        le=100,
    )


class LearnerSubjectResponse(BaseModel):
    id: UUID
    subject_id: UUID
    learning_goal_id: UUID
    target_mastery: float
    started_at: datetime
    completed_at: datetime | None
    status: str

    model_config = {"from_attributes": True}


# ============================================================
# LEARNER PROFILE
# ============================================================

LearningStyle = Literal[
    "visual",
    "reading",
    "practice",
    "mixed",
]

LearningSpeed = Literal[
    "fast",
    "moderate",
    "slow",
]

StudyPeriod = Literal[
    "morning",
    "afternoon",
    "evening",
    "late_night",
]


class LearnerProfileUpdate(BaseModel):
    learning_style: LearningStyle | None = None
    learning_speed: LearningSpeed | None = None

    preferred_session_minutes: int | None = Field(
        default=None,
        gt=0,
        le=480,
    )

    preferred_study_period: StudyPeriod | None = None

    timezone: str | None = Field(
        default=None,
        min_length=1,
        max_length=80,
    )


class LearnerProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    learning_style: str | None
    learning_speed: str | None
    preferred_session_minutes: int | None
    preferred_study_period: str | None
    timezone: str | None
    onboarding_completed_at: datetime | None

    model_config = {"from_attributes": True}


# ============================================================
# DIAGNOSTIC ASSESSMENT
# ============================================================

class DiagnosticOptionResponse(BaseModel):
    option_key: str
    option_text: str


class DiagnosticQuestionResponse(BaseModel):
    id: UUID
    concept_id: UUID
    question_type: str
    prompt: str
    difficulty: float | None
    options: list[DiagnosticOptionResponse]


class DiagnosticStartResponse(BaseModel):
    assessment_id: UUID
    attempt_id: UUID
    assessment_type: str
    status: str
    total_items: int
    questions: list[DiagnosticQuestionResponse]