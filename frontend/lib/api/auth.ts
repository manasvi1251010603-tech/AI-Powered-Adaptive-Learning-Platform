import { apiClient } from "./client";

export type LoginRequest = {
  email: string;
  password: string;
};

export type RegisterRequest = {
  email: string;
  password: string;
  full_name: string;
};

export type TokenResponse = {
  access_token: string;
};

export type UserResponse = {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
};

export async function login(
  payload: LoginRequest,
): Promise<TokenResponse> {
  return apiClient<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function register(
  payload: RegisterRequest,
): Promise<UserResponse> {
  return apiClient<UserResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getCurrentUser(
  token: string,
): Promise<UserResponse> {
  return apiClient<UserResponse>("/auth/me", {
    method: "GET",
    token,
  });
} 