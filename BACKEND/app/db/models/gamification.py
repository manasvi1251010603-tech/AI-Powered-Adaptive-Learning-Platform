"""Achievements, XP ledger, and learner streaks."""

from __future__ import annotations

from datetime import date, datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class Achievement(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "achievements"

    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    criteria: Mapped[dict | list] = mapped_column(JSON, nullable=False)

    user_achievements: Mapped[List["UserAchievement"]] = relationship(
        back_populates="achievement"
    )


class UserAchievement(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "user_achievements"
    __table_args__ = (
        Index("uq_user_achievements_user_achievement", "user_id", "achievement_id", unique=True),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    achievement_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False
    )
    earned_at: Mapped[datetime] = mapped_column(nullable=False)
    achievement_metadata: Mapped[dict | list] = mapped_column(
        "metadata", JSON, nullable=False
    )

    user: Mapped["User"] = relationship()
    achievement: Mapped["Achievement"] = relationship(back_populates="user_achievements")


class XPTransaction(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "xp_transactions"
    __table_args__ = (
        Index("ix_xp_transactions_user_created", "user_id", "created_at"),
        CheckConstraint("amount <> 0", name="amount_nonzero"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(60), nullable=False)
    source_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source_id: Mapped[UUID | None] = mapped_column(GUID(), nullable=True)

    user: Mapped["User"] = relationship()


class Streak(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "streaks"

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    current_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_activity_date: Mapped[date | None] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship()
