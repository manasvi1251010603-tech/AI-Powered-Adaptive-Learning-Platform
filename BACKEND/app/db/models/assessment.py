"""Assessment definitions, questions, attempts, and learner responses."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, TimestampMixin, GUID, UUIDPrimaryKeyMixin
from ..enums import ASSESSMENT_STATUSES, ASSESSMENT_TYPES, ATTEMPT_STATUSES, QUESTION_TYPES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class Assessment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assessments"
    __table_args__ = (
        Index("ix_assessments_learner_subject_id", "learner_subject_id"),
        CheckConstraint(
            f"assessment_type IN ({_values(ASSESSMENT_TYPES)})",
            name="assessment_type_allowed",
        ),
        CheckConstraint(
            f"status IN ({_values(ASSESSMENT_STATUSES)})", name="status_allowed"
        ),
    )

    learner_subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("learner_subjects.id", ondelete="CASCADE"), nullable=False
    )
    assessment_type: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")
    target_concepts: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    learner_subject: Mapped["LearnerSubject"] = relationship()
    items: Mapped[List["AssessmentItem"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan",
        order_by="AssessmentItem.sequence_number",
    )
    attempts: Mapped[List["AssessmentAttempt"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )


class Question(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "questions"
    __table_args__ = (
        Index("ix_questions_concept_id", "concept_id"),
        CheckConstraint(
            f"question_type IN ({_values(QUESTION_TYPES)})",
            name="question_type_allowed",
        ),
        CheckConstraint(
            "difficulty IS NULL OR difficulty BETWEEN 0 AND 100",
            name="difficulty_range",
        ),
    )

    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False
    )
    question_type: Mapped[str] = mapped_column(String(40), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    answer_data: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    source: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ai_generation_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("ai_generations.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str | None] = mapped_column(String(30), nullable=True)

    concept: Mapped["Concept"] = relationship()
    ai_generation: Mapped["AIGeneration | None"] = relationship()
    options: Mapped[List["QuestionOption"]] = relationship(
        back_populates="question", cascade="all, delete-orphan", order_by="QuestionOption.sort_order"
    )
    assessment_items: Mapped[List["AssessmentItem"]] = relationship(
        back_populates="question"
    )


class QuestionOption(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "question_options"
    __table_args__ = (Index("ix_question_options_question_sort", "question_id", "sort_order"),)

    question_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_key: Mapped[str] = mapped_column(String(20), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_correct: Mapped[bool] = mapped_column(nullable=False, default=False)

    question: Mapped["Question"] = relationship(back_populates="options")


class AssessmentItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assessment_items"
    __table_args__ = (
        Index("ix_assessment_items_assessment_sequence", "assessment_id", "sequence_number"),
        CheckConstraint(
            "selected_difficulty IS NULL OR selected_difficulty BETWEEN 0 AND 100",
            name="selected_difficulty_range",
        ),
    )

    assessment_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    selected_difficulty: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    generated_at: Mapped[datetime] = mapped_column(nullable=False)

    assessment: Mapped["Assessment"] = relationship(back_populates="items")
    question: Mapped["Question"] = relationship(back_populates="assessment_items")
    concept: Mapped["Concept"] = relationship()
    responses: Mapped[List["AssessmentResponse"]] = relationship(
        back_populates="assessment_item"
    )


class AssessmentAttempt(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assessment_attempts"
    __table_args__ = (
        Index("ix_assessment_attempts_user_status", "user_id", "status"),
        CheckConstraint(
            f"status IN ({_values(ATTEMPT_STATUSES)})", name="status_allowed"
        ),
        CheckConstraint("total_items >= 0", name="total_items_nonnegative"),
        CheckConstraint("answered_items >= 0", name="answered_items_nonnegative"),
        CheckConstraint(
            "answered_items <= total_items", name="answered_not_over_total"
        ),
    )

    assessment_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="in_progress")
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    total_items: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    answered_items: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    assessment: Mapped["Assessment"] = relationship(back_populates="attempts")
    user: Mapped["User"] = relationship()
    responses: Mapped[List["AssessmentResponse"]] = relationship(
        back_populates="attempt", cascade="all, delete-orphan"
    )


class AssessmentResponse(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "assessment_responses"
    __table_args__ = (
        Index("ix_assessment_responses_attempt_id", "attempt_id"),
        CheckConstraint(
            "score IS NULL OR score BETWEEN 0 AND 100", name="score_range"
        ),
        CheckConstraint(
            "confidence_rating IS NULL OR confidence_rating BETWEEN 1 AND 5",
            name="confidence_rating_range",
        ),
        CheckConstraint(
            "response_time_ms IS NULL OR response_time_ms >= 0",
            name="response_time_nonnegative",
        ),
    )

    attempt_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=False
    )
    assessment_item_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("assessment_items.id", ondelete="RESTRICT"), nullable=False
    )
    answer_data: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    is_correct: Mapped[bool | None] = mapped_column(nullable=True)
    score: Mapped[float | None] = mapped_column(Numeric(6, 3), nullable=True)
    response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(nullable=False)
    attempt: Mapped["AssessmentAttempt"] = relationship(back_populates="responses")
    assessment_item: Mapped["AssessmentItem"] = relationship(back_populates="responses")
