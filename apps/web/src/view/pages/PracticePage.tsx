import { Alert, Button, Paper, Stack, Typography } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import type { ChoiceSubmitResult, GrammarEntry } from "../../domain/grammar/entities";
import { AsyncState } from "../components/AsyncState";
import { PageStack, SectionHead, Surface } from "../components/Surface";

type PracticePageProps = {
  getGrammarDetail: (grammarId: string) => Promise<GrammarEntry | null>;
  submitPracticeChoice: (
    grammarId: string,
    selectedOption: string,
  ) => Promise<ChoiceSubmitResult>;
};

export function PracticePage({
  getGrammarDetail,
  submitPracticeChoice,
}: PracticePageProps) {
  const { id = "" } = useParams();
  const [grammar, setGrammar] = useState<GrammarEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitResult, setSubmitResult] = useState<string | null>(null);

  const loadGrammar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const item = await getGrammarDetail(id);
      setGrammar(item);
      if (!item) {
        setError("未找到练习对应的文法。");
      }
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "练习数据加载失败");
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
          <Typography>未找到练习对应的文法。</Typography>
        </Surface>
      </PageStack>
    );
  }

  const question = grammar.questions[0];

  const handleSubmitChoice = async (option: string) => {
    try {
      const result = await submitPracticeChoice(grammar.id, option);
      setSubmitResult(`已提交：${result.selected_option}，状态：${result.result}`);
    } catch (submitError) {
      setSubmitResult(
        submitError instanceof Error ? submitError.message : "提交练习结果失败",
      );
    }
  };

  return (
    <PageStack>
      <Surface>
        <SectionHead title="选择题练习" meta={grammar.title} />
        <Paper sx={{ p: 2 }}>
          <Stack spacing={1.5}>
          <Typography>{question.question}</Typography>
          <Stack spacing={1}>
            {question.options.map((option) => (
              <Button
                key={option}
                onClick={() => void handleSubmitChoice(option)}
                type="button"
                variant="outlined"
              >
                {option}
              </Button>
            ))}
          </Stack>
          <Typography color="text.secondary">{question.explanation}</Typography>
          {submitResult ? <Alert severity="info">{submitResult}</Alert> : null}
          </Stack>
        </Paper>
      </Surface>
    </PageStack>
  );
}
