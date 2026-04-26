import type {
  ChoiceSubmitResult,
  CreationCompletion,
  CreationSession,
  FavoriteToggleResult,
  GrammarEntry,
  LoginResult,
  RegistrationResult,
  SearchGrammarResult,
  SentenceFeedbackResult,
  UserGrammarListItem,
  UserRecent,
} from "../../domain/grammar/entities";

export interface GrammarRepository {
  listRecommended(): Promise<GrammarEntry[]>;
  getById(id: string): Promise<GrammarEntry | null>;
  search(query: string): Promise<SearchGrammarResult>;
  listMyGrammar(): Promise<UserGrammarListItem[]>;
  getUserRecent(): Promise<UserRecent>;
  register(email: string, password: string, inviteCode?: string): Promise<RegistrationResult>;
  login(email: string, password: string): Promise<LoginResult>;
  submitChoice(grammarId: string, selectedOption: string): Promise<ChoiceSubmitResult>;
  submitSentenceFeedback(
    grammarId: string,
    sentence: string,
  ): Promise<SentenceFeedbackResult>;
  createCreationSession(
    grammarText: string,
    description?: string,
  ): Promise<CreationSession>;
  getCreationSession(sessionId: string): Promise<CreationSession>;
  applyCreationFollowUp(
    sessionId: string,
    question: string,
  ): Promise<CreationSession>;
  completeCreationSession(sessionId: string): Promise<CreationCompletion>;
  toggleFavorite(grammarId: string): Promise<FavoriteToggleResult>;
  recordRecentView(grammarId: string): Promise<void>;
}
