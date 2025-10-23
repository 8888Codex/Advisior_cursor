import { useState, useEffect, useCallback, useRef } from "react";

export interface ExpertStatus {
  expertId: string;
  expertName: string;
  status: "waiting" | "researching" | "analyzing" | "completed" | "failed";
  progress: number; // 0-100
  insightCount?: number;
  recommendationCount?: number;
  error?: string;
}

export interface ActivityEvent {
  id: string;
  timestamp: number;
  expertName?: string;
  message: string;
  type: "info" | "success" | "error";
}

export interface CouncilStreamState {
  isStreaming: boolean;
  expertStatuses: Map<string, ExpertStatus>;
  activityFeed: ActivityEvent[];
  finalAnalysis: any | null;
  error: string | null;
}

interface UseCouncilStreamProps {
  problem: string;
  expertIds: string[];
  enabled: boolean;
}

export function useCouncilStream({ problem, expertIds, enabled }: UseCouncilStreamProps) {
  const [state, setState] = useState<CouncilStreamState>({
    isStreaming: false,
    expertStatuses: new Map(),
    activityFeed: [],
    finalAnalysis: null,
    error: null,
  });

  const eventSourceRef = useRef<EventSource | null>(null);
  const activityIdCounter = useRef(0);

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
    
    setState((prev) => ({
      ...prev,
      activityFeed: [...prev.activityFeed, activity].slice(-10), // Keep last 10
    }));
  }, []);

  const updateExpertStatus = useCallback((
    expertId: string,
    expertName: string,
    updates: Partial<ExpertStatus>
  ) => {
    setState((prev) => {
      const newStatuses = new Map(prev.expertStatuses);
      const current = newStatuses.get(expertId) || {
        expertId,
        expertName,
        status: "waiting" as const,
        progress: 0,
      };
      newStatuses.set(expertId, { ...current, ...updates });
      return { ...prev, expertStatuses: newStatuses };
    });
  }, []);

  const startStreaming = useCallback(async () => {
    if (!enabled || !problem || expertIds.length === 0) return;
    
    // Initialize expert statuses
    const initialStatuses = new Map<string, ExpertStatus>();
    expertIds.forEach((expertId) => {
      initialStatuses.set(expertId, {
        expertId,
        expertName: "", // Will be populated from events
        status: "waiting",
        progress: 0,
      });
    });

    setState({
      isStreaming: true,
      expertStatuses: initialStatuses,
      activityFeed: [],
      finalAnalysis: null,
      error: null,
    });

    try {
      // Create EventSource connection
      const params = new URLSearchParams();
      params.append("problem", problem);
      expertIds.forEach((id) => params.append("expertIds", id));

      // Use fetch with SSE for POST data
      const response = await fetch("/api/council/analyze-stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ problem, expertIds }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No response body");
      }

      let buffer = "";

      while (true) {
        const { done, value} = await reader.read();
        
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const blocks = buffer.split("\n\n");
        buffer = blocks.pop() || "";

        for (const block of blocks) {
          if (!block.trim()) continue;
          
          const lines = block.split("\n");
          let eventType: string | null = null;
          let eventData: string | null = null;

          for (const line of lines) {
            if (line.startsWith("event:")) {
              eventType = line.substring(7).trim();
            } else if (line.startsWith("data:")) {
              eventData = line.substring(6).trim();
            }
          }

          if (eventType && eventData) {
            try {
              const data = JSON.parse(eventData);
              handleSSEEvent(eventType, data);
            } catch (e) {
              console.error("Failed to parse SSE data:", eventData, e);
            }
          }
        }
      }

    } catch (error: any) {
      console.error("Stream error:", error);
      setState((prev) => ({
        ...prev,
        isStreaming: false,
        error: error.message || "Stream connection failed",
      }));
      addActivity(`Error: ${error.message}`, "error");
    }
  }, [enabled, problem, expertIds, addActivity]);

  const handleSSEEvent = useCallback((eventType: string, data: any) => {
    console.log("SSE Event:", eventType, data);

    switch (eventType) {
      case "analysis_started":
        addActivity(`Starting analysis with ${data.expertCount} experts`, "info");
        // Populate expert names from data.experts
        data.experts?.forEach((expert: any) => {
          updateExpertStatus(expert.id, expert.name, {
            expertName: expert.name,
            status: "waiting",
            progress: 0,
          });
        });
        break;

      case "research_started":
        addActivity(data.message, "info");
        break;

      case "research_completed":
        addActivity(`${data.message} (${data.citations} sources)`, "success");
        break;

      case "research_failed":
        addActivity(data.message, "error");
        break;

      case "expert_started":
        updateExpertStatus(data.expertId, data.expertName, {
          status: "analyzing",
          progress: 25,
        });
        addActivity(data.message, "info", data.expertName);
        break;

      case "expert_completed":
        updateExpertStatus(data.expertId, data.expertName, {
          status: "completed",
          progress: 100,
          insightCount: data.insightCount,
          recommendationCount: data.recommendationCount,
        });
        addActivity(
          `Completed analysis (${data.insightCount} insights, ${data.recommendationCount} recommendations)`,
          "success",
          data.expertName
        );
        break;

      case "expert_failed":
        updateExpertStatus(data.expertId, data.expertName, {
          status: "failed",
          progress: 0,
          error: data.error,
        });
        addActivity(`Failed: ${data.error}`, "error", data.expertName);
        break;

      case "consensus_started":
        addActivity(data.message, "info");
        break;

      case "analysis_complete":
        setState((prev) => ({
          ...prev,
          isStreaming: false,
          finalAnalysis: data.analysis,
        }));
        addActivity("Council analysis complete!", "success");
        break;

      case "error":
        setState((prev) => ({
          ...prev,
          isStreaming: false,
          error: data.message,
        }));
        addActivity(data.message, "error");
        break;

      default:
        console.warn("Unknown SSE event type:", eventType);
    }
  }, [addActivity, updateExpertStatus]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return {
    ...state,
    startStreaming,
    expertStatusArray: Array.from(state.expertStatuses.values()),
  };
}
