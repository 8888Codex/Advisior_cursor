import { ThemeProvider } from "../ThemeProvider";
import { ThemeToggle } from "../ThemeToggle";

export default function ThemeToggleExample() {
  return (
    <ThemeProvider>
      <div className="flex items-center justify-center p-8 bg-background">
        <ThemeToggle />
      </div>
    </ThemeProvider>
  );
}
