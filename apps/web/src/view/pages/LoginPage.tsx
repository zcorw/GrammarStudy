import { Alert, Button, Link, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { Link as RouterLink, useNavigate, useSearchParams } from "react-router-dom";

import type { LoginResult } from "../../domain/grammar/entities";
import { saveAuthSession } from "../../infrastructure/auth/session";
import { PageStack, Surface } from "../components/Surface";

type LoginPageProps = {
  loginWithEmail: (email: string, password: string) => Promise<LoginResult>;
};

export function LoginPage({ loginWithEmail }: LoginPageProps) {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const authError = searchParams.get("error");
  const returnPath = searchParams.get("return");
  const safeReturnPath =
    returnPath && returnPath.startsWith("/") && !returnPath.startsWith("//")
      ? returnPath
      : "/";

  const handleLogin = async () => {
    setError(null);
    try {
      const response = await loginWithEmail(email, password);
      saveAuthSession(response);
      navigate(safeReturnPath, { replace: true });
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "登录失败");
    }
  };

  return (
    <PageStack>
      <Surface hero>
        <Stack spacing={1.5}>
        <Typography color="primary" sx={{ fontSize: 12, fontWeight: 700 }}>
          账号登录
        </Typography>
        <Typography variant="h1">使用邮箱和密码登录</Typography>
        <Typography>注册完成后，登录统一使用邮箱加密码。邀请码或审核只影响账号是否通过准入。</Typography>
        </Stack>
      </Surface>
      <Surface>
        <Stack spacing={1.5}>
        <TextField onChange={(event) => setEmail(event.target.value)} placeholder="邮箱" value={email} />
        <TextField
          onChange={(event) => setPassword(event.target.value)}
          placeholder="密码"
          type="password"
          value={password}
        />
        <Button onClick={() => void handleLogin()} type="button" variant="contained">
          登录
        </Button>
        <Typography color="text.secondary">
          还没有账号？<Link component={RouterLink} to="/register">先注册</Link>
        </Typography>
        {authError ? <Alert severity="warning">{authError}</Alert> : null}
        {error ? <Alert severity="error">{error}</Alert> : null}
        </Stack>
      </Surface>
    </PageStack>
  );
}
