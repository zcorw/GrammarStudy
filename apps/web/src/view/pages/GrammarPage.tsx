import { Alert, Button, Stack, Typography } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { Link as RouterLink, useParams } from "react-router-dom";

import type { FavoriteToggleResult, GrammarEntry } from "../../domain/grammar/entities";
import { AsyncState } from "../components/AsyncState";
import { GrammarCard } from "../components/GrammarCard";
import { PageStack, Surface } from "../components/Surface";

type GrammarPageProps = {
  getGrammarDetail: (grammarId: string) => Promise<GrammarEntry | null>;
  toggleFavorite: (grammarId: string) => Promise<FavoriteToggleResult>;
  recordRecentView: (grammarId: string) => Promise<void>;
};

export function GrammarPage({
  getGrammarDetail,
  toggleFavorite,
  recordRecentView,
}: GrammarPageProps) {
  const { id = "" } = useParams();
  const [grammar, setGrammar] = useState<GrammarEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [favoriteMessage, setFavoriteMessage] = useState<string | null>(null);

  const loadGrammar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const item = await getGrammarDetail(id);
      setGrammar(item);
      if (!item) {
        setError("未找到对应文法。");
        return;
      }
      void recordRecentView(id).catch(() => undefined);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "文法详情加载失败");
    } finally {
      setLoading(false);
    }
  }, [getGrammarDetail, id, recordRecentView]);

  useEffect(() => {
    void loadGrammar();
  }, [loadGrammar]);

  const handleToggleFavorite = async () => {
    if (!grammar) {
      return;
    }

    try {
      const result = await toggleFavorite(grammar.id);
      setFavoriteMessage(result.is_favorite ? "已加入收藏。" : "已取消收藏。");
    } catch (favoriteError) {
      setFavoriteMessage(
        favoriteError instanceof Error ? favoriteError.message : "收藏操作失败",
      );
    }
  };

  if (loading || error) {
    return (
      <PageStack>
        <AsyncState loading={loading} error={error} onRetry={loadGrammar} />
      </PageStack>
    );
  }

  if (!grammar) {
    return (
      <PageStack>
        <Surface>
          <Typography>未找到对应文法。</Typography>
        </Surface>
      </PageStack>
    );
  }

  return (
    <PageStack>
      <GrammarCard grammar={grammar} />
      <Surface>
        <Stack spacing={1.5}>
        <Button component={RouterLink} to={`/practice/${grammar.id}`} variant="contained">
          开始练习
        </Button>
        <Button
          color="secondary"
          component={RouterLink}
          to={`/sentence/${grammar.id}`}
          variant="contained"
        >
          去自由造句点评
        </Button>
        <Button onClick={() => void handleToggleFavorite()} type="button" variant="outlined">
          收藏这条文法
        </Button>
        {favoriteMessage ? <Alert severity="info">{favoriteMessage}</Alert> : null}
        </Stack>
      </Surface>
    </PageStack>
  );
}
