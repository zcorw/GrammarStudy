import type { GrammarRepository } from "../ports/GrammarRepository";
import type { ChoiceSubmitResult } from "../../domain/grammar/entities";

export function submitPracticeChoice(
  repository: GrammarRepository,
  grammarId: string,
  selectedOption: string,
): Promise<ChoiceSubmitResult> {
  return repository.submitChoice(grammarId, selectedOption);
}
