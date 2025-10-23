import { Link } from "wouter";
import { ThemeToggle } from "./ThemeToggle";
import { Sparkles } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/">
          <a className="flex items-center gap-2 hover-elevate active-elevate-2 px-3 py-2 rounded-lg -ml-3" data-testid="link-home">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold tracking-tight">AdvisorIA</span>
          </a>
        </Link>

        <nav className="hidden md:flex items-center gap-6">
          <Link href="/experts">
            <a className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors" data-testid="link-experts">
              Especialistas
            </a>
          </Link>
          <Link href="/create">
            <a className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors" data-testid="link-create">
              Criar Especialista
            </a>
          </Link>
        </nav>

        <ThemeToggle />
      </div>
    </header>
  );
}
