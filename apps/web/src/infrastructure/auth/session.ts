import type { LoginResult } from "../../domain/grammar/entities";

const STORAGE_KEY = "grammar-study-session";

type StoredSession = Pick<
  LoginResult,
  | "user_id"
  | "email"
  | "access_state"
  | "is_admin"
  | "access_token"
  | "token_type"
  | "expires_in"
>;

export function saveAuthSession(result: LoginResult) {
  const payload: StoredSession = {
    user_id: result.user_id,
    email: result.email,
    access_state: result.access_state,
    is_admin: result.is_admin,
    access_token: result.access_token,
    token_type: result.token_type,
    expires_in: result.expires_in,
  };
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

export function clearAuthSession() {
  window.localStorage.removeItem(STORAGE_KEY);
}

export function getAuthSession(): StoredSession | null {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as StoredSession;
  } catch {
    clearAuthSession();
    return null;
  }
}

export function getAccessToken() {
  return getAuthSession()?.access_token ?? null;
}

export function isLoggedIn() {
  return getAuthSession() !== null;
}

export function isApprovedUser() {
  return getAuthSession()?.access_state === "approved";
}
