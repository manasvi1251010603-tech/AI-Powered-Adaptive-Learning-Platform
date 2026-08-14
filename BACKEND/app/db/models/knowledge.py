"""Learner knowledge graph state and mastery evidence."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, JSON, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import MASTERY_EVENT_TYPES, MASTERY_REASONS, MASTERY_STATES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class LearnerConceptMastery(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "learner_concept_mastery"
    __table_args__ = (
        Index("uq_mastery_user_concept", "user_id", "concept_id", unique=True),
        Index("ix_mastery_user_subject", "user_id", "subject_id"),
        Index("ix_mastery_user_state", "user_id", "mastery_state"),
        CheckConstraint(
            "mastery_score BETWEEN 0 AND 100", name="mastery_score_range"
        ),
        CheckConstraint(
            "confidence_score BETWEEN 0 AND 100", name="confidence_score_range"
        ),
        CheckConstraint(
            f"mastery_state IN ({_values(MASTERY_STATES)})",
            name="mastery_state_allowed",
        ),
        CheckConstraint("attempts >= 0", name="attempts_nonnegative"),
        CheckConstraint("correct_attempts >= 0", name="correct_attempts_nonnegative"),
        CheckConstraint(
            "correct_attempts <= attempts", name="correct_not_over_attempts"
        ),
        CheckConstraint(
            "decay_score IS NULL OR decay_score BETWEEN 0 AND 100",
            name="decay_score_range",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    mastery_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    confidence_score: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, default=0
    )
    mastery_state: Mapped[str] = mapped_column(
        String(20), nullable=False, default="unknown"
    )
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_assessed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_practiced_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_revised_at: Mapped[datetime | None] = mapped_column(nullable=True)
    next_review_at: Mapped[datetime | None] = mapped_column(nullable=True)
    decay_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    user: Mapped["User"] = relationship()
    subject: Mapped["Subject"] = relationship()
    concept: Mapped["Concept"] = relationship()
    history: Mapped[List["MasteryHistory"]] = relationship(
        back_populates="mastery", cascade="all, delete-orphan"
    )


class MasteryHistory(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "mastery_history"
    __table_args__ = (
        Index("ix_mastery_history_mastery_created", "learner_concept_mastery_id", "created_at"),
        CheckConstraint(
            "previous_score BETWEEN 0 AND 100", name="previous_score_range"
        ),
        CheckConstraint("new_score BETWEEN 0 AND 100", name="new_score_range"),
        CheckConstraint(
            f"previous_state IN ({_values(MASTERY_STATES)})",
            name="previous_state_allowed",
        ),
        CheckConstraint(
            f"new_state IN ({_values(MASTERY_STATES)})", name="new_state_allowed"
        ),
        CheckConstraint(
            f"reason IN ({_values(MASTERY_REASONS)})", name="reason_allowed"
        ),
    )

    learner_concept_mastery_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("learner_concept_mastery.id", ondelete="CASCADE"),
        nullable=False,
    )
    previous_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    new_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    previous_state: Mapped[str] = mapped_column(String(20), nullable=False)
    new_state: Mapped[str] = mapped_column(String(20), nullable=False)
    reason: Mapped[str] = mapped_column(String(50), nullable=False)
    source_event_id: Mapped[UUID | None] = mapped_column(GUID(), nullable=True)

    mastery: Mapped["LearnerConceptMastery"] = relationship(back_populates="history")


class MasteryEvent(Base):
    __tablename__ = "mastery_events"
    __table_args__ = (
        Index("ix_mastery_events_user_concept", "user_id", "concept_id"),
        Index("ix_mastery_events_processed_at", "processed_at"),
        CheckConstraint(
            f"event_type IN ({_values(MASTERY_EVENT_TYPES)})",
            name="event_type_allowed",
        ),
    )

    id: Mapped[UUID] = mapped_column(GUID(), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[UUID | None] = mapped_column(GUID(), nullable=True)
    payload: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(
        String(180), unique=True, nullable=False
    )
    occurred_at: Mapped[datetime] = mapped_column(nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship()
    subject: Mapped["Subject"] = relationship()
    concept: Mapped["Concept"] = relationship()
