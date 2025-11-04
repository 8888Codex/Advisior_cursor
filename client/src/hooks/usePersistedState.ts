import { useState, useEffect, Dispatch, SetStateAction } from 'react';

/**
 * Hook para persistir estado no localStorage
 * Funciona como useState mas salva automaticamente
 * 
 * Usage:
 *   const [value, setValue] = usePersistedState('myKey', defaultValue);
 */
export function usePersistedState<T>(
  key: string,
  defaultValue: T,
  options?: {
    expireAfter?: number;  // Tempo em ms para expirar (opcional)
    sessionOnly?: boolean; // Usar sessionStorage ao invés de localStorage
  }
): [T, Dispatch<SetStateAction<T>>, () => void] {
  const storage = options?.sessionOnly ? sessionStorage : localStorage;
  const storageKey = `advisoria-${key}`;
  
  // Inicializar estado
  const [state, setState] = useState<T>(() => {
    try {
      const stored = storage.getItem(storageKey);
      if (!stored) return defaultValue;
      
      const parsed = JSON.parse(stored);
      
      // Verificar expiração se configurado
      if (options?.expireAfter && parsed.timestamp) {
        const now = Date.now();
        const elapsed = now - parsed.timestamp;
        if (elapsed > options.expireAfter) {
          // Expirado, remover e retornar default
          storage.removeItem(storageKey);
          return defaultValue;
        }
      }
      
      return parsed.value ?? defaultValue;
    } catch (error) {
      console.error(`[usePersistedState] Erro ao carregar ${key}:`, error);
      return defaultValue;
    }
  });
  
  // Salvar quando estado mudar
  useEffect(() => {
    try {
      const toStore = {
        value: state,
        timestamp: Date.now(),
      };
      storage.setItem(storageKey, JSON.stringify(toStore));
    } catch (error) {
      console.error(`[usePersistedState] Erro ao salvar ${key}:`, error);
    }
  }, [state, storageKey, storage]);
  
  // Função para limpar manualmente
  const clearPersistedState = () => {
    try {
      storage.removeItem(storageKey);
      setState(defaultValue);
    } catch (error) {
      console.error(`[usePersistedState] Erro ao limpar ${key}:`, error);
    }
  };
  
  return [state, setState, clearPersistedState];
}

/**
 * Hook especializado para persistir estado de análise do conselho
 */
export function usePersistedCouncilAnalysis(analysisId: string | null) {
  const key = analysisId ? `council-analysis-${analysisId}` : 'council-analysis-temp';
  
  return usePersistedState(key, null, {
    expireAfter: 24 * 60 * 60 * 1000, // 24 horas
  });
}

/**
 * Hook especializado para persistir mensagens de chat
 */
export function usePersistedChatMessages(conversationId: string | null) {
  const key = conversationId ? `chat-messages-${conversationId}` : 'chat-messages-temp';
  
  return usePersistedState(key, [], {
    expireAfter: 7 * 24 * 60 * 60 * 1000, // 7 dias
  });
}

/**
 * Hook especializado para persistir estado de criação de especialista
 */
export function usePersistedExpertCreation() {
  return usePersistedState('expert-creation', null, {
    expireAfter: 2 * 60 * 60 * 1000, // 2 horas
  });
}

