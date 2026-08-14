from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SubjectResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None
    icon_url: str | None
    is_published: bool

    model_config = {"from_attributes": True}


class LearningGoalResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    default_mastery_threshold: float

    model_config = {"from_attributes": True}


class EnrollSubjectRequest(BaseModel):
    subject_id: UUID
    learning_goal_id: UUID
    target_mastery: float = Field(default=80, ge=0, le=100)


class LearnerSubjectResponse(BaseModel):
    id: UUID
    subject_id: UUID
    learning_goal_id: UUID
    target_mastery: float
    started_at: datetime
    completed_at: datetime | None
    status: str

    model_config = {"from_attributes": True}