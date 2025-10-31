import { ReactNode } from "react";
import { Header } from "./Header";

interface ShellProps {
  children: ReactNode;
  className?: string;
}

/**
 * Shell component - Wrapper reutilizável para páginas internas
 * Fornece estrutura base com Header e container padronizado
 */
export function Shell({ children, className = "" }: ShellProps) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <main className={className}>
        {children}
      </main>
    </div>
  );
}

