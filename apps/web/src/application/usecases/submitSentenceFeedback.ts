import type { GrammarRepository } from "../ports/GrammarRepository";
import type { SentenceFeedbackResult } from "../../domain/grammar/entities";

export function submitSentenceFeedback(
  repository: GrammarRepository,
  grammarId: string,
  sentence: string,
): Promise<SentenceFeedbackResult> {
  return repository.submitSentenceFeedback(grammarId, sentence);
}
