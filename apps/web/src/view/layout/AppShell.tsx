import { Box, Button, Container, Stack, Typography } from "@mui/material";
import type { PropsWithChildren } from "react";
import { Link as RouterLink } from "react-router-dom";

import { clearAuthSession, getAuthSession } from "../../infrastructure/auth/session";

export function AppShell({ children }: PropsWithChildren) {
  const session = getAuthSession();

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Stack
        component="header"
        direction={{ xs: "column", sm: "row" }}
        spacing={2}
        sx={{
          alignItems: { xs: "flex-start", sm: "center" },
          justifyContent: "space-between",
          mb: 3,
        }}
      >
        <Box>
          <Typography sx={{ fontWeight: 800 }} variant="h1">
            文法手帐
          </Typography>
          <Typography color="text.secondary">
            {session
              ? `当前状态：${session.access_state} / ${session.email}`
              : "PWA 首版骨架"}
          </Typography>
        </Box>
        <Stack component="nav" direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
          <Button component={RouterLink} to="/" variant="text">
            发现
          </Button>
          <Button component={RouterLink} to="/my" variant="text">
            我的
          </Button>
          <Button component={RouterLink} to="/login" variant="text">
            登录
          </Button>
          <Button component={RouterLink} to="/register" variant="text">
            注册
          </Button>
          {session ? (
            <Button
              onClick={() => {
                clearAuthSession();
                window.location.assign("/");
              }}
              type="button"
              variant="outlined"
            >
              退出
            </Button>
          ) : null}
        </Stack>
      </Stack>
      {children}
    </Container>
  );
}
