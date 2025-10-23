import { ThemeProvider } from "../ThemeProvider";
import { Header } from "../Header";

export default function HeaderExample() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background">
        <Header />
        <div className="p-8 text-center text-muted-foreground">
          Content below header
        </div>
      </div>
    </ThemeProvider>
  );
}
