import type { GrammarRepository } from "../ports/GrammarRepository";
import type { LoginResult } from "../../domain/grammar/entities";

export function loginWithEmail(
  repository: GrammarRepository,
  email: string,
  password: string,
): Promise<LoginResult> {
  return repository.login(email, password);
}
