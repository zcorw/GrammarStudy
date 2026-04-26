import type { GrammarRepository } from "../ports/GrammarRepository";

export function recordRecentView(
  repository: GrammarRepository,
  grammarId: string,
) {
  return repository.recordRecentView(grammarId);
}
