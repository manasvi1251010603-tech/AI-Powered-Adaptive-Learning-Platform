"use client";

import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  Check,
  Clock3,
  Sparkles,
  Zap,
} from "lucide-react";
import { useState } from "react";

type Question = {
  id: number;
  difficulty: "Easy" | "Medium" | "Hard";
  topic: string;
  question: string;
  options: string[];
  correctAnswer: number;
};

const questions: Question[] = [
  {
    id: 1,
    difficulty: "Easy",
    topic: "Python Basics",
    question: "Which of the following is used to create a variable in Python?",
    options: [
      "var x = 10",
      "int x = 10",
      "x = 10",
      "declare x = 10",
    ],
    correctAnswer: 2,
  },
  {
    id: 2,
    difficulty: "Easy",
    topic: "Python Basics",
    question: "What is the output of: len([10, 20, 30, 40])?",
    options: ["3", "4", "5", "40"],
    correctAnswer: 1,
  },
  {
    id: 3,
    difficulty: "Medium",
    topic: "Lists",
    question: "Which method adds an element to the end of a Python list?",
    options: ["add()", "insert()", "append()", "push()"],
    correctAnswer: 2,
  },
  {
    id: 4,
    difficulty: "Medium",
    topic: "Functions",
    question: "Which keyword is used to define a function in Python?",
    options: ["function", "def", "func", "define"],
    correctAnswer: 1,
  },
  {
    id: 5,
    difficulty: "Hard",
    topic: "Functions",
    question:
      "What does a Python function return if it reaches the end without a return statement?",
    options: ["0", "False", "None", "An error"],
    correctAnswer: 2,
  },
];

const difficultyStyles = {
  Easy: {
    badge: "bg-[#eaf7f2] text-[#3a9476]",
    dot: "bg-[#48a984]",
  },
  Medium: {
    badge: "bg-[#fff6e5] text-[#b57c20]",
    dot: "bg-[#e4a83e]",
  },
  Hard: {
    badge: "bg-[#eef3ff] text-[#3970e8]",
    dot: "bg-[#3970e8]",
  },
};

export default function AssessmentPage() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [showFeedback, setShowFeedback] = useState(false);

  const question = questions[currentQuestion];
  const totalQuestions = questions.length;
  const progress = ((currentQuestion + 1) / totalQuestions) * 100;

  const isLastQuestion = currentQuestion === totalQuestions - 1;

  const selectAnswer = (index: number) => {
    if (showFeedback) return;

    setSelectedAnswer(index);
  };

  const nextQuestion = () => {
    if (selectedAnswer === null) return;

    setAnswers((previous) => ({
      ...previous,
      [question.id]: selectedAnswer,
    }));

    setShowFeedback(true);

    setTimeout(() => {
      setShowFeedback(false);

      if (!isLastQuestion) {
        setCurrentQuestion((previous) => previous + 1);
        setSelectedAnswer(null);
      } else {
        // The final analysis page will be connected later.
        window.location.href = "/analysis";
      }
    }, 650);
  };

  const previousQuestion = () => {
    if (currentQuestion === 0) return;

    setCurrentQuestion((previous) => previous - 1);
    setSelectedAnswer(answers[question.id - 1] ?? null);
    setShowFeedback(false);
  };

  return (
    <main className="min-h-screen bg-[#eef4fb] px-3 py-3 sm:px-5 sm:py-5 lg:px-7">
      <div className="relative min-h-[calc(100vh-24px)] overflow-hidden rounded-[28px] border border-white bg-[#f8fbff] shadow-[0_20px_70px_rgba(48,78,125,0.10)]">

        {/* =====================================================
            BACKGROUND
        ===================================================== */}

        <div className="pointer-events-none absolute right-[-100px] top-[-100px] h-[400px] w-[400px] rounded-full bg-[#dce9ff] opacity-60 blur-[100px]" />

        <motion.div
          animate={{
            x: [0, 15, 0],
            y: [0, -10, 0],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="pointer-events-none absolute bottom-[-120px] left-[-100px] h-[350px] w-[350px] rounded-full bg-[#e4efff] blur-[90px]"
        />

        {/* =====================================================
            NAVBAR
        ===================================================== */}

        <nav className="relative z-20 flex h-[72px] items-center justify-between px-5 sm:px-8 lg:px-10">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#eaf1ff] text-[#3265e8]">
              <Brain size={18} />
            </div>

            <span className="text-[15px] font-bold tracking-tight text-[#172033]">
              LearnFlow
            </span>
          </Link>

          <div className="flex items-center gap-2 text-[10px] font-medium text-[#7f8998]">
            <Clock3 size={12} />
            Diagnostic assessment
          </div>
        </nav>

        {/* =====================================================
            PROGRESS
        ===================================================== */}

        <div className="relative z-20 mx-auto max-w-[850px] px-6 sm:px-8">
          <div className="flex items-center justify-between text-[9px] font-semibold text-[#7c8797]">
            <span>
              Question {currentQuestion + 1} of {totalQuestions}
            </span>

            <span>{Math.round(progress)}%</span>
          </div>

          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[#e3e9f2]">
            <motion.div
              className="h-full rounded-full bg-[#3970e8]"
              animate={{
                width: `${progress}%`,
              }}
              transition={{
                duration: 0.45,
                ease: "easeInOut",
              }}
            />
          </div>
        </div>

        {/* =====================================================
            MAIN ASSESSMENT
        ===================================================== */}

        <div className="relative z-10 mx-auto flex min-h-[calc(100vh-155px)] max-w-[850px] flex-col px-5 pb-8 pt-10 sm:px-8 sm:pt-14">

          <AnimatePresence mode="wait">
            <motion.div
              key={question.id}
              initial={{
                opacity: 0,
                x: 25,
              }}
              animate={{
                opacity: 1,
                x: 0,
              }}
              exit={{
                opacity: 0,
                x: -25,
              }}
              transition={{
                duration: 0.35,
              }}
            >

              {/* Topic + difficulty */}

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3970e8]">
                    <Brain size={15} />
                  </div>

                  <span className="text-[10px] font-semibold text-[#687486]">
                    {question.topic}
                  </span>
                </div>

                <div
                  className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[9px] font-semibold ${difficultyStyles[question.difficulty].badge}`}
                >
                  <span
                    className={`h-1.5 w-1.5 rounded-full ${difficultyStyles[question.difficulty].dot}`}
                  />

                  {question.difficulty}
                </div>
              </div>

              {/* Question */}

              <div className="mt-9">
                <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-[#3970e8]">
                  Question {currentQuestion + 1}
                </p>

                <h1 className="mt-3 max-w-[750px] text-[27px] font-bold leading-[1.25] tracking-[-0.035em] text-[#152033] sm:text-[34px]">
                  {question.question}
                </h1>
              </div>

              {/* Options */}

              <div className="mt-9 space-y-3">
                {question.options.map((option, index) => {
                  const selected = selectedAnswer === index;
                  const correct = question.correctAnswer === index;

                  let optionStyle =
                    "border-[#e0e7f0] bg-white hover:border-[#c6d5eb] hover:shadow-sm";

                  if (selected && !showFeedback) {
                    optionStyle =
                      "border-[#6f9bef] bg-[#edf4ff] shadow-[0_8px_25px_rgba(57,112,232,0.10)]";
                  }

                  if (showFeedback && selected && correct) {
                    optionStyle =
                      "border-[#67b99a] bg-[#edf9f4]";
                  }

                  if (showFeedback && selected && !correct) {
                    optionStyle =
                      "border-[#e0a3a3] bg-[#fff3f3]";
                  }

                  return (
                    <motion.button
                      key={option}
                      type="button"
                      whileHover={{
                        x: selected ? 0 : 3,
                      }}
                      whileTap={{
                        scale: 0.995,
                      }}
                      onClick={() => selectAnswer(index)}
                      className={`relative flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition duration-300 ${optionStyle}`}
                    >
                      {/* Letter */}

                      <div
                        className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-[11px] font-bold ${
                          selected
                            ? "bg-[#3970e8] text-white"
                            : "bg-[#edf3ff] text-[#3970e8]"
                        }`}
                      >
                        {String.fromCharCode(65 + index)}
                      </div>

                      {/* Text */}

                      <span className="text-[12px] font-medium leading-5 text-[#455164] sm:text-[13px]">
                        {option}
                      </span>

                      {/* Selected indicator */}

                      {selected && (
                        <motion.div
                          initial={{
                            scale: 0,
                          }}
                          animate={{
                            scale: 1,
                          }}
                          className="absolute right-4 flex h-5 w-5 items-center justify-center rounded-full bg-[#3970e8] text-white"
                        >
                          {showFeedback && correct ? (
                            <Check size={11} />
                          ) : (
                            <span className="h-1.5 w-1.5 rounded-full bg-white" />
                          )}
                        </motion.div>
                      )}
                    </motion.button>
                  );
                })}
              </div>

              {/* Adaptive learning note */}

              <motion.div
                initial={{
                  opacity: 0,
                }}
                animate={{
                  opacity: 1,
                }}
                transition={{
                  delay: 0.3,
                }}
                className="mt-6 flex items-center gap-2 rounded-xl border border-[#e4ebf4] bg-white/65 px-4 py-3"
              >
                <Sparkles
                  size={13}
                  className="shrink-0 text-[#3970e8]"
                />

                <p className="text-[9px] leading-5 text-[#8490a0]">
                  Questions adapt to your answers so we can identify your
                  actual knowledge gaps.
                </p>
              </motion.div>
            </motion.div>
          </AnimatePresence>

          {/* ===================================================
              BOTTOM NAVIGATION
          =================================================== */}

          <div className="mt-auto flex items-center justify-between border-t border-[#e5ebf3] pt-6">

            <button
              type="button"
              onClick={previousQuestion}
              disabled={currentQuestion === 0}
              className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-[10px] font-semibold transition ${
                currentQuestion === 0
                  ? "cursor-not-allowed text-[#c4cad3]"
                  : "text-[#697587] hover:bg-white hover:text-[#3970e8]"
              }`}
            >
              <ArrowLeft size={13} />
              Previous
            </button>

            <motion.button
              type="button"
              disabled={selectedAnswer === null}
              onClick={nextQuestion}
              whileHover={
                selectedAnswer !== null
                  ? {
                      y: -2,
                    }
                  : {}
              }
              whileTap={
                selectedAnswer !== null
                  ? {
                      scale: 0.98,
                    }
                  : {}
              }
              className={`group flex items-center gap-2 rounded-xl px-5 py-3 text-[10px] font-semibold text-white transition ${
                selectedAnswer !== null
                  ? "bg-[#121c2c] shadow-[0_8px_20px_rgba(18,28,44,0.15)]"
                  : "cursor-not-allowed bg-[#cbd2dc]"
              }`}
            >
              {isLastQuestion ? "Analyze My Knowledge" : "Next Question"}

              {isLastQuestion ? (
                <Zap
                  size={13}
                  className={
                    selectedAnswer !== null
                      ? "transition-transform group-hover:scale-110"
                      : ""
                  }
                />
              ) : (
                <ArrowRight
                  size={13}
                  className={
                    selectedAnswer !== null
                      ? "transition-transform group-hover:translate-x-1"
                      : ""
                  }
                />
              )}
            </motion.button>
          </div>
        </div>
      </div>
    </main>
  );
}