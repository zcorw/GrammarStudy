import type { GrammarRepository } from "../ports/GrammarRepository";

export function toggleFavorite(
  repository: GrammarRepository,
  grammarId: string,
) {
  return repository.toggleFavorite(grammarId);
}
