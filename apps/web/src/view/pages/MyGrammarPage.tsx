import { Button, CardActionArea, Chip, Paper, Stack, TextField, Typography } from "@mui/material";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link as RouterLink } from "react-router-dom";

import type { UserGrammarListItem, UserRecent } from "../../domain/grammar/entities";
import { AsyncState } from "../components/AsyncState";
import { PageStack, SectionHead, Surface } from "../components/Surface";

type MyGrammarPageProps = {
  getMyGrammarList: () => Promise<UserGrammarListItem[]>;
  getUserRecent: () => Promise<UserRecent>;
};

export function MyGrammarPage({
  getMyGrammarList,
  getUserRecent,
}: MyGrammarPageProps) {
  const [items, setItems] = useState<UserGrammarListItem[]>([]);
  const [recent, setRecent] = useState<UserRecent | null>(null);
  const [keyword, setKeyword] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadMyGrammar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [itemResult, recentResult] = await Promise.all([
        getMyGrammarList(),
        getUserRecent(),
      ]);
      setItems(itemResult);
      setRecent(recentResult);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "我的文法加载失败");
    } finally {
      setLoading(false);
    }
  }, [getMyGrammarList, getUserRecent]);

  useEffect(() => {
    void loadMyGrammar();
  }, [loadMyGrammar]);

  const filteredItems = useMemo(() => {
    const trimmed = keyword.trim().toLowerCase();
    if (!trimmed) {
      return items;
    }
    return items.filter((item) => item.title.toLowerCase().includes(trimmed));
  }, [items, keyword]);

  return (
    <PageStack>
      <Surface>
        <SectionHead title="我的文法" meta="按最近学习 / 浏览排序" />
        <TextField
          onChange={(event) => setKeyword(event.target.value)}
          placeholder="搜索我学过、收藏或创建的文法"
          value={keyword}
        />
      </Surface>

      <AsyncState loading={loading} error={error} onRetry={loadMyGrammar} />

      {!loading && !error && recent ? (
        <Surface>
          <SectionHead title="近期概览" meta="真实用户数据" />
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
            <Chip color="primary" label={`最近浏览 ${recent.recent_views.length}`} />
            <Chip label={`练习记录 ${recent.practice_records.length}`} variant="outlined" />
            <Chip label={`收藏 ${recent.favorites.length}`} variant="outlined" />
          </Stack>
        </Surface>
      ) : null}

      {!loading && !error ? (
        <Surface>
          <Stack spacing={1.5}>
            {filteredItems.length === 0 ? (
              <Paper sx={{ p: 2 }}>
                <Stack spacing={1.5}>
                <Typography variant="h3">还没有可展示的文法</Typography>
                <Typography>先去搜索学习，或登录后完成一条创建流程。</Typography>
                <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
                  <Button color="secondary" component={RouterLink} to="/search" variant="contained">
                    去搜索
                  </Button>
                  <Button color="secondary" component={RouterLink} to="/create" variant="contained">
                    去创建
                  </Button>
                  <Button component={RouterLink} to="/login" variant="outlined">
                    去登录
                  </Button>
                </Stack>
                </Stack>
              </Paper>
            ) : (
              filteredItems.map((item) => (
                <Paper key={`${item.source}-${item.id}`} sx={{ overflow: "hidden" }}>
                  <CardActionArea component={RouterLink} sx={{ p: 2 }} to={`/grammar/${item.id}`}>
                    <SectionHead
                      title={item.title}
                      meta={item.source === "created" ? "我创建的" : "我收藏的"}
                    />
                    <Typography color="text.secondary">
                      最后活动时间：{new Date(item.last_activity_at).toLocaleString()}
                    </Typography>
                  </CardActionArea>
                </Paper>
              ))
            )}
          </Stack>
        </Surface>
      ) : null}
    </PageStack>
  );
}
