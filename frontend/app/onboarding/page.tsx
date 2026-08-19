"use client";

import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  BriefcaseBusiness,
  Code2,
  GraduationCap,
  LineChart,
  Rocket,
  Sparkles,
  Target,
} from "lucide-react";
import { useEffect, useState } from "react";

import { apiClient } from "@/lib/api/client";

type Subject = {
  id: string;
  name: string;
  slug: string;
  description?: string | null;
};

type LearningGoal = {
  id: string;
  name: string;
  description?: string | null;
};

type EnrollmentResponse = {
  id: string;
  subject_id: string;
  learning_goal_id: string;
  target_mastery: number;
};

const subjectIcons: Record<string, typeof Code2> = {
  python: Code2,
  sql: LineChart,
  "machine-learning": Brain,
  "data-science": Sparkles,
};

const goalIcons: Record<string, typeof GraduationCap> = {
  academics: GraduationCap,
  projects: Rocket,
  career: BriefcaseBusiness,
  mastery: Target,
};

const levels = [
  {
    id: "beginner",
    title: "I'm just starting",
    description: "Little or no previous experience.",
  },
  {
    id: "familiar",
    title: "I know the basics",
    description: "I've studied some concepts but need practice.",
  },
  {
    id: "intermediate",
    title: "I'm fairly comfortable",
    description: "I can solve basic problems on my own.",
  },
  {
    id: "advanced",
    title: "I know quite a bit",
    description: "I want to fill specific gaps and go deeper.",
  },
];

const levelToSpeed: Record<
  string,
  "slow" | "moderate" | "fast"
> = {
  beginner: "slow",
  familiar: "moderate",
  intermediate: "moderate",
  advanced: "fast",
};

export default function OnboardingPage() {
  const [step, setStep] = useState(1);

  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [goals, setGoals] = useState<LearningGoal[]>([]);

  const [subject, setSubject] = useState("");
  const [goal, setGoal] = useState("");
  const [level, setLevel] = useState("");

  const [loadingData, setLoadingData] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const totalSteps = 3;

  // ==========================================================
  // LOAD SUBJECTS + GOALS
  // ==========================================================

  useEffect(() => {
    async function loadOnboardingData() {
      try {
        setLoadingData(true);
        setError("");

        const [subjectData, goalData] = await Promise.all([
          apiClient<Subject[]>("/learning/subjects"),
          apiClient<LearningGoal[]>("/learning/learning-goals"),
        ]);

        setSubjects(subjectData);
        setGoals(goalData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load onboarding data.",
        );
      } finally {
        setLoadingData(false);
      }
    }

    loadOnboardingData();
  }, []);

  const canContinue =
    step === 1
      ? !!subject
      : step === 2
        ? !!goal
        : !!level;

  // ==========================================================
  // START LEARNING JOURNEY
  // ==========================================================

  const createLearningPath = async () => {
    if (!subject || !goal || !level) {
      return;
    }

    try {
      setSubmitting(true);
      setError("");

      // ------------------------------------------------------
      // 1. Create learner-subject enrollment
      // ------------------------------------------------------

      const enrollment =
        await apiClient<EnrollmentResponse>(
          "/learning/subjects/enroll",
          {
            method: "POST",
            body: JSON.stringify({
              subject_id: subject,
              learning_goal_id: goal,
              target_mastery: 80,
            }),
          },
        );

      // ------------------------------------------------------
      // 2. Save learner preferences
      // ------------------------------------------------------

      await apiClient("/learning/profile", {
        method: "PUT",
        body: JSON.stringify({
          learning_speed: levelToSpeed[level],
          preferred_session_minutes: 30,
        }),
      });

      // ------------------------------------------------------
      // 3. Start diagnostic for selected subject
      // ------------------------------------------------------

      const diagnostic = await apiClient<{
        assessment_id: string;
        attempt_id: string;
        total_items: number;
      }>(
        `/learning/diagnostic/start?learner_subject_id=${encodeURIComponent(
          enrollment.id,
        )}`,
        {
          method: "POST",
        },
      );

      // ------------------------------------------------------
      // 4. Move to assessment
      // ------------------------------------------------------

      const params = new URLSearchParams({
        assessment_id: diagnostic.assessment_id,
        attempt_id: diagnostic.attempt_id,
      });

      window.location.href = `/assessment?${params.toString()}`;
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while creating your learning path.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  const nextStep = async () => {
    if (!canContinue || submitting) {
      return;
    }

    if (step < totalSteps) {
      setStep(step + 1);
      return;
    }

    await createLearningPath();
  };

  const previousStep = () => {
    if (submitting) {
      return;
    }

    if (step > 1) {
      setStep(step - 1);
    }
  };

  // ==========================================================
  // UI
  // ==========================================================

  return (
    <main className="min-h-screen overflow-hidden bg-[#eef4fb] px-3 py-3 sm:px-5 sm:py-5 lg:px-7">
      <div className="relative min-h-[calc(100vh-24px)] overflow-hidden rounded-[28px] border border-white bg-[#f8fbff] shadow-[0_20px_70px_rgba(48,78,125,0.10)]">

        {/* Background decoration */}

        <div className="pointer-events-none absolute -right-32 -top-32 h-[420px] w-[420px] rounded-full bg-[#dce9ff] opacity-60 blur-[100px]" />

        <motion.div
          animate={{
            x: [0, 12, 0],
            y: [0, -8, 0],
          }}
          transition={{
            duration: 7,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="pointer-events-none absolute bottom-[-100px] left-[-100px] h-[350px] w-[350px] rounded-full bg-[#e2edff] blur-[90px]"
        />

        {/* Navbar */}

        <nav className="relative z-20 flex h-[72px] items-center justify-between px-5 sm:px-8 lg:px-10">
          <Link
            href="/"
            className="flex items-center gap-2.5"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#eaf1ff] text-[#3265e8]">
              <Brain size={18} />
            </div>

            <span className="text-[15px] font-bold tracking-tight text-[#172033]">
              LearnFlow
            </span>
          </Link>

          <div className="text-[10px] font-medium text-[#8993a2]">
            Step {step} of {totalSteps}
          </div>
        </nav>

        {/* Progress */}

        <div className="relative z-20 mx-auto mt-4 max-w-[650px] px-6">
          <div className="h-1 overflow-hidden rounded-full bg-[#e4eaf2]">
            <motion.div
              className="h-full rounded-full bg-[#3970e8]"
              animate={{
                width: `${(step / totalSteps) * 100}%`,
              }}
              transition={{
                duration: 0.5,
                ease: "easeInOut",
              }}
            />
          </div>
        </div>

        {/* Main */}

        <div className="relative z-10 mx-auto flex min-h-[calc(100vh-145px)] max-w-[900px] flex-col px-5 pb-10 pt-12 sm:px-8 sm:pt-16">

          <AnimatePresence mode="wait">

            {/* =================================================
                STEP 1 — SUBJECT
            ================================================= */}

            {step === 1 && (
              <motion.div
                key="step-one"
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
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eaf1ff] text-[#3970e8]">
                    <Brain size={22} />
                  </div>

                  <h1 className="mt-6 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                    What do you want to learn?
                  </h1>

                  <p className="mx-auto mt-3 max-w-[480px] text-sm leading-6 text-[#778292]">
                    Pick a subject and we&apos;ll figure out where you
                    actually need to spend your time.
                  </p>
                </div>

                {loadingData ? (
                  <LoadingCards />
                ) : (
                  <div className="mx-auto mt-10 grid max-w-[760px] gap-3 sm:grid-cols-2">
                    {subjects.map((item) => {
                      const Icon =
                        subjectIcons[item.slug] ?? Brain;

                      const selected =
                        subject === item.id;

                      return (
                        <SelectionCard
                          key={item.id}
                          selected={selected}
                          onClick={() =>
                            setSubject(item.id)
                          }
                          icon={<Icon size={19} />}
                          title={item.name}
                          description={
                            item.description ??
                            "Build practical understanding."
                          }
                        />
                      );
                    })}
                  </div>
                )}
              </motion.div>
            )}

            {/* =================================================
                STEP 2 — GOAL
            ================================================= */}

            {step === 2 && (
              <motion.div
                key="step-two"
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
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eaf1ff] text-[#3970e8]">
                    <Target size={22} />
                  </div>

                  <h1 className="mt-6 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                    What&apos;s your goal?
                  </h1>

                  <p className="mx-auto mt-3 max-w-[480px] text-sm leading-6 text-[#778292]">
                    There&apos;s no wrong answer. This helps us understand
                    what &quot;good&quot; looks like for you.
                  </p>
                </div>

                {loadingData ? (
                  <LoadingCards />
                ) : (
                  <div className="mx-auto mt-10 grid max-w-[760px] gap-3 sm:grid-cols-2">
                    {goals.map((item) => {
                      const Icon =
                        goalIcons[item.name.toLowerCase()] ??
                        Target;

                      const selected =
                        goal === item.id;

                      return (
                        <SelectionCard
                          key={item.id}
                          selected={selected}
                          onClick={() =>
                            setGoal(item.id)
                          }
                          icon={<Icon size={19} />}
                          title={item.name}
                          description={
                            item.description ??
                            "Choose the outcome you want."
                          }
                        />
                      );
                    })}
                  </div>
                )}
              </motion.div>
            )}

            {/* =================================================
                STEP 3 — LEVEL
            ================================================= */}

            {step === 3 && (
              <motion.div
                key="step-three"
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
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eaf1ff] text-[#3970e8]">
                    <Sparkles size={22} />
                  </div>

                  <h1 className="mt-6 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                    How much do you already know?
                  </h1>

                  <p className="mx-auto mt-3 max-w-[500px] text-sm leading-6 text-[#778292]">
                    Don&apos;t worry about getting this perfect. We&apos;ll
                    verify your level with a diagnostic assessment next.
                  </p>
                </div>

                <div className="mx-auto mt-10 max-w-[620px] space-y-3">
                  {levels.map((item, index) => {
                    const selected =
                      level === item.id;

                    return (
                      <motion.button
                        key={item.id}
                        type="button"
                        whileHover={{ x: 3 }}
                        whileTap={{
                          scale: 0.99,
                        }}
                        onClick={() =>
                          setLevel(item.id)
                        }
                        className={`relative flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition duration-300 ${
                          selected
                            ? "border-[#76a0f2] bg-[#edf4ff] shadow-[0_10px_30px_rgba(57,112,232,0.10)]"
                            : "border-[#e1e8f1] bg-white hover:border-[#cbd8ec] hover:shadow-md"
                        }`}
                      >
                        <div
                          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
                            selected
                              ? "bg-[#3970e8] text-white"
                              : "bg-[#edf3ff] text-[#3970e8]"
                          }`}
                        >
                          0{index + 1}
                        </div>

                        <div>
                          <h3 className="text-[13px] font-bold text-[#273246]">
                            {item.title}
                          </h3>

                          <p className="mt-1 text-[10px] leading-5 text-[#8490a0]">
                            {item.description}
                          </p>
                        </div>

                        {selected && (
                          <motion.div
                            initial={{
                              scale: 0,
                            }}
                            animate={{
                              scale: 1,
                            }}
                            className="absolute right-4 top-1/2 flex h-5 w-5 -translate-y-1/2 items-center justify-center rounded-full bg-[#3970e8] text-white"
                          >
                            <span className="text-[10px]">
                              ✓
                            </span>
                          </motion.div>
                        )}
                      </motion.button>
                    );
                  })}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error */}

          {error && (
            <motion.div
              initial={{
                opacity: 0,
                y: 8,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              className="mx-auto mt-5 w-full max-w-[760px] rounded-xl border border-[#f0caca] bg-[#fff5f5] px-4 py-3 text-[10px] leading-5 text-[#b34b4b]"
            >
              {error}
            </motion.div>
          )}

          {/* =================================================
              BOTTOM NAVIGATION
          ================================================= */}

          <div className="mx-auto mt-auto flex w-full max-w-[760px] items-center justify-between border-t border-[#e7ecf3] pt-6">

            <button
              type="button"
              onClick={previousStep}
              disabled={
                step === 1 || submitting
              }
              className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-[10px] font-semibold transition ${
                step === 1 || submitting
                  ? "cursor-not-allowed text-[#c2c8d1]"
                  : "text-[#697587] hover:bg-white hover:text-[#3265e8]"
              }`}
            >
              <ArrowLeft size={13} />
              Back
            </button>

            <motion.button
              type="button"
              whileHover={
                canContinue && !submitting
                  ? { y: -2 }
                  : {}
              }
              whileTap={
                canContinue && !submitting
                  ? { scale: 0.98 }
                  : {}
              }
              onClick={nextStep}
              disabled={
                !canContinue ||
                loadingData ||
                submitting
              }
              className={`group flex items-center gap-2 rounded-xl px-5 py-3 text-[10px] font-semibold text-white transition duration-300 ${
                canContinue &&
                !loadingData &&
                !submitting
                  ? "bg-[#121c2c] shadow-[0_8px_20px_rgba(18,28,44,0.15)] hover:shadow-[0_12px_25px_rgba(18,28,44,0.20)]"
                  : "cursor-not-allowed bg-[#cbd2dc]"
              }`}
            >
              {submitting ? (
                <>
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                  Building your path...
                </>
              ) : step === totalSteps ? (
                <>
                  Map my starting point
                  <ArrowRight
                    size={13}
                    className="transition-transform group-hover:translate-x-1"
                  />
                </>
              ) : (
                <>
                  Continue
                  <ArrowRight
                    size={13}
                    className="transition-transform group-hover:translate-x-1"
                  />
                </>
              )}
            </motion.button>
          </div>
        </div>
      </div>
    </main>
  );
}

/* ============================================================
   REUSABLE SELECTION CARD
   ============================================================ */

function SelectionCard({
  selected,
  onClick,
  icon,
  title,
  description,
}: {
  selected: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <motion.button
      type="button"
      whileHover={{ y: -3 }}
      whileTap={{ scale: 0.985 }}
      onClick={onClick}
      className={`relative flex items-center gap-4 rounded-2xl border p-5 text-left transition duration-300 ${
        selected
          ? "border-[#76a0f2] bg-[#edf4ff] shadow-[0_10px_30px_rgba(57,112,232,0.10)]"
          : "border-[#e1e8f1] bg-white hover:border-[#cbd8ec] hover:shadow-md"
      }`}
    >
      <div
        className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition ${
          selected
            ? "bg-[#3970e8] text-white"
            : "bg-[#edf3ff] text-[#3970e8]"
        }`}
      >
        {icon}
      </div>

      <div>
        <h3 className="text-[14px] font-bold text-[#273246]">
          {title}
        </h3>

        <p className="mt-1 text-[11px] leading-5 text-[#8490a0]">
          {description}
        </p>
      </div>

      {selected && (
        <motion.div
          initial={{
            scale: 0,
          }}
          animate={{
            scale: 1,
          }}
          className="absolute right-4 top-4 flex h-5 w-5 items-center justify-center rounded-full bg-[#3970e8] text-white"
        >
          <span className="text-[10px]">✓</span>
        </motion.div>
      )}
    </motion.button>
  );
}

/* ============================================================
   LOADING SKELETON
   ============================================================ */

function LoadingCards() {
  return (
    <div className="mx-auto mt-10 grid max-w-[760px] gap-3 sm:grid-cols-2">
      {[1, 2, 3, 4].map((item) => (
        <motion.div
          key={item}
          animate={{
            opacity: [0.45, 0.8, 0.45],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            delay: item * 0.1,
          }}
          className="h-[96px] rounded-2xl border border-[#e1e8f1] bg-white"
        />
      ))}
    </div>
  );
}