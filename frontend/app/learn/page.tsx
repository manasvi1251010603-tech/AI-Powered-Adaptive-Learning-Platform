"use client";

import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  Check,
  ChevronRight,
  Clock3,
  Lightbulb,
  Play,
  RotateCcw,
  Sparkles,
  Target,
  X,
} from "lucide-react";
import { useState } from "react";

const timestamps = [
  {
    id: 1,
    time: "02:14",
    seconds: 134,
    title: "What is a function?",
    description: "Understand why functions exist and when to use them.",
    relevance: "Core concept",
  },
  {
    id: 2,
    time: "06:38",
    seconds: 398,
    title: "Parameters & arguments",
    description: "Learn how information moves into a function.",
    relevance: "Your knowledge gap",
  },
  {
    id: 3,
    time: "11:52",
    seconds: 712,
    title: "Return values",
    description: "Understand how functions produce and return results.",
    relevance: "Your knowledge gap",
  },
  {
    id: 4,
    time: "15:47",
    seconds: 947,
    title: "Common mistakes",
    description: "Avoid the mistakes beginners commonly make.",
    relevance: "Practice",
  },
];

const practiceQuestions = [
  {
    question: "Which keyword is used to define a function in Python?",
    options: ["function", "def", "define", "func"],
    answer: 1,
  },
  {
    question: "What does a return statement do?",
    options: [
      "Stops Python completely",
      "Prints a value",
      "Sends a value back from a function",
      "Creates a variable",
    ],
    answer: 2,
  },
];

export default function LearnPage() {
  const [activeTimestamp, setActiveTimestamp] = useState(1);
  const [videoPlaying, setVideoPlaying] = useState(false);
  const [showPractice, setShowPractice] = useState(false);
  const [practiceQuestion, setPracticeQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [practiceComplete, setPracticeComplete] = useState(false);

  const currentTimestamp = timestamps.find(
    (item) => item.id === activeTimestamp,
  );

  const currentPractice = practiceQuestions[practiceQuestion];

  const handleTimestamp = (id: number) => {
    setActiveTimestamp(id);
    setVideoPlaying(true);

    // Later this will control the actual YouTube player.
    console.log("Jump to timestamp:", id);
  };

  const submitPractice = () => {
    if (selectedAnswer === null) return;

    if (practiceQuestion < practiceQuestions.length - 1) {
      setPracticeQuestion((previous) => previous + 1);
      setSelectedAnswer(null);
    } else {
      setPracticeComplete(true);
    }
  };

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
            <Link href="/learning-path" className="hover:text-[#3970e8]">
              My Path
            </Link>

            <span className="font-semibold text-[#3970e8]">
              Learn
            </span>

            <span>Progress</span>
          </div>

          <div className="flex items-center gap-2 rounded-xl border border-[#e1e8f1] bg-white px-3 py-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-[#edf4ff] text-[#3970e8]">
              <Target size={12} />
            </div>

            <div className="hidden sm:block">
              <p className="text-[8px] font-bold text-[#485365]">
                Functions & Scope
              </p>

              <p className="text-[7px] text-[#98a0ad]">
                43% mastery
              </p>
            </div>
          </div>
        </nav>

        {/* =====================================================
            CONTENT
        ===================================================== */}

        <div className="relative z-10 mx-auto max-w-[1180px] px-5 pb-12 pt-7 sm:px-8 lg:px-10">

          {/* Back */}

          <Link
            href="/learning-path"
            className="inline-flex items-center gap-1.5 text-[9px] font-semibold text-[#7d8898] transition hover:text-[#3970e8]"
          >
            <ArrowLeft size={12} />
            Back to your learning path
          </Link>

          {/* Header */}

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55 }}
            className="mt-6"
          >
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full bg-[#edf4ff] px-3 py-1.5 text-[8px] font-bold text-[#3970e8]">
                PRIORITY TOPIC
              </span>

              <span className="text-[9px] text-[#929baa]">
                Module 3 of 5
              </span>
            </div>

            <h1 className="mt-3 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
              Functions & Scope
            </h1>

            <p className="mt-2 max-w-[600px] text-[13px] leading-6 text-[#778292]">
              Learn the parts of functions you haven&apos;t mastered yet.
              We&apos;ll skip the basics you already understand.
            </p>
          </motion.div>

          {/* ===================================================
              MAIN GRID
          =================================================== */}

          <div className="mt-7 grid gap-5 lg:grid-cols-[1.55fr_0.7fr]">

            {/* =================================================
                LEFT COLUMN
            ================================================= */}

            <div className="space-y-5">

              {/* VIDEO */}

              <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1, duration: 0.55 }}
                className="overflow-hidden rounded-2xl border border-[#dfe7f1] bg-[#111b2a] shadow-[0_12px_35px_rgba(25,42,67,0.12)]"
              >

                {/* Video area */}

                <div className="relative aspect-video overflow-hidden bg-[#142237]">

                  {/* abstract video background */}

                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_40%,rgba(85,139,235,0.18),transparent_35%),radial-gradient(circle_at_80%_60%,rgba(70,116,210,0.15),transparent_30%)]" />

                  <div className="absolute inset-0 flex items-center justify-center">

                    <motion.div
                      animate={{
                        scale: videoPlaying ? [1, 1.04, 1] : 1,
                      }}
                      transition={{
                        duration: 2,
                        repeat: videoPlaying ? Infinity : 0,
                      }}
                      className="flex h-20 w-20 items-center justify-center rounded-full border border-white/20 bg-white/10 text-white backdrop-blur"
                    >
                      <Play
                        size={29}
                        fill="currentColor"
                        className="ml-1"
                      />
                    </motion.div>
                  </div>

                  {/* AI selected section */}

                  <div className="absolute left-4 top-4 flex items-center gap-2 rounded-xl border border-white/10 bg-[#17263b]/85 px-3 py-2 backdrop-blur">
                    <Sparkles size={12} className="text-[#8db4ff]" />

                    <div>
                      <p className="text-[8px] font-bold text-white">
                        AI-selected section
                      </p>

                      <p className="text-[7px] text-[#aebbd0]">
                        {currentTimestamp?.title}
                      </p>
                    </div>
                  </div>

                  {/* video controls */}

                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-[#0c1522] via-[#0c1522]/80 to-transparent px-4 pb-4 pt-12">

                    <div className="mb-3 h-1 overflow-hidden rounded-full bg-white/15">
                      <motion.div
                        animate={{
                          width: videoPlaying ? ["18%", "38%"] : "18%",
                        }}
                        transition={{
                          duration: 5,
                          repeat: videoPlaying ? Infinity : 0,
                          ease: "linear",
                        }}
                        className="h-full rounded-full bg-[#76a5fa]"
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <button
                          type="button"
                          onClick={() => setVideoPlaying(!videoPlaying)}
                          className="text-white transition hover:text-[#8db4ff]"
                        >
                          {videoPlaying ? (
                            <span className="text-[12px]">Ⅱ</span>
                          ) : (
                            <Play size={14} fill="currentColor" />
                          )}
                        </button>

                        <span className="text-[8px] text-[#c4cedd]">
                          {currentTimestamp?.time}
                        </span>
                      </div>

                      <span className="text-[8px] text-[#9caabd]">
                        18:42
                      </span>
                    </div>
                  </div>
                </div>

                {/* Video info */}

                <div className="border-t border-white/5 bg-[#111b2a] px-5 py-4">
                  <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                    <div>
                      <p className="text-[11px] font-bold text-white">
                        Python Functions — Complete Guide
                      </p>

                      <p className="mt-1 text-[8px] text-[#8897ad]">
                        Selected specifically for your current knowledge gaps.
                      </p>
                    </div>

                    <div className="flex items-center gap-2 text-[8px] text-[#8c9ab0]">
                      <Clock3 size={11} />
                      18 min
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* =================================================
                  TIMESTAMPS
              ================================================= */}

              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25 }}
                className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)] sm:p-6"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <Sparkles
                        size={14}
                        className="text-[#3970e8]"
                      />

                      <p className="text-[10px] font-bold uppercase tracking-[0.13em] text-[#3970e8]">
                        AI timestamp map
                      </p>
                    </div>

                    <h2 className="mt-2 text-lg font-bold text-[#273246]">
                      You only need these sections.
                    </h2>

                    <p className="mt-1 text-[10px] leading-5 text-[#8993a1]">
                      We found the parts of this video that match your
                      knowledge gaps.
                    </p>
                  </div>

                  <span className="hidden rounded-full bg-[#edf4ff] px-3 py-1.5 text-[8px] font-bold text-[#3970e8] sm:block">
                    4 relevant sections
                  </span>
                </div>

                <div className="mt-5 space-y-2">
                  {timestamps.map((item, index) => {
                    const active = activeTimestamp === item.id;

                    return (
                      <motion.button
                        key={item.id}
                        type="button"
                        whileHover={{ x: 3 }}
                        onClick={() => handleTimestamp(item.id)}
                        className={`group relative flex w-full items-center gap-3 rounded-xl border p-3 text-left transition duration-300 ${
                          active
                            ? "border-[#a9c3f5] bg-[#edf4ff]"
                            : "border-[#e7ecf2] bg-white hover:border-[#cbd9ed] hover:bg-[#fbfcfe]"
                        }`}
                      >
                        <div
                          className={`flex h-9 w-12 shrink-0 items-center justify-center rounded-lg text-[9px] font-bold ${
                            active
                              ? "bg-[#3970e8] text-white"
                              : "bg-[#eef3f9] text-[#687689]"
                          }`}
                        >
                          {item.time}
                        </div>

                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <p className="text-[10px] font-bold text-[#455164]">
                              {item.title}
                            </p>

                            {index === 1 || index === 2 ? (
                              <span className="rounded-full bg-[#eaf7f2] px-2 py-0.5 text-[6px] font-bold text-[#3d9878]">
                                YOUR GAP
                              </span>
                            ) : null}
                          </div>

                          <p className="mt-1 truncate text-[8px] text-[#929baa]">
                            {item.description}
                          </p>
                        </div>

                        <ChevronRight
                          size={13}
                          className={`shrink-0 transition-transform ${
                            active
                              ? "translate-x-0.5 text-[#3970e8]"
                              : "text-[#a4acb7] group-hover:translate-x-0.5"
                          }`}
                        />
                      </motion.button>
                    );
                  })}
                </div>

                {/* AI explanation */}

                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeTimestamp}
                    initial={{
                      opacity: 0,
                      y: 6,
                    }}
                    animate={{
                      opacity: 1,
                      y: 0,
                    }}
                    className="mt-4 flex gap-3 rounded-xl bg-[#f4f8fd] p-4"
                  >
                    <Lightbulb
                      size={15}
                      className="mt-0.5 shrink-0 text-[#3970e8]"
                    />

                    <div>
                      <p className="text-[9px] font-bold text-[#4d596a]">
                        Why this section?
                      </p>

                      <p className="mt-1 text-[9px] leading-5 text-[#7c8797]">
                        This section was selected because it directly covers{" "}
                        <strong className="text-[#536174]">
                          {currentTimestamp?.title.toLowerCase()}
                        </strong>
                        , which is part of your current knowledge gap.
                      </p>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </motion.div>

              {/* =================================================
                  PRACTICE
              ================================================= */}

              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35 }}
                className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)] sm:p-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <Target
                        size={14}
                        className="text-[#3970e8]"
                      />

                      <p className="text-[10px] font-bold uppercase tracking-[0.13em] text-[#3970e8]">
                        Quick practice
                      </p>
                    </div>

                    <h2 className="mt-2 text-lg font-bold text-[#273246]">
                      Make sure it actually sticks.
                    </h2>
                  </div>

                  <span className="text-[8px] text-[#929baa]">
                    2 questions
                  </span>
                </div>

                {!showPractice && !practiceComplete && (
                  <div className="mt-5 flex flex-col items-center justify-between gap-4 rounded-xl bg-[#f4f8fd] p-4 sm:flex-row">
                    <p className="max-w-[470px] text-[9px] leading-5 text-[#7d8999]">
                      Test your understanding before moving to the next
                      concept. Your answers will help LearnFlow update your
                      mastery score.
                    </p>

                    <button
                      type="button"
                      onClick={() => setShowPractice(true)}
                      className="flex shrink-0 items-center gap-2 rounded-xl bg-[#121c2c] px-4 py-2.5 text-[9px] font-semibold text-white transition hover:-translate-y-0.5"
                    >
                      Start practice
                      <ArrowRight size={11} />
                    </button>
                  </div>
                )}

                {showPractice && !practiceComplete && (
                  <motion.div
                    initial={{
                      opacity: 0,
                      y: 10,
                    }}
                    animate={{
                      opacity: 1,
                      y: 0,
                    }}
                    className="mt-5"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[8px] font-bold text-[#3970e8]">
                        Question {practiceQuestion + 1} /{" "}
                        {practiceQuestions.length}
                      </span>

                      <span className="text-[8px] text-[#929baa]">
                        Practice
                      </span>
                    </div>

                    <h3 className="mt-3 text-[13px] font-bold leading-5 text-[#3c485a]">
                      {currentPractice.question}
                    </h3>

                    <div className="mt-4 space-y-2">
                      {currentPractice.options.map((option, index) => {
                        const selected = selectedAnswer === index;

                        return (
                          <button
                            key={option}
                            type="button"
                            onClick={() => setSelectedAnswer(index)}
                            className={`flex w-full items-center gap-3 rounded-xl border p-3 text-left text-[9px] transition ${
                              selected
                                ? "border-[#8aabeb] bg-[#edf4ff] text-[#3970e8]"
                                : "border-[#e5ebf2] bg-white text-[#687486] hover:border-[#cbd8eb]"
                            }`}
                          >
                            <span
                              className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-lg text-[8px] font-bold ${
                                selected
                                  ? "bg-[#3970e8] text-white"
                                  : "bg-[#eef3f9] text-[#7b8796]"
                              }`}
                            >
                              {String.fromCharCode(65 + index)}
                            </span>

                            {option}
                          </button>
                        );
                      })}
                    </div>

                    <div className="mt-4 flex justify-end">
                      <button
                        type="button"
                        disabled={selectedAnswer === null}
                        onClick={submitPractice}
                        className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-[9px] font-semibold text-white ${
                          selectedAnswer !== null
                            ? "bg-[#121c2c]"
                            : "cursor-not-allowed bg-[#cbd2dc]"
                        }`}
                      >
                        {practiceQuestion === practiceQuestions.length - 1
                          ? "Finish practice"
                          : "Next"}
                        <ArrowRight size={11} />
                      </button>
                    </div>
                  </motion.div>
                )}

                {practiceComplete && (
                  <motion.div
                    initial={{
                      opacity: 0,
                      scale: 0.98,
                    }}
                    animate={{
                      opacity: 1,
                      scale: 1,
                    }}
                    className="mt-5 rounded-xl bg-[#edf8f3] p-5 text-center"
                  >
                    <div className="mx-auto flex h-9 w-9 items-center justify-center rounded-full bg-[#53ad8d] text-white">
                      <Check size={17} />
                    </div>

                    <h3 className="mt-3 text-[13px] font-bold text-[#3e6858]">
                      Nice. Concept reinforced.
                    </h3>

                    <p className="mx-auto mt-1 max-w-[400px] text-[9px] leading-5 text-[#718c80]">
                      Your answers will be used to update your mastery profile.
                    </p>
                  </motion.div>
                )}
              </motion.div>
            </div>

            {/* =================================================
                RIGHT SIDEBAR
            ================================================= */}

            <aside className="space-y-4">

              {/* Current goal */}

              <motion.div
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
              >
                <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                  Current goal
                </p>

                <div className="mt-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#edf4ff] text-[#3970e8]">
                    <Target size={17} />
                  </div>

                  <div>
                    <p className="text-[11px] font-bold text-[#3e4a5c]">
                      Master Python
                    </p>

                    <p className="mt-1 text-[8px] text-[#929baa]">
                      Current mastery: 58%
                    </p>
                  </div>
                </div>

                <div className="mt-5 h-2 overflow-hidden rounded-full bg-[#e8edf4]">
                  <motion.div
                    initial={{
                      width: 0,
                    }}
                    animate={{
                      width: "58%",
                    }}
                    transition={{
                      delay: 0.8,
                      duration: 1,
                    }}
                    className="h-full rounded-full bg-[#3970e8]"
                  />
                </div>

                <p className="mt-2 text-right text-[8px] font-semibold text-[#3970e8]">
                  58%
                </p>
              </motion.div>

              {/* Why this lesson */}

              <motion.div
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="rounded-2xl border border-[#d9e5f5] bg-[#edf4ff] p-5"
              >
                <div className="flex items-center gap-2">
                  <Sparkles size={14} className="text-[#3970e8]" />

                  <p className="text-[10px] font-bold text-[#344054]">
                    Why you&apos;re seeing this
                  </p>
                </div>

                <p className="mt-4 text-[10px] leading-5 text-[#68778b]">
                  Your assessment showed strong knowledge of Python basics,
                  but functions were one of your biggest gaps.
                </p>

                <div className="mt-4 rounded-xl bg-white/70 p-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[8px] text-[#7e8999]">
                      Functions mastery
                    </span>

                    <span className="text-[9px] font-bold text-[#3970e8]">
                      43%
                    </span>
                  </div>

                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[#dfe8f6]">
                    <motion.div
                      initial={{
                        width: 0,
                      }}
                      animate={{
                        width: "43%",
                      }}
                      transition={{
                        delay: 0.9,
                        duration: 0.8,
                      }}
                      className="h-full rounded-full bg-[#3970e8]"
                    />
                  </div>
                </div>
              </motion.div>

              {/* Next */}

              <motion.div
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
              >
                <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                  Up next
                </p>

                <div className="mt-4 flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#f1f5fa] text-[#758194]">
                    <Brain size={15} />
                  </div>

                  <div>
                    <p className="text-[10px] font-bold text-[#4a5667]">
                      OOP Fundamentals
                    </p>

                    <p className="mt-1 text-[8px] text-[#949daa]">
                      Unlocks after Functions
                    </p>
                  </div>
                </div>

                <div className="mt-4 flex items-center gap-2 text-[8px] text-[#8a95a4]">
                  <Clock3 size={11} />
                  Approximately 60 minutes
                </div>
              </motion.div>

              {/* Reset */}

              <button
                type="button"
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-[#e0e7ef] bg-white py-3 text-[8px] font-semibold text-[#8993a1] transition hover:text-[#3970e8]"
              >
                <RotateCcw size={11} />
                Recalibrate my path
              </button>
            </aside>
          </div>

          {/* Bottom completion */}

          <motion.div
            initial={{
              opacity: 0,
              y: 10,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            transition={{
              delay: 0.7,
            }}
            className="mt-6 flex flex-col items-center justify-between gap-4 rounded-2xl border border-[#dce6f3] bg-[#edf4ff] p-5 sm:flex-row"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-[#3970e8]">
                <Check size={15} />
              </div>

              <div>
                <p className="text-[10px] font-bold text-[#3c4859]">
                  One concept at a time.
                </p>

                <p className="mt-0.5 text-[8px] text-[#7d899a]">
                  Master this topic before moving to the next gap.
                </p>
              </div>
            </div>

            <Link
              href="/learning-path"
              className="flex items-center gap-2 rounded-xl bg-[#121c2c] px-5 py-3 text-[9px] font-semibold text-white transition hover:-translate-y-0.5"
            >
              Back to my path
              <ArrowRight size={11} />
            </Link>
          </motion.div>
        </div>
      </div>
    </main>
  );
}