import type { GrammarRepository } from "../ports/GrammarRepository";
import type { GrammarEntry } from "../../domain/grammar/entities";

export function getRecommendedGrammar(
  repository: GrammarRepository,
): Promise<GrammarEntry[]> {
  return repository.listRecommended();
}
