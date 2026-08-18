"use client";

import { ReactNode, useEffect, useState } from "react";
import { Brain } from "lucide-react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { verifyAuthentication } from "@/lib/auth";

type AuthGuardProps = {
  children: ReactNode;
};

export default function AuthGuard({
  children,
}: AuthGuardProps) {
  const router = useRouter();

  const [checking, setChecking] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    let mounted = true;

    async function checkAuthentication() {
      const user = await verifyAuthentication();

      if (!mounted) {
        return;
      }

      if (!user) {
        router.replace("/login");
        return;
      }

      setAuthenticated(true);
      setChecking(false);
    }

    checkAuthentication();

    return () => {
      mounted = false;
    };
  }, [router]);

  if (checking) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#eef4fb]">
        <div className="flex flex-col items-center">

          <motion.div
            animate={{
              y: [0, -4, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white text-[#3970e8] shadow-[0_10px_30px_rgba(48,78,125,0.10)]"
          >
            <Brain size={20} />
          </motion.div>

          <div className="mt-5 h-1 w-32 overflow-hidden rounded-full bg-[#dce6f4]">
            <motion.div
              initial={{ x: "-100%" }}
              animate={{ x: "200%" }}
              transition={{
                duration: 1.4,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="h-full w-1/2 rounded-full bg-[#3970e8]"
            />
          </div>

          <p className="mt-3 text-[9px] font-medium text-[#8994a4]">
            Checking your learning space...
          </p>
        </div>
      </main>
    );
  }

  if (!authenticated) {
    return null;
  }

  return <>{children}</>;
}