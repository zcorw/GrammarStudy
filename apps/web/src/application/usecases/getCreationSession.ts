import type { GrammarRepository } from "../ports/GrammarRepository";

export function getCreationSession(
  repository: GrammarRepository,
  sessionId: string,
) {
  return repository.getCreationSession(sessionId);
}
