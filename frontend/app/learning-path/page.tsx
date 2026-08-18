"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  Check,
  ChevronDown,
  Clock3,
  Play,
  Sparkles,
  Target,
  Trophy,
  Zap,
} from "lucide-react";
import { useState } from "react";

const modules = [
  {
    id: 1,
    title: "Python Basics",
    subtitle: "Variables, data types & syntax",
    mastery: 92,
    status: "mastered",
    time: "Already know this",
  },
  {
    id: 2,
    title: "Lists & Tuples",
    subtitle: "Collections, indexing & operations",
    mastery: 71,
    status: "review",
    time: "15 min review",
  },
  {
    id: 3,
    title: "Functions & Scope",
    subtitle: "Functions, parameters, return values",
    mastery: 43,
    status: "priority",
    time: "45 min",
  },
  {
    id: 4,
    title: "Object-Oriented Programming",
    subtitle: "Classes, objects & inheritance",
    mastery: 24,
    status: "priority",
    time: "60 min",
  },
  {
    id: 5,
    title: "Error Handling",
    subtitle: "Exceptions & defensive programming",
    mastery: 31,
    status: "upcoming",
    time: "30 min",
  },
];

const resources = [
  {
    type: "VIDEO",
    title: "Python Functions — Complete Guide",
    source: "YouTube",
    duration: "18 min",
    timestamps: "3 relevant sections",
  },
  {
    type: "VIDEO",
    title: "Object-Oriented Python",
    source: "YouTube",
    duration: "27 min",
    timestamps: "5 relevant sections",
  },
  {
    type: "PRACTICE",
    title: "Functions Coding Challenge",
    source: "LearnFlow",
    duration: "15 min",
    timestamps: "12 questions",
  },
];

export default function LearningPathPage() {
  const [expanded, setExpanded] = useState<number | null>(3);

  return (
    <main className="min-h-screen bg-[#eef4fb] px-3 py-3 sm:px-5 sm:py-5 lg:px-7">
      <div className="relative min-h-[calc(100vh-24px)] overflow-hidden rounded-[28px] border border-white bg-[#f8fbff] shadow-[0_20px_70px_rgba(48,78,125,0.10)]">

        {/* Background */}
        <div className="pointer-events-none absolute right-[-120px] top-[-120px] h-[430px] w-[430px] rounded-full bg-[#dce9ff] opacity-60 blur-[100px]" />

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

        <nav className="relative z-20 flex h-[72px] items-center justify-between border-b border-[#e6ecf4] px-5 sm:px-8 lg:px-10">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#eaf1ff] text-[#3265e8]">
              <Brain size={18} />
            </div>

            <span className="text-[15px] font-bold tracking-tight text-[#172033]">
              LearnFlow
            </span>
          </Link>

          <div className="hidden items-center gap-7 text-[10px] font-medium text-[#687486] sm:flex">
            <span className="text-[#3970e8]">My Path</span>
            <span>Progress</span>
            <span>Resources</span>
          </div>

          <div className="flex items-center gap-2 rounded-xl border border-[#e1e8f1] bg-white px-3 py-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-[#edf4ff] text-[#3970e8]">
              <Trophy size={12} />
            </div>

            <div className="hidden sm:block">
              <p className="text-[8px] font-bold text-[#485365]">
                58% mastery
              </p>
              <p className="text-[7px] text-[#98a0ad]">
                Python
              </p>
            </div>
          </div>
        </nav>

        {/* =====================================================
            CONTENT
        ===================================================== */}

        <div className="relative z-10 mx-auto max-w-[1120px] px-5 pb-12 pt-8 sm:px-8 lg:px-10">

          {/* Header */}

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"
          >
            <div>
              <div className="flex items-center gap-2 text-[9px] font-bold uppercase tracking-[0.16em] text-[#3970e8]">
                <Sparkles size={12} />
                AI-generated learning path
              </div>

              <h1 className="mt-2 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                Your path to Python mastery.
              </h1>

              <p className="mt-3 max-w-[560px] text-sm leading-6 text-[#778292]">
                We&apos;ve skipped what you already know and prioritized the
                concepts that will move you forward fastest.
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-xl border border-[#dfe7f1] bg-white px-4 py-3">
              <Clock3 size={14} className="text-[#3970e8]" />

              <div>
                <p className="text-[9px] font-bold text-[#4b5667]">
                  Estimated learning time
                </p>

                <p className="mt-0.5 text-[11px] font-semibold text-[#3970e8]">
                  ~2h 45m
                </p>
              </div>
            </div>
          </motion.div>

          {/* ===================================================
              PATH + SIDEBAR
          =================================================== */}

          <div className="mt-9 grid gap-5 lg:grid-cols-[1.4fr_0.6fr]">

            {/* ================= PATH ================= */}

            <div className="relative rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)] sm:p-7">

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[9px] font-bold uppercase tracking-[0.14em] text-[#8b95a4]">
                    Learning sequence
                  </p>

                  <h2 className="mt-1 text-lg font-bold text-[#273246]">
                    Your adaptive path
                  </h2>
                </div>

                <div className="flex items-center gap-2 rounded-full bg-[#edf4ff] px-3 py-1.5 text-[8px] font-semibold text-[#3970e8]">
                  <Zap size={10} />
                  AI optimized
                </div>
              </div>

              {/* Vertical line */}

              <div className="relative mt-8">

                <div className="absolute bottom-8 left-[19px] top-8 w-px bg-[#dce5f0]" />

                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: "58%" }}
                  transition={{
                    delay: 0.5,
                    duration: 1.2,
                    ease: "easeOut",
                  }}
                  className="absolute left-[19px] top-8 w-px bg-[#3970e8]"
                />

                <div className="space-y-3">
                  {modules.map((module, index) => {
                    const isExpanded = expanded === module.id;
                    const mastered = module.status === "mastered";
                    const priority = module.status === "priority";

                    return (
                      <motion.div
                        key={module.id}
                        initial={{ opacity: 0, x: -15 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{
                          delay: 0.15 + index * 0.1,
                        }}
                        className="relative pl-11"
                      >
                        {/* Node */}

                        <div
                          className={`absolute left-0 top-4 z-10 flex h-10 w-10 items-center justify-center rounded-full border-4 border-white ${
                            mastered
                              ? "bg-[#53ad8d] text-white"
                              : priority
                                ? "bg-[#3970e8] text-white shadow-[0_0_0_5px_rgba(57,112,232,0.10)]"
                                : "bg-[#eaf1ff] text-[#3970e8]"
                          }`}
                        >
                          {mastered ? (
                            <Check size={15} />
                          ) : (
                            <span className="text-[10px] font-bold">
                              {module.id}
                            </span>
                          )}
                        </div>

                        <button
                          type="button"
                          onClick={() =>
                            setExpanded(isExpanded ? null : module.id)
                          }
                          className={`w-full rounded-2xl border p-4 text-left transition duration-300 ${
                            priority
                              ? "border-[#bfd2f4] bg-[#f7faff]"
                              : "border-[#e5ebf3] bg-white"
                          } hover:shadow-md`}
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div>
                              <div className="flex flex-wrap items-center gap-2">
                                <h3 className="text-[13px] font-bold text-[#293448]">
                                  {module.title}
                                </h3>

                                {mastered && (
                                  <span className="rounded-full bg-[#eaf7f2] px-2 py-1 text-[7px] font-bold text-[#3c9878]">
                                    MASTERED
                                  </span>
                                )}

                                {priority && (
                                  <span className="rounded-full bg-[#edf4ff] px-2 py-1 text-[7px] font-bold text-[#3970e8]">
                                    PRIORITY
                                  </span>
                                )}
                              </div>

                              <p className="mt-1 text-[9px] text-[#8993a1]">
                                {module.subtitle}
                              </p>
                            </div>

                            <ChevronDown
                              size={14}
                              className={`shrink-0 text-[#9ca6b4] transition-transform ${
                                isExpanded ? "rotate-180" : ""
                              }`}
                            />
                          </div>

                          <div className="mt-4 flex items-center gap-3">
                            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-[#e8edf4]">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{
                                  width: `${module.mastery}%`,
                                }}
                                transition={{
                                  delay: 0.6 + index * 0.1,
                                  duration: 0.8,
                                }}
                                className={`h-full rounded-full ${
                                  mastered
                                    ? "bg-[#53ad8d]"
                                    : priority
                                      ? "bg-[#3970e8]"
                                      : "bg-[#86a9ed]"
                                }`}
                              />
                            </div>

                            <span className="w-[30px] text-right text-[8px] font-bold text-[#6e7a8b]">
                              {module.mastery}%
                            </span>

                            <span className="w-[70px] text-right text-[8px] text-[#929baa]">
                              {module.time}
                            </span>
                          </div>

                          {/* Expanded section */}

                          {isExpanded && (
                            <motion.div
                              initial={{
                                opacity: 0,
                                height: 0,
                              }}
                              animate={{
                                opacity: 1,
                                height: "auto",
                              }}
                              className="overflow-hidden"
                            >
                              <div className="mt-4 border-t border-[#e8edf3] pt-4">
                                {mastered ? (
                                  <div className="flex items-center gap-2 rounded-xl bg-[#f1faf6] px-3 py-3">
                                    <Check
                                      size={13}
                                      className="text-[#3c9878]"
                                    />

                                    <p className="text-[9px] leading-5 text-[#668476]">
                                      You already understand this well. LearnFlow
                                      will skip the full lesson and only bring
                                      it back if a future assessment shows a gap.
                                    </p>
                                  </div>
                                ) : (
                                  <div>
                                    <p className="text-[9px] font-semibold text-[#526071]">
                                      What you&apos;ll learn
                                    </p>

                                    <div className="mt-2 flex flex-wrap gap-2">
                                      {[
                                        "Core concepts",
                                        "Examples",
                                        "Practice",
                                        "Assessment",
                                      ].map((tag) => (
                                        <span
                                          key={tag}
                                          className="rounded-lg bg-[#f2f6fb] px-2.5 py-1.5 text-[8px] font-medium text-[#748092]"
                                        >
                                          {tag}
                                        </span>
                                      ))}
                                    </div>

                                    <Link
                                      href="/learn"
                                      className="mt-4 inline-flex items-center gap-1.5 text-[9px] font-bold text-[#3970e8]"
                                    >
                                      Start this module
                                      <ArrowRight size={11} />
                                    </Link>
                                  </div>
                                )}
                              </div>
                            </motion.div>
                          )}
                        </button>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* ================= SIDEBAR ================= */}

            <div className="space-y-4">

              {/* AI summary */}

              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35 }}
                className="rounded-2xl border border-[#d9e5f5] bg-[#edf4ff] p-5"
              >
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-[#3970e8]">
                    <Sparkles size={14} />
                  </div>

                  <p className="text-[10px] font-bold text-[#344054]">
                    AI says
                  </p>
                </div>

                <p className="mt-4 text-[11px] leading-6 text-[#637186]">
                  You&apos;re strong on Python fundamentals. Don&apos;t spend
                  another hour watching beginner tutorials. Your biggest gains
                  will come from functions and OOP.
                </p>
              </motion.div>

              {/* Progress */}

              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.45 }}
                className="rounded-2xl border border-[#e0e8f2] bg-white p-5"
              >
                <p className="text-[9px] font-bold uppercase tracking-[0.14em] text-[#8b95a4]">
                  Path progress
                </p>

                <div className="mt-4 flex items-end justify-between">
                  <div>
                    <p className="text-3xl font-bold tracking-[-0.05em] text-[#172033]">
                      28%
                    </p>

                    <p className="mt-1 text-[9px] text-[#8c96a4]">
                      of personalized path
                    </p>
                  </div>

                  <div className="text-right">
                    <p className="text-[9px] font-semibold text-[#3970e8]">
                      2 / 5
                    </p>

                    <p className="text-[8px] text-[#929baa]">
                      modules
                    </p>
                  </div>
                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-[#e8edf4]">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: "28%" }}
                    transition={{ delay: 0.7, duration: 1 }}
                    className="h-full rounded-full bg-[#3970e8]"
                  />
                </div>
              </motion.div>

              {/* Resources */}

              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.55 }}
                className="rounded-2xl border border-[#e0e8f2] bg-white p-5"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[9px] font-bold uppercase tracking-[0.14em] text-[#8b95a4]">
                      Recommended now
                    </p>

                    <h3 className="mt-1 text-[13px] font-bold text-[#344054]">
                      Focus resources
                    </h3>
                  </div>

                  <span className="rounded-full bg-[#edf4ff] px-2 py-1 text-[7px] font-bold text-[#3970e8]">
                    AI PICK
                  </span>
                </div>

                <div className="mt-4 space-y-3">
                  {resources.map((resource) => (
                    <div
                      key={resource.title}
                      className="rounded-xl border border-[#e8edf3] p-3 transition hover:border-[#cad8ed] hover:bg-[#fbfcfe]"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-[7px] font-bold text-[#3970e8]">
                          {resource.type}
                        </span>

                        <span className="text-[7px] text-[#929baa]">
                          {resource.duration}
                        </span>
                      </div>

                      <p className="mt-2 text-[9px] font-semibold leading-4 text-[#465164]">
                        {resource.title}
                      </p>

                      <div className="mt-2 flex items-center justify-between">
                        <span className="text-[7px] text-[#9aa2ae]">
                          {resource.source}
                        </span>

                        <span className="text-[7px] font-medium text-[#3970e8]">
                          {resource.timestamps}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>

                <Link
                  href="/learn"
                  className="mt-4 flex h-9 items-center justify-center gap-2 rounded-xl bg-[#121c2c] text-[9px] font-semibold text-white transition hover:-translate-y-0.5"
                >
                  Continue learning
                  <ArrowRight size={11} />
                </Link>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}