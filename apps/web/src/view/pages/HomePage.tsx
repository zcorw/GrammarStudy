import { Button, CardActionArea, Chip, Paper, Stack, TextField, Typography } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import type { GrammarEntry } from "../../domain/grammar/entities";
import { AsyncState } from "../components/AsyncState";
import { PageStack, SectionHead, Surface } from "../components/Surface";

type HomePageProps = {
  getRecommendedGrammar: () => Promise<GrammarEntry[]>;
};

export function HomePage({ getRecommendedGrammar }: HomePageProps) {
  const [query, setQuery] = useState("");
  const [recommended, setRecommended] = useState<GrammarEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const loadRecommended = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await getRecommendedGrammar();
      setRecommended(items);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "推荐文法加载失败");
    } finally {
      setLoading(false);
    }
  }, [getRecommendedGrammar]);

  useEffect(() => {
    void loadRecommended();
  }, [loadRecommended]);

  const handleSearch = () => {
    const trimmed = query.trim();
    if (!trimmed) {
      return;
    }
    navigate(`/search?q=${encodeURIComponent(trimmed)}`);
  };

  return (
    <PageStack>
      <Surface hero>
        <Stack spacing={2}>
        <Typography color="primary" sx={{ fontSize: 12, fontWeight: 700 }}>
          推荐优先
        </Typography>
        <Typography variant="h1">先看公共文法，再决定是否创建</Typography>
        <Typography>
          首版首页优先承接推荐内容与搜索学习。创建动作延后到搜索后的推荐复用阶段。
        </Typography>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
          <TextField
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="输入文法关键词或句型"
          />
          <Button onClick={handleSearch} type="button" variant="contained">
            搜索
          </Button>
        </Stack>
        </Stack>
      </Surface>

      <AsyncState loading={loading} error={error} onRetry={loadRecommended} />

      {!loading && !error ? <Surface>
        <SectionHead title="推荐文法" meta="移动端优先" />
        <Stack spacing={1.5}>
          {recommended.map((grammar) => (
            <Paper key={grammar.id} sx={{ overflow: "hidden" }}>
              <CardActionArea component={RouterLink} sx={{ p: 2 }} to={`/grammar/${grammar.id}`}>
              <Stack spacing={1}>
                <Stack direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
                <Chip color="primary" label={grammar.level} size="small" />
                {grammar.tags.slice(0, 2).map((tag) => (
                  <Chip key={tag} label={tag} size="small" variant="outlined" />
                ))}
                </Stack>
              <Typography variant="h3">{grammar.title}</Typography>
              <Typography>{grammar.meaning}</Typography>
              </Stack>
              </CardActionArea>
            </Paper>
          ))}
        </Stack>
      </Surface> : null}
    </PageStack>
  );
}
