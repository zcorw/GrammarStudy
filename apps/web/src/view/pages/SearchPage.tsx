import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { Link as RouterLink, useSearchParams } from "react-router-dom";

import type {
  FavoriteToggleResult,
  GrammarEntry,
  SearchGrammarResult,
} from "../../domain/grammar/entities";
import { AsyncState } from "../components/AsyncState";
import { GrammarCard } from "../components/GrammarCard";
import { PageStack, SectionHead, Surface } from "../components/Surface";

type SearchPageProps = {
  searchGrammarEntries: (query: string) => Promise<SearchGrammarResult>;
  toggleFavorite: (grammarId: string) => Promise<FavoriteToggleResult>;
};

export function SearchPage({
  searchGrammarEntries,
  toggleFavorite,
}: SearchPageProps) {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get("q") ?? "";
  const [result, setResult] = useState<SearchGrammarResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [favoriteMessage, setFavoriteMessage] = useState<string | null>(null);

  const loadSearch = useCallback(async () => {
    if (!query.trim()) {
      setResult(null);
      setLoading(false);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const nextResult = await searchGrammarEntries(query.trim());
      setResult(nextResult);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "搜索失败");
    } finally {
      setLoading(false);
    }
  }, [query, searchGrammarEntries]);

  useEffect(() => {
    void loadSearch();
  }, [loadSearch]);

  const cards = result
    ? ([result.best_match, ...result.similar_cards].filter(Boolean) as GrammarEntry[])
    : [];
  const grammar = cards[0];
  const hasSearched = Boolean(query.trim() && result);

  const handleFavorite = async () => {
    if (!grammar) {
      return;
    }

    try {
      const mutation = await toggleFavorite(grammar.id);
      setFavoriteMessage(mutation.is_favorite ? "已加入收藏。" : "已取消收藏。");
    } catch (favoriteError) {
      setFavoriteMessage(
        favoriteError instanceof Error ? favoriteError.message : "收藏操作失败",
      );
    }
  };

  return (
    <PageStack>
      <Surface>
        <SectionHead title="推荐复用" meta="与详情页共用卡片骨架" />
        <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
          <TextField
            value={query}
            onChange={(event) =>
              setSearchParams(
                event.target.value ? { q: event.target.value } : {},
                { replace: true },
              )
            }
            placeholder="输入文法关键词或句型"
          />
          <Button
            component={RouterLink}
            to={`/search?q=${encodeURIComponent(query)}`}
            variant="contained"
          >
            重新搜索
          </Button>
        </Stack>
      </Surface>

      <AsyncState loading={loading} error={error} onRetry={loadSearch} />

      {grammar ? (
        <>
          <GrammarCard grammar={grammar} />
          <Surface>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
            <Button component={RouterLink} to={`/grammar/${grammar.id}`} variant="contained">
              开始学习
            </Button>
            <Button
              color="secondary"
              component={RouterLink}
              to={`/create?q=${encodeURIComponent(query)}`}
              variant="contained"
            >
              继续创建
            </Button>
            <Button onClick={() => void handleFavorite()} type="button" variant="outlined">
              收藏
            </Button>
            </Stack>
          </Surface>
          {favoriteMessage ? (
            <Alert severity="info">{favoriteMessage}</Alert>
          ) : null}
        </>
      ) : !loading && !error && hasSearched ? (
        <Surface>
          <Stack spacing={1.5}>
          <SectionHead title="没有匹配的文法" meta="可以手动创建" />
          <Typography>
            公共库里暂时没有找到“{query.trim()}”的最佳匹配或相近文法。你可以从当前输入开始创建一条新文法。
          </Typography>
          <Button
            component={RouterLink}
            to={`/create?q=${encodeURIComponent(query.trim())}`}
            variant="contained"
          >
            手动创建文法
          </Button>
          </Stack>
        </Surface>
      ) : !loading && !error ? (
        <Surface>
          <Typography>输入文法后，这里会优先展示最佳匹配和相近文法。</Typography>
        </Surface>
      ) : null}
    </PageStack>
  );
}
