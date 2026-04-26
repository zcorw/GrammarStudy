import type { GrammarRepository } from "../ports/GrammarRepository";

export function completeCreationSession(
  repository: GrammarRepository,
  sessionId: string,
) {
  return repository.completeCreationSession(sessionId);
}
