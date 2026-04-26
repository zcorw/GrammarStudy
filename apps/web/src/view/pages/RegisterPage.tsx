import { Alert, Button, Link, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { Link as RouterLink } from "react-router-dom";

import type { RegistrationResult } from "../../domain/grammar/entities";
import { PageStack, Surface } from "../components/Surface";

type RegisterPageProps = {
  registerWithEmail: (
    email: string,
    password: string,
    inviteCode?: string,
  ) => Promise<RegistrationResult>;
};

export function RegisterPage({ registerWithEmail }: RegisterPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [inviteCode, setInviteCode] = useState("");
  const [result, setResult] = useState<RegistrationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRegister = async () => {
    setError(null);
    setResult(null);
    try {
      const response = await registerWithEmail(
        email,
        password,
        inviteCode || undefined,
      );
      setResult(response);
    } catch (registerError) {
      setError(registerError instanceof Error ? registerError.message : "注册失败");
    }
  };

  return (
    <PageStack>
      <Surface hero>
        <Stack spacing={1.5}>
        <Typography color="primary" sx={{ fontSize: 12, fontWeight: 700 }}>
          账号注册
        </Typography>
        <Typography variant="h1">先创建账号，再等待通过准入</Typography>
        <Typography>有邀请码可直接通过；没有邀请码会进入待审核状态。注册完成后，登录统一使用邮箱和密码。</Typography>
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
        <TextField
          onChange={(event) => setInviteCode(event.target.value)}
          placeholder="邀请码（可选）"
          value={inviteCode}
        />
        <Button onClick={() => void handleRegister()} type="button" variant="contained">
          注册
        </Button>
        {result ? (
          <>
            <Alert severity="success">
              注册完成，当前状态：{result.access_state}
              {result.is_admin ? " / 管理员" : ""}
            </Alert>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
              <Button color="secondary" component={RouterLink} to="/login" variant="contained">
                去登录
              </Button>
              <Button component={RouterLink} to="/" variant="outlined">
                返回首页
              </Button>
            </Stack>
          </>
        ) : null}
        <Typography color="text.secondary">
          已有账号？<Link component={RouterLink} to="/login">去登录</Link>
        </Typography>
        {error ? <Alert severity="error">{error}</Alert> : null}
        </Stack>
      </Surface>
    </PageStack>
  );
}
