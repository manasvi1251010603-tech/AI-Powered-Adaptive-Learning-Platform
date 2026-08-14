"""Certificates, instructor cohorts, enrollments, and notifications."""

from __future__ import annotations

from datetime import date, datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import NOTIFICATION_TYPES


class Certificate(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "certificates"
    __table_args__ = (
        Index("uq_certificates_learner_subject", "learner_subject_id", unique=True),
        CheckConstraint("mastery_score BETWEEN 0 AND 100", name="mastery_score_range"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    learner_subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("learner_subjects.id", ondelete="CASCADE"), nullable=False
    )
    certificate_number: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    mastery_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(nullable=False)
    storage_key: Mapped[str] = mapped_column(Text, nullable=False)
    verification_token: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )

    user: Mapped["User"] = relationship()
    learner_subject: Mapped["LearnerSubject"] = relationship()


class Cohort(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "cohorts"
    __table_args__ = (Index("ix_cohorts_instructor_subject", "instructor_id", "subject_id"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    instructor_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    start_date: Mapped[date | None] = mapped_column(nullable=True)
    end_date: Mapped[date | None] = mapped_column(nullable=True)

    instructor: Mapped["User"] = relationship()
    subject: Mapped["Subject"] = relationship()
    members: Mapped[List["CohortMember"]] = relationship(
        back_populates="cohort", cascade="all, delete-orphan"
    )


class CohortMember(CreatedAtMixin, Base):
    __tablename__ = "cohort_members"

    cohort_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("cohorts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    joined_at: Mapped[datetime] = mapped_column(nullable=False)

    cohort: Mapped["Cohort"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship()


class Enrollment(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        Index("uq_enrollments_user_course", "user_id", "course_id", unique=True),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    enrolled_at: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship()
    course: Mapped["Course"] = relationship()


class Notification(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "notifications"
    __table_args__ = (
        Index("ix_notifications_user_read_created", "user_id", "read_at", "created_at"),
        CheckConstraint(
            f"type IN ({', '.join(repr(value) for value in NOTIFICATION_TYPES)})",
            name="type_allowed",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    action_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship()
