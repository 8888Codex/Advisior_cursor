import { QueryClient, QueryFunction } from "@tanstack/react-query";

const DEFAULT_TIMEOUT_MS = 30000; // 30 segundos

async function throwIfResNotOk(res: Response) {
  if (!res.ok) {
    try {
      const text = await res.text();
      let errorMessage = text || res.statusText;
      
      // Tentar parsear JSON para mensagem estruturada
      try {
        const json = JSON.parse(text);
        if (json.message) {
          errorMessage = json.message;
        } else if (json.error) {
          errorMessage = json.error;
        } else if (json.detail) {
          errorMessage = json.detail;
        }
      } catch {
        // Não é JSON, usar texto como está
      }
      
      // Verificar códigos de erro específicos
      if (text.includes('resource_exhausted') || errorMessage.includes('resource_exhausted')) {
        throw new Error('Limite de recursos atingido. Por favor, aguarde um momento e tente novamente.');
      }
      
      if (res.status === 401) {
        throw new Error('Não autorizado. Verifique suas credenciais.');
      }
      
      if (res.status === 429) {
        throw new Error('Muitas requisições. Aguarde um momento antes de tentar novamente.');
      }
      
      if (res.status >= 500) {
        throw new Error(`Erro do servidor (${res.status}). Tente novamente mais tarde.`);
      }
      
      throw new Error(`${res.status}: ${errorMessage}`);
    } catch (e) {
      if (e instanceof Error) {
        throw e;
      }
      throw new Error(`${res.status}: ${res.statusText}`);
    }
  }
}

export async function apiRequest(
  url: string,
  options?: RequestInit & { timeout?: number },
): Promise<Response> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT_MS;
  
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
      credentials: "include",
    });
    
    clearTimeout(timeoutId);
    await throwIfResNotOk(res);
    return res;
  } catch (error) {
    if (error instanceof Error) {
      // Timeout
      if (error.name === 'AbortError' || error.message.includes('aborted')) {
        throw new Error(`Requisição expirou após ${timeout}ms. Tente novamente.`);
      }
      
      // Erro de rede/conexão
      if (error.message.includes('Failed to fetch') || 
          error.message.includes('NetworkError') ||
          error.message.includes('Connection failed') ||
          error.message.includes('Network request failed')) {
        throw new Error('Erro de conexão. Verifique sua internet ou VPN e tente novamente.');
      }
      
      // Erro de resource_exhausted (já tratado em throwIfResNotOk, mas garantir)
      if (error.message.includes('resource_exhausted')) {
        throw new Error('Limite de recursos atingido. Por favor, aguarde um momento e tente novamente.');
      }
    }
    throw error;
  }
}

export async function apiRequestJson<T = any>(
  url: string,
  options?: RequestInit & { timeout?: number },
): Promise<T> {
  const res = await apiRequest(url, options);
  return await res.json();
}

type UnauthorizedBehavior = "returnNull" | "throw";
export const getQueryFn: <T>(options: {
  on401: UnauthorizedBehavior;
  timeout?: number;
}) => QueryFunction<T> =
  ({ on401: unauthorizedBehavior, timeout = DEFAULT_TIMEOUT_MS }) =>
  async ({ queryKey }) => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);
      
      // Construir URL corretamente - se começar com /, usar direto; senão, juntar
      let url: string;
      if (typeof queryKey[0] === 'string' && queryKey[0].startsWith('/')) {
        url = queryKey[0] as string;
        // Se há mais partes na queryKey e a primeira parte termina sem parâmetro de rota, construir caminho
        if (queryKey.length > 1) {
          const rest = queryKey.slice(1).filter(Boolean);
          if (rest.length > 0) {
            // Se a URL termina com algo como "/experts" e o próximo é um ID, fazer "/experts/{id}"
            const lastPart = rest[0] as string;
            // Se a URL não tem ? (não é query param), adicionar como path
            if (!url.includes('?') && !url.endsWith('/')) {
              url += '/' + lastPart;
              // Se houver mais partes (query params), adicionar com ?
              if (rest.length > 1) {
                url += '?' + rest.slice(1).join('&');
              }
            } else {
              // É query param, adicionar normalmente
              url += (url.includes('?') ? '&' : '?') + rest.join('&');
            }
          }
        }
      } else {
        url = queryKey.join("/") as string;
        // Garantir que começa com / se não começar
        if (!url.startsWith('/')) {
          url = '/' + url;
        }
      }
      
      const res = await fetch(url, {
        credentials: "include",
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);

      if (unauthorizedBehavior === "returnNull" && res.status === 401) {
        return null;
      }

      await throwIfResNotOk(res);
      return await res.json();
    } catch (error) {
      if (error instanceof Error) {
        // Timeout
        if (error.name === 'AbortError' || error.message.includes('aborted')) {
          throw new Error(`Requisição expirou após ${timeout}ms. Tente novamente.`);
        }
        
        // Erro de rede/conexão
        if (error.message.includes('Failed to fetch') || 
            error.message.includes('NetworkError') ||
            error.message.includes('Connection failed') ||
            error.message.includes('Network request failed')) {
          throw new Error('Erro de conexão. Verifique sua internet ou VPN e tente novamente.');
        }
        
        // Erro de resource_exhausted
        if (error.message.includes('resource_exhausted')) {
          throw new Error('Limite de recursos atingido. Por favor, aguarde um momento e tente novamente.');
        }
      }
      throw error;
    }
  };

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: getQueryFn({ on401: "throw" }),
      refetchInterval: false,
      refetchOnWindowFocus: false,
      staleTime: Infinity,
      retry: false,
    },
    mutations: {
      retry: false,
    },
  },
});
