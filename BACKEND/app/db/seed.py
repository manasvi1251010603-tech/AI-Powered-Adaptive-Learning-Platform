from datetime import datetime, timezone

from sqlalchemy import select

from app.db.models.assessment import Question, QuestionOption
from app.db.models.taxonomy import Concept, Subject, Topic
from app.db.session import SessionLocal


SUBJECTS = [
    {
        "name": "Python",
        "slug": "python",
        "description": "Learn Python programming from fundamentals to advanced concepts.",
    },
    {
        "name": "Data Structures & Algorithms",
        "slug": "data-structures-algorithms",
        "description": "Learn data structures, algorithms, problem solving, and complexity analysis.",
    },
    {
        "name": "SQL & Databases",
        "slug": "sql-databases",
        "description": "Learn SQL, relational databases, database design, and querying.",
    },
    {
        "name": "Machine Learning",
        "slug": "machine-learning",
        "description": "Learn machine learning concepts, algorithms, model training, and evaluation.",
    },
    {
        "name": "Artificial Intelligence",
        "slug": "artificial-intelligence",
        "description": "Learn artificial intelligence concepts and practical AI techniques.",
    },
]


LEARNING_GOALS = [
    {
        "code": "MASTER_SUBJECT",
        "name": "Master the Subject",
        "description": "Build strong understanding from fundamentals to advanced concepts.",
        "default_mastery_threshold": 80,
    },
    {
        "code": "EXAM_PREPARATION",
        "name": "Prepare for Exams",
        "description": "Focus learning on concepts and practice relevant to examinations.",
        "default_mastery_threshold": 80,
    },
    {
        "code": "PRACTICAL_SKILLS",
        "name": "Build Practical Skills",
        "description": "Focus on applying concepts through practical exercises and projects.",
        "default_mastery_threshold": 80,
    },
    {
        "code": "INTERVIEW_PREPARATION",
        "name": "Prepare for Interviews",
        "description": "Focus on concepts, problem solving, and interview-oriented practice.",
        "default_mastery_threshold": 80,
    },
]


PYTHON_TOPICS = [
    {
        "slug": "fundamentals",
        "name": "Python Fundamentals",
        "description": "Core Python programming concepts.",
        "sort_order": 1,
    },
    {
        "slug": "control-flow",
        "name": "Control Flow",
        "description": "Conditions and loops used to control program execution.",
        "sort_order": 2,
    },
]


PYTHON_CONCEPTS = [
    {
        "topic_slug": "fundamentals",
        "slug": "variables",
        "name": "Variables",
        "description": "Variables, assignment, and storing values.",
        "difficulty_baseline": 20,
    },
    {
        "topic_slug": "fundamentals",
        "slug": "data-types",
        "name": "Data Types",
        "description": "Python's basic built-in data types.",
        "difficulty_baseline": 25,
    },
    {
        "topic_slug": "fundamentals",
        "slug": "operators",
        "name": "Operators",
        "description": "Arithmetic, comparison, logical, and assignment operators.",
        "difficulty_baseline": 30,
    },
    {
        "topic_slug": "fundamentals",
        "slug": "functions",
        "name": "Functions",
        "description": "Defining, calling, and using Python functions.",
        "difficulty_baseline": 40,
    },
    {
        "topic_slug": "control-flow",
        "slug": "conditions",
        "name": "Conditions",
        "description": "Using if, elif, and else to make decisions.",
        "difficulty_baseline": 30,
    },
    {
        "topic_slug": "control-flow",
        "slug": "loops",
        "name": "Loops",
        "description": "Using for and while loops for repetition.",
        "difficulty_baseline": 35,
    },
]


QUESTIONS = [
    {
        "concept_slug": "variables",
        "question_type": "mcq",
        "prompt": "Which statement correctly assigns the value 10 to a variable named x?",
        "explanation": "Python uses the assignment operator = to assign a value to a variable.",
        "difficulty": 20,
        "options": [
            ("A", "x = 10", True),
            ("B", "10 = x", False),
            ("C", "x == 10", False),
            ("D", "int x = 10", False),
        ],
        "answer_data": {"correct_option": "A"},
    },
    {
        "concept_slug": "variables",
        "question_type": "mcq",
        "prompt": "What is the value of x after executing x = 5 followed by x = 8?",
        "explanation": "The second assignment replaces the previous value.",
        "difficulty": 25,
        "options": [
            ("A", "5", False),
            ("B", "8", True),
            ("C", "13", False),
            ("D", "Error", False),
        ],
        "answer_data": {"correct_option": "B"},
    },
    {
        "concept_slug": "data-types",
        "question_type": "mcq",
        "prompt": "What is the data type of the value 3.14 in Python?",
        "explanation": "A number containing a decimal point is a float.",
        "difficulty": 20,
        "options": [
            ("A", "int", False),
            ("B", "str", False),
            ("C", "float", True),
            ("D", "bool", False),
        ],
        "answer_data": {"correct_option": "C"},
    },
    {
        "concept_slug": "data-types",
        "question_type": "mcq",
        "prompt": "Which Python data type represents True or False?",
        "explanation": "Boolean values in Python use the bool type.",
        "difficulty": 25,
        "options": [
            ("A", "int", False),
            ("B", "bool", True),
            ("C", "float", False),
            ("D", "list", False),
        ],
        "answer_data": {"correct_option": "B"},
    },
    {
        "concept_slug": "operators",
        "question_type": "mcq",
        "prompt": "What is the result of 10 % 3 in Python?",
        "explanation": "The modulo operator % returns the remainder after division.",
        "difficulty": 30,
        "options": [
            ("A", "0", False),
            ("B", "1", True),
            ("C", "3", False),
            ("D", "3.33", False),
        ],
        "answer_data": {"correct_option": "B"},
    },
    {
        "concept_slug": "functions",
        "question_type": "mcq",
        "prompt": "Which keyword is used to define a function in Python?",
        "explanation": "Python uses the def keyword to define functions.",
        "difficulty": 30,
        "options": [
            ("A", "function", False),
            ("B", "define", False),
            ("C", "def", True),
            ("D", "fun", False),
        ],
        "answer_data": {"correct_option": "C"},
    },
    {
        "concept_slug": "conditions",
        "question_type": "mcq",
        "prompt": "Which keyword is used to test a condition in Python?",
        "explanation": "The if keyword begins a conditional statement.",
        "difficulty": 25,
        "options": [
            ("A", "when", False),
            ("B", "if", True),
            ("C", "check", False),
            ("D", "condition", False),
        ],
        "answer_data": {"correct_option": "B"},
    },
    {
        "concept_slug": "conditions",
        "question_type": "mcq",
        "prompt": "What will this print? if 5 > 3: print('Yes')",
        "explanation": "Because 5 is greater than 3, the condition is true.",
        "difficulty": 30,
        "options": [
            ("A", "Yes", True),
            ("B", "No", False),
            ("C", "5 > 3", False),
            ("D", "Error", False),
        ],
        "answer_data": {"correct_option": "A"},
    },
    {
        "concept_slug": "loops",
        "question_type": "mcq",
        "prompt": "Which loop is commonly used to iterate over the elements of a list?",
        "explanation": "A for loop is commonly used to iterate through iterable objects such as lists.",
        "difficulty": 30,
        "options": [
            ("A", "if", False),
            ("B", "for", True),
            ("C", "switch", False),
            ("D", "case", False),
        ],
        "answer_data": {"correct_option": "B"},
    },
    {
        "concept_slug": "loops",
        "question_type": "mcq",
        "prompt": "How many times does this loop print? for i in range(3): print(i)",
        "explanation": "range(3) produces 0, 1, and 2, so the loop runs three times.",
        "difficulty": 35,
        "options": [
            ("A", "2", False),
            ("B", "3", True),
            ("C", "4", False),
            ("D", "0", False),
        ],
        "answer_data": {"correct_option": "B"},
    },
]


def seed_subjects(db) -> None:
    for data in SUBJECTS:
        existing = db.scalar(
            select(Subject).where(Subject.slug == data["slug"])
        )

        if existing is None:
            db.add(
                Subject(
                    **data,
                    is_published=True,
                )
            )


def seed_learning_goals(db) -> None:
    from app.db.models.taxonomy import LearningGoal

    for data in LEARNING_GOALS:
        existing = db.scalar(
            select(LearningGoal).where(
                LearningGoal.code == data["code"]
            )
        )

        if existing is None:
            db.add(LearningGoal(**data))


def seed_python_taxonomy(db) -> None:
    python_subject = db.scalar(
        select(Subject).where(Subject.slug == "python")
    )

    if python_subject is None:
        raise RuntimeError(
            "Python subject was not found. Seed subjects first."
        )

    topics = {}

    for data in PYTHON_TOPICS:
        topic = db.scalar(
            select(Topic).where(
                Topic.subject_id == python_subject.id,
                Topic.slug == data["slug"],
            )
        )

        if topic is None:
            topic = Topic(
                subject_id=python_subject.id,
                **data,
            )
            db.add(topic)
            db.flush()

        topics[data["slug"]] = topic

    concepts = {}

    for data in PYTHON_CONCEPTS:
        concept = db.scalar(
            select(Concept).where(
                Concept.subject_id == python_subject.id,
                Concept.slug == data["slug"],
            )
        )

        if concept is None:
            concept = Concept(
                subject_id=python_subject.id,
                topic_id=topics[data["topic_slug"]].id,
                name=data["name"],
                slug=data["slug"],
                description=data["description"],
                difficulty_baseline=data["difficulty_baseline"],
                is_active=True,
            )
            db.add(concept)
            db.flush()

        concepts[data["slug"]] = concept

    return concepts


def seed_questions(db, concepts) -> None:
    for data in QUESTIONS:
        concept = concepts[data["concept_slug"]]

        existing = db.scalar(
            select(Question).where(
                Question.concept_id == concept.id,
                Question.prompt == data["prompt"],
            )
        )

        if existing is not None:
            continue

        question = Question(
            concept_id=concept.id,
            question_type=data["question_type"],
            prompt=data["prompt"],
            explanation=data["explanation"],
            difficulty=data["difficulty"],
            answer_data=data["answer_data"],
            source="seed",
            status="active",
        )

        db.add(question)
        db.flush()

        for key, option_text, is_correct in data["options"]:
            db.add(
                QuestionOption(
                    question_id=question.id,
                    option_text=option_text,
                    option_key=key,
                    sort_order=ord(key) - ord("A"),
                    is_correct=is_correct,
                )
            )


def main() -> None:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured.")

    db = SessionLocal()

    try:
        seed_subjects(db)
        seed_learning_goals(db)

        db.flush()

        concepts = seed_python_taxonomy(db)
        seed_questions(db, concepts)

        db.commit()

        print("SEED_SUCCESS")
        print("SUBJECT_COUNT:", db.query(Subject).count())
        print("TOPIC_COUNT:", db.query(Topic).count())
        print("CONCEPT_COUNT:", db.query(Concept).count())
        print("QUESTION_COUNT:", db.query(Question).count())
        print("OPTION_COUNT:", db.query(QuestionOption).count())

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()