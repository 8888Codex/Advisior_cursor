/**
 * Hook Unificado para Análise do Conselho
 * Abstrai a complexidade dos 3 modos: SSE Stream, Background Polling e Traditional
 */

import { useState, useCallback } from "react";
import { useCouncilStream } from "./useCouncilStream";
import { useCouncilBackground } from "./useCouncilBackground";
import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { handleCouncilError } from "@/lib/errors";
import { validateCouncilRequest } from "@/lib/validation";
import type {
  CouncilAnalysis,
  CouncilMode,
  ExpertStatus,
  ActivityEvent,
  CouncilAnalysisRequest,
} from "@/types/council";

interface UseCouncilProps {
  mode?: CouncilMode;
  onSuccess?: (analysis: CouncilAnalysis) => void;
  onError?: (error: any) => void;
}

interface UseCouncilReturn {
  // Estado
  isAnalyzing: boolean;
  analysis: CouncilAnalysis | null;
  error: string | null;
  progress: number;
  
  // Dados visuais
  expertStatuses: ExpertStatus[];
  activityFeed: ActivityEvent[];
  
  // Ações
  startAnalysis: (request: CouncilAnalysisRequest) => Promise<void>;
  reset: () => void;
  
  // Metadados
  mode: CouncilMode;
}

/**
 * Hook unificado que gerencia todos os modos de análise do conselho
 */
export function useCouncil({
  mode = "background-polling",
  onSuccess,
  onError,
}: UseCouncilProps = {}): UseCouncilReturn {
  
  const [currentMode, setCurrentMode] = useState<CouncilMode>(mode);
  const [streamingEnabled, setStreamingEnabled] = useState(false);

  // Hook para SSE streaming
  const streamState = useCouncilStream({
    problem: "",
    expertIds: [],
    personaId: undefined,
    enabled: streamingEnabled && currentMode === "sse-stream",
  });

  // Hook para background polling
  const backgroundState = useCouncilBackground({
    problem: "",
    expertIds: [],
    personaId: undefined,
    enabled: streamingEnabled && currentMode === "background-polling",
  });

  // Mutation tradicional
  const traditionalMutation = useMutation({
    mutationFn: async (data: CouncilAnalysisRequest) => {
      const response = await apiRequest("/api/council/analyze", {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      });
      return response.json();
    },
    onSuccess,
    onError,
  });

  /**
   * Iniciar análise com validação automática
   */
  const startAnalysis = useCallback(async (request: CouncilAnalysisRequest) => {
    // Validação automática
    const validation = validateCouncilRequest(request, (props) => {
      // Toast será chamado pelo componente pai
      console.error("[useCouncil] Validation failed:", props);
    });

    if (!validation) {
      return; // Validação falhou
    }

    try {
      switch (currentMode) {
        case "sse-stream":
          // Usar streaming SSE
          setStreamingEnabled(true);
          // streamState.startStreaming() será chamado automaticamente
          break;

        case "background-polling":
          // Usar background polling
          setStreamingEnabled(true);
          // backgroundState.startAnalysis() será chamado automaticamente
          break;

        case "traditional":
          // Usar mutation tradicional
          traditionalMutation.mutate(request);
          break;
      }
    } catch (error) {
      if (onError) {
        onError(error);
      }
    }
  }, [currentMode, traditionalMutation, onError]);

  /**
   * Reset completo do estado
   */
  const reset = useCallback(() => {
    setStreamingEnabled(false);
    traditionalMutation.reset();
  }, [traditionalMutation]);

  // Combinar dados de todos os modos
  const isAnalyzing = 
    currentMode === "background-polling" ? backgroundState.isProcessing :
    currentMode === "sse-stream" ? streamState.isStreaming :
    traditionalMutation.isPending;

  const analysis =
    backgroundState.analysis ||
    streamState.finalAnalysis ||
    (traditionalMutation.data as CouncilAnalysis | undefined) ||
    null;

  const error =
    backgroundState.error ||
    streamState.error ||
    (traditionalMutation.error as any)?.message ||
    null;

  const expertStatuses =
    currentMode === "background-polling" ? backgroundState.expertStatusArray || [] :
    currentMode === "sse-stream" ? streamState.expertStatusArray || [] :
    [];

  const activityFeed =
    currentMode === "background-polling" ? backgroundState.activityFeed || [] :
    currentMode === "sse-stream" ? streamState.activityFeed || [] :
    [];

  const progress =
    currentMode === "background-polling" ? backgroundState.progress :
    currentMode === "sse-stream" ? (streamState.isStreaming ? 50 : 100) :
    0;

  return {
    isAnalyzing,
    analysis,
    error,
    progress,
    expertStatuses,
    activityFeed,
    startAnalysis,
    reset,
    mode: currentMode,
  };
}

