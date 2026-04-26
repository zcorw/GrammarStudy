import { Box, Paper, Stack, Typography } from "@mui/material";
import type { PropsWithChildren, ReactNode } from "react";

type SurfaceProps = PropsWithChildren<{
  hero?: boolean;
}>;

export function PageStack({ children }: PropsWithChildren) {
  return (
    <Stack component="main" spacing={2.25}>
      {children}
    </Stack>
  );
}

export function Surface({ children, hero = false }: SurfaceProps) {
  return (
    <Paper
      component="section"
      sx={{
        background: hero
          ? "linear-gradient(145deg, #fff7eb, #ecdcc4)"
          : "rgba(255, 249, 240, 0.9)",
        borderRadius: "28px",
        p: 2.5,
      }}
    >
      {children}
    </Paper>
  );
}

export function SectionHead({
  title,
  meta,
  id,
}: {
  title: string;
  meta?: ReactNode;
  id?: string;
}) {
  return (
    <Box
      sx={{
        alignItems: "center",
        display: "flex",
        gap: 1.5,
        justifyContent: "space-between",
        mb: 1.5,
      }}
    >
      <Typography id={id} variant="h2">
        {title}
      </Typography>
      {meta ? (
        <Typography color="text.secondary" sx={{ textAlign: "right" }}>
          {meta}
        </Typography>
      ) : null}
    </Box>
  );
}
