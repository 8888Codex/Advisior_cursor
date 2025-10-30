import { useState, useEffect, useCallback } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";

export interface UserPreferences {
  style_preference?: "objetivo" | "detalhado";
  focus_preference?: "ROI-first" | "brand-first";
  tone_preference?: "prático" | "estratégico";
  communication_preference?: "bullets" | "blocos";
  conversation_style?: "coach" | "consultor" | "direto";
}

const STORAGE_KEY = "advisor_ia_user_preferences";
const STORAGE_USER_ID_KEY = "advisor_ia_user_id";

/**
 * Hook para gerenciar preferências persistentes do usuário
 * Usa localStorage para persistência local + sincronização com backend quando autenticado
 */
export function useUserPreferences(userId?: string, isAuthenticated: boolean = false) {
  const queryClient = useQueryClient();
  
  // Gerar ou recuperar user ID persistente
  const getStoredUserId = useCallback((): string => {
    if (userId) return userId;
    
    let storedId = localStorage.getItem(STORAGE_USER_ID_KEY);
    if (!storedId) {
      storedId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem(STORAGE_USER_ID_KEY, storedId);
    }
    return storedId;
  }, [userId]);

  // Carregar preferências do backend se autenticado
  const { data: backendPreferences, isLoading: isLoadingBackend } = useQuery<UserPreferences>({
    queryKey: ["/api/user/preferences"],
    queryFn: async () => {
      const response = await apiRequest("/api/user/preferences", {
        method: "GET",
      });
      return response.json();
    },
    enabled: isAuthenticated,
    retry: false, // Não retry se não autenticado
  });

  const [preferences, setPreferences] = useState<UserPreferences>(() => {
    // Carregar preferências do localStorage na inicialização
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        return JSON.parse(stored) as UserPreferences;
      }
    } catch (error) {
      console.warn("Erro ao carregar preferências do localStorage:", error);
    }
    return {};
  });

  const [currentUserId] = useState<string>(getStoredUserId);

  // Sincronizar preferências do backend quando disponíveis
  useEffect(() => {
    if (isAuthenticated && backendPreferences && Object.keys(backendPreferences).length > 0) {
      setPreferences(backendPreferences);
      // Salvar no localStorage também para cache offline
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(backendPreferences));
      } catch (error) {
        console.warn("Erro ao salvar preferências no localStorage:", error);
      }
    }
  }, [isAuthenticated, backendPreferences]);

  // Mutation para salvar no backend
  const savePreferencesMutation = useMutation({
    mutationFn: async (prefs: Partial<UserPreferences>) => {
      const response = await apiRequest("/api/user/preferences", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(prefs),
      });
      return response.json();
    },
    onSuccess: (data) => {
      queryClient.setQueryData(["/api/user/preferences"], data);
      setPreferences(data);
    },
  });

  // Salvar preferências (localStorage + backend se autenticado)
  const savePreferences = useCallback((newPreferences: Partial<UserPreferences>) => {
    const updated = { ...preferences, ...newPreferences };
    setPreferences(updated);
    
    // Sempre salvar no localStorage
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    } catch (error) {
      console.warn("Erro ao salvar preferências no localStorage:", error);
    }
    
    // Sincronizar com backend se autenticado
    if (isAuthenticated) {
      savePreferencesMutation.mutate(newPreferences);
    }
  }, [preferences, isAuthenticated, savePreferencesMutation]);

  // Mutation para deletar no backend
  const deletePreferencesMutation = useMutation({
    mutationFn: async () => {
      const response = await apiRequest("/api/user/preferences", {
        method: "DELETE",
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.setQueryData(["/api/user/preferences"], {});
      setPreferences({});
    },
  });

  // Atualizar preferência específica
  const updatePreference = useCallback(<K extends keyof UserPreferences>(
    key: K,
    value: UserPreferences[K]
  ) => {
    savePreferences({ [key]: value });
  }, [savePreferences]);

  // Limpar todas as preferências
  const clearPreferences = useCallback(() => {
    setPreferences({});
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      console.warn("Erro ao limpar preferências:", error);
    }
    
    // Limpar no backend também se autenticado
    if (isAuthenticated) {
      deletePreferencesMutation.mutate();
    }
  }, [isAuthenticated, deletePreferencesMutation]);

  // Detectar preferências implicitamente de uma mensagem
  const detectPreferencesFromMessage = useCallback((message: string): Partial<UserPreferences> => {
    const detected: Partial<UserPreferences> = {};
    const messageLower = message.toLowerCase();

    // Detectar estilo
    if (messageLower.match(/\b(direto|objetivo|resumo|resumido)\b/)) {
      detected.style_preference = "objetivo";
    } else if (messageLower.match(/\b(detalhado|completo|explicação completa)\b/)) {
      detected.style_preference = "detalhado";
    }

    // Detectar foco
    if (messageLower.match(/\b(roi|conversão|vendas|resultado|métricas)\b/)) {
      detected.focus_preference = "ROI-first";
    } else if (messageLower.match(/\b(marca|brand|reputação|posicionamento)\b/)) {
      detected.focus_preference = "brand-first";
    }

    // Detectar tom
    if (messageLower.match(/\b(prático|ação|implementar|como fazer)\b/)) {
      detected.tone_preference = "prático";
    } else if (messageLower.match(/\b(estratégico|visão|planejamento|longo prazo)\b/)) {
      detected.tone_preference = "estratégico";
    }

    // Detectar comunicação
    if (messageLower.match(/\b(bullets|pontos|lista)\b/)) {
      detected.communication_preference = "bullets";
    } else if (messageLower.match(/\b(blocos|parágrafos|texto completo)\b/)) {
      detected.communication_preference = "blocos";
    }

    return detected;
  }, []);

  // Aplicar detecção automática e salvar
  const applyDetectionFromMessage = useCallback((message: string) => {
    const detected = detectPreferencesFromMessage(message);
    if (Object.keys(detected).length > 0) {
      savePreferences(detected);
      return detected;
    }
    return null;
  }, [detectPreferencesFromMessage, savePreferences]);

  return {
    preferences,
    userId: currentUserId,
    isLoading: isLoadingBackend,
    updatePreference,
    savePreferences,
    clearPreferences,
    detectPreferencesFromMessage,
    applyDetectionFromMessage,
  };
}

