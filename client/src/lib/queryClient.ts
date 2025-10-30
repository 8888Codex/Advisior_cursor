import { QueryClient, QueryFunction } from "@tanstack/react-query";

async function throwIfResNotOk(res: Response) {
  if (!res.ok) {
    try {
      const text = await res.text();
      // Verificar se é um erro de resource_exhausted
      if (text.includes('resource_exhausted')) {
        throw new Error('Limite de recursos atingido. Por favor, aguarde um momento e tente novamente.');
      } else {
        throw new Error(`${res.status}: ${text || res.statusText}`);
      }
    } catch (e) {
      if (e instanceof Error && e.message.includes('resource_exhausted')) {
        throw e;
      }
      throw new Error(`${res.status}: ${res.statusText}`);
    }
  }
}

export async function apiRequest(
  url: string,
  options?: RequestInit,
): Promise<Response> {
  try {
    const res = await fetch(url, {
      ...options,
      credentials: "include",
    });

    await throwIfResNotOk(res);
    return res;
  } catch (error) {
    if (error instanceof Error) {
      // Verificar se é um erro de rede ou conexão
      if (error.message.includes('Failed to fetch') || 
          error.message.includes('NetworkError') ||
          error.message.includes('Connection failed')) {
        throw new Error('Erro de conexão. Verifique sua internet ou VPN e tente novamente.');
      }
      
      // Verificar se é um erro de resource_exhausted
      if (error.message.includes('resource_exhausted')) {
        throw new Error('Limite de recursos atingido. Por favor, aguarde um momento e tente novamente.');
      }
    }
    throw error;
  }
}

export async function apiRequestJson<T = any>(
  url: string,
  options?: RequestInit,
): Promise<T> {
  const res = await apiRequest(url, options);
  return await res.json();
}

type UnauthorizedBehavior = "returnNull" | "throw";
export const getQueryFn: <T>(options: {
  on401: UnauthorizedBehavior;
}) => QueryFunction<T> =
  ({ on401: unauthorizedBehavior }) =>
  async ({ queryKey }) => {
    try {
      const res = await fetch(queryKey.join("/") as string, {
        credentials: "include",
      });

      if (unauthorizedBehavior === "returnNull" && res.status === 401) {
        return null;
      }

      await throwIfResNotOk(res);
      return await res.json();
    } catch (error) {
      if (error instanceof Error) {
        // Verificar se é um erro de rede ou conexão
        if (error.message.includes('Failed to fetch') || 
            error.message.includes('NetworkError') ||
            error.message.includes('Connection failed')) {
          throw new Error('Erro de conexão. Verifique sua internet ou VPN e tente novamente.');
        }
        
        // Verificar se é um erro de resource_exhausted
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
