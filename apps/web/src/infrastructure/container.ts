import { applyCreationFollowUp } from "../application/usecases/applyCreationFollowUp";
import { completeCreationSession } from "../application/usecases/completeCreationSession";
import { createCreationSession } from "../application/usecases/createCreationSession";
import { getCreationSession } from "../application/usecases/getCreationSession";
import { getGrammarDetail } from "../application/usecases/getGrammarDetail";
import { getMyGrammarList } from "../application/usecases/getMyGrammarList";
import { getRecommendedGrammar } from "../application/usecases/getRecommendedGrammar";
import { getUserRecent } from "../application/usecases/getUserRecent";
import { loginWithEmail } from "../application/usecases/loginWithEmail";
import { recordRecentView } from "../application/usecases/recordRecentView";
import { registerWithEmail } from "../application/usecases/registerWithEmail";
import { searchGrammarEntries } from "../application/usecases/searchGrammarEntries";
import { submitPracticeChoice } from "../application/usecases/submitPracticeChoice";
import { submitSentenceFeedback } from "../application/usecases/submitSentenceFeedback";
import { toggleFavorite } from "../application/usecases/toggleFavorite";
import { ApiGrammarRepository } from "./repositories/ApiGrammarRepository";

const grammarRepository = new ApiGrammarRepository();

export const webContainer = {
  getGrammarDetail: (grammarId: string) =>
    getGrammarDetail(grammarRepository, grammarId),
  getRecommendedGrammar: () => getRecommendedGrammar(grammarRepository),
  searchGrammarEntries: (query: string) =>
    searchGrammarEntries(grammarRepository, query),
  getMyGrammarList: () => getMyGrammarList(grammarRepository),
  getUserRecent: () => getUserRecent(grammarRepository),
  registerWithEmail: (email: string, password: string, inviteCode?: string) =>
    registerWithEmail(grammarRepository, email, password, inviteCode),
  loginWithEmail: (email: string, password: string) =>
    loginWithEmail(grammarRepository, email, password),
  submitPracticeChoice: (grammarId: string, selectedOption: string) =>
    submitPracticeChoice(grammarRepository, grammarId, selectedOption),
  submitSentenceFeedback: (grammarId: string, sentence: string) =>
    submitSentenceFeedback(grammarRepository, grammarId, sentence),
  createCreationSession: (grammarText: string, description?: string) =>
    createCreationSession(grammarRepository, grammarText, description),
  getCreationSession: (sessionId: string) =>
    getCreationSession(grammarRepository, sessionId),
  applyCreationFollowUp: (sessionId: string, question: string) =>
    applyCreationFollowUp(grammarRepository, sessionId, question),
  completeCreationSession: (sessionId: string) =>
    completeCreationSession(grammarRepository, sessionId),
  toggleFavorite: (grammarId: string) => toggleFavorite(grammarRepository, grammarId),
  recordRecentView: (grammarId: string) =>
    recordRecentView(grammarRepository, grammarId),
};
