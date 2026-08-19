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
  UserRound,
} from "lucide-react";
import { FormEvent, useState } from "react";
import { register } from "@/lib/api/auth";

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();
    setError("");

    if (
      !fullName.trim() ||
      !email.trim() ||
      !password ||
      !confirmPassword
    ) {
      setError("Please fill in all required fields.");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      await register({
        full_name: fullName.trim(),
        email: email.trim(),
        password,
      });

      window.location.href = "/login?registered=true";
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Unable to create your account.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#eef4fb] p-3 sm:p-5 lg:p-7">
      <div className="mx-auto grid min-h-[calc(100vh-24px)] max-w-[1450px] overflow-hidden rounded-[28px] border border-white bg-white shadow-[0_20px_70px_rgba(48,78,125,0.10)] lg:grid-cols-2">

        {/* =====================================================
            LEFT VISUAL
        ===================================================== */}

        <section className="relative hidden overflow-hidden bg-[#eaf2ff] lg:block">

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
            transition={{
              delay: 0.2,
              duration: 0.7,
            }}
            className="absolute left-10 top-[31%] z-10 max-w-[440px]"
          >
            <p className="mb-3 text-[10px] font-bold uppercase tracking-[0.18em] text-[#3970e8]">
              Your learning journey starts here
            </p>

            <h1 className="text-[44px] font-bold leading-[1.02] tracking-[-0.055em] text-[#132038]">
              Stop learning
              <br />
              <span className="text-[#3265e8]">
                what you already know.
              </span>
            </h1>

            <p className="mt-5 max-w-[350px] text-[13px] leading-6 text-[#66758a]">
              LearnFlow figures out where you stand first, then
              builds the shortest path to where you want to go.
            </p>
          </motion.div>

          {/* Animated path */}

          <svg
            viewBox="0 0 600 400"
            className="absolute bottom-[-10px] left-[-30px] h-[55%] w-[115%]"
            fill="none"
          >
            <defs>
              <linearGradient
                id="registerPath"
                x1="40"
                y1="300"
                x2="550"
                y2="90"
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#c5dbff" />
                <stop
                  offset="0.5"
                  stopColor="#7da7f5"
                />
                <stop
                  offset="1"
                  stopColor="#b7d0ff"
                />
              </linearGradient>

              <filter
                id="registerGlow"
                x="-100%"
                y="-100%"
                width="300%"
                height="300%"
              >
                <feGaussianBlur stdDeviation="7" />
              </filter>
            </defs>

            <motion.path
              id="registerKnowledgePath"
              d="M30 350 C130 330 75 230 180 210 C280 190 230 90 330 100 C440 110 350 250 470 260 C530 265 510 160 580 120"
              stroke="#6e9cf4"
              strokeWidth="18"
              opacity="0.12"
              filter="url(#registerGlow)"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{
                duration: 2.2,
              }}
            />

            <motion.path
              d="M30 350 C130 330 75 230 180 210 C280 190 230 90 330 100 C440 110 350 250 470 260 C530 265 510 160 580 120"
              stroke="url(#registerPath)"
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{
                duration: 2.2,
              }}
            />

            <circle
              r="5"
              fill="#4c7fea"
            >
              <animateMotion
                dur="7s"
                repeatCount="indefinite"
                rotate="auto"
              >
                <mpath href="#registerKnowledgePath" />
              </animateMotion>
            </circle>
          </svg>

          {/* Floating card */}

          <motion.div
            animate={{
              y: [0, -6, 0],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="absolute right-[10%] top-[22%] rounded-xl border border-white bg-white/90 px-4 py-3 shadow-[0_12px_30px_rgba(47,86,145,0.12)] backdrop-blur"
          >
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#edf3ff] text-[#3970e8]">
                <Brain size={14} />
              </div>

              <div>
                <p className="text-[9px] font-semibold text-[#4c5768]">
                  AI-powered
                </p>

                <p className="mt-0.5 text-[8px] text-[#929baa]">
                  learning path
                </p>
              </div>
            </div>
          </motion.div>

          {/* Floating bottom card */}

          <motion.div
            animate={{
              y: [0, 6, 0],
            }}
            transition={{
              duration: 4.5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 1,
            }}
            className="absolute bottom-[23%] left-[11%] flex items-center gap-2 rounded-xl border border-white bg-white/90 px-3 py-2 shadow-[0_12px_30px_rgba(47,86,145,0.10)]"
          >
            <Check
              size={13}
              className="text-[#4ba887]"
            />

            <span className="text-[8px] font-semibold text-[#667285]">
              Learn less. Master more.
            </span>
          </motion.div>
        </section>

        {/* =====================================================
            RIGHT REGISTER
        ===================================================== */}

        <section className="flex items-center justify-center px-6 py-10 sm:px-12 lg:px-16">

          <motion.div
            initial={{
              opacity: 0,
              y: 20,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            transition={{
              duration: 0.65,
              ease: [0.22, 1, 0.36, 1],
            }}
            className="w-full max-w-[390px]"
          >

            {/* Mobile logo */}

            <div className="mb-8 flex items-center gap-2.5 lg:hidden">
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
                Create your account.
              </h2>

              <p className="mt-2 text-[13px] text-[#7a8595]">
                Let&apos;s build your learning path.
              </p>
            </div>

            {/* Form */}

            <form
              onSubmit={handleRegister}
              className="mt-8 space-y-4"
            >

              {/* Full name */}

              <div>
                <label
                  htmlFor="fullName"
                  className="mb-2 block text-[10px] font-semibold text-[#4e5969]"
                >
                  Full name
                </label>

                <div className="relative">
                  <UserRound
                    size={15}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-[#a0a9b7]"
                  />

                  <input
                    id="fullName"
                    type="text"
                    value={fullName}
                    onChange={(event) =>
                      setFullName(event.target.value)
                    }
                    placeholder="Your name"
                    autoComplete="name"
                    disabled={loading}
                    className="h-11 w-full rounded-xl border border-[#e0e6ef] bg-[#fbfcfe] pl-10 pr-4 text-[12px] outline-none transition placeholder:text-[#b0b7c2] focus:border-[#6f98ed] focus:bg-white focus:ring-4 focus:ring-[#e9f0ff] disabled:opacity-60"
                  />
                </div>
              </div>

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
                    value={email}
                    onChange={(event) =>
                      setEmail(event.target.value)
                    }
                    placeholder="you@example.com"
                    autoComplete="email"
                    disabled={loading}
                    className="h-11 w-full rounded-xl border border-[#e0e6ef] bg-[#fbfcfe] pl-10 pr-4 text-[12px] outline-none transition placeholder:text-[#b0b7c2] focus:border-[#6f98ed] focus:bg-white focus:ring-4 focus:ring-[#e9f0ff] disabled:opacity-60"
                  />
                </div>
              </div>

              {/* Password */}

              <div>
                <label
                  htmlFor="password"
                  className="mb-2 block text-[10px] font-semibold text-[#4e5969]"
                >
                  Password
                </label>

                <div className="relative">
                  <LockKeyhole
                    size={15}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-[#a0a9b7]"
                  />

                  <input
                    id="password"
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    value={password}
                    onChange={(event) =>
                      setPassword(event.target.value)
                    }
                    placeholder="At least 8 characters"
                    autoComplete="new-password"
                    disabled={loading}
                    className="h-11 w-full rounded-xl border border-[#e0e6ef] bg-[#fbfcfe] pl-10 pr-11 text-[12px] outline-none transition placeholder:text-[#b0b7c2] focus:border-[#6f98ed] focus:bg-white focus:ring-4 focus:ring-[#e9f0ff] disabled:opacity-60"
                  />

                  <button
                    type="button"
                    disabled={loading}
                    onClick={() =>
                      setShowPassword(
                        !showPassword,
                      )
                    }
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9ca5b3] transition hover:text-[#3970e8]"
                    aria-label={
                      showPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showPassword ? (
                      <EyeOff size={15} />
                    ) : (
                      <Eye size={15} />
                    )}
                  </button>
                </div>
              </div>

              {/* Confirm password */}

              <div>
                <label
                  htmlFor="confirmPassword"
                  className="mb-2 block text-[10px] font-semibold text-[#4e5969]"
                >
                  Confirm password
                </label>

                <div className="relative">
                  <LockKeyhole
                    size={15}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-[#a0a9b7]"
                  />

                  <input
                    id="confirmPassword"
                    type={
                      showConfirmPassword
                        ? "text"
                        : "password"
                    }
                    value={confirmPassword}
                    onChange={(event) =>
                      setConfirmPassword(
                        event.target.value,
                      )
                    }
                    placeholder="Re-enter your password"
                    autoComplete="new-password"
                    disabled={loading}
                    className="h-11 w-full rounded-xl border border-[#e0e6ef] bg-[#fbfcfe] pl-10 pr-11 text-[12px] outline-none transition placeholder:text-[#b0b7c2] focus:border-[#6f98ed] focus:bg-white focus:ring-4 focus:ring-[#e9f0ff] disabled:opacity-60"
                  />

                  <button
                    type="button"
                    disabled={loading}
                    onClick={() =>
                      setShowConfirmPassword(
                        !showConfirmPassword,
                      )
                    }
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9ca5b3] transition hover:text-[#3970e8]"
                    aria-label={
                      showConfirmPassword
                        ? "Hide confirm password"
                        : "Show confirm password"
                    }
                  >
                    {showConfirmPassword ? (
                      <EyeOff size={15} />
                    ) : (
                      <Eye size={15} />
                    )}
                  </button>
                </div>
              </div>

              {/* Error */}

              {error && (
                <motion.div
                  initial={{
                    opacity: 0,
                    y: -5,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                  }}
                  className="rounded-xl border border-[#f0caca] bg-[#fff4f4] px-3 py-2.5 text-[9px] leading-4 text-[#b34b4b]"
                >
                  {error}
                </motion.div>
              )}

              {/* Submit */}

              <button
                type="submit"
                disabled={loading}
                className="group mt-2 flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-[#121c2c] text-[11px] font-semibold text-white shadow-[0_8px_20px_rgba(18,28,44,0.15)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_12px_25px_rgba(18,28,44,0.2)] disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0"
              >
                {loading ? (
                  <>
                    <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                    Creating account...
                  </>
                ) : (
                  <>
                    Create account

                    <ArrowRight
                      size={13}
                      className="transition-transform group-hover:translate-x-1"
                    />
                  </>
                )}
              </button>
            </form>

            {/* Login link */}

            <p className="mt-7 text-center text-[10px] text-[#8993a1]">
              Already have an account?{" "}
              <Link
                href="/login"
                className="font-semibold text-[#3265e8] hover:underline"
              >
                Log in
              </Link>
            </p>

            {/* Privacy */}

            <div className="mt-6 flex items-center justify-center gap-2 text-[9px] text-[#a0a8b5]">
              <Check
                size={11}
                className="text-[#4ba887]"
              />
              Your learning data stays private.
            </div>
          </motion.div>
        </section>
      </div>
    </main>
  );
}