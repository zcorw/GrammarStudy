export const AUTH_REQUIRED_EVENT = "grammar-study:auth-required";

export type AuthRequiredEventDetail = {
  message: string;
};

export function notifyAuthRequired(message: string) {
  window.dispatchEvent(
    new CustomEvent<AuthRequiredEventDetail>(AUTH_REQUIRED_EVENT, {
      detail: { message },
    }),
  );
}
