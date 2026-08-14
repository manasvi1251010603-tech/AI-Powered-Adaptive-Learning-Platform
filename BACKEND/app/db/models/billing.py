"""Future billing tables retained in the model baseline."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, TimestampMixin, GUID, UUIDPrimaryKeyMixin


class Plan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "plans"
    __table_args__ = (
        CheckConstraint("price_minor >= 0", name="price_nonnegative"),
        CheckConstraint("active IN (0, 1)", name="active_boolean"),
    )

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    billing_interval: Mapped[str] = mapped_column(String(20), nullable=False)
    features: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False, default=True)

    subscriptions: Mapped[List["Subscription"]] = relationship(
        back_populates="plan"
    )


class Subscription(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        Index("ix_subscriptions_user_status", "user_id", "status"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    plan_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False
    )
    provider_subscription_id: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    current_period_start: Mapped[datetime] = mapped_column(nullable=False)
    current_period_end: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship()
    plan: Mapped["Plan"] = relationship(back_populates="subscriptions")
    payment_transactions: Mapped[List["PaymentTransaction"]] = relationship(
        back_populates="subscription"
    )


class PaymentTransaction(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "payment_transactions"
    __table_args__ = (
        Index("ix_payment_transactions_user_created", "user_id", "created_at"),
        CheckConstraint("amount_minor >= 0", name="amount_nonnegative"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subscription_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True
    )
    provider_transaction_id: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False
    )
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    user: Mapped["User"] = relationship()
    subscription: Mapped["Subscription | None"] = relationship(
        back_populates="payment_transactions"
    )
