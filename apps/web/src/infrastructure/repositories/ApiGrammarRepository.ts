import type { GrammarRepository } from "../../application/ports/GrammarRepository";
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
import { HttpError, httpRequest } from "../api/httpClient";

type GrammarSummaryDto = Omit<GrammarEntry, "questions">;

type SearchGrammarDto = {
  best_match: GrammarSummaryDto | null;
  similar_cards: GrammarSummaryDto[];
  search_confidence: number;
  should_offer_ai_generation: boolean;
};

type MyGrammarResponse = {
  items: UserGrammarListItem[];
};

export class ApiGrammarRepository implements GrammarRepository {
  listRecommended(): Promise<GrammarEntry[]> {
    return httpRequest<GrammarEntry[]>("/grammar/recommended");
  }

  async getById(id: string): Promise<GrammarEntry | null> {
    try {
      return await httpRequest<GrammarEntry>(`/grammar/${id}`);
    } catch (error) {
      if (error instanceof HttpError && error.status === 404) {
        return null;
      }
      throw error;
    }
  }

  async search(query: string): Promise<SearchGrammarResult> {
    const result = await httpRequest<SearchGrammarDto>(
      `/search/grammar?q=${encodeURIComponent(query)}`,
    );

    return {
      best_match: result.best_match
        ? { ...result.best_match, questions: [] }
        : null,
      similar_cards: result.similar_cards.map((item) => ({
        ...item,
        questions: [],
      })),
      search_confidence: result.search_confidence,
      should_offer_ai_generation: result.should_offer_ai_generation,
    };
  }

  async listMyGrammar(): Promise<UserGrammarListItem[]> {
    const result = await httpRequest<MyGrammarResponse>("/user/my-grammar");
    return result.items;
  }

  getUserRecent(): Promise<UserRecent> {
    return httpRequest<UserRecent>("/user/recent");
  }

  register(
    email: string,
    password: string,
    inviteCode?: string,
  ): Promise<RegistrationResult> {
    return httpRequest<RegistrationResult>("/auth/register", {
      method: "POST",
      auth: "omit",
      body: {
        email,
        password,
        invite_code: inviteCode || undefined,
      },
    });
  }

  login(email: string, password: string): Promise<LoginResult> {
    return httpRequest<LoginResult>("/auth/login", {
      method: "POST",
      auth: "omit",
      body: {
        email,
        password,
      },
    });
  }

  submitChoice(
    grammarId: string,
    selectedOption: string,
  ): Promise<ChoiceSubmitResult> {
    return httpRequest<ChoiceSubmitResult>("/practice/choice/submit", {
      method: "POST",
      body: {
        grammar_id: grammarId,
        selected_option: selectedOption,
      },
    });
  }

  submitSentenceFeedback(
    grammarId: string,
    sentence: string,
  ): Promise<SentenceFeedbackResult> {
    return httpRequest<SentenceFeedbackResult>("/practice/sentence-feedback", {
      method: "POST",
      body: {
        grammar_id: grammarId,
        sentence,
      },
    });
  }

  createCreationSession(
    grammarText: string,
    description?: string,
  ): Promise<CreationSession> {
    return httpRequest<CreationSession>("/creation/sessions", {
      method: "POST",
      body: {
        grammar_text: grammarText,
        description,
      },
    });
  }

  getCreationSession(sessionId: string): Promise<CreationSession> {
    return httpRequest<CreationSession>(`/creation/sessions/${sessionId}`);
  }

  applyCreationFollowUp(
    sessionId: string,
    question: string,
  ): Promise<CreationSession> {
    return httpRequest<CreationSession>(`/creation/sessions/${sessionId}/follow-up`, {
      method: "POST",
      body: {
        question,
      },
    });
  }

  completeCreationSession(sessionId: string): Promise<CreationCompletion> {
    return httpRequest<CreationCompletion>(`/creation/sessions/${sessionId}/complete`, {
      method: "POST",
    });
  }

  toggleFavorite(grammarId: string): Promise<FavoriteToggleResult> {
    return httpRequest<FavoriteToggleResult>(`/user/favorites/${grammarId}`, {
      method: "POST",
    });
  }

  recordRecentView(grammarId: string): Promise<void> {
    return httpRequest<void>(`/user/recent-views/${grammarId}`, {
      method: "POST",
    });
  }
}
