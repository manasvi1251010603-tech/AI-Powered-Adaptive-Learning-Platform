"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  Check,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,

} from "lucide-react";
import { useState } from "react";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <main className="min-h-screen bg-[#eef4fb] p-3 sm:p-5 lg:p-7">
      <div className="mx-auto grid min-h-[calc(100vh-24px)] max-w-[1450px] overflow-hidden rounded-[28px] border border-white bg-white shadow-[0_20px_70px_rgba(48,78,125,0.10)] lg:grid-cols-2">

        {/* =====================================================
            LEFT VISUAL
        ===================================================== */}
        <section className="relative hidden overflow-hidden bg-[#eaf2ff] lg:block">

          {/* Background glow */}
          <div className="absolute -left-20 top-20 h-[420px] w-[420px] rounded-full bg-[#c9dcff] opacity-60 blur-[90px]" />

          <div className="absolute -bottom-20 right-[-80px] h-[400px] w-[400px] rounded-full bg-[#d7e6ff] opacity-70 blur-[90px]" />

          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="absolute left-8 top-8 z-20 flex items-center gap-2.5"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-[#3265e8] shadow-sm">
              <Brain size={18} />
            </div>

            <span className="text-[15px] font-bold tracking-tight text-[#172033]">
              LearnFlow
            </span>
          </motion.div>

          {/* Main message */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.7 }}
            className="absolute left-10 top-[34%] z-10 max-w-[430px]"
          >
            <p className="mb-3 text-[10px] font-bold uppercase tracking-[0.18em] text-[#3970e8]">
              Personalized learning
            </p>

            <h1 className="text-[44px] font-bold leading-[1.02] tracking-[-0.055em] text-[#132038]">
              Learn what
              <br />
              <span className="text-[#3265e8]">actually matters.</span>
            </h1>

            <p className="mt-5 max-w-[330px] text-[13px] leading-6 text-[#66758a]">
              Your journey starts with understanding what you already know.
            </p>
          </motion.div>

          {/* Animated knowledge path */}
          <svg
            viewBox="0 0 600 400"
            className="absolute bottom-[-10px] left-[-30px] h-[55%] w-[115%]"
            fill="none"
          >
            <defs>
              <linearGradient
                id="loginPath"
                x1="40"
                y1="300"
                x2="550"
                y2="90"
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#c5dbff" />
                <stop offset="0.5" stopColor="#7da7f5" />
                <stop offset="1" stopColor="#b7d0ff" />
              </linearGradient>

              <filter
                id="loginGlow"
                x="-100%"
                y="-100%"
                width="300%"
                height="300%"
              >
                <feGaussianBlur stdDeviation="7" />
              </filter>
            </defs>

            <motion.path
              id="loginKnowledgePath"
              d="M30 350 C130 330 75 230 180 210 C280 190 230 90 330 100 C440 110 350 250 470 260 C530 265 510 160 580 120"
              stroke="#6e9cf4"
              strokeWidth="18"
              opacity="0.12"
              filter="url(#loginGlow)"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 2.2 }}
            />

            <motion.path
              d="M30 350 C130 330 75 230 180 210 C280 190 230 90 330 100 C440 110 350 250 470 260 C530 265 510 160 580 120"
              stroke="url(#loginPath)"
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 2.2 }}
            />

            <circle r="5" fill="#4c7fea">
              <animateMotion
                dur="7s"
                repeatCount="indefinite"
                rotate="auto"
              >
                <mpath href="#loginKnowledgePath" />
              </animateMotion>
            </circle>
          </svg>

          {/* Floating insight */}
          <motion.div
            animate={{
              y: [0, -6, 0],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="absolute right-[12%] top-[25%] flex items-center gap-2 rounded-xl border border-white bg-white/90 px-3 py-2 shadow-[0_12px_30px_rgba(47,86,145,0.12)] backdrop-blur"
          >
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3970e8]">
              <Brain size={14} />
            </div>

            <div>
              <p className="text-[9px] font-semibold text-[#4c5768]">
                Your learning path
              </p>

              <p className="mt-0.5 text-[8px] text-[#929baa]">
                adapts to you
              </p>
            </div>
          </motion.div>
        </section>

        {/* =====================================================
            RIGHT LOGIN
        ===================================================== */}
        <section className="flex items-center justify-center px-6 py-12 sm:px-12 lg:px-16">

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.65,
              ease: [0.22, 1, 0.36, 1],
            }}
            className="w-full max-w-[390px]"
          >

            {/* Mobile logo */}
            <div className="mb-10 flex items-center gap-2.5 lg:hidden">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#edf3ff] text-[#3265e8]">
                <Brain size={18} />
              </div>

              <span className="text-[15px] font-bold">
                LearnFlow
              </span>
            </div>

            {/* Heading */}
            <div>
              <h2 className="text-[32px] font-bold tracking-[-0.045em] text-[#172033]">
                Welcome back!
              </h2>

              <p className="mt-2 text-[13px] text-[#7a8595]">
                Continue your learning journey.
              </p>
            </div>

            {/* Form */}
            <form className="mt-9 space-y-5">

              {/* Email */}
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-[10px] font-semibold text-[#4e5969]"
                >
                  Email
                </label>

                <div className="relative">
                  <Mail
                    size={15}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-[#a0a9b7]"
                  />

                  <input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    className="h-11 w-full rounded-xl border border-[#e0e6ef] bg-[#fbfcfe] pl-10 pr-4 text-[12px] outline-none transition placeholder:text-[#b0b7c2] focus:border-[#6f98ed] focus:bg-white focus:ring-4 focus:ring-[#e9f0ff]"
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="text-[10px] font-semibold text-[#4e5969]"
                  >
                    Password
                  </label>

                  <button
                    type="button"
                    className="text-[9px] font-medium text-[#3970e8] hover:underline"
                  >
                    Forgot password?
                  </button>
                </div>

                <div className="relative">
                  <LockKeyhole
                    size={15}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-[#a0a9b7]"
                  />

                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    className="h-11 w-full rounded-xl border border-[#e0e6ef] bg-[#fbfcfe] pl-10 pr-11 text-[12px] outline-none transition placeholder:text-[#b0b7c2] focus:border-[#6f98ed] focus:bg-white focus:ring-4 focus:ring-[#e9f0ff]"
                  />

                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9ca5b3] transition hover:text-[#3970e8]"
                  >
                    {showPassword ? (
                      <EyeOff size={15} />
                    ) : (
                      <Eye size={15} />
                    )}
                  </button>
                </div>
              </div>

              {/* Login */}
              <button
                type="submit"
                className="group flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-[#121c2c] text-[11px] font-semibold text-white shadow-[0_8px_20px_rgba(18,28,44,0.15)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_12px_25px_rgba(18,28,44,0.2)]"
              >
                Log in

                <ArrowRight
                  size={13}
                  className="transition-transform group-hover:translate-x-1"
                />
              </button>
            </form>

            {/* Divider */}
            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-[#e8ecf2]" />
              <span className="text-[9px] text-[#a1a8b4]">
                or
              </span>
              <div className="h-px flex-1 bg-[#e8ecf2]" />
            </div>

            {/* Google */}
            <button className="flex h-11 w-full items-center justify-center gap-2 rounded-xl border border-[#e0e6ef] bg-white text-[11px] font-semibold text-[#3f4958] transition duration-300 hover:-translate-y-0.5 hover:bg-[#f9fbff] hover:shadow-sm">
              <span className="text-[14px] font-bold text-[#4285f4]">
                G
              </span>

              Continue with Google
            </button>

            {/* Sign up */}
            <p className="mt-8 text-center text-[10px] text-[#8993a1]">
              Don&apos;t have an account?{" "}
              <Link
                href="/register"
                className="font-semibold text-[#3265e8] hover:underline"
              >
                Sign up
              </Link>
            </p>

            {/* Small trust line */}
            <div className="mt-8 flex items-center justify-center gap-2 text-[9px] text-[#a0a8b5]">
              <Check size={11} className="text-[#4ba887]" />
              Your learning data stays private.
            </div>
          </motion.div>
        </section>
      </div>
    </main>
  );
}