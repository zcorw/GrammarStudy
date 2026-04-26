import { notifyAuthRequired } from "../auth/authEvents";
import { clearAuthSession, getAccessToken } from "../auth/session";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export class HttpError extends Error {
  status: number;
  code?: string;
  details?: unknown;

  constructor(status: number, message: string, code?: string, details?: unknown) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

type RequestOptions = {
  method?: "GET" | "POST";
  body?: unknown;
  auth?: "auto" | "omit";
};

export async function httpRequest<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const accessToken = options.auth === "omit" ? null : getAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const raw = await response.text();
    let parsedError:
      | { error?: { code?: string; message?: string; details?: unknown } }
      | null;
    try {
      parsedError = JSON.parse(raw) as {
        error?: { code?: string; message?: string; details?: unknown };
      };
    } catch {
      parsedError = null;
    }

    const message =
      parsedError?.error?.message ?? raw ?? `Request failed: ${response.status}`;

    if (response.status === 401 && options.auth !== "omit") {
      clearAuthSession();
      notifyAuthRequired(message || "登录已失效，请重新登录。");
    }

    throw new HttpError(
      response.status,
      message,
      parsedError?.error?.code,
      parsedError?.error?.details,
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
