from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth.dependencies import get_current_user
from app.api.learning.schemas import (
    EnrollSubjectRequest,
    LearnerSubjectResponse,
    LearningGoalResponse,
    SubjectResponse,
)
from app.db.models.identity import User
from app.db.models.taxonomy import (
    LearnerSubject,
    LearningGoal,
    Subject,
)
from app.db.session import get_db


router = APIRouter(prefix="/learning", tags=["learning"])


@router.get(
    "/subjects",
    response_model=list[SubjectResponse],
)
def list_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Subject]:
    return list(
        db.scalars(
            select(Subject)
            .where(Subject.is_published.is_(True))
            .order_by(Subject.name)
        ).all()
    )


@router.get(
    "/learning-goals",
    response_model=list[LearningGoalResponse],
)
def list_learning_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[LearningGoal]:
    return list(
        db.scalars(
            select(LearningGoal)
            .order_by(LearningGoal.name)
        ).all()
    )


@router.post(
    "/subjects/enroll",
    response_model=LearnerSubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def enroll_in_subject(
    payload: EnrollSubjectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LearnerSubject:
    subject = db.scalar(
        select(Subject).where(
            Subject.id == payload.subject_id,
            Subject.is_published.is_(True),
        )
    )

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or not published.",
        )

    learning_goal = db.scalar(
        select(LearningGoal).where(
            LearningGoal.id == payload.learning_goal_id
        )
    )

    if learning_goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning goal not found.",
        )

    existing_enrollment = db.scalar(
        select(LearnerSubject).where(
            LearnerSubject.user_id == current_user.id,
            LearnerSubject.subject_id == subject.id,
        )
    )

    if existing_enrollment is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already enrolled in this subject.",
        )

    enrollment = LearnerSubject(
        user_id=current_user.id,
        subject_id=subject.id,
        learning_goal_id=learning_goal.id,
        target_mastery=payload.target_mastery,
        started_at=datetime.now(timezone.utc),
        status="active",
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment