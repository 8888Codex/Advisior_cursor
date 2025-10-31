import { createContext, useContext, useState, useCallback, ReactNode } from "react";

interface GlobalError {
  title?: string;
  message: string;
  onRetry?: () => void;
  retryLabel?: string;
}

interface GlobalErrorContextType {
  error: GlobalError | null;
  setGlobalError: (err: GlobalError) => void;
  clearError: () => void;
}

const GlobalErrorContext = createContext<GlobalErrorContextType | undefined>(undefined);

export function GlobalErrorProvider({ children }: { children: ReactNode }) {
  const [error, setError] = useState<GlobalError | null>(null);

  const setGlobalError = useCallback((err: GlobalError) => {
    setError(err);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return (
    <GlobalErrorContext.Provider value={{ error, setGlobalError, clearError }}>
      {children}
    </GlobalErrorContext.Provider>
  );
}

/**
 * Hook para gerenciar erros globais na aplicação
 * Útil para erros críticos que devem ser exibidos em toda a aplicação
 */
export function useGlobalError() {
  const context = useContext(GlobalErrorContext);
  if (!context) {
    throw new Error("useGlobalError must be used within GlobalErrorProvider");
  }
  return context;
}

