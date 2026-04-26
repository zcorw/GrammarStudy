export type GrammarExample = {
  japanese: string;
  chinese: string;
};

export type PracticeQuestion = {
  question: string;
  options: string[];
  explanation: string;
};

export type GrammarEntry = {
  id: string;
  title: string;
  meaning: string;
  level: string;
  tags: string[];
  connection: string;
  context: string;
  examples: GrammarExample[];
  questions: PracticeQuestion[];
};

export type SearchGrammarResult = {
  best_match: GrammarEntry | null;
  similar_cards: GrammarEntry[];
  search_confidence: number;
  should_offer_ai_generation: boolean;
};

export type UserGrammarListItem = {
  id: string;
  title: string;
  source: string;
  last_activity_at: string;
};

export type UserRecent = {
  recent_views: string[];
  practice_records: string[];
  favorites: string[];
};

export type LoginResult = {
  user_id: number;
  email: string;
  access_state: string;
  is_admin: boolean;
  approval_mode: string;
  access_token: string;
  token_type: string;
  expires_in: number;
};

export type RegistrationResult = {
  user_id: number;
  email: string;
  access_state: string;
  is_admin: boolean;
  approval_mode: string;
};

export type ChoiceSubmitResult = {
  grammar_id: string;
  selected_option: string;
  result: string;
};

export type SentenceFeedbackResult = {
  grammar_id: string;
  feedback: string;
};

export type FavoriteToggleResult = {
  grammar_id: string;
  is_favorite: boolean;
};

export type GeneratedGrammarDraft = {
  title: string;
  meaning: string;
  level: string;
  tags: string[];
  connection: string;
  context: string;
  examples: GrammarExample[];
  questions: PracticeQuestion[];
};

export type CreationSession = {
  id: string;
  grammar_text: string;
  description: string | null;
  status: string;
  next_step: string;
  draft_card: GeneratedGrammarDraft;
  follow_up_history: string[];
  published_grammar_id: string | null;
};

export type CreationCompletion = {
  card_id: string;
  status: string;
};
