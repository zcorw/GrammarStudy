import { Stack, Typography } from "@mui/material";

type ConnectionListProps = {
  connection: string;
};

export function ConnectionList({ connection }: ConnectionListProps) {
  const lines = connection
    .split(/\r?\n/)
    .map((line) => line.replace(/^[-・•]\s*/, "").trim())
    .filter(Boolean);

  return (
    <Stack component="ul" spacing={1} sx={{ m: 0, pl: 2.25 }}>
      {lines.map((line) => (
        <li key={line}>
          <Typography sx={{ fontWeight: 700 }}>{line}</Typography>
        </li>
      ))}
    </Stack>
  );
}
