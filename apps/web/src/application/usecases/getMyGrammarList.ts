import type { GrammarRepository } from "../ports/GrammarRepository";
import type { UserGrammarListItem } from "../../domain/grammar/entities";

export function getMyGrammarList(
  repository: GrammarRepository,
): Promise<UserGrammarListItem[]> {
  return repository.listMyGrammar();
}
