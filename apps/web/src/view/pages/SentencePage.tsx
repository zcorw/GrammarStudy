import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import type { GrammarEntry, SentenceFeedbackResult } from "../../domain/grammar/entities";
import { AsyncState } from "../components/AsyncState";
import { PageStack, SectionHead, Surface } from "../components/Surface";

type SentencePageProps = {
  getGrammarDetail: (grammarId: string) => Promise<GrammarEntry | null>;
  submitSentenceFeedback: (
    grammarId: string,
    sentence: string,
  ) => Promise<SentenceFeedbackResult>;
};

export function SentencePage({
  getGrammarDetail,
  submitSentenceFeedback,
}: SentencePageProps) {
  const { id = "" } = useParams();
  const [grammar, setGrammar] = useState<GrammarEntry | null>(null);
  const [sentence, setSentence] = useState("");
  const [feedback, setFeedback] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadGrammar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const item = await getGrammarDetail(id);
      setGrammar(item);
      setSentence(item?.examples[0]?.japanese ?? "");
      if (!item) {
        setError("未找到点评对应的文法。");
      }
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "点评页面加载失败");
    } finally {
      setLoading(false);
    }
  }, [getGrammarDetail, id]);

  useEffect(() => {
    void loadGrammar();
  }, [loadGrammar]);

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
          <Typography>未找到点评对应的文法。</Typography>
        </Surface>
      </PageStack>
    );
  }

  const handleSubmitFeedback = async () => {
    try {
      const result = await submitSentenceFeedback(grammar.id, sentence);
      setFeedback(result.feedback);
    } catch (submitError) {
      setFeedback(submitError instanceof Error ? submitError.message : "点评提交失败");
    }
  };

  return (
    <PageStack>
      <Surface>
        <Stack spacing={1.5}>
        <SectionHead title="自由造句点评" meta={grammar.title} />
        <TextField
          minRows={5}
          onChange={(event) => setSentence(event.target.value)}
          multiline
          value={sentence}
        />
        <Stack spacing={1.5}>
          <Button onClick={() => void handleSubmitFeedback()} type="button" variant="contained">
            提交点评
          </Button>
          <Typography color="text.secondary">点评结果只进入个人学习记录，不修改公共卡片。</Typography>
          {feedback ? <Alert severity="info">{feedback}</Alert> : null}
        </Stack>
        </Stack>
      </Surface>
    </PageStack>
  );
}
