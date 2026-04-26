import { createTheme } from "@mui/material/styles";

export const appTheme = createTheme({
  palette: {
    background: {
      default: "#f5efe4",
      paper: "#fff9f0",
    },
    primary: {
      main: "#bb602d",
      contrastText: "#fff9f4",
    },
    secondary: {
      main: "#eadbc7",
      contrastText: "#1f1911",
    },
    text: {
      primary: "#1f1911",
      secondary: "#6f6556",
    },
  },
  shape: {
    borderRadius: 20,
  },
  typography: {
    fontFamily: '"Segoe UI", "PingFang SC", sans-serif',
    h1: {
      fontSize: "2rem",
      fontWeight: 800,
      letterSpacing: 0,
    },
    h2: {
      fontSize: "1.5rem",
      fontWeight: 800,
      letterSpacing: 0,
    },
    h3: {
      fontSize: "1.1rem",
      fontWeight: 700,
      letterSpacing: 0,
    },
    button: {
      fontWeight: 700,
      letterSpacing: 0,
      textTransform: "none",
    },
  },
  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          borderRadius: 16,
          paddingBlock: 12,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          border: "1px solid rgba(211, 197, 174, 0.85)",
          boxShadow: "0 18px 40px rgba(77, 52, 28, 0.08)",
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        fullWidth: true,
      },
    },
  },
});
