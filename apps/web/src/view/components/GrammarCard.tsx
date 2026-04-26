import { Box, Chip, Stack, Typography } from "@mui/material";

import type { GrammarEntry } from "../../domain/grammar/entities";
import { ConnectionList } from "./ConnectionList";
import { Surface } from "./Surface";

type GrammarCardProps = {
  grammar: GrammarEntry;
  compact?: boolean;
};

export function GrammarCard({
  grammar,
  compact = false,
}: GrammarCardProps) {
  return (
    <Surface>
      <Stack spacing={2}>
        <Stack direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
          <Chip color="primary" label={grammar.level} size="small" />
          {grammar.tags.map((tag) => (
            <Chip key={tag} label={tag} size="small" variant="outlined" />
          ))}
        </Stack>
        <Typography variant="h2">{grammar.title}</Typography>
        <Typography>{grammar.meaning}</Typography>
        {!compact && (
          <Stack spacing={2}>
            <Stack spacing={0.5}>
              <Typography variant="h3">接续</Typography>
              <ConnectionList connection={grammar.connection} />
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="h3">语气/语境</Typography>
              <Typography>{grammar.context}</Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="h3">例句</Typography>
              <Stack component="ul" spacing={1} sx={{ m: 0, pl: 2.25 }}>
                {grammar.examples.map((example) => (
                  <li key={example.japanese}>
                    <Box component="strong" sx={{ display: "block", fontWeight: 700 }}>
                      {example.japanese}
                    </Box>
                    <Typography color="text.secondary">{example.chinese}</Typography>
                  </li>
                ))}
              </Stack>
            </Stack>
          </Stack>
        )}
      </Stack>
    </Surface>
  );
}
