"""Learning taxonomy, goals, and learner-subject enrollment models."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, TimestampMixin, GUID, UUIDPrimaryKeyMixin
from ..enums import LEARNER_SUBJECT_STATUSES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class Subject(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "subjects"
    __table_args__ = (Index("ix_subjects_is_published", "is_published"),)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_by_id: Mapped[UUID | None] = mapped_column(
        "created_by", GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    topics: Mapped[List["Topic"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )
    concepts: Mapped[List["Concept"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )
    courses: Mapped[List["Course"]] = relationship(back_populates="subject")


class Topic(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "topics"
    __table_args__ = (
        Index("ix_topics_subject_id", "subject_id"),
        Index("uq_topics_subject_slug", "subject_id", "slug", unique=True),
    )

    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    parent_topic_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    subject: Mapped["Subject"] = relationship(back_populates="topics")
    parent_topic: Mapped["Topic | None"] = relationship(
        remote_side="Topic.id", back_populates="child_topics"
    )
    child_topics: Mapped[List["Topic"]] = relationship(back_populates="parent_topic")
    concepts: Mapped[List["Concept"]] = relationship(back_populates="topic")


class Concept(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "concepts"
    __table_args__ = (
        Index("ix_concepts_subject_id", "subject_id"),
        Index("ix_concepts_topic_id", "topic_id"),
        Index("ix_concepts_parent_concept_id", "parent_concept_id"),
        CheckConstraint(
            "difficulty_baseline IS NULL OR difficulty_baseline BETWEEN 0 AND 100",
            name="difficulty_baseline_range",
        ),
    )

    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True
    )
    parent_concept_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty_baseline: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    subject: Mapped["Subject"] = relationship(back_populates="concepts")
    topic: Mapped["Topic | None"] = relationship(back_populates="concepts")
    parent_concept: Mapped["Concept | None"] = relationship(
        remote_side="Concept.id", back_populates="child_concepts"
    )
    child_concepts: Mapped[List["Concept"]] = relationship(back_populates="parent_concept")


class ConceptPrerequisite(CreatedAtMixin, Base):
    __tablename__ = "concept_prerequisites"
    __table_args__ = (
        Index("ix_concept_prerequisites_concept_id", "concept_id"),
        Index("ix_concept_prerequisites_prerequisite_id", "prerequisite_concept_id"),
        CheckConstraint("concept_id <> prerequisite_concept_id", name="not_self_reference"),
        CheckConstraint(
            "strength IS NULL OR strength BETWEEN 0 AND 100",
            name="strength_range",
        ),
    )

    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True
    )
    prerequisite_concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True
    )
    strength: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    concept: Mapped["Concept"] = relationship(foreign_keys=[concept_id])
    prerequisite_concept: Mapped["Concept"] = relationship(
        foreign_keys=[prerequisite_concept_id]
    )


class LearningGoal(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "learning_goals"
    __table_args__ = (
        CheckConstraint(
            "default_mastery_threshold BETWEEN 0 AND 100",
            name="mastery_threshold_range",
        ),
    )

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_mastery_threshold: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, default=80
    )


class LearnerSubject(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "learner_subjects"
    __table_args__ = (
        Index("ix_learner_subjects_user_subject", "user_id", "subject_id"),
        Index(
            "ix_learner_subjects_user_subject_status",
            "user_id",
            "subject_id",
            "status",
        ),
        CheckConstraint(
            f"status IN ({_values(LEARNER_SUBJECT_STATUSES)})",
            name="status_allowed",
        ),
        CheckConstraint(
            "target_mastery BETWEEN 0 AND 100", name="target_mastery_range"
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    learning_goal_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("learning_goals.id", ondelete="RESTRICT"), nullable=False
    )
    target_mastery: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=80)
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")

    user: Mapped["User"] = relationship(back_populates="learner_subjects")
    subject: Mapped["Subject"] = relationship()
    learning_goal: Mapped["LearningGoal"] = relationship()
