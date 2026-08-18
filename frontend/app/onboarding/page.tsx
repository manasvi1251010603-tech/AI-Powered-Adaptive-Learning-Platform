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
import { useState } from "react";

const subjects = [
  {
    id: "python",
    title: "Python",
    description: "Programming & problem solving",
    icon: Code2,
  },
  {
    id: "sql",
    title: "SQL",
    description: "Databases & data",
    icon: LineChart,
  },
  {
    id: "machine-learning",
    title: "Machine Learning",
    description: "Models & intelligent systems",
    icon: Brain,
  },
  {
    id: "data-science",
    title: "Data Science",
    description: "Data, statistics & insights",
    icon: Sparkles,
  },
];

const goals = [
  {
    id: "academics",
    title: "Ace my academics",
    description: "Understand concepts and perform better in college.",
    icon: GraduationCap,
  },
  {
    id: "projects",
    title: "Build projects",
    description: "Learn enough to actually create things.",
    icon: Rocket,
  },
  {
    id: "career",
    title: "Prepare for my career",
    description: "Build practical skills for internships and jobs.",
    icon: BriefcaseBusiness,
  },
  {
    id: "mastery",
    title: "Master the subject",
    description: "Go beyond the basics and build deep understanding.",
    icon: Target,
  },
];

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

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [subject, setSubject] = useState("");
  const [goal, setGoal] = useState("");
  const [level, setLevel] = useState("");

  const totalSteps = 3;

  const canContinue =
    step === 1 ? !!subject : step === 2 ? !!goal : !!level;

  const nextStep = () => {
    if (!canContinue) return;

    if (step < totalSteps) {
      setStep(step + 1);
    }
  };

  const previousStep = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

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
          <Link href="/" className="flex items-center gap-2.5">
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
                STEP 1
            ================================================= */}
            {step === 1 && (
              <motion.div
                key="step-one"
                initial={{ opacity: 0, x: 25 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -25 }}
                transition={{ duration: 0.35 }}
              >
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eaf1ff] text-[#3970e8]">
                    <Brain size={22} />
                  </div>

                  <h1 className="mt-6 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                    What do you want to learn?
                  </h1>

                  <p className="mx-auto mt-3 max-w-[480px] text-sm leading-6 text-[#778292]">
                    Pick a subject and we'll figure out where you actually
                    need to spend your time.
                  </p>
                </div>

                <div className="mx-auto mt-10 grid max-w-[760px] gap-3 sm:grid-cols-2">
                  {subjects.map((item) => {
                    const Icon = item.icon;
                    const selected = subject === item.id;

                    return (
                      <motion.button
                        key={item.id}
                        type="button"
                        whileHover={{ y: -3 }}
                        whileTap={{ scale: 0.985 }}
                        onClick={() => setSubject(item.id)}
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
                          <Icon size={19} />
                        </div>

                        <div>
                          <h3 className="text-[14px] font-bold text-[#273246]">
                            {item.title}
                          </h3>

                          <p className="mt-1 text-[11px] leading-5 text-[#8490a0]">
                            {item.description}
                          </p>
                        </div>

                        {selected && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="absolute right-4 top-4 flex h-5 w-5 items-center justify-center rounded-full bg-[#3970e8] text-white"
                          >
                            <span className="text-[10px]">✓</span>
                          </motion.div>
                        )}
                      </motion.button>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {/* =================================================
                STEP 2
            ================================================= */}
            {step === 2 && (
              <motion.div
                key="step-two"
                initial={{ opacity: 0, x: 25 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -25 }}
                transition={{ duration: 0.35 }}
              >
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eaf1ff] text-[#3970e8]">
                    <Target size={22} />
                  </div>

                  <h1 className="mt-6 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                    What's your goal?
                  </h1>

                  <p className="mx-auto mt-3 max-w-[480px] text-sm leading-6 text-[#778292]">
                    There's no wrong answer. This helps us understand what
                    "good" looks like for you.
                  </p>
                </div>

                <div className="mx-auto mt-10 grid max-w-[760px] gap-3 sm:grid-cols-2">
                  {goals.map((item) => {
                    const Icon = item.icon;
                    const selected = goal === item.id;

                    return (
                      <motion.button
                        key={item.id}
                        type="button"
                        whileHover={{ y: -3 }}
                        whileTap={{ scale: 0.985 }}
                        onClick={() => setGoal(item.id)}
                        className={`relative flex items-center gap-4 rounded-2xl border p-5 text-left transition duration-300 ${
                          selected
                            ? "border-[#76a0f2] bg-[#edf4ff] shadow-[0_10px_30px_rgba(57,112,232,0.10)]"
                            : "border-[#e1e8f1] bg-white hover:border-[#cbd8ec] hover:shadow-md"
                        }`}
                      >
                        <div
                          className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${
                            selected
                              ? "bg-[#3970e8] text-white"
                              : "bg-[#edf3ff] text-[#3970e8]"
                          }`}
                        >
                          <Icon size={19} />
                        </div>

                        <div>
                          <h3 className="text-[14px] font-bold text-[#273246]">
                            {item.title}
                          </h3>

                          <p className="mt-1 text-[11px] leading-5 text-[#8490a0]">
                            {item.description}
                          </p>
                        </div>

                        {selected && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="absolute right-4 top-4 flex h-5 w-5 items-center justify-center rounded-full bg-[#3970e8] text-white"
                          >
                            <span className="text-[10px]">✓</span>
                          </motion.div>
                        )}
                      </motion.button>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {/* =================================================
                STEP 3
            ================================================= */}
            {step === 3 && (
              <motion.div
                key="step-three"
                initial={{ opacity: 0, x: 25 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -25 }}
                transition={{ duration: 0.35 }}
              >
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eaf1ff] text-[#3970e8]">
                    <Sparkles size={22} />
                  </div>

                  <h1 className="mt-6 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                    How much do you already know?
                  </h1>

                  <p className="mx-auto mt-3 max-w-[500px] text-sm leading-6 text-[#778292]">
                    Don't worry about getting this perfect. We'll verify your
                    level with a diagnostic assessment next.
                  </p>
                </div>

                <div className="mx-auto mt-10 max-w-[620px] space-y-3">
                  {levels.map((item, index) => {
                    const selected = level === item.id;

                    return (
                      <motion.button
                        key={item.id}
                        type="button"
                        whileHover={{ x: 3 }}
                        whileTap={{ scale: 0.99 }}
                        onClick={() => setLevel(item.id)}
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
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="absolute right-4 top-1/2 flex h-5 w-5 -translate-y-1/2 items-center justify-center rounded-full bg-[#3970e8] text-white"
                          >
                            <span className="text-[10px]">✓</span>
                          </motion.div>
                        )}
                      </motion.button>
                    );
                  })}
                </div>
              </motion.div>
            )}

          </AnimatePresence>

          {/* Bottom navigation */}
          <div className="mx-auto mt-auto flex w-full max-w-[760px] items-center justify-between border-t border-[#e7ecf3] pt-6">
            <button
              type="button"
              onClick={previousStep}
              disabled={step === 1}
              className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-[10px] font-semibold transition ${
                step === 1
                  ? "cursor-not-allowed text-[#c2c8d1]"
                  : "text-[#697587] hover:bg-white hover:text-[#3265e8]"
              }`}
            >
              <ArrowLeft size={13} />
              Back
            </button>

            <motion.button
              type="button"
              whileHover={canContinue ? { y: -2 } : {}}
              whileTap={canContinue ? { scale: 0.98 } : {}}
              onClick={nextStep}
              disabled={!canContinue}
              className={`group flex items-center gap-2 rounded-xl px-5 py-3 text-[10px] font-semibold text-white transition duration-300 ${
                canContinue
                  ? "bg-[#121c2c] shadow-[0_8px_20px_rgba(18,28,44,0.15)] hover:shadow-[0_12px_25px_rgba(18,28,44,0.20)]"
                  : "cursor-not-allowed bg-[#cbd2dc]"
              }`}
            >
              {step === totalSteps ? "Create My Learning Path" : "Continue"}

              <ArrowRight
                size={13}
                className={
                  canContinue
                    ? "transition-transform group-hover:translate-x-1"
                    : ""
                }
              />
            </motion.button>
          </div>
        </div>
      </div>
    </main>
  );
}