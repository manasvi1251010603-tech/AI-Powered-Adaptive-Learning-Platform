"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  Check,
  Play,
  Sparkles,
  Target,
  Zap,
} from "lucide-react";

const steps = [
  {
    icon: Target,
    title: "Assess",
    subtitle: "Smart Diagnostic",
  },
  {
    icon: Brain,
    title: "Understand",
    subtitle: "Deep Insights",
  },
  {
    icon: Sparkles,
    title: "Personalize",
    subtitle: "AI Learning Path",
  },
  {
    icon: Play,
    title: "Learn",
    subtitle: "Focused Content",
  },
  {
    icon: Zap,
    title: "Master",
    subtitle: "Track Progress",
  },
];

const fadeUp = {
  hidden: { opacity: 0, y: 18 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.65,
      ease: [0.22, 1, 0.36, 1],
    },
  },
};

export default function Home() {
  return (
    <main className="min-h-screen overflow-x-hidden bg-[#eef4fb] text-[#101828]">
      {/* =========================================================
          HERO
      ========================================================= */}
      <section className="mx-3 mt-3 overflow-hidden rounded-[26px] border border-white bg-[#f8fbff] shadow-[0_18px_60px_rgba(48,88,145,0.10)] sm:mx-5 sm:mt-5 lg:mx-7">
        {/* ================= NAVBAR ================= */}
        <nav className="relative z-30 flex h-[72px] items-center justify-between px-5 sm:px-8 lg:px-10">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#eaf1ff] text-[#3265e8]">
              <Brain size={19} strokeWidth={2.2} />
            </div>

            <span className="text-[15px] font-bold tracking-[-0.025em]">
              LearnFlow
            </span>
          </Link>

          {/* Navigation */}
          <div className="hidden items-center gap-7 text-[10px] font-medium text-[#626d7d] lg:flex">
            <a
              href="#features"
              className="transition-colors hover:text-[#3265e8]"
            >
              Features
            </a>

            <a
              href="#how-it-works"
              className="transition-colors hover:text-[#3265e8]"
            >
              How it works
            </a>

            <a
              href="#students"
              className="transition-colors hover:text-[#3265e8]"
            >
              For Students
            </a>

            <a
              href="#educators"
              className="transition-colors hover:text-[#3265e8]"
            >
              For Educators
            </a>

            <a
              href="#pricing"
              className="transition-colors hover:text-[#3265e8]"
            >
              Pricing
            </a>
          </div>

          {/* Auth */}
          <div className="flex items-center gap-2">
            <Link
              href="/login"
              className="hidden rounded-xl border border-[#e3e9f2] bg-white px-4 py-2 text-[10px] font-semibold text-[#273142] shadow-[0_3px_10px_rgba(50,75,110,0.04)] transition duration-300 hover:-translate-y-0.5 hover:shadow-md sm:block"
            >
              Log in
            </Link>

            <Link
              href="/register"
              className="group flex items-center gap-1.5 rounded-xl bg-[#3265e8] px-4 py-2.5 text-[10px] font-semibold text-white shadow-[0_7px_18px_rgba(50,101,232,0.25)] transition duration-300 hover:-translate-y-0.5 hover:bg-[#2859d5]"
            >
              Get Started
              <ArrowRight
                size={11}
                className="transition-transform duration-300 group-hover:translate-x-0.5"
              />
            </Link>
          </div>
        </nav>

        {/* ================= HERO CONTENT ================= */}
        <div className="relative px-5 pb-6 pt-4 sm:px-9 lg:px-11">
          {/* subtle blue atmosphere */}
          <div className="pointer-events-none absolute right-[8%] top-[7%] h-[390px] w-[390px] rounded-full bg-[#dce9ff]/60 blur-[95px]" />

          <div className="relative z-10 grid min-h-[470px] items-center lg:grid-cols-[0.88fr_1.12fr]">
            {/* ================= LEFT ================= */}
            <motion.div
              initial="hidden"
              animate="visible"
              variants={{
                hidden: {},
                visible: {
                  transition: {
                    staggerChildren: 0.12,
                  },
                },
              }}
              className="relative z-20 max-w-[530px]"
            >
              {/* small badge */}
              <motion.div
                variants={fadeUp}
                className="mb-5 inline-flex items-center gap-2 rounded-xl border border-[#dfe7f3] bg-white/85 px-3 py-2 shadow-[0_5px_18px_rgba(50,80,125,0.06)]"
              >
                <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3265e8]">
                  <Brain size={13} />
                </span>

                <div className="leading-none">
                  <p className="text-[9px] font-semibold text-[#586477]">
                    AI analyzes
                  </p>
                  <p className="mt-1 text-[8px] text-[#929baa]">
                    your knowledge
                  </p>
                </div>
              </motion.div>

              {/* headline */}
              <motion.h1
                variants={fadeUp}
                className="text-[48px] font-bold leading-[0.98] tracking-[-0.055em] sm:text-[57px] lg:text-[67px]"
              >
                Stop learning
                <br />
                what you
                <br />
                <span className="text-[#3265e8]">already know.</span>
              </motion.h1>

              {/* description */}
              <motion.p
                variants={fadeUp}
                className="mt-6 max-w-[350px] text-[13px] leading-[1.7] text-[#697587] sm:text-[14px]"
              >
                AI finds your knowledge gaps and builds a learning path
                that&apos;s 100% about <strong className="text-[#3f4958]">YOU.</strong>
              </motion.p>

              {/* CTA */}
              <motion.div variants={fadeUp} className="mt-7">
                <Link
                  href="/register"
                  className="group inline-flex items-center gap-3 rounded-xl bg-[#121c2c] px-5 py-3 text-[11px] font-semibold text-white shadow-[0_9px_22px_rgba(18,28,44,0.18)] transition duration-300 hover:-translate-y-1 hover:shadow-[0_14px_28px_rgba(18,28,44,0.22)]"
                >
                  Start Your Journey
                  <ArrowRight
                    size={13}
                    className="transition-transform duration-300 group-hover:translate-x-1"
                  />
                </Link>
              </motion.div>

              {/* learner proof */}
              <motion.div
                variants={fadeUp}
                className="mt-7 flex items-center gap-3"
              >
                <div className="flex -space-x-2">
                  {["#d8e5ff", "#c8dcff", "#e1ebff", "#c3d8ff"].map(
                    (color, index) => (
                      <div
                        key={index}
                        className="flex h-7 w-7 items-center justify-center rounded-full border-2 border-[#f8fbff]"
                        style={{ backgroundColor: color }}
                      >
                        <span className="text-[9px] font-bold text-[#5274bd]">
                          {["M", "A", "R", "S"][index]}
                        </span>
                      </div>
                    ),
                  )}
                </div>

                <div>
                  <p className="text-[9px] font-semibold text-[#4c5666]">
                    Join 25,000+ learners
                  </p>
                  <p className="mt-0.5 text-[8px] text-[#929aa8]">
                    learning smarter every day
                  </p>
                </div>
              </motion.div>
            </motion.div>

            {/* ================= RIGHT VISUAL ================= */}
            <div className="relative mt-8 h-[390px] w-full sm:h-[420px] lg:mt-0 lg:h-[450px]">
              {/* Main knowledge path */}
              <svg
                viewBox="0 0 720 470"
                className="absolute inset-0 h-full w-full"
                fill="none"
                preserveAspectRatio="xMidYMid meet"
              >
                <defs>
                  <linearGradient
                    id="bluePath"
                    x1="55"
                    y1="350"
                    x2="675"
                    y2="135"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop stopColor="#d3e2ff" />
                    <stop offset="0.35" stopColor="#a8c4ff" />
                    <stop offset="0.7" stopColor="#78a2f8" />
                    <stop offset="1" stopColor="#d4e3ff" />
                  </linearGradient>

                  <filter
                    id="softGlow"
                    x="-100%"
                    y="-100%"
                    width="300%"
                    height="300%"
                  >
                    <feGaussianBlur stdDeviation="8" />
                  </filter>

                  <filter
                    id="dotGlow"
                    x="-200%"
                    y="-200%"
                    width="400%"
                    height="400%"
                  >
                    <feGaussianBlur stdDeviation="5" />
                  </filter>
                </defs>

                {/* soft glow path */}
                <motion.path
                  d="M58 335 C140 330 105 220 215 190 C330 160 260 72 370 88 C495 106 405 245 535 260 C610 268 590 165 675 140"
                  stroke="#76a4ff"
                  strokeWidth="17"
                  opacity="0.13"
                  filter="url(#softGlow)"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{
                    duration: 2.5,
                    ease: "easeInOut",
                  }}
                />

                {/* actual path */}
                <motion.path
                  id="knowledge-path"
                  d="M58 335 C140 330 105 220 215 190 C330 160 260 72 370 88 C495 106 405 245 535 260 C610 268 590 165 675 140"
                  stroke="url(#bluePath)"
                  strokeWidth="3.2"
                  strokeLinecap="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{
                    duration: 2.5,
                    ease: "easeInOut",
                  }}
                />

                {/* bright inner line */}
                <motion.path
                  d="M58 335 C140 330 105 220 215 190 C330 160 260 72 370 88 C495 106 405 245 535 260 C610 268 590 165 675 140"
                  stroke="white"
                  strokeWidth="1.2"
                  strokeLinecap="round"
                  opacity="0.9"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{
                    delay: 0.4,
                    duration: 2.5,
                    ease: "easeInOut",
                  }}
                />

                {/* Actual moving dot */}
                <circle r="5" fill="#4d7ff0">
                  <animateMotion
                    dur="8s"
                    repeatCount="indefinite"
                    rotate="auto"
                  >
                    <mpath href="#knowledge-path" />
                  </animateMotion>
                </circle>

                {/* dot glow */}
                <circle r="13" fill="#6e9aff" opacity="0.13">
                  <animateMotion
                    dur="8s"
                    repeatCount="indefinite"
                    rotate="auto"
                  >
                    <mpath href="#knowledge-path" />
                  </animateMotion>
                </circle>
              </svg>

              {/* ================= FLOATING CARD 1 ================= */}
              <motion.div
                initial={{ opacity: 0, x: 15, y: -8 }}
                animate={{ opacity: 1, x: 0, y: 0 }}
                transition={{ delay: 1.15, duration: 0.65 }}
                className="absolute left-[10%] top-[2%] z-20 flex items-center gap-2 rounded-xl border border-white bg-white/90 px-3 py-2 shadow-[0_10px_30px_rgba(48,84,140,0.12)] backdrop-blur"
              >
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3970e8]">
                  <Brain size={14} />
                </div>

                <div>
                  <p className="text-[9px] font-semibold text-[#4a5566]">
                    AI analyzes
                  </p>
                  <p className="mt-0.5 text-[8px] text-[#939ba8]">
                    your knowledge
                  </p>
                </div>
              </motion.div>

              {/* ================= FLOATING CARD 2 ================= */}
              <motion.div
                initial={{ opacity: 0, x: -10, y: 12 }}
                animate={{ opacity: 1, x: 0, y: 0 }}
                transition={{ delay: 1.45, duration: 0.65 }}
                className="absolute bottom-[12%] left-[38%] z-20 flex items-center gap-2 rounded-xl border border-white bg-white/92 px-3 py-2 shadow-[0_10px_30px_rgba(48,84,140,0.12)] backdrop-blur"
              >
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3970e8]">
                  <Sparkles size={14} />
                </div>

                <div>
                  <p className="text-[9px] font-semibold text-[#4a5566]">
                    Builds your
                  </p>
                  <p className="mt-0.5 text-[8px] text-[#939ba8]">
                    personalized path
                  </p>
                </div>
              </motion.div>

              {/* ================= SOFT ORBS ================= */}
              <motion.div
                animate={{
                  y: [-4, 6, -4],
                  x: [0, 3, 0],
                }}
                transition={{
                  duration: 5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="absolute right-[8%] top-[3%] h-32 w-32 rounded-full border border-white/80 bg-[#dce8ff]/45"
              />

              <motion.div
                animate={{
                  y: [5, -5, 5],
                }}
                transition={{
                  duration: 6,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="absolute right-[4%] top-[21%] h-24 w-24 rounded-full bg-[#dce8ff]/35 blur-xl"
              />

              {/* tiny learning nodes */}
              <div className="absolute right-[13%] top-[34%] flex flex-col gap-3">
                {[0, 1, 2].map((item) => (
                  <motion.div
                    key={item}
                    animate={{
                      opacity: [0.3, 1, 0.3],
                      scale: [0.9, 1, 0.9],
                    }}
                    transition={{
                      duration: 2.4,
                      delay: item * 0.4,
                      repeat: Infinity,
                    }}
                    className="h-2 w-2 rounded-full bg-[#8caef4]"
                  />
                ))}
              </div>
            </div>
          </div>

          {/* ================= PROCESS BAR ================= */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.45, duration: 0.65 }}
            className="relative z-20 grid overflow-hidden rounded-2xl border border-[#e1e8f2] bg-white/90 shadow-[0_8px_25px_rgba(48,78,125,0.07)] sm:grid-cols-5"
          >
            {steps.map((step, index) => {
              const Icon = step.icon;

              return (
                <motion.div
                  key={step.title}
                  whileHover={{ y: -2 }}
                  className="group flex items-center gap-3 border-b border-[#edf1f6] px-4 py-3 transition last:border-0 sm:border-b-0 sm:border-r sm:last:border-r-0"
                >
                  <motion.div
                    whileHover={{ scale: 1.08 }}
                    className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3970e8]"
                  >
                    <Icon size={14} />
                  </motion.div>

                  <div>
                    <p className="text-[10px] font-bold text-[#3c4656]">
                      {step.title}
                    </p>
                    <p className="mt-0.5 text-[8px] text-[#949daa]">
                      {step.subtitle}
                    </p>
                  </div>

                  {index < steps.length - 1 && (
                    <ArrowRight
                      size={11}
                      className="ml-auto hidden text-[#c7d0dc] sm:block"
                    />
                  )}
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* =========================================================
          FEATURES PREVIEW
      ========================================================= */}
      <section
        id="features"
        className="mx-3 my-5 rounded-[26px] border border-white bg-white px-5 py-16 shadow-[0_15px_50px_rgba(48,78,125,0.07)] sm:mx-5 sm:px-8 lg:mx-7 lg:px-11"
      >
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-[10px] font-bold tracking-[0.18em] text-[#3970e8]">
              WHY LEARNFLOW
            </p>

            <h2 className="mt-3 max-w-2xl text-3xl font-bold tracking-[-0.04em] sm:text-4xl">
              Your learning should adapt to your brain.
            </h2>

            <p className="mt-4 max-w-2xl text-sm leading-7 text-[#737e8e]">
              Not another course library. LearnFlow identifies what you know,
              what you don&apos;t, and what you should learn next.
            </p>
          </motion.div>

          <div className="mt-12 grid gap-4 md:grid-cols-3">
            {[
              {
                number: "01",
                icon: Target,
                title: "Know your level",
                text: "A diagnostic assessment maps your current understanding.",
              },
              {
                number: "02",
                icon: Brain,
                title: "Find your gaps",
                text: "Concept-level mastery shows exactly where your effort belongs.",
              },
              {
                number: "03",
                icon: Sparkles,
                title: "Learn smarter",
                text: "AI finds useful content and the exact sections you need.",
              },
            ].map((item, index) => {
              const Icon = item.icon;

              return (
                <motion.div
                  key={item.number}
                  initial={{ opacity: 0, y: 22 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{
                    delay: index * 0.1,
                    duration: 0.55,
                  }}
                  whileHover={{
                    y: -5,
                    boxShadow: "0 16px 35px rgba(48,78,125,0.10)",
                  }}
                  className="rounded-2xl border border-[#e4eaf2] bg-[#f9fbfe] p-6 transition"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#edf3ff] text-[#3970e8]">
                      <Icon size={18} />
                    </div>

                    <span className="text-[10px] font-bold text-[#b0b8c5]">
                      {item.number}
                    </span>
                  </div>

                  <h3 className="mt-7 text-[17px] font-bold tracking-tight">
                    {item.title}
                  </h3>

                  <p className="mt-2 text-[13px] leading-6 text-[#747f8f]">
                    {item.text}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =========================================================
          FOOTER
      ========================================================= */}
      <footer className="px-5 pb-8 pt-3 text-center text-[10px] text-[#8993a2]">
        LearnFlow — learn what matters. Skip what doesn&apos;t.
      </footer>
    </main>
  );
}