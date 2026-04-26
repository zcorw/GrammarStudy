import { Alert, Button, CircularProgress, Stack, Typography } from "@mui/material";

import { Surface } from "./Surface";

type AsyncStateProps = {
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
};

export function AsyncState({ loading, error, onRetry }: AsyncStateProps) {
  if (loading) {
    return (
      <Surface>
        <Stack direction="row" spacing={1.5} sx={{ alignItems: "center" }}>
          <CircularProgress size={22} />
          <Typography>加载中...</Typography>
        </Stack>
      </Surface>
    );
  }

  if (error) {
    return (
      <Surface>
        <Stack spacing={1.5}>
          <Alert severity="error">{error}</Alert>
        {onRetry ? (
          <Button color="secondary" onClick={onRetry} type="button" variant="contained">
            重试
          </Button>
        ) : null}
        </Stack>
      </Surface>
    );
  }

  return null;
}
