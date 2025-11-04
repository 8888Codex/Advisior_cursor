import { useState, useEffect, useCallback, useRef } from "react";
import { apiRequest } from "@/lib/queryClient";
import type {
  BackgroundTask,
  ExpertStatus,
  ActivityEvent,
} from "@/types/council";

// Re-export para compatibilidade com código existente
export type { ExpertStatus, ActivityEvent, BackgroundTask };

interface UseCouncilBackgroundProps {
  problem: string;
  expertIds: string[];
  personaId?: string;
  enabled: boolean;
}

export function useCouncilBackground({ problem, expertIds, personaId, enabled }: UseCouncilBackgroundProps) {
  const [task, setTask] = useState<BackgroundTask | null>(null);
  const [analysis, setAnalysis] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [expertStatuses, setExpertStatuses] = useState<Map<string, ExpertStatus>>(new Map());
  const [activityFeed, setActivityFeed] = useState<ActivityEvent[]>([]);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const taskIdRef = useRef<string | null>(null);
  const activityIdCounter = useRef(0);
  const prevProgressRef = useRef(0);
  
  // Helper para adicionar atividade ao feed
  const addActivity = useCallback((
    message: string,
    type: "info" | "success" | "error",
    expertName?: string
  ) => {
    const activity: ActivityEvent = {
      id: `activity-${activityIdCounter.current++}`,
      timestamp: Date.now(),
      expertName,
      message,
      type,
    };
    
    setActivityFeed((prev) => [...prev, activity].slice(-10)); // Keep last 10
  }, []);
  
  // Helper para atualizar status de especialista
  const updateExpertStatus = useCallback((
    expertId: string,
    expertName: string,
    updates: Partial<ExpertStatus>
  ) => {
    setExpertStatuses((prev) => {
      const newStatuses = new Map(prev);
      const current = newStatuses.get(expertId) || {
        expertId,
        expertName,
        status: "waiting" as const,
        progress: 0,
      };
      newStatuses.set(expertId, { ...current, ...updates });
      return newStatuses;
    });
  }, []);

  // Polling function - continues even if component unmounts
  const pollTaskStatus = useCallback(async (taskId: string) => {
    try {
      console.log(`[Council Background] Polling task: ${taskId}`);
      
      const response = await apiRequest(`/api/tasks/${taskId}`, {
        method: "GET",
      });
      
      const taskData: BackgroundTask = await response.json();
      const prevProgress = prevProgressRef.current;
      prevProgressRef.current = taskData.progress;
      setTask(taskData);
      
      console.log(`[Council Background] Task status: ${taskData.status}, progress: ${taskData.progress}%`);
      
      // Atualizar status dos especialistas baseado no progresso
      if (taskData.progress > prevProgress) {
        const progress = taskData.progress;
        const expertsCount = expertIds.length;
        
        // Distribuir progresso entre especialistas
        expertIds.forEach((expertId, index) => {
          const expertStart = (index / expertsCount) * 100;
          const expertEnd = ((index + 1) / expertsCount) * 100;
          const expertProgress = Math.min(100, Math.max(0, ((progress - expertStart) / (expertEnd - expertStart)) * 100));
          
          let status: ExpertStatus["status"] = "waiting";
          if (expertProgress >= 100) {
            status = "completed";
          } else if (expertProgress > 0) {
            status = "analyzing";
          }
          
          // Pegar nome do expert (se já temos na análise, usar; senão, placeholder)
          const expertName = taskData.result?.contributions?.find((c: any) => c.expertId === expertId)?.expertName || `Especialista ${index + 1}`;
          
          // Apenas atualizar se status mudou
          const currentStatus = expertStatuses.get(expertId);
          if (!currentStatus || currentStatus.status !== status || Math.abs(currentStatus.progress - expertProgress) > 5) {
          updateExpertStatus(expertId, expertName, {
            status,
            progress: expertProgress,
          });
          
            // Adicionar atividade quando especialista começar ou completar
            if (status === "analyzing" && (!currentStatus || currentStatus.status === "waiting")) {
              addActivity(`${expertName} está analisando...`, "info", expertName);
            } else if (status === "completed" && currentStatus?.status !== "completed") {
              addActivity(`${expertName} completou análise`, "success", expertName);
            }
          }
        });
      }
      
      if (taskData.status === "completed") {
        console.log("[Council Background] Task completed!", taskData.result);
        setAnalysis(taskData.result);
        setIsProcessing(false);
        
        // Marcar todos especialistas como completados com nomes reais
        if (taskData.result?.contributions) {
          taskData.result.contributions.forEach((contrib: any) => {
            updateExpertStatus(contrib.expertId, contrib.expertName, {
            status: "completed",
            progress: 100,
              insightCount: contrib.keyInsights?.length || 0,
              recommendationCount: contrib.recommendations?.length || 0,
            });
          });
        }
        
        addActivity("Análise do conselho completa!", "success");
        
        // Stop polling
        if (pollingIntervalRef.current) {
          clearInterval(pollingIntervalRef.current);
          pollingIntervalRef.current = null;
        }
      } else if (taskData.status === "failed") {
        console.error("[Council Background] Task failed:", taskData.error);
        setError(taskData.error || "Task failed");
        setIsProcessing(false);
        
        addActivity(`Erro: ${taskData.error}`, "error");
        
        // Stop polling
        if (pollingIntervalRef.current) {
          clearInterval(pollingIntervalRef.current);
          pollingIntervalRef.current = null;
        }
      }
      
    } catch (err: any) {
      console.error("[Council Background] Polling error:", err);
      // Continue polling even on errors (transient network issues)
    }
  }, [expertIds, expertStatuses, updateExpertStatus, addActivity]);

  // Start analysis
  const startAnalysis = useCallback(async () => {
    if (!personaId || !problem || expertIds.length === 0) {
      setError("Missing required fields");
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);
      setAnalysis(null);
      
      // Inicializar especialistas com status "waiting"
      const initialStatuses = new Map<string, ExpertStatus>();
      expertIds.forEach((expertId, index) => {
        initialStatuses.set(expertId, {
          expertId,
          expertName: `Especialista ${index + 1}`, // Placeholder até obter nome real
          status: "waiting",
          progress: 0,
        });
      });
      setExpertStatuses(initialStatuses);
      setActivityFeed([]);
      prevProgressRef.current = 0;
      
      console.log("[Council Background] Starting analysis...");
      addActivity(`Iniciando análise com ${expertIds.length} especialistas`, "info");
      
      // Start background task
      const response = await apiRequest("/api/council/analyze-async", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem,
          expertIds,
          personaId,
        }),
      });
      
      const taskData: BackgroundTask = await response.json();
      setTask(taskData);
      taskIdRef.current = taskData.id;
      
      console.log(`[Council Background] Task created: ${taskData.id}`);
      addActivity("Análise em background iniciada", "info");
      
      // Start polling every 3 seconds
      pollingIntervalRef.current = setInterval(() => {
        pollTaskStatus(taskData.id);
      }, 3000);
      
      // Poll immediately
      pollTaskStatus(taskData.id);
      
    } catch (err: any) {
      console.error("[Council Background] Start error:", err);
      setError(err.message || "Failed to start analysis");
      setIsProcessing(false);
    }
  }, [problem, expertIds, personaId, pollTaskStatus, addActivity]);

  // Resume polling on mount if there's a saved taskId
  useEffect(() => {
    if (taskIdRef.current && !pollingIntervalRef.current && isProcessing) {
      console.log(`[Council Background] Resuming polling for task: ${taskIdRef.current}`);
      
      // Start polling
      pollingIntervalRef.current = setInterval(() => {
        pollTaskStatus(taskIdRef.current!);
      }, 3000);
      
      // Poll immediately
      pollTaskStatus(taskIdRef.current);
    }
  }, [isProcessing, pollTaskStatus]);

  // Auto-start when enabled
  useEffect(() => {
    console.log('[useCouncilBackground] Auto-start check:', {
      enabled,
      isProcessing,
      hasAnalysis: !!analysis,
      hasError: !!error,
      willStart: enabled && !isProcessing && !analysis && !error
    });
    
    if (enabled && !isProcessing && !analysis && !error) {
      console.log('[useCouncilBackground] Auto-starting analysis...');
      startAnalysis();
    }
  }, [enabled, isProcessing, analysis, error, startAnalysis]);

  // Cleanup on unmount - DON'T stop the polling, just clear the interval
  // The task continues running on the server
  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    };
  }, []);

  return {
    task,
    analysis,
    error,
    isProcessing,
    progress: task?.progress || 0,
    startAnalysis,
    // Dados para visualização dos especialistas
    expertStatusArray: Array.from(expertStatuses.values()),
    activityFeed,
  };
}
