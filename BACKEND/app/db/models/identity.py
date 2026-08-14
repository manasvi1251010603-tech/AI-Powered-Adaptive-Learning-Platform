"""Identity, roles, and learner preference models."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import LEARNING_SPEEDS, LEARNING_STYLES, STUDY_PERIODS


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_is_active", "is_active"),)

    email: Mapped[str] = mapped_column(
        String(320, collation="utf8mb4_0900_ai_ci"), unique=True, nullable=False
    )
    password_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(nullable=True)

    role_assignments: Mapped[List["UserRole"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    learner_profile: Mapped["LearnerProfile | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    learner_subjects: Mapped[List["LearnerSubject"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Role(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_assignments: Mapped[List["UserRole"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )


class UserRole(CreatedAtMixin, Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["User"] = relationship(back_populates="role_assignments")
    role: Mapped["Role"] = relationship(back_populates="user_assignments")


class LearnerProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "learner_profiles"
    __table_args__ = (
        CheckConstraint(
            f"learning_style IN ({_values(LEARNING_STYLES)})",
            name="learning_style_allowed",
        ),
        CheckConstraint(
            f"learning_speed IN ({_values(LEARNING_SPEEDS)})",
            name="learning_speed_allowed",
        ),
        CheckConstraint(
            f"preferred_study_period IN ({_values(STUDY_PERIODS)})",
            name="study_period_allowed",
        ),
        CheckConstraint(
            "preferred_session_minutes IS NULL OR preferred_session_minutes > 0",
            name="session_minutes_positive",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    learning_style: Mapped[str | None] = mapped_column(String(30), nullable=True)
    learning_speed: Mapped[str | None] = mapped_column(String(20), nullable=True)
    preferred_session_minutes: Mapped[int | None] = mapped_column(nullable=True)
    preferred_study_period: Mapped[str | None] = mapped_column(String(30), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    onboarding_completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="learner_profile")
