import {
  Alert,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useMemo, useState } from "react";
import { Link as RouterLink, useSearchParams } from "react-router-dom";

import type {
  CreationCompletion,
  CreationSession,
} from "../../domain/grammar/entities";
import { ConnectionList } from "../components/ConnectionList";
import { PageStack, SectionHead, Surface } from "../components/Surface";

type CreatePageProps = {
  createCreationSession: (
    grammarText: string,
    description?: string,
  ) => Promise<CreationSession>;
  applyCreationFollowUp: (
    sessionId: string,
    question: string,
  ) => Promise<CreationSession>;
  completeCreationSession: (sessionId: string) => Promise<CreationCompletion>;
};

export function CreatePage({
  createCreationSession,
  applyCreationFollowUp,
  completeCreationSession,
}: CreatePageProps) {
  const [searchParams] = useSearchParams();
  const [grammarText, setGrammarText] = useState("");
  const [description, setDescription] = useState("");
  const [followUpText, setFollowUpText] = useState("");
  const [session, setSession] = useState<CreationSession | null>(null);
  const [completion, setCompletion] = useState<CreationCompletion | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const query = searchParams.get("q");
    if (query) {
      setGrammarText(query);
    }
  }, [searchParams]);

  const currentStep = useMemo(() => {
    if (completion) {
      return 4;
    }
    if (session) {
      return 3;
    }
    if (loading) {
      return 2;
    }
    return 1;
  }, [completion, loading, session]);

  const steps = ["输入文法", "生成草稿", "追问调整", "完成入库"];

  const handleStart = async () => {
    const trimmed = grammarText.trim();
    if (!trimmed) {
      setError("请先输入要创建的文法。");
      return;
    }

    setLoading(true);
    setError(null);
    setCompletion(null);
    try {
      const nextSession = await createCreationSession(trimmed, description.trim() || undefined);
      setSession(nextSession);
    } catch (requestError) {
      setError(
        requestError instanceof Error ? requestError.message : "创建流程启动失败。",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFollowUp = async () => {
    if (!session || !followUpText.trim()) {
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const nextSession = await applyCreationFollowUp(session.id, followUpText.trim());
      setSession(nextSession);
      setFollowUpText("");
    } catch (requestError) {
      setError(
        requestError instanceof Error ? requestError.message : "追加提问提交失败。",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async () => {
    if (!session) {
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await completeCreationSession(session.id);
      setCompletion(result);
      setSession((current) =>
        current
          ? { ...current, published_grammar_id: result.card_id, status: result.status }
          : current,
      );
    } catch (requestError) {
      setError(
        requestError instanceof Error ? requestError.message : "完成创建失败。",
      );
    } finally {
      setLoading(false);
    }
  };

  const resetFlow = () => {
    setDescription("");
    setFollowUpText("");
    setSession(null);
    setCompletion(null);
    setError(null);
  };

  return (
    <PageStack>
      <Surface hero>
        <Stack spacing={2}>
          <Typography color="primary" sx={{ fontSize: 12, fontWeight: 700 }}>
            分步骤创建
          </Typography>
          <Typography variant="h1">先生成结构化草稿，再决定是否入库</Typography>
          <Typography>
            登录并通过准入后，创建内容会保存在你的会话里，确认完成后再写入公共库。
          </Typography>
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
            {steps.map((step, index) => (
              <Chip
                color={index + 1 === currentStep ? "primary" : "default"}
                key={step}
                label={step}
                variant={index + 1 === currentStep ? "filled" : "outlined"}
              />
            ))}
          </Stack>
        </Stack>
      </Surface>

      {currentStep === 1 ? (
        <Surface>
          <Stack spacing={1.5}>
          <TextField
            onChange={(event) => setGrammarText(event.target.value)}
            placeholder="输入文法关键词或句型"
            value={grammarText}
          />
          <TextField
            minRows={5}
            multiline
            onChange={(event) => setDescription(event.target.value)}
            placeholder="补充你想让 AI 重点说明的内容，例如场景、对比点、例句要求。"
            value={description}
          />
          <Button onClick={() => void handleStart()} type="button" variant="contained">
            开始生成
          </Button>
          </Stack>
        </Surface>
      ) : null}

      {currentStep === 2 ? (
        <Surface>
          <SectionHead title="正在生成草稿" meta="请稍候" />
          <Typography>系统正在创建结构化卡片草稿并准备例句与选择题。</Typography>
        </Surface>
      ) : null}

      {session ? (
        <Surface>
          <Stack spacing={2}>
          <SectionHead title={session.draft_card.title} meta={session.draft_card.level} />
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
            {session.draft_card.tags.map((tag) => (
              <Chip key={tag} label={tag} size="small" variant="outlined" />
            ))}
          </Stack>
          <Stack spacing={2}>
            <Stack spacing={0.5}>
              <Typography variant="h3">含义</Typography>
              <Typography>{session.draft_card.meaning}</Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="h3">接续</Typography>
              <ConnectionList connection={session.draft_card.connection} />
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="h3">语境</Typography>
              <Typography>{session.draft_card.context}</Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="h3">例句</Typography>
              <Stack component="ul" spacing={1} sx={{ m: 0, pl: 2.25 }}>
                {session.draft_card.examples.map((example) => (
                  <li key={example.japanese}>
                    <Box component="strong" sx={{ display: "block", fontWeight: 700 }}>
                      {example.japanese}
                    </Box>
                    <Typography color="text.secondary">{example.chinese}</Typography>
                  </li>
                ))}
              </Stack>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="h3">练习预览</Typography>
              <Stack component="ul" spacing={1} sx={{ m: 0, pl: 2.25 }}>
                {session.draft_card.questions.map((question) => (
                  <li key={question.question}>
                    <Box component="strong" sx={{ display: "block", fontWeight: 700 }}>
                      {question.question}
                    </Box>
                    <Typography color="text.secondary">{question.explanation}</Typography>
                  </li>
                ))}
              </Stack>
            </Stack>
          </Stack>
          <Stack spacing={1.5}>
            <TextField
              minRows={5}
              multiline
              onChange={(event) => setFollowUpText(event.target.value)}
              placeholder="继续追问，例如补更多例句、强调相近文法对比。"
              value={followUpText}
            />
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
              <Button
                color="secondary"
                disabled={loading || !followUpText.trim()}
                onClick={() => void handleFollowUp()}
                type="button"
                variant="contained"
              >
                提交追问
              </Button>
              <Button
                disabled={loading}
                onClick={() => void handleComplete()}
                type="button"
                variant="contained"
              >
                完成创建
              </Button>
              <Button onClick={resetFlow} type="button" variant="outlined">
                重新开始
              </Button>
            </Stack>
          </Stack>
          {session.follow_up_history.length > 0 ? (
            <Stack spacing={0.5}>
                <Typography variant="h3">追加提问记录</Typography>
                <Stack component="ul" spacing={1} sx={{ m: 0, pl: 2.25 }}>
                  {session.follow_up_history.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </Stack>
            </Stack>
          ) : null}
          </Stack>
        </Surface>
      ) : null}

      {error ? (
        <Surface>
          <Stack spacing={1.5}>
          <Alert severity="error">{error}</Alert>
          <Button color="secondary" component={RouterLink} to="/login" variant="contained">
            去登录 / 查看准入状态
          </Button>
          </Stack>
        </Surface>
      ) : null}

      {completion ? (
        <Dialog
          aria-labelledby="completion-title"
          fullWidth
          maxWidth="sm"
          onClose={resetFlow}
          open
        >
          <DialogTitle id="completion-title">创建完成</DialogTitle>
          <DialogContent>
            <Stack spacing={1.5}>
              <Chip label={completion.status} sx={{ alignSelf: "flex-start" }} />
              <Typography>新文法已经写入公共库，可以直接进入详情页继续学习。</Typography>
            </Stack>
          </DialogContent>
          <DialogActions sx={{ flexDirection: "row", p: 3, pt: 0 }}>
            <Button component={RouterLink} to={`/grammar/${completion.card_id}`} variant="contained">
              查看新文法
            </Button>
            <Button color="secondary" onClick={resetFlow} type="button" variant="contained">
              继续创建
            </Button>
          </DialogActions>
        </Dialog>
      ) : null}
    </PageStack>
  );
}
