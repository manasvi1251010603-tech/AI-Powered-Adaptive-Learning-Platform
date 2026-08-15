from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.personalization import (
    LearningPath,
    LearningPathStep,
)
from app.db.models.content import (
    Resource,
    ResourceConcept,
)
from app.db.models.video import (
    Video,
    VideoSegment,
    VideoSegmentConcept,
)
from app.db.models.personalization import Recommendation
from app.db.models.knowledge import LearnerConceptMastery
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
    LearningPathResponse,
    LearningPathStepResponse,
    ResourceRecommendationResponse,
    ResourceSectionResponse,
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
    ConceptPrerequisite,
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
# ============================================================
# PERSONALIZED LEARNING PATH
# ============================================================

@router.post(
    "/path/generate",
    response_model=LearningPathResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_learning_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LearningPathResponse:

    # --------------------------------------------------------
    # 1. Find the learner's active subject
    # --------------------------------------------------------

    learner_subject = db.scalar(
        select(LearnerSubject).where(
            LearnerSubject.user_id == current_user.id,
            LearnerSubject.status == "active",
        )
        .order_by(LearnerSubject.started_at.desc())
    )

    if learner_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active learning subject found.",
        )

    target_mastery = float(
        learner_subject.target_mastery
    )

    # --------------------------------------------------------
    # 2. Load all active concepts
    # --------------------------------------------------------

    concepts = list(
        db.scalars(
            select(Concept).where(
                Concept.subject_id == learner_subject.subject_id,
                Concept.is_active.is_(True),
            )
        ).all()
    )

    if not concepts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No concepts found for this subject.",
        )

    concept_map = {
        concept.id: concept
        for concept in concepts
    }

    concept_ids = set(concept_map.keys())

    # --------------------------------------------------------
    # 3. Load learner mastery
    # --------------------------------------------------------

    mastery_records = list(
        db.scalars(
            select(LearnerConceptMastery).where(
                LearnerConceptMastery.user_id == current_user.id,
                LearnerConceptMastery.subject_id
                == learner_subject.subject_id,
                LearnerConceptMastery.concept_id.in_(
                    concept_ids
                ),
            )
        ).all()
    )

    mastery_map = {
        mastery.concept_id: mastery
        for mastery in mastery_records
    }

    def mastery_score(concept_id: UUID) -> float:
        mastery = mastery_map.get(concept_id)

        if mastery is None:
            return 0.0

        return float(mastery.mastery_score)

    def mastery_state(concept_id: UUID) -> str:
        mastery = mastery_map.get(concept_id)

        if mastery is None:
            return "unknown"

        return mastery.mastery_state

    # --------------------------------------------------------
    # 4. Identify concepts that actually need learning
    #
    # Mastered concepts are skipped.
    # --------------------------------------------------------

    required_concepts = set()

    for concept in concepts:

        score = mastery_score(concept.id)

        if score < target_mastery:
            required_concepts.add(concept.id)

    if not required_concepts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "You have already reached the target mastery "
                "for all concepts."
            ),
        )

    # --------------------------------------------------------
    # 5. Load prerequisites
    # --------------------------------------------------------

    prerequisites = list(
        db.scalars(
            select(ConceptPrerequisite).where(
                ConceptPrerequisite.concept_id.in_(
                    required_concepts
                )
            )
        ).all()
    )

    prerequisite_map: dict[UUID, list[UUID]] = {}

    for prerequisite in prerequisites:

        if (
            prerequisite.prerequisite_concept_id
            not in concept_ids
        ):
            continue

        prerequisite_map.setdefault(
            prerequisite.concept_id,
            [],
        ).append(
            prerequisite.prerequisite_concept_id
        )

    # --------------------------------------------------------
    # 6. Include weak prerequisites automatically
    #
    # If concept B needs concept A and A is weak,
    # A must appear before B.
    # --------------------------------------------------------

    changed = True

    while changed:

        changed = False

        for concept_id in list(required_concepts):

            for prerequisite_id in prerequisite_map.get(
                concept_id,
                [],
            ):

                if (
                    mastery_score(prerequisite_id)
                    < target_mastery
                    and prerequisite_id
                    not in required_concepts
                ):
                    required_concepts.add(
                        prerequisite_id
                    )
                    changed = True

    # --------------------------------------------------------
    # 7. Topological ordering
    #
    # Prerequisites always appear before dependent concepts.
    # --------------------------------------------------------

    ordered_ids: list[UUID] = []
    remaining = set(required_concepts)

    while remaining:

        ready = []

        for concept_id in remaining:

            dependencies = [
                prerequisite_id
                for prerequisite_id in prerequisite_map.get(
                    concept_id,
                    [],
                )
                if prerequisite_id in remaining
            ]

            if not dependencies:
                ready.append(concept_id)

        # Safety against circular prerequisite data.
        if not ready:
            ready = sorted(
                remaining,
                key=lambda cid: (
                    mastery_score(cid),
                    concept_map[cid].name.lower(),
                ),
            )[:1]

        # Weakest first among concepts currently available.
        ready.sort(
            key=lambda cid: (
                mastery_score(cid),
                concept_map[cid].name.lower(),
            )
        )

        for concept_id in ready:
            ordered_ids.append(concept_id)
            remaining.remove(concept_id)

    # --------------------------------------------------------
    # 8. Supersede an existing active path
    # --------------------------------------------------------

    existing_path = db.scalar(
        select(LearningPath).where(
            LearningPath.learner_subject_id
            == learner_subject.id,
            LearningPath.status == "active",
        )
    )

    if existing_path is not None:
        existing_path.status = "superseded"

    # --------------------------------------------------------
    # 9. Create new learning path
    # --------------------------------------------------------

    now = datetime.now(timezone.utc)

    learning_path = LearningPath(
        learner_subject_id=learner_subject.id,
        status="active",
        estimated_minutes=0,
        progress_percent=0,
        generated_at=now,
    )

    db.add(learning_path)
    db.flush()

    # --------------------------------------------------------
    # 10. Create learning path steps
    # --------------------------------------------------------

    step_responses = []
    total_minutes = 0

    for sequence_number, concept_id in enumerate(
        ordered_ids,
        start=1,
    ):

        concept = concept_map[concept_id]

        score = mastery_score(concept_id)
        state = mastery_state(concept_id)

        # ----------------------------------------------------
        # Estimate time based on mastery.
        #
        # This is intentionally simple for MVP.
        # Later AI/content metadata can improve it.
        # ----------------------------------------------------

        if score < 40:
            estimated_minutes = 30
        elif score < 70:
            estimated_minutes = 20
        else:
            estimated_minutes = 10

        total_minutes += estimated_minutes

        # ----------------------------------------------------
        # Determine prerequisite status
        # ----------------------------------------------------

        concept_prerequisites = prerequisite_map.get(
            concept_id,
            [],
        )

        if not concept_prerequisites:

            prerequisite_status = "satisfied"
            step_status = (
                "ready"
                if sequence_number == 1
                else "locked"
            )

        else:

            unsatisfied = [
                prerequisite_id
                for prerequisite_id in concept_prerequisites
                if mastery_score(prerequisite_id)
                < target_mastery
            ]

            if not unsatisfied:

                prerequisite_status = "satisfied"

                step_status = (
                    "ready"
                    if sequence_number == 1
                    else "locked"
                )

            else:

                prerequisite_status = "scheduled_before"
                step_status = "locked"

        step = LearningPathStep(
            learning_path_id=learning_path.id,
            concept_id=concept.id,
            sequence_number=sequence_number,
            status=step_status,
            mastery_threshold=target_mastery,
            estimated_minutes=estimated_minutes,
            prerequisite_status=prerequisite_status,
        )

        db.add(step)

        step_responses.append(
            (
                step,
                concept,
                score,
                state,
            )
        )

    learning_path.estimated_minutes = total_minutes

    db.commit()

    db.refresh(learning_path)

    # --------------------------------------------------------
    # 11. Build response
    # --------------------------------------------------------

    response_steps = []

    for (
        step,
        concept,
        score,
        state,
    ) in step_responses:

        response_steps.append(
            LearningPathStepResponse(
                id=step.id,
                concept_id=concept.id,
                concept_name=concept.name,
                sequence_number=step.sequence_number,
                status=step.status,
                mastery_threshold=float(
                    step.mastery_threshold
                ),
                estimated_minutes=step.estimated_minutes,
                prerequisite_status=(
                    step.prerequisite_status
                ),
                current_mastery=score,
                mastery_state=state,
            )
        )

    return LearningPathResponse(
        id=learning_path.id,
        learner_subject_id=learning_path.learner_subject_id,
        status=learning_path.status,
        estimated_minutes=learning_path.estimated_minutes,
        progress_percent=float(
            learning_path.progress_percent
        ),
        generated_at=learning_path.generated_at,
        steps=response_steps,
    )
# ============================================================
# GET CURRENT LEARNING PATH
# ============================================================

@router.get(
    "/path",
    response_model=LearningPathResponse,
)
def get_learning_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LearningPathResponse:

    learning_path = db.scalar(
        select(LearningPath)
        .join(
            LearnerSubject,
            LearnerSubject.id
            == LearningPath.learner_subject_id,
        )
        .where(
            LearnerSubject.user_id == current_user.id,
            LearnerSubject.status == "active",
            LearningPath.status == "active",
        )
        .order_by(
            LearningPath.generated_at.desc()
        )
    )

    if learning_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active learning path found.",
        )

    steps = list(
        db.scalars(
            select(LearningPathStep)
            .where(
                LearningPathStep.learning_path_id
                == learning_path.id,
            )
            .order_by(
                LearningPathStep.sequence_number
            )
        ).all()
    )

    response_steps = []

    for step in steps:

        mastery = db.scalar(
            select(LearnerConceptMastery).where(
                LearnerConceptMastery.user_id
                == current_user.id,
                LearnerConceptMastery.concept_id
                == step.concept_id,
            )
        )

        current_mastery = (
            float(mastery.mastery_score)
            if mastery is not None
            else 0.0
        )

        current_state = (
            mastery.mastery_state
            if mastery is not None
            else "unknown"
        )

        response_steps.append(
            LearningPathStepResponse(
                id=step.id,
                concept_id=step.concept_id,
                concept_name=step.concept.name,
                sequence_number=step.sequence_number,
                status=step.status,
                mastery_threshold=float(
                    step.mastery_threshold
                ),
                estimated_minutes=step.estimated_minutes,
                prerequisite_status=(
                    step.prerequisite_status
                ),
                current_mastery=current_mastery,
                mastery_state=current_state,
            )
        )

    return LearningPathResponse(
        id=learning_path.id,
        learner_subject_id=learning_path.learner_subject_id,
        status=learning_path.status,
        estimated_minutes=learning_path.estimated_minutes,
        progress_percent=float(
            learning_path.progress_percent
        ),
        generated_at=learning_path.generated_at,
        steps=response_steps,
    )

# ============================================================
# AI RESOURCE RECOMMENDATIONS
# ============================================================

@router.get(
    "/resources/recommendations",
    response_model=list[
        ResourceRecommendationResponse
    ],
)
def recommend_resources(
    concept_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------------
    # 1. Find concept
    # --------------------------------------------------------

    concept = db.scalar(
        select(Concept).where(
            Concept.id == concept_id,
            Concept.is_active.is_(True),
        )
    )

    if concept is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concept not found.",
        )

    # --------------------------------------------------------
    # 2. Find learner mastery
    # --------------------------------------------------------

    mastery = db.scalar(
        select(LearnerConceptMastery).where(
            LearnerConceptMastery.user_id
            == current_user.id,
            LearnerConceptMastery.concept_id
            == concept.id,
        )
    )

    mastery_score = (
        float(mastery.mastery_score)
        if mastery is not None
        else 0.0
    )

    # --------------------------------------------------------
    # 3. Search YouTube
    # --------------------------------------------------------

    from app.services.youtube_service import (
        YouTubeService,
    )

    from app.services.resource_intelligence import (
        ResourceIntelligenceService,
    )

    youtube = YouTubeService()
    intelligence = ResourceIntelligenceService()

    query = f"{concept.name} tutorial explained"

    videos = youtube.search_videos(
        query,
        max_results=5,
    )

    recommendations = []

    # --------------------------------------------------------
    # 4. Process candidate videos
    # --------------------------------------------------------

    for video_data in videos:

        try:
            transcript = intelligence.get_transcript(
                video_data["video_id"]
            )

        except Exception:
            # No usable transcript.
            # Never invent timestamps.
            continue

        if not transcript:
            continue

        transcript = (
            intelligence.combine_transcript_chunks(
                transcript
            )
        )

        sections = (
            intelligence.map_concept_to_transcript(
                concept_name=concept.name,
                concept_description=(
                    concept.description or ""
                ),
                transcript=transcript,
                mastery_score=mastery_score,
            )
        )

        if not sections:
            continue

        # ----------------------------------------------------
        # 5. Save Resource
        # ----------------------------------------------------

        resource = db.scalar(
            select(Resource).where(
                Resource.url
                == video_data["url"],
                Resource.subject_id
                == concept.subject_id,
            )
        )

        if resource is None:

            resource = Resource(
                subject_id=concept.subject_id,
                resource_type="video",
                title=video_data["title"][:250],
                description=(
                    video_data["description"]
                    or None
                ),
                url=video_data["url"],
                storage_key=video_data["video_id"],
                thumbnail_url=(
                    video_data["thumbnail_url"]
                ),
                language="en",
                status="published",
                created_by_id=current_user.id,
            )

            db.add(resource)
            db.flush()

        # ----------------------------------------------------
        # 6. Link Resource → Concept
        # ----------------------------------------------------

        resource_concept = db.scalar(
            select(ResourceConcept).where(
                ResourceConcept.resource_id
                == resource.id,
                ResourceConcept.concept_id
                == concept.id,
            )
        )

        if resource_concept is None:

            average_confidence = (
                sum(
                    section.confidence
                    for section in sections
                )
                / len(sections)
                * 100
            )

            db.add(
                ResourceConcept(
                    resource_id=resource.id,
                    concept_id=concept.id,
                    relevance_score=min(
                        100,
                        average_confidence,
                    ),
                )
            )

        # ----------------------------------------------------
        # 7. Create / update Video
        # ----------------------------------------------------

        video = db.scalar(
            select(Video).where(
                Video.resource_id
                == resource.id
            )
        )

        if video is None:

            video = Video(
                resource_id=resource.id,
                storage_key=video_data[
                    "video_id"
                ],
                transcript_status="completed",
                segmentation_status="completed",
            )

            db.add(video)
            db.flush()

        # ----------------------------------------------------
        # 8. Store AI-selected timestamp sections
        # ----------------------------------------------------

        stored_sections = []

        for index, section in enumerate(
            sections,
            start=1,
        ):

            segment_title = (
                f"{concept.name} - Section {index}"
            )

            video_segment = VideoSegment(
                video_id=video.id,
                title=segment_title[:250],
                start_seconds=section.start_seconds,
                end_seconds=section.end_seconds,
                transcript_text=None,
                ai_confidence=(
                    section.confidence * 100
                ),
                source="ai",
                review_status="pending",
            )

            db.add(video_segment)
            db.flush()

            db.add(
                VideoSegmentConcept(
                    segment_id=video_segment.id,
                    concept_id=concept.id,
                    confidence=(
                        section.confidence * 100
                    ),
                    is_primary=True,
                )
            )

            stored_sections.append(
                video_segment
            )

        # ----------------------------------------------------
        # 9. Create recommendation
        # ----------------------------------------------------

        best_confidence = max(
            section.confidence
            for section in sections
        )

        recommendation = Recommendation(
            user_id=current_user.id,
            concept_id=concept.id,
            resource_id=resource.id,
            recommendation_type="video",
            score=best_confidence * 100,
            reason=(
                f"Recommended because this video contains "
                f"AI-identified sections relevant to "
                f"{concept.name}, which currently has "
                f"{mastery_score:.1f}% mastery."
            ),
            generated_by="ai",
        )

        db.add(recommendation)

        recommendations.append(
            ResourceRecommendationResponse(
                video_id=video_data["video_id"],
                title=video_data["title"],
                description=(
                    video_data["description"]
                ),
                channel_title=(
                    video_data["channel_title"]
                ),
                url=video_data["url"],
                thumbnail_url=(
                    video_data["thumbnail_url"]
                ),
                sections=[
                    ResourceSectionResponse(
                        start_seconds=(
                            section.start_seconds
                        ),
                        end_seconds=(
                            section.end_seconds
                        ),
                        concept=section.concept,
                        reason=section.reason,
                        confidence=section.confidence,
                    )
                    for section in sections
                ],
            )
        )

        if len(recommendations) >= 3:
            break

    db.commit()

    return recommendations
def recommend_resources(
    concept_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------------
    # 1. Load concept
    # --------------------------------------------------------

    concept = db.scalar(
        select(Concept).where(
            Concept.id == concept_id,
            Concept.is_active.is_(True),
        )
    )

    if concept is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concept not found.",
        )

    # --------------------------------------------------------
    # 2. Load learner mastery
    # --------------------------------------------------------

    mastery = db.scalar(
        select(LearnerConceptMastery).where(
            LearnerConceptMastery.user_id
            == current_user.id,
            LearnerConceptMastery.concept_id
            == concept.id,
        )
    )

    mastery_score = (
        float(mastery.mastery_score)
        if mastery is not None
        else 0.0
    )

    # --------------------------------------------------------
    # 3. Search YouTube
    # --------------------------------------------------------

    from app.services.youtube_service import (
        YouTubeService,
    )

    from app.services.resource_intelligence import (
        ResourceIntelligenceService,
    )

    youtube = YouTubeService()

    ai_service = (
        ResourceIntelligenceService()
    )

    query = f"{concept.name} tutorial explained"

    videos = youtube.search_videos(
        query,
        max_results=5,
    )

    recommendations = []

    # --------------------------------------------------------
    # 4. Process candidates
    # --------------------------------------------------------

    for video in videos:

        try:

            transcript = (
                ai_service.get_transcript(
                    video["video_id"]
                )
            )

        except Exception:
            # Transcript unavailable.
            # Skip this candidate rather than
            # inventing timestamps.
            continue

        if not transcript:
            continue

        transcript = (
            ai_service.combine_transcript_chunks(
                transcript
            )
        )

        sections = (
            ai_service.map_concept_to_transcript(
                concept_name=concept.name,
                concept_description=(
                    concept.description or ""
                ),
                transcript=transcript,
                mastery_score=mastery_score,
            )
        )

        if not sections:
            continue

        recommendations.append(
            ResourceRecommendationResponse(
                video_id=video["video_id"],
                title=video["title"],
                description=video[
                    "description"
                ],
                channel_title=video[
                    "channel_title"
                ],
                url=video["url"],
                thumbnail_url=video[
                    "thumbnail_url"
                ],
                sections=[
                    ResourceSectionResponse(
                        start_seconds=(
                            section.start_seconds
                        ),
                        end_seconds=(
                            section.end_seconds
                        ),
                        concept=section.concept,
                        reason=section.reason,
                        confidence=section.confidence,
                    )
                    for section in sections
                ],
            )
        )

        # MVP: return at most 3 strong resources.
        if len(recommendations) >= 3:
            break

    return recommendations