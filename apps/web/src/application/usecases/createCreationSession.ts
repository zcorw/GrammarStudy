import type { GrammarRepository } from "../ports/GrammarRepository";

export function createCreationSession(
  repository: GrammarRepository,
  grammarText: string,
  description?: string,
) {
  return repository.createCreationSession(grammarText, description);
}
