from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth.dependencies import get_current_user
from app.api.learning.schemas import (
    DiagnosticOptionResponse,
    DiagnosticQuestionResponse,
    DiagnosticStartResponse,
    EnrollSubjectRequest,
    LearnerProfileResponse,
    LearnerProfileUpdate,
    LearnerSubjectResponse,
    LearningGoalResponse,
    SubjectResponse,
)
from app.db.models.assessment import (
    Assessment,
    AssessmentAttempt,
    AssessmentItem,
    Question,
)
from app.db.models.identity import LearnerProfile, User
from app.db.models.taxonomy import (
    Concept,
    LearnerSubject,
    LearningGoal,
    Subject,
)
from app.db.session import get_db


router = APIRouter(
    prefix="/learning",
    tags=["learning"],
)


# ============================================================
# SUBJECTS
# ============================================================

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
            .where(
                Subject.is_published.is_(True)
            )
            .order_by(Subject.name)
        ).all()
    )


# ============================================================
# LEARNING GOALS
# ============================================================

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


# ============================================================
# SUBJECT ENROLLMENT
# ============================================================

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


# ============================================================
# LEARNER PROFILE
# ============================================================

@router.get(
    "/profile",
    response_model=LearnerProfileResponse,
)
def get_learner_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LearnerProfile:

    profile = db.scalar(
        select(LearnerProfile).where(
            LearnerProfile.user_id == current_user.id
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner profile not found.",
        )

    return profile


@router.put(
    "/profile",
    response_model=LearnerProfileResponse,
)
def update_learner_profile(
    payload: LearnerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LearnerProfile:

    profile = db.scalar(
        select(LearnerProfile).where(
            LearnerProfile.user_id == current_user.id
        )
    )

    if profile is None:
        profile = LearnerProfile(
            user_id=current_user.id,
        )
        db.add(profile)

    if payload.learning_style is not None:
        profile.learning_style = payload.learning_style

    if payload.learning_speed is not None:
        profile.learning_speed = payload.learning_speed

    if payload.preferred_session_minutes is not None:
        profile.preferred_session_minutes = (
            payload.preferred_session_minutes
        )

    if payload.preferred_study_period is not None:
        profile.preferred_study_period = (
            payload.preferred_study_period
        )

    if payload.timezone is not None:
        profile.timezone = payload.timezone

    profile.onboarding_completed_at = datetime.now(
        timezone.utc
    )

    db.commit()
    db.refresh(profile)

    return profile


# ============================================================
# DIAGNOSTIC ASSESSMENT
# ============================================================

@router.post(
    "/diagnostic/start",
    response_model=DiagnosticStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_diagnostic(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticStartResponse:

    # --------------------------------------------------------
    # 1. Find the learner's active Python enrollment
    # --------------------------------------------------------

    learner_subject = db.scalar(
        select(LearnerSubject)
        .join(
            Subject,
            Subject.id == LearnerSubject.subject_id,
        )
        .where(
            LearnerSubject.user_id == current_user.id,
            LearnerSubject.status == "active",
            Subject.slug == "python",
        )
    )

    if learner_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not actively enrolled in Python.",
        )

    # --------------------------------------------------------
    # 2. Find Python concepts
    # --------------------------------------------------------

    concepts = list(
        db.scalars(
            select(Concept)
            .where(
                Concept.subject_id
                == learner_subject.subject_id,
                Concept.is_active.is_(True),
            )
            .order_by(Concept.name)
        ).all()
    )

    if not concepts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "No learning concepts are available "
                "for this subject."
            ),
        )

    concept_ids = [
        concept.id
        for concept in concepts
    ]

    # --------------------------------------------------------
    # 3. Find active diagnostic questions
    # --------------------------------------------------------

    questions = list(
        db.scalars(
            select(Question)
            .where(
                Question.concept_id.in_(concept_ids),
                Question.status == "active",
            )
            .order_by(
                Question.difficulty,
                Question.created_at,
            )
        ).all()
    )

    # First diagnostic contains at most 10 questions.
    questions = questions[:10]

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "No diagnostic questions are available."
            ),
        )

    now = datetime.now(timezone.utc)

    # --------------------------------------------------------
    # 4. Create the assessment
    # --------------------------------------------------------

    assessment = Assessment(
        learner_subject_id=learner_subject.id,
        assessment_type="diagnostic",
        status="in_progress",
        target_concepts=concept_ids,
        started_at=now,
    )

    db.add(assessment)
    db.flush()

    # --------------------------------------------------------
    # 5. Create assessment items
    # --------------------------------------------------------

    for sequence_number, question in enumerate(
        questions,
        start=1,
    ):
        db.add(
            AssessmentItem(
                assessment_id=assessment.id,
                question_id=question.id,
                concept_id=question.concept_id,
                sequence_number=sequence_number,
                selected_difficulty=question.difficulty,
                generated_at=now,
            )
        )

    # --------------------------------------------------------
    # 6. Create learner attempt
    # --------------------------------------------------------

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        user_id=current_user.id,
        status="in_progress",
        started_at=now,
        total_items=len(questions),
        answered_items=0,
    )

    db.add(attempt)

    db.commit()

    db.refresh(assessment)
    db.refresh(attempt)

    # --------------------------------------------------------
    # 7. Build safe response
    #
    # IMPORTANT:
    # We deliberately DO NOT expose is_correct.
    # --------------------------------------------------------

    question_responses = []

    for question in questions:

        question_responses.append(
            DiagnosticQuestionResponse(
                id=question.id,
                concept_id=question.concept_id,
                question_type=question.question_type,
                prompt=question.prompt,
                difficulty=(
                    float(question.difficulty)
                    if question.difficulty is not None
                    else None
                ),
                options=[
                    DiagnosticOptionResponse(
                        option_key=option.option_key,
                        option_text=option.option_text,
                    )
                    for option in question.options
                ],
            )
        )

    # --------------------------------------------------------
    # 8. Return diagnostic
    # --------------------------------------------------------

    return DiagnosticStartResponse(
        assessment_id=assessment.id,
        attempt_id=attempt.id,
        assessment_type=assessment.assessment_type,
        status=assessment.status,
        total_items=len(questions),
        questions=question_responses,
    )