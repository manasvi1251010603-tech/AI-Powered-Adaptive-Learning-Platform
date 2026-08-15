from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth.dependencies import get_current_user
from app.api.learning.schemas import (
    DiagnosticAnalysisResponse,
    DiagnosticAnswerRequest,
    DiagnosticAnswerResponse,
    DiagnosticCompleteResponse,
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
    AssessmentResponse,
    Question,
)
from app.db.models.identity import LearnerProfile, User
from app.db.models.knowledge import (
    LearnerConceptMastery,
    MasteryHistory,
)
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
                Concept.subject_id == learner_subject.subject_id,
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
            detail="No diagnostic questions are available.",
        )

    now = datetime.now(timezone.utc)

    # --------------------------------------------------------
    # 4. Create the assessment
    # --------------------------------------------------------

    assessment = Assessment(
        learner_subject_id=learner_subject.id,
        assessment_type="diagnostic",
        status="in_progress",
        target_concepts=[str(concept_id) for concept_id in concept_ids],
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
    # We deliberately DO NOT expose the answer key.
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


# ============================================================
# DIAGNOSTIC ANSWER SUBMISSION
# ============================================================

@router.post(
    "/diagnostic/{assessment_id}/answer",
    response_model=DiagnosticAnswerResponse,
)
def submit_diagnostic_answer(
    assessment_id: UUID,
    payload: DiagnosticAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticAnswerResponse:

    # --------------------------------------------------------
    # 1. Verify assessment belongs to the current learner
    # --------------------------------------------------------

    assessment = db.scalar(
        select(Assessment)
        .join(
            LearnerSubject,
            LearnerSubject.id == Assessment.learner_subject_id,
        )
        .where(
            Assessment.id == assessment_id,
            LearnerSubject.user_id == current_user.id,
        )
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    if assessment.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This assessment is no longer in progress.",
        )

    # --------------------------------------------------------
    # 2. Verify attempt belongs to this assessment + learner
    # --------------------------------------------------------

    attempt = db.scalar(
        select(AssessmentAttempt).where(
            AssessmentAttempt.id == payload.attempt_id,
            AssessmentAttempt.assessment_id == assessment.id,
            AssessmentAttempt.user_id == current_user.id,
        )
    )

    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found.",
        )

    if attempt.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This assessment attempt is no longer active.",
        )

    # --------------------------------------------------------
    # 3. Find the assessment item
    # --------------------------------------------------------

    item = db.scalar(
        select(AssessmentItem).where(
            AssessmentItem.id == payload.assessment_item_id,
            AssessmentItem.assessment_id == assessment.id,
        )
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment question not found.",
        )

    # --------------------------------------------------------
    # 4. Prevent duplicate submissions
    # --------------------------------------------------------

    existing_response = db.scalar(
        select(AssessmentResponse).where(
            AssessmentResponse.attempt_id == attempt.id,
            AssessmentResponse.assessment_item_id == item.id,
        )
    )

    if existing_response is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This question has already been answered.",
        )

    # --------------------------------------------------------
    # 5. Load question + answer key
    # --------------------------------------------------------

    question = db.scalar(
        select(Question).where(
            Question.id == item.question_id,
        )
    )

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found.",
        )

    # --------------------------------------------------------
    # 6. Evaluate answer
    #
    # MVP currently supports MCQ selected_option.
    # --------------------------------------------------------

    selected_option = payload.answer_data.get(
        "selected_option"
    )

    if not isinstance(selected_option, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "answer_data.selected_option "
                "is required."
            ),
        )

    correct_option = question.answer_data.get(
        "correct_option"
    )

    if correct_option is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Question answer configuration is invalid.",
        )

    is_correct = (
        selected_option.strip().upper()
        == str(correct_option).strip().upper()
    )

    score = 100.0 if is_correct else 0.0

    now = datetime.now(timezone.utc)

    # --------------------------------------------------------
    # 7. Save response
    # --------------------------------------------------------

    response = AssessmentResponse(
        attempt_id=attempt.id,
        assessment_item_id=item.id,
        answer_data=payload.answer_data,
        is_correct=is_correct,
        score=score,
        confidence_rating=payload.confidence_rating,
        answered_at=now,
    )

    db.add(response)

    # --------------------------------------------------------
    # 8. Update attempt counters
    # --------------------------------------------------------

    attempt.answered_items += 1

    # --------------------------------------------------------
    # 9. Find/create learner mastery record
    # --------------------------------------------------------

    mastery = db.scalar(
        select(LearnerConceptMastery).where(
            LearnerConceptMastery.user_id == current_user.id,
            LearnerConceptMastery.concept_id == item.concept_id,
        )
    )

    if mastery is None:
        mastery = LearnerConceptMastery(
            user_id=current_user.id,
            subject_id=assessment.learner_subject.subject_id,
            concept_id=item.concept_id,
            mastery_score=0,
            confidence_score=0,
            mastery_state="unknown",
            attempts=0,
            correct_attempts=0,
        )

        db.add(mastery)
        db.flush()

    previous_score = float(mastery.mastery_score)
    previous_state = mastery.mastery_state

    mastery.attempts += 1

    if is_correct:
        mastery.correct_attempts += 1

    # --------------------------------------------------------
    # 10. Calculate mastery
    #
    # MVP:
    # accuracy = correct answers / total attempts
    # --------------------------------------------------------

    mastery.mastery_score = round(
        (
            mastery.correct_attempts
            / mastery.attempts
        ) * 100,
        2,
    )

    if mastery.mastery_score >= 80:
        mastery.mastery_state = "mastered"
    elif mastery.mastery_score >= 40:
        mastery.mastery_state = "partial"
    else:
        mastery.mastery_state = "weak"

    if payload.confidence_rating is not None:
        mastery.confidence_score = (
            payload.confidence_rating * 20
        )

    mastery.last_assessed_at = now

    # --------------------------------------------------------
    # 11. Save mastery history
    # --------------------------------------------------------

    history = MasteryHistory(
        learner_concept_mastery_id=mastery.id,
        previous_score=previous_score,
        new_score=float(mastery.mastery_score),
        previous_state=previous_state,
        new_state=mastery.mastery_state,
        reason="assessment",
    )

    db.add(history)

    db.commit()

    return DiagnosticAnswerResponse(
        is_correct=is_correct,
        score=score,
        concept_id=item.concept_id,
        concept_name=item.concept.name,
        mastery_update={
            "previous_score": previous_score,
            "new_score": float(mastery.mastery_score),
            "state": mastery.mastery_state,
        },
    )


# ============================================================
# COMPLETE DIAGNOSTIC
# ============================================================

@router.post(
    "/diagnostic/{assessment_id}/complete",
    response_model=DiagnosticCompleteResponse,
)
def complete_diagnostic(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticCompleteResponse:

    assessment = db.scalar(
        select(Assessment)
        .join(
            LearnerSubject,
            LearnerSubject.id == Assessment.learner_subject_id,
        )
        .where(
            Assessment.id == assessment_id,
            LearnerSubject.user_id == current_user.id,
        )
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    attempt = db.scalar(
        select(AssessmentAttempt).where(
            AssessmentAttempt.assessment_id == assessment.id,
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.status == "in_progress",
        )
    )

    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active assessment attempt not found.",
        )

    if attempt.answered_items < attempt.total_items:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Assessment is incomplete. "
                f"{attempt.answered_items}/"
                f"{attempt.total_items} questions answered."
            ),
        )

    now = datetime.now(timezone.utc)

    attempt.status = "completed"
    attempt.completed_at = now

    assessment.status = "completed"
    assessment.completed_at = now

    db.commit()

    return DiagnosticCompleteResponse(
        attempt_id=attempt.id,
        assessment_id=assessment.id,
        status="completed",
        answered_items=attempt.answered_items,
        total_items=attempt.total_items,
        analysis_available=True,
    )


# ============================================================
# DIAGNOSTIC ANALYSIS
# ============================================================

@router.get(
    "/diagnostic/{assessment_id}/analysis",
    response_model=DiagnosticAnalysisResponse,
)
def get_diagnostic_analysis(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticAnalysisResponse:

    assessment = db.scalar(
        select(Assessment)
        .join(
            LearnerSubject,
            LearnerSubject.id == Assessment.learner_subject_id,
        )
        .where(
            Assessment.id == assessment_id,
            LearnerSubject.user_id == current_user.id,
        )
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    mastery_records = list(
        db.scalars(
            select(LearnerConceptMastery)
            .join(
                Concept,
                Concept.id == LearnerConceptMastery.concept_id,
            )
            .where(
                LearnerConceptMastery.user_id == current_user.id,
                LearnerConceptMastery.subject_id
                == assessment.learner_subject.subject_id,
            )
            .order_by(Concept.name)
        ).all()
    )

    mastered = 0
    partial = 0
    weak = 0
    unknown = 0

    concepts = []

    for mastery in mastery_records:

        state = mastery.mastery_state

        if state == "mastered":
            mastered += 1
        elif state == "partial":
            partial += 1
        elif state == "weak":
            weak += 1
        else:
            unknown += 1

        concepts.append(
            {
                "concept_id": mastery.concept_id,
                "name": mastery.concept.name,
                "mastery_score": float(
                    mastery.mastery_score
                ),
                "mastery_state": state,
                "confidence_score": float(
                    mastery.confidence_score
                ),
                "attempts": mastery.attempts,
                "correct_attempts": mastery.correct_attempts,
            }
        )

    return DiagnosticAnalysisResponse(
        assessment_id=assessment.id,
        summary={
            "mastered": mastered,
            "partial": partial,
            "weak": weak,
            "unknown": unknown,
        },
        concepts=concepts,
    )