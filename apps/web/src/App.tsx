import { CssBaseline, ThemeProvider } from "@mui/material";

import { AppShell } from "./view/layout/AppShell";
import { AppRoutes } from "./view/routes/AppRoutes";
import { appTheme } from "./view/theme";

function App() {
  return (
    <ThemeProvider theme={appTheme}>
      <CssBaseline />
      <AppShell>
        <AppRoutes />
      </AppShell>
    </ThemeProvider>
  );
}

export default App;
