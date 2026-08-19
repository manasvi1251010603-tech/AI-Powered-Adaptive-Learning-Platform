import { getCurrentUser } from "@/lib/api/auth";
import { register } from "@/lib/api/auth";
const TOKEN_KEY = "access_token";
const USER_KEY = "current_user";

export function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser<T = unknown>(): T | null {
  if (typeof window === "undefined") {
    return null;
  }

  const storedUser = localStorage.getItem(USER_KEY);

  if (!storedUser) {
    return null;
  }

  try {
    return JSON.parse(storedUser) as T;
  } catch {
    return null;
  }
}

export async function verifyAuthentication() {
  const token = getToken();

  if (!token) {
    return null;
  }

  try {
    const user = await getCurrentUser(token);

    localStorage.setItem(
      USER_KEY,
      JSON.stringify(user),
    );

    return user;
  } catch {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);

    return null;
  }
}

export function logout(): void {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);

  window.location.href = "/login";
}