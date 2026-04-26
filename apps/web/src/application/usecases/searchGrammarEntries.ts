import type { GrammarRepository } from "../ports/GrammarRepository";
import type { SearchGrammarResult } from "../../domain/grammar/entities";

export function searchGrammarEntries(
  repository: GrammarRepository,
  query: string,
): Promise<SearchGrammarResult> {
  return repository.search(query);
}
