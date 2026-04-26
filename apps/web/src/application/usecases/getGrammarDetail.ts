import type { GrammarRepository } from "../ports/GrammarRepository";
import type { GrammarEntry } from "../../domain/grammar/entities";

export function getGrammarDetail(
  repository: GrammarRepository,
  grammarId: string,
): Promise<GrammarEntry | null> {
  return repository.getById(grammarId);
}
