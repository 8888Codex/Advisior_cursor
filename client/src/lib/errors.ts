/**
 * Sistema de Tratamento de Erros Unificado
 * Centraliza toda a lógica de erro do sistema de conselho
 */

export class CouncilError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = "CouncilError";
  }
}

export class RateLimitError extends CouncilError {
  constructor(
    message: string,
    public retryAfter: number // segundos até poder tentar novamente
  ) {
    super(message, "RATE_LIMIT_EXCEEDED");
  }
}

export class ValidationError extends CouncilError {
  constructor(message: string, public field: string) {
    super(message, "VALIDATION_ERROR", { field });
  }
}

export class BackendError extends CouncilError {
  constructor(message: string, public statusCode: number) {
    super(message, "BACKEND_ERROR", { statusCode });
  }
}

export class NetworkError extends CouncilError {
  constructor(message: string = "Erro de conexão com o servidor") {
    super(message, "NETWORK_ERROR");
  }
}

/**
 * Converte erro genérico em CouncilError tipado
 */
export function parseError(error: any): CouncilError {
  // Erro já é CouncilError
  if (error instanceof CouncilError) {
    return error;
  }

  // Erro de rede/fetch
  if (error instanceof TypeError && error.message.includes("fetch")) {
    return new NetworkError("Não foi possível conectar ao servidor. Verifique se o backend está rodando.");
  }

  // Erro HTTP com status code
  if (error?.statusCode || error?.status) {
    const status = error.statusCode || error.status;
    const message = error?.message || error?.detail || "Erro no servidor";

    // Rate limit (429)
    if (status === 429) {
      const retryAfter = error?.retryAfter || 3600; // default 1 hora
      return new RateLimitError(
        "Muitas requisições. Aguarde antes de tentar novamente.",
        retryAfter
      );
    }

    // Bad request (400)
    if (status === 400) {
      return new ValidationError(message, "unknown");
    }

    // Server error (500+)
    if (status >= 500) {
      return new BackendError(message, status);
    }

    return new BackendError(message, status);
  }

  // Erro genérico
  return new CouncilError(
    error?.message || "Erro desconhecido",
    "UNKNOWN_ERROR",
    error
  );
}

/**
 * Formata mensagem de erro para toast
 */
export function formatErrorForToast(error: CouncilError): {
  title: string;
  description: string;
  variant: "destructive";
  duration?: number;
} {
  const base = {
    variant: "destructive" as const,
  };

  if (error instanceof RateLimitError) {
    const minutes = Math.ceil(error.retryAfter / 60);
    return {
      ...base,
      title: "Limite de requisições atingido",
      description: `Você atingiu o limite de análises. Tente novamente em ${minutes} minuto${minutes > 1 ? 's' : ''}.`,
      duration: 8000,
    };
  }

  if (error instanceof ValidationError) {
    return {
      ...base,
      title: "Dados inválidos",
      description: error.message,
      duration: 5000,
    };
  }

  if (error instanceof NetworkError) {
    return {
      ...base,
      title: "Erro de conexão",
      description: error.message,
      duration: 5000,
    };
  }

  if (error instanceof BackendError) {
    return {
      ...base,
      title: "Erro no servidor",
      description: `${error.message} (código: ${error.statusCode})`,
      duration: 6000,
    };
  }

  return {
    ...base,
    title: "Erro inesperado",
    description: error.message || "Ocorreu um erro. Tente novamente.",
    duration: 5000,
  };
}

/**
 * Handler unificado de erros para o sistema de conselho
 */
export function handleCouncilError(
  error: any,
  toast: (props: any) => void,
  options?: {
    onRateLimit?: () => void;
    onValidation?: () => void;
    onNetwork?: () => void;
  }
): void {
  const councilError = parseError(error);
  const toastProps = formatErrorForToast(councilError);

  // Log estruturado para debug
  console.error("[Council Error]", {
    code: councilError.code,
    message: councilError.message,
    details: councilError.details,
  });

  // Mostrar toast ao usuário
  toast(toastProps);

  // Callbacks específicos
  if (councilError instanceof RateLimitError && options?.onRateLimit) {
    options.onRateLimit();
  } else if (councilError instanceof ValidationError && options?.onValidation) {
    options.onValidation();
  } else if (councilError instanceof NetworkError && options?.onNetwork) {
    options.onNetwork();
  }
}

