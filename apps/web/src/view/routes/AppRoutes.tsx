import { useEffect } from "react";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";

import {
  AUTH_REQUIRED_EVENT,
  type AuthRequiredEventDetail,
} from "../../infrastructure/auth/authEvents";
import { webContainer } from "../../infrastructure/container";
import { CreatePage } from "../pages/CreatePage";
import { GrammarPage } from "../pages/GrammarPage";
import { HomePage } from "../pages/HomePage";
import { LoginPage } from "../pages/LoginPage";
import { MyGrammarPage } from "../pages/MyGrammarPage";
import { PracticePage } from "../pages/PracticePage";
import { RegisterPage } from "../pages/RegisterPage";
import { SearchPage } from "../pages/SearchPage";
import { SentencePage } from "../pages/SentencePage";

export function AppRoutes() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleAuthRequired = (event: Event) => {
      const authEvent = event as CustomEvent<AuthRequiredEventDetail>;
      const currentPath = `${location.pathname}${location.search}`;
      const loginParams = new URLSearchParams({
        error: authEvent.detail.message,
      });

      if (location.pathname !== "/login") {
        loginParams.set("return", currentPath);
      }

      navigate(`/login?${loginParams.toString()}`, { replace: true });
    };

    window.addEventListener(AUTH_REQUIRED_EVENT, handleAuthRequired);
    return () => {
      window.removeEventListener(AUTH_REQUIRED_EVENT, handleAuthRequired);
    };
  }, [location.pathname, location.search, navigate]);

  return (
    <Routes>
      <Route
        path="/"
        element={<HomePage getRecommendedGrammar={webContainer.getRecommendedGrammar} />}
      />
      <Route
        path="/search"
        element={
          <SearchPage
            searchGrammarEntries={webContainer.searchGrammarEntries}
            toggleFavorite={webContainer.toggleFavorite}
          />
        }
      />
      <Route
        path="/grammar/:id"
        element={
          <GrammarPage
            getGrammarDetail={webContainer.getGrammarDetail}
            toggleFavorite={webContainer.toggleFavorite}
            recordRecentView={webContainer.recordRecentView}
          />
        }
      />
      <Route
        path="/practice/:id"
        element={
          <PracticePage
            getGrammarDetail={webContainer.getGrammarDetail}
            submitPracticeChoice={webContainer.submitPracticeChoice}
          />
        }
      />
      <Route
        path="/create"
        element={
          <CreatePage
            createCreationSession={webContainer.createCreationSession}
            applyCreationFollowUp={webContainer.applyCreationFollowUp}
            completeCreationSession={webContainer.completeCreationSession}
          />
        }
      />
      <Route
        path="/sentence/:id"
        element={
          <SentencePage
            getGrammarDetail={webContainer.getGrammarDetail}
            submitSentenceFeedback={webContainer.submitSentenceFeedback}
          />
        }
      />
      <Route
        path="/login"
        element={<LoginPage loginWithEmail={webContainer.loginWithEmail} />}
      />
      <Route
        path="/register"
        element={<RegisterPage registerWithEmail={webContainer.registerWithEmail} />}
      />
      <Route
        path="/my"
        element={
          <MyGrammarPage
            getMyGrammarList={webContainer.getMyGrammarList}
            getUserRecent={webContainer.getUserRecent}
          />
        }
      />
    </Routes>
  );
}
