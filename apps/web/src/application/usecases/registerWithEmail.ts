import type { RegistrationResult } from "../../domain/grammar/entities";
import type { GrammarRepository } from "../ports/GrammarRepository";

export function registerWithEmail(
  repository: GrammarRepository,
  email: string,
  password: string,
  inviteCode?: string,
): Promise<RegistrationResult> {
  return repository.register(email, password, inviteCode);
}
