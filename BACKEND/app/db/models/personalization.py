"""Personalized learning paths, steps, and recommendation feedback."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import (
    PATH_STATUSES,
    PATH_STEP_STATUSES,
    PREREQUISITE_STATUSES,
    RECOMMENDATION_FEEDBACK,
    RECOMMENDATION_TYPES,
)


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class LearningPath(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "learning_paths"
    __table_args__ = (
        Index("ix_learning_paths_learner_subject_status", "learner_subject_id", "status"),
        CheckConstraint(
            f"status IN ({_values(PATH_STATUSES)})", name="status_allowed"
        ),
        CheckConstraint(
            "progress_percent BETWEEN 0 AND 100", name="progress_percent_range"
        ),
        CheckConstraint(
            "estimated_minutes IS NULL OR estimated_minutes >= 0",
            name="estimated_minutes_nonnegative",
        ),
    )

    learner_subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("learner_subjects.id", ondelete="CASCADE"), nullable=False
    )
    generated_from_mastery_version: Mapped[UUID | None] = mapped_column(
        GUID(), nullable=True
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")
    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    progress_percent: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, default=0
    )
    generated_at: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    learner_subject: Mapped["LearnerSubject"] = relationship()
    steps: Mapped[List["LearningPathStep"]] = relationship(
        back_populates="learning_path",
        cascade="all, delete-orphan",
        order_by="LearningPathStep.sequence_number",
    )


class LearningPathStep(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "learning_path_steps"
    __table_args__ = (
        Index("ix_learning_path_steps_path_sequence", "learning_path_id", "sequence_number"),
        CheckConstraint(
            f"status IN ({_values(PATH_STEP_STATUSES)})", name="status_allowed"
        ),
        CheckConstraint(
            f"prerequisite_status IN ({_values(PREREQUISITE_STATUSES)})",
            name="prerequisite_status_allowed",
        ),
        CheckConstraint(
            "mastery_threshold BETWEEN 0 AND 100", name="mastery_threshold_range"
        ),
    )

    learning_path_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="locked")
    mastery_threshold: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, default=80
    )
    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prerequisite_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="blocked"
    )
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    learning_path: Mapped["LearningPath"] = relationship(back_populates="steps")
    concept: Mapped["Concept"] = relationship()


class Recommendation(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "recommendations"
    __table_args__ = (
        Index("ix_recommendations_user_concept", "user_id", "concept_id"),
        CheckConstraint(
            f"recommendation_type IN ({_values(RECOMMENDATION_TYPES)})",
            name="recommendation_type_allowed",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    resource_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("resources.id", ondelete="SET NULL"), nullable=True
    )
    recommendation_type: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    generated_by: Mapped[str] = mapped_column(String(40), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship()
    concept: Mapped["Concept"] = relationship()
    resource: Mapped["Resource | None"] = relationship()
    feedback: Mapped[List["RecommendationFeedback"]] = relationship(
        back_populates="recommendation", cascade="all, delete-orphan"
    )


class RecommendationFeedback(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "recommendation_feedback"
    __table_args__ = (
        Index("ix_recommendation_feedback_recommendation_id", "recommendation_id"),
        CheckConstraint(
            f"feedback IN ({_values(RECOMMENDATION_FEEDBACK)})",
            name="feedback_allowed",
        ),
    )

    recommendation_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    feedback: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    recommendation: Mapped["Recommendation"] = relationship(back_populates="feedback")
    user: Mapped["User"] = relationship()
