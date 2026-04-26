import type { GrammarRepository } from "../ports/GrammarRepository";

export function applyCreationFollowUp(
  repository: GrammarRepository,
  sessionId: string,
  question: string,
) {
  return repository.applyCreationFollowUp(sessionId, question);
}
