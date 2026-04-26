import type { GrammarRepository } from "../ports/GrammarRepository";

export function getUserRecent(repository: GrammarRepository) {
  return repository.getUserRecent();
}
