/**
 * Tipos centralizados para o sistema de Conselho
 * Single source of truth para todos os componentes e hooks
 */

// Status de processamento de um especialista
export interface ExpertStatus {
  expertId: string;
  expertName: string;
  expertAvatar?: string;
  status: "waiting" | "researching" | "analyzing" | "completed" | "failed";
  progress: number; // 0-100
  insightCount?: number;
  recommendationCount?: number;
  error?: string;
}

// Evento no feed de atividades
export interface ActivityEvent {
  id: string;
  timestamp: number;
  expertName?: string;
  message: string;
  type: "info" | "success" | "error";
}

// Contribuição de um especialista
export interface ExpertContribution {
  expertId: string;
  expertName: string;
  analysis: string;
  keyInsights: string[];
  recommendations: string[];
}

// Ação no plano de ação
export interface Action {
  actionNumber: number;
  title: string;
  description: string;
  estimatedTime: string;
  tools: string[];
  steps: string[];
}

// Fase do plano de ação
export interface Phase {
  phaseNumber: number;
  name: string;
  duration: string;
  objectives: string[];
  actions: Action[];
  dependencies: string[];
  deliverables: string[];
}

// Plano de ação completo
export interface ActionPlan {
  phases: Phase[];
  totalDuration?: string;
  estimatedBudget?: string;
  successMetrics: string[];
}

// Análise completa do conselho
export interface CouncilAnalysis {
  id: string;
  problem: string;
  personaId?: string;
  contributions: ExpertContribution[];
  consensus: string;
  actionPlan?: ActionPlan;
  createdAt?: string;
}

// Recomendação de especialista baseada no problema
export interface ExpertRecommendation {
  expertId: string;
  expertName: string;
  relevanceScore: number;  // 1-5 stars
  justification: string;
}

// Expert básico
export interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  avatar?: string;
  category?: string;
}

// Persona do cliente
export interface Persona {
  id: string;
  name: string;
  researchMode: "quick" | "strategic";
}

// Task de background
export interface BackgroundTask {
  id: string;
  userId: string;
  taskType: string;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  progress: number;
  result?: any;
  error?: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}

// Modos de análise do conselho
export type CouncilMode = "sse-stream" | "background-polling" | "traditional";

// Props para análise do conselho
export interface CouncilAnalysisRequest {
  problem: string;
  expertIds: string[];
  personaId: string;
}

// Estado do stream SSE
export interface CouncilStreamState {
  isStreaming: boolean;
  expertStatuses: Map<string, ExpertStatus>;
  activityFeed: ActivityEvent[];
  finalAnalysis: CouncilAnalysis | null;
  error: string | null;
}

// Task de background (também usado no backend)
export interface BackgroundTask {
  id: string;
  userId: string;
  taskType: string;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  progress: number;
  result?: any;
  error?: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}

