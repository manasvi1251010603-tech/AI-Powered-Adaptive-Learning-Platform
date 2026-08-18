"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  BarChart3,
  Brain,
  CalendarDays,
  Check,
  ChevronRight,
  Flame,
  Play,
  Sparkles,
  Target,
  TrendingUp,
  Trophy,
} from "lucide-react";

import AuthGuard from "@/components/AuthGuard";

const weeklyProgress = [
  { day: "Mon", value: 42 },
  { day: "Tue", value: 58 },
  { day: "Wed", value: 46 },
  { day: "Thu", value: 72 },
  { day: "Fri", value: 64 },
  { day: "Sat", value: 88 },
  { day: "Sun", value: 76 },
];

const topics = [
  {
    title: "Python Basics",
    mastery: 92,
    status: "Mastered",
  },
  {
    title: "Data Types",
    mastery: 84,
    status: "Strong",
  },
  {
    title: "Lists & Tuples",
    mastery: 71,
    status: "Good",
  },
  {
    title: "Functions",
    mastery: 61,
    status: "Improving",
  },
  {
    title: "OOP",
    mastery: 38,
    status: "Needs focus",
  },
];

const activities = [
  {
    title: "Functions & Scope",
    description: "Completed 3 timestamp sections",
    time: "Today",
    icon: Play,
  },
  {
    title: "Quick Practice",
    description: "Scored 4 / 5",
    time: "Yesterday",
    icon: Target,
  },
  {
    title: "Python Basics",
    description: "Marked as mastered",
    time: "2 days ago",
    icon: Check,
  },
];

/* ============================================================
   DASHBOARD CONTENT
   ============================================================ */

function DashboardContent() {
  return (
    <main className="min-h-screen bg-[#eef4fb] px-3 py-3 sm:px-5 sm:py-5 lg:px-7">
      <div className="relative min-h-[calc(100vh-24px)] overflow-hidden rounded-[28px] border border-white bg-[#f8fbff] shadow-[0_20px_70px_rgba(48,78,125,0.10)]">

        {/* =====================================================
            BACKGROUND
        ===================================================== */}

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
            <span className="font-semibold text-[#3970e8]">
              Dashboard
            </span>

            <Link
              href="/learning-path"
              className="transition hover:text-[#3970e8]"
            >
              My Path
            </Link>

            <Link
              href="/learn"
              className="transition hover:text-[#3970e8]"
            >
              Learn
            </Link>
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden items-center gap-2 rounded-xl border border-[#e1e8f1] bg-white px-3 py-2 sm:flex">
              <Flame size={12} className="text-[#e3a53e]" />

              <span className="text-[8px] font-bold text-[#566173]">
                6 day streak
              </span>
            </div>

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#121c2c] text-[10px] font-bold text-white">
              ML
            </div>
          </div>
        </nav>

        {/* =====================================================
            CONTENT
        ===================================================== */}

        <div className="relative z-10 mx-auto max-w-[1150px] px-5 pb-12 pt-8 sm:px-8 lg:px-10">

          {/* ===================================================
              HEADER
          =================================================== */}

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"
          >
            <div>
              <p className="text-[9px] font-bold uppercase tracking-[0.16em] text-[#3970e8]">
                Your learning dashboard
              </p>

              <h1 className="mt-2 text-3xl font-bold tracking-[-0.045em] text-[#152033] sm:text-4xl">
                Keep the momentum going.
              </h1>

              <p className="mt-3 max-w-[540px] text-sm leading-6 text-[#778292]">
                You&apos;re making progress. Here&apos;s what changed and what
                deserves your attention next.
              </p>
            </div>

            <Link
              href="/learn"
              className="group flex w-fit items-center gap-2 rounded-xl bg-[#121c2c] px-5 py-3 text-[9px] font-semibold text-white shadow-[0_8px_20px_rgba(18,28,44,0.15)] transition hover:-translate-y-0.5"
            >
              Continue learning

              <ArrowRight
                size={12}
                className="transition-transform group-hover:translate-x-1"
              />
            </Link>
          </motion.div>

          {/* ===================================================
              TOP STATS
          =================================================== */}

          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">

            {/* Overall mastery */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
            >
              <div className="flex items-center justify-between">
                <span className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                  Overall mastery
                </span>

                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#edf4ff] text-[#3970e8]">
                  <Brain size={14} />
                </div>
              </div>

              <div className="mt-5 flex items-end gap-2">
                <span className="text-3xl font-bold tracking-[-0.05em] text-[#172033]">
                  63%
                </span>

                <span className="mb-1 flex items-center gap-1 text-[8px] font-bold text-[#4b9b7c]">
                  <TrendingUp size={10} />
                  +5%
                </span>
              </div>

              <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-[#e8edf4]">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: "63%" }}
                  transition={{
                    delay: 0.5,
                    duration: 1,
                  }}
                  className="h-full rounded-full bg-[#3970e8]"
                />
              </div>
            </motion.div>

            {/* Study time */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
            >
              <div className="flex items-center justify-between">
                <span className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                  This week
                </span>

                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#edf4ff] text-[#3970e8]">
                  <CalendarDays size={14} />
                </div>
              </div>

              <div className="mt-5">
                <span className="text-3xl font-bold tracking-[-0.05em] text-[#172033]">
                  4.8h
                </span>

                <p className="mt-1 text-[8px] text-[#8c96a4]">
                  focused learning time
                </p>
              </div>
            </motion.div>

            {/* Streak */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
            >
              <div className="flex items-center justify-between">
                <span className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                  Streak
                </span>

                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#fff6e6] text-[#e3a53e]">
                  <Flame size={14} />
                </div>
              </div>

              <div className="mt-5">
                <span className="text-3xl font-bold tracking-[-0.05em] text-[#172033]">
                  6
                </span>

                <span className="ml-1 text-[10px] font-semibold text-[#7c8797]">
                  days
                </span>

                <p className="mt-1 text-[8px] text-[#8c96a4]">
                  Your longest: 9 days
                </p>
              </div>
            </motion.div>

            {/* Modules */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.25 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)]"
            >
              <div className="flex items-center justify-between">
                <span className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                  Modules
                </span>

                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#edf4ff] text-[#3970e8]">
                  <Trophy size={14} />
                </div>
              </div>

              <div className="mt-5">
                <span className="text-3xl font-bold tracking-[-0.05em] text-[#172033]">
                  2
                </span>

                <span className="ml-1 text-[10px] font-semibold text-[#7c8797]">
                  / 5
                </span>

                <p className="mt-1 text-[8px] text-[#8c96a4]">
                  modules completed
                </p>
              </div>
            </motion.div>
          </div>

          {/* ===================================================
              MAIN GRID
          =================================================== */}

          <div className="mt-5 grid gap-5 lg:grid-cols-[1.25fr_0.75fr]">

            {/* Weekly graph */}

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)] sm:p-6"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <BarChart3
                      size={14}
                      className="text-[#3970e8]"
                    />

                    <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#3970e8]">
                      Learning activity
                    </p>
                  </div>

                  <h2 className="mt-2 text-lg font-bold text-[#273246]">
                    Your week at a glance.
                  </h2>

                  <p className="mt-1 text-[9px] text-[#929baa]">
                    Focused learning activity
                  </p>
                </div>

                <span className="rounded-full bg-[#edf4ff] px-3 py-1.5 text-[8px] font-bold text-[#3970e8]">
                  This week
                </span>
              </div>

              <div className="relative mt-8 h-[220px]">

                {/* Horizontal grid lines */}

                <div className="absolute inset-0 flex flex-col justify-between">
                  {[100, 75, 50, 25, 0].map((value) => (
                    <div
                      key={value}
                      className="flex items-center gap-3"
                    >
                      <span className="w-6 text-right text-[7px] text-[#a0a8b4]">
                        {value}
                      </span>

                      <div className="h-px flex-1 bg-[#edf1f5]" />
                    </div>
                  ))}
                </div>

                {/* Animated bars */}

                <div className="absolute bottom-0 left-9 right-0 top-0 flex items-end justify-between gap-2 px-2">
                  {weeklyProgress.map((item, index) => (
                    <div
                      key={item.day}
                      className="flex h-full flex-1 flex-col items-center justify-end gap-2"
                    >
                      <motion.div
                        initial={{ height: 0 }}
                        animate={{
                          height: `${item.value * 1.75}px`,
                        }}
                        transition={{
                          delay: 0.5 + index * 0.1,
                          duration: 0.8,
                          ease: "easeOut",
                        }}
                        className="w-full max-w-[34px] rounded-t-xl bg-[#8eb0ef] transition hover:bg-[#3970e8]"
                      />

                      <span className="text-[7px] font-medium text-[#8e98a7]">
                        {item.day}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-5 flex items-center justify-between rounded-xl bg-[#f4f8fd] px-4 py-3">
                <div className="flex items-center gap-2">
                  <TrendingUp
                    size={13}
                    className="text-[#4a9d7e]"
                  />

                  <span className="text-[8px] font-semibold text-[#667285]">
                    Your consistency improved this week.
                  </span>
                </div>

                <span className="text-[8px] font-bold text-[#4a9d7e]">
                  +18%
                </span>
              </div>
            </motion.div>

            {/* AI insight */}

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="rounded-2xl border border-[#d9e5f5] bg-[#edf4ff] p-6"
            >
              <div className="flex items-center gap-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-[#3970e8] shadow-sm">
                  <Sparkles size={16} />
                </div>

                <div>
                  <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#3970e8]">
                    Your AI coach
                  </p>

                  <p className="mt-0.5 text-[8px] text-[#8793a4]">
                    Personalized insight
                  </p>
                </div>
              </div>

              <h2 className="mt-7 text-xl font-bold leading-7 tracking-[-0.03em] text-[#283448]">
                Don&apos;t go back to beginner tutorials yet.
              </h2>

              <p className="mt-4 text-[10px] leading-6 text-[#66758a]">
                Your Python fundamentals are now strong enough that repeating
                basic syntax won&apos;t give you much return.
              </p>

              <div className="mt-5 rounded-xl bg-white/75 p-4">
                <p className="text-[8px] font-bold uppercase tracking-[0.12em] text-[#8a95a4]">
                  Focus next
                </p>

                <div className="mt-3 flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#3970e8] text-white">
                    <Target size={15} />
                  </div>

                  <div>
                    <p className="text-[10px] font-bold text-[#455164]">
                      Object-Oriented Programming
                    </p>

                    <p className="mt-1 text-[8px] text-[#8d97a5]">
                      38% mastery · highest priority
                    </p>
                  </div>
                </div>
              </div>

              <Link
                href="/learn"
                className="mt-5 flex items-center justify-center gap-2 rounded-xl bg-[#121c2c] py-3 text-[9px] font-semibold text-white transition hover:-translate-y-0.5"
              >
                Continue where you left off
                <ArrowRight size={11} />
              </Link>
            </motion.div>
          </div>

          {/* ===================================================
              TOPIC MASTERY + ACTIVITY
          =================================================== */}

          <div className="mt-5 grid gap-5 lg:grid-cols-[1fr_1fr]">

            {/* Topic mastery */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)] sm:p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                    Knowledge profile
                  </p>

                  <h2 className="mt-1 text-lg font-bold text-[#273246]">
                    Topic mastery
                  </h2>
                </div>

                <Link
                  href="/analysis"
                  className="text-[8px] font-semibold text-[#3970e8]"
                >
                  View analysis
                </Link>
              </div>

              <div className="mt-6 space-y-4">
                {topics.map((topic, index) => (
                  <div key={topic.title}>
                    <div className="flex items-center justify-between">
                      <span className="text-[9px] font-semibold text-[#556173]">
                        {topic.title}
                      </span>

                      <div className="flex items-center gap-2">
                        <span className="text-[8px] text-[#9099a6]">
                          {topic.status}
                        </span>

                        <span className="w-7 text-right text-[9px] font-bold text-[#3970e8]">
                          {topic.mastery}%
                        </span>
                      </div>
                    </div>

                    <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[#e9eef5]">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{
                          width: `${topic.mastery}%`,
                        }}
                        transition={{
                          delay: 0.6 + index * 0.1,
                          duration: 0.8,
                        }}
                        className={`h-full rounded-full ${
                          topic.mastery >= 80
                            ? "bg-[#53ad8d]"
                            : topic.mastery >= 60
                              ? "bg-[#3970e8]"
                              : "bg-[#e3a84c]"
                        }`}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Recent activity */}

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="rounded-2xl border border-[#dfe7f1] bg-white p-5 shadow-[0_8px_25px_rgba(48,78,125,0.05)] sm:p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-[#8b95a4]">
                    Recent activity
                  </p>

                  <h2 className="mt-1 text-lg font-bold text-[#273246]">
                    What you&apos;ve been doing
                  </h2>
                </div>

                <span className="text-[8px] text-[#929baa]">
                  Last 7 days
                </span>
              </div>

              <div className="mt-6 space-y-2">
                {activities.map((activity, index) => {
                  const Icon = activity.icon;

                  return (
                    <motion.div
                      key={activity.title}
                      initial={{
                        opacity: 0,
                        x: 10,
                      }}
                      animate={{
                        opacity: 1,
                        x: 0,
                      }}
                      transition={{
                        delay: 0.7 + index * 0.1,
                      }}
                      className="flex items-center gap-3 rounded-xl border border-[#e8edf3] p-3"
                    >
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#edf4ff] text-[#3970e8]">
                        <Icon size={14} />
                      </div>

                      <div className="min-w-0 flex-1">
                        <p className="text-[9px] font-bold text-[#4a5667]">
                          {activity.title}
                        </p>

                        <p className="mt-1 truncate text-[8px] text-[#929baa]">
                          {activity.description}
                        </p>
                      </div>

                      <span className="shrink-0 text-[7px] text-[#9ba3af]">
                        {activity.time}
                      </span>

                      <ChevronRight
                        size={12}
                        className="text-[#adb5c0]"
                      />
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          </div>

          {/* ===================================================
              BOTTOM CTA
          =================================================== */}

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="mt-5 flex flex-col items-center justify-between gap-4 rounded-2xl border border-[#dce6f3] bg-[#edf4ff] p-5 sm:flex-row"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-[#3970e8] shadow-sm">
                <Sparkles size={16} />
              </div>

              <div>
                <p className="text-[10px] font-bold text-[#3c4859]">
                  Your path keeps adapting.
                </p>

                <p className="mt-0.5 text-[8px] text-[#7d899a]">
                  Every assessment updates what LearnFlow recommends next.
                </p>
              </div>
            </div>

            <Link
              href="/learning-path"
              className="group flex items-center gap-2 rounded-xl bg-[#121c2c] px-5 py-3 text-[9px] font-semibold text-white transition hover:-translate-y-0.5"
            >
              View my learning path

              <ArrowRight
                size={11}
                className="transition-transform group-hover:translate-x-1"
              />
            </Link>
          </motion.div>
        </div>
      </div>
    </main>
  );
}

/* ============================================================
   PROTECTED DASHBOARD
   ============================================================ */

export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}