"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  Check,
  Clock3,
  Play,
  Sparkles,
  Target,
  TrendingUp,
} from "lucide-react";
import { useEffect, useState } from "react";

const topics = [
  {
    name: "Python Basics",
    score: 92,
    status: "Strong",
  },
  {
    name: "Data Types",
    score: 84,
    status: "Strong",
  },
  {
    name: "Lists & Tuples",
    score: 71,
    status: "Good",
  },
  {
    name: "Functions",
    score: 43,
    status: "Needs work",
  },
  {
    name: "Object-Oriented Programming",
    score: 24,
    status: "Gap",
  },
];

const recommendations = [
  {
    title: "Functions & Scope",
    description:
      "Strengthen function definitions, parameters, return values and variable scope.",
    duration: "18 min",
    type: "Concept",
  },
  {
    title: "Object-Oriented Programming",
    description:
      "Build your foundation with classes, objects, inheritance and encapsulation.",
    duration: "27 min",
    type: "Concept",
  },
  {
    title: "Practice: Functions",
    description:
      "Apply what you learned through progressively harder coding problems.",
    duration: "15 min",
    type: "Practice",
  },
];

export default function AnalysisPage() {
  const [phase, setPhase] = useState<"analyzing" | "results">("analyzing");
  const [analysisProgress, setAnalysisProgress] = useState(0);

  useEffect(() => {
    const duration = 3000;
    const interval = 30;
    const increment = 100 / (duration / interval);

    const timer = setInterval(() => {
      setAnalysisProgress((previous) => {
        const next = previous + increment;

        if (next >= 100) {
          clearInterval(timer);
          return 100;
        }

        return next;
      });
    }, interval);

    const resultTimer = setTimeout(() => {
      setPhase("results");
    }, 3500);

    return () => {
      clearInterval(timer);
      clearTimeout(resultTimer);
    };
  }, []);

  return (
    <main className="min-h-screen bg-[#eef4fb] px-3 py-3 sm:px-5 sm:py-5 lg:px-7">
      <div className="relative min-h-[calc(100vh-24px)] overflow-hidden rounded-[28px] border border-white bg-[#f8fbff] shadow-[0_20px_70px_rgba(48,78,125,0.10)]">

        {/* =====================================================
            BACKGROUND
        ===================================================== */}

        <div className="pointer-events-none absolute right-[-100px] top-[-100px] h-[430px] w-[430px] rounded-full bg-[#dce9ff] opacity-60 blur-[100px]" />

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
            <Sparkles size={12} className="text-[#3970e8]" />
            AI Knowledge Analysis
          </div>
        </nav>

        {/* =====================================================
            ANALYZING STATE
        ===================================================== */}

        {phase === "analyzing" && (
          <div className="relative z-10 flex min-h-[calc(100vh-95px)] items-center justify-center px-6 pb-10">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="w-full max-w-[560px] text-center"
            >
              {/* Animated brain */}
              <div className="relative mx-auto h-36 w-36">
                <motion.div
                  animate={{
                    scale: [1, 1.05, 1],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="absolute inset-0 rounded-full bg-[#e5efff]"
                />

                <motion.div
                  animate={{
                    rotate: 360,
                  }}
                  transition={{
                    duration: 8,
                    repeat: Infinity,
                    ease: "linear",
                  }}
                  className="absolute inset-2 rounded-full border border-dashed border-[#9ebcf5]"
                />

                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-[#3970e8] shadow-[0_10px_30px_rgba(57,112,232,0.14)]">
                    <Brain size={30} />
                  </div>
                </div>

                {/* orbiting dots */}
                {[0, 1, 2].map((item) => (
                  <motion.span
                    key={item}
                    animate={{
                      rotate: 360,
                    }}
                    transition={{
                      duration: 3 + item,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    className="absolute left-1/2 top-1/2 h-2 w-2 origin-[0_68px] rounded-full bg-[#3970e8]"
                  />
                ))}
              </div>

              <p className="mt-9 text-[10px] font-bold uppercase tracking-[0.18em] text-[#3970e8]">
                AI analysis in progress
              </p>

              <h1 className="mt-3 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                Mapping your knowledge...
              </h1>

              <p className="mx-auto mt-4 max-w-[430px] text-sm leading-6 text-[#778292]">
                We're analyzing your answers to understand what you know,
                where your gaps are, and what you should learn next.
              </p>

              {/* Progress */}
              <div className="mx-auto mt-9 max-w-[430px]">
                <div className="flex items-center justify-between text-[9px] font-semibold text-[#7d8999]">
                  <span>Analyzing responses</span>
                  <span>{Math.round(analysisProgress)}%</span>
                </div>

                <div className="mt-2 h-2 overflow-hidden rounded-full bg-[#e3eaf3]">
                  <motion.div
                    className="h-full rounded-full bg-[#3970e8]"
                    style={{
                      width: `${analysisProgress}%`,
                    }}
                  />
                </div>
              </div>

              {/* Analysis items */}
              <div className="mx-auto mt-8 grid max-w-[430px] grid-cols-3 gap-2">
                {[
                  "Answers",
                  "Knowledge gaps",
                  "Learning path",
                ].map((item, index) => (
                  <motion.div
                    key={item}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{
                      opacity: analysisProgress > index * 28 ? 1 : 0.35,
                      y: 0,
                    }}
                    className="rounded-xl border border-[#e2e9f2] bg-white px-2 py-3"
                  >
                    <div className="mx-auto flex h-6 w-6 items-center justify-center rounded-full bg-[#edf4ff] text-[#3970e8]">
                      {analysisProgress > (index + 1) * 28 ? (
                        <Check size={11} />
                      ) : (
                        <span className="h-1.5 w-1.5 rounded-full bg-[#3970e8]" />
                      )}
                    </div>

                    <p className="mt-2 text-[8px] font-medium text-[#727e8f]">
                      {item}
                    </p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        )}

        {/* =====================================================
            RESULTS
        ===================================================== */}

        {phase === "results" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="relative z-10 mx-auto max-w-[1100px] px-5 pb-12 pt-8 sm:px-8 lg:px-10"
          >
            {/* Header */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-[#eaf1ff] text-[#3970e8]">
                <TrendingUp size={20} />
              </div>

              <p className="mt-5 text-[10px] font-bold uppercase tracking-[0.18em] text-[#3970e8]">
                Your knowledge profile
              </p>

              <h1 className="mt-2 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                Here&apos;s where you stand.
              </h1>

              <p className="mx-auto mt-3 max-w-[500px] text-sm leading-6 text-[#778292]">
                You don't need to relearn everything. We've identified where
                your time will have the biggest impact.
              </p>
            </motion.div>

            {/* =================================================
                SCORE + SUMMARY
            ================================================= */}

            <div className="mt-10 grid gap-4 lg:grid-cols-[0.72fr_1.28fr]">

              {/* Overall score */}

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 }}
                className="rounded-2xl border border-[#e0e8f2] bg-white p-6 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
              >
                <p className="text-[9px] font-bold uppercase tracking-[0.15em] text-[#8a95a4]">
                  Overall mastery
                </p>

                <div className="mt-6 flex items-center justify-center">
                  <div className="relative h-48 w-48">
                    {/* Background ring */}
                    <svg
                      viewBox="0 0 200 200"
                      className="h-full w-full -rotate-90"
                    >
                      <circle
                        cx="100"
                        cy="100"
                        r="78"
                        fill="none"
                        stroke="#e8eef6"
                        strokeWidth="13"
                      />

                      <motion.circle
                        cx="100"
                        cy="100"
                        r="78"
                        fill="none"
                        stroke="#3970e8"
                        strokeWidth="13"
                        strokeLinecap="round"
                        strokeDasharray="490"
                        initial={{
                          strokeDashoffset: 490,
                        }}
                        animate={{
                          strokeDashoffset: 490 - 490 * 0.58,
                        }}
                        transition={{
                          delay: 0.35,
                          duration: 1.6,
                          ease: "easeOut",
                        }}
                      />
                    </svg>

                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <motion.span
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 1 }}
                        className="text-5xl font-bold tracking-[-0.06em] text-[#172033]"
                      >
                        58%
                      </motion.span>

                      <span className="mt-1 text-[9px] font-medium text-[#8b95a3]">
                        current mastery
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-5 rounded-xl bg-[#f4f8fd] p-4">
                  <div className="flex items-center gap-2">
                    <Sparkles size={13} className="text-[#3970e8]" />

                    <p className="text-[10px] font-bold text-[#455164]">
                      Your biggest opportunity
                    </p>
                  </div>

                  <p className="mt-2 text-[11px] leading-5 text-[#7b8797]">
                    Functions and OOP are holding your progress back. Focus
                    there first instead of repeating basic Python concepts.
                  </p>
                </div>
              </motion.div>

              {/* Topic mastery */}

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25 }}
                className="rounded-2xl border border-[#e0e8f2] bg-white p-6 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[9px] font-bold uppercase tracking-[0.15em] text-[#8a95a4]">
                      Topic mastery
                    </p>

                    <h2 className="mt-1 text-lg font-bold tracking-tight text-[#273246]">
                      What you already know
                    </h2>
                  </div>

                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#edf4ff] text-[#3970e8]">
                    <Brain size={17} />
                  </div>
                </div>

                <div className="mt-7 space-y-5">
                  {topics.map((topic, index) => (
                    <div key={topic.name}>
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-semibold text-[#4d596a]">
                          {topic.name}
                        </span>

                        <span
                          className={`text-[9px] font-bold ${
                            topic.score >= 70
                              ? "text-[#3970e8]"
                              : "text-[#d18d31]"
                          }`}
                        >
                          {topic.score}%
                        </span>
                      </div>

                      <div className="mt-2 flex items-center gap-2">
                        <div className="h-2 flex-1 overflow-hidden rounded-full bg-[#e9eef5]">
                          <motion.div
                            initial={{
                              width: 0,
                            }}
                            animate={{
                              width: `${topic.score}%`,
                            }}
                            transition={{
                              delay: 0.5 + index * 0.15,
                              duration: 1,
                              ease: "easeOut",
                            }}
                            className={`h-full rounded-full ${
                              topic.score >= 70
                                ? "bg-[#3970e8]"
                                : topic.score >= 40
                                  ? "bg-[#7ea4ee]"
                                  : "bg-[#e5aa4d]"
                            }`}
                          />
                        </div>

                        <span className="w-[55px] text-right text-[8px] text-[#929ba9]">
                          {topic.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            </div>

            {/* =================================================
                AI RECOMMENDATIONS
            ================================================= */}

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="mt-4"
            >
              <div className="mb-4 flex items-end justify-between">
                <div>
                  <p className="text-[9px] font-bold uppercase tracking-[0.15em] text-[#3970e8]">
                    AI recommendation
                  </p>

                  <h2 className="mt-1 text-xl font-bold tracking-tight text-[#273246]">
                    Here&apos;s what you should learn next.
                  </h2>
                </div>

                <span className="hidden text-[9px] text-[#8a95a4] sm:block">
                  Personalized for you
                </span>
              </div>

              <div className="grid gap-3 md:grid-cols-3">
                {recommendations.map((item, index) => (
                  <motion.div
                    key={item.title}
                    initial={{
                      opacity: 0,
                      y: 20,
                    }}
                    animate={{
                      opacity: 1,
                      y: 0,
                    }}
                    transition={{
                      delay: 0.9 + index * 0.15,
                    }}
                    whileHover={{
                      y: -4,
                    }}
                    className="group rounded-2xl border border-[#e0e8f2] bg-white p-5 shadow-[0_7px_22px_rgba(48,78,125,0.04)] transition-shadow hover:shadow-[0_15px_30px_rgba(48,78,125,0.09)]"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#edf4ff] text-[#3970e8]">
                        {item.type === "Practice" ? (
                          <Target size={16} />
                        ) : (
                          <Play size={16} />
                        )}
                      </div>

                      <span className="rounded-full bg-[#f1f5fa] px-2 py-1 text-[8px] font-semibold text-[#7f8998]">
                        {item.duration}
                      </span>
                    </div>

                    <h3 className="mt-5 text-[14px] font-bold text-[#273246]">
                      {item.title}
                    </h3>

                    <p className="mt-2 text-[10px] leading-5 text-[#7d8898]">
                      {item.description}
                    </p>

                    <div className="mt-5 flex items-center gap-1 text-[9px] font-semibold text-[#3970e8]">
                      Start topic
                      <ArrowRight
                        size={11}
                        className="transition-transform group-hover:translate-x-1"
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* =================================================
                CTA
            ================================================= */}

            <motion.div
              initial={{
                opacity: 0,
                y: 15,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              transition={{
                delay: 1.35,
              }}
              className="mt-7 flex flex-col items-center justify-between gap-4 rounded-2xl border border-[#dce6f3] bg-[#edf4ff] p-5 sm:flex-row"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-[#3970e8] shadow-sm">
                  <Sparkles size={17} />
                </div>

                <div>
                  <p className="text-[11px] font-bold text-[#334054]">
                    Your path is ready.
                  </p>

                  <p className="mt-0.5 text-[9px] text-[#778599]">
                    We&apos;ll prioritize your gaps and skip what you&apos;ve already mastered.
                  </p>
                </div>
              </div>

              <Link
                href="/learning-path"
                className="group flex shrink-0 items-center gap-2 rounded-xl bg-[#121c2c] px-5 py-3 text-[10px] font-semibold text-white shadow-[0_8px_20px_rgba(18,28,44,0.15)] transition hover:-translate-y-0.5"
              >
                Build My Learning Path

                <ArrowRight
                  size={12}
                  className="transition-transform group-hover:translate-x-1"
                />
              </Link>
            </motion.div>
          </motion.div>
        )}
      </div>
    </main>
  );
}