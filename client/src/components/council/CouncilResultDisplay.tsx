import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { TrendingUp, Users, Loader2, Target, Lightbulb, FileText, MessageCircle, CheckCircle, Clock } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useTypingDelay } from "@/hooks/useTypingDelay";
import { ActionPlanDisplay } from "./ActionPlanDisplay";
import { useLocation } from "wouter";
import { useMutation } from "@tanstack/react-query";
import { apiRequestJson } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import { useEffect, useRef, useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import Confetti from "react-confetti";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

// Configuração de typing delay
const TYPING_DELAY_CONFIG = {
  speed: 25, // caracteres por segundo (velocidade natural de leitura)
  delay: 500, // delay inicial em ms antes de começar a digitar
} as const;

// Função helper para gerar avatar colorido baseado no nome do expert
// Sistema expandido com mais cores e mapeamento por nome para consistência
const EXPERT_COLOR_MAP: Record<string, { bg: string; text: string }> = {
  "Philip Kotler": { bg: "bg-blue-600", text: "text-white" },
  "Neil Patel": { bg: "bg-purple-600", text: "text-white" },
  "Sean Ellis": { bg: "bg-green-600", text: "text-white" },
  "Bill Bernbach": { bg: "bg-orange-500", text: "text-white" },
  "Seth Godin": { bg: "bg-indigo-600", text: "text-white" },
  "Ann Handley": { bg: "bg-pink-500", text: "text-white" },
  "Gary Vaynerchuk": { bg: "bg-red-500", text: "text-white" },
  "Dan Kennedy": { bg: "bg-amber-600", text: "text-white" },
  "David Ogilvy": { bg: "bg-teal-600", text: "text-white" },
  "Al Ries": { bg: "bg-cyan-600", text: "text-white" },
  "Jack Trout": { bg: "bg-emerald-600", text: "text-white" },
};

const DEFAULT_COLORS = [
  { bg: "bg-blue-500", text: "text-white" },
  { bg: "bg-purple-500", text: "text-white" },
  { bg: "bg-green-500", text: "text-white" },
  { bg: "bg-orange-500", text: "text-white" },
  { bg: "bg-pink-500", text: "text-white" },
  { bg: "bg-indigo-500", text: "text-white" },
  { bg: "bg-red-500", text: "text-white" },
  { bg: "bg-teal-500", text: "text-white" },
  { bg: "bg-cyan-500", text: "text-white" },
  { bg: "bg-emerald-500", text: "text-white" },
];

function getExpertAvatarColor(expertName: string): { bg: string; text: string } {
  // Verificar se há cor mapeada para este expert
  if (EXPERT_COLOR_MAP[expertName]) {
    return EXPERT_COLOR_MAP[expertName];
  }
  
  // Hash simples do nome para escolher cor consistente
  let hash = 0;
  for (let i = 0; i < expertName.length; i++) {
    hash = expertName.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % DEFAULT_COLORS.length;
  return DEFAULT_COLORS[index];
}

function getExpertInitials(expertName: string): string {
  return expertName
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

interface Action {
  id: string;
  title: string;
  description: string;
  responsible: string;
  priority: "alta" | "média" | "baixa";
  estimatedTime: string;
  tools: string[];
  steps: string[];
}

interface Phase {
  phaseNumber: number;
  name: string;
  duration: string;
  objectives: string[];
  actions: Action[];
  dependencies: string[];
  deliverables: string[];
}

interface ActionPlan {
  phases: Phase[];
  totalDuration: string;
  estimatedBudget?: string;
  successMetrics: string[];
}

interface CouncilAnalysis {
  id: string;
  problem: string;
  contributions: Array<{
    expertId: string;
    expertName: string;
    analysis: string;
    keyInsights: string[];
    recommendations: string[];
  }>;
  consensus: string;
  actionPlan?: ActionPlan;
}

interface CouncilResultDisplayProps {
  analysis: CouncilAnalysis | undefined;
  isStreaming: boolean;
}

export function CouncilResultDisplay({ analysis, isStreaming }: CouncilResultDisplayProps) {
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  const resultsRef = useRef<HTMLDivElement>(null);
  const prevAnalysisIdRef = useRef<string | undefined>(undefined);
  const [showConfetti, setShowConfetti] = useState(false);
  const [showSuccessBanner, setShowSuccessBanner] = useState(false);
  const [activeTab, setActiveTab] = useState("consensus");
  const showResults = analysis && !isStreaming;
  
  // Typing delay para consenso usando configuração centralizada
  const consensusText = useTypingDelay({
    text: analysis?.consensus || "",
    speed: TYPING_DELAY_CONFIG.speed,
    enabled: showResults && !!analysis?.consensus,
    delay: TYPING_DELAY_CONFIG.delay,
  });

  // Toast de sucesso quando análise completar
  useEffect(() => {
    if (analysis && analysis.id !== prevAnalysisIdRef.current && !isStreaming) {
      prevAnalysisIdRef.current = analysis.id;
      setShowConfetti(true);
      setShowSuccessBanner(true);
      
      toast({
        title: "✅ Análise completa!",
        description: `${analysis.contributions.length} especialista${analysis.contributions.length !== 1 ? 's' : ''} analisaram seu problema`,
        duration: 5000,
      });
      
      // Scroll automático para resultados após um pequeno delay
      setTimeout(() => {
        if (resultsRef.current) {
          resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
        }
        setShowConfetti(false); // Para confetti após 4 segundos
        setTimeout(() => setShowSuccessBanner(false), 3000); // Hide banner após 3s
      }, 500);
    }
  }, [analysis?.id, isStreaming, toast, analysis?.contributions.length]);

  // Mutation para criar conversa do conselho
  const createConversationMutation = useMutation({
    mutationFn: async () => {
      if (!analysis?.personaId || !analysis.contributions || analysis.contributions.length === 0) {
        throw new Error("Dados insuficientes para criar conversa");
      }
      
      const expertIds = analysis.contributions.map((c) => c.expertId);
      
      const response = await apiRequestJson<{ id: string }>("/api/council/conversations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem: analysis.problem,
          personaId: analysis.personaId,
          expertIds: expertIds,
          analysisId: analysis.id,  // Passar o ID da análise para contexto
        }),
      });
      
      return response;
    },
    onSuccess: (data) => {
      // Navegar para a página de chat
      setLocation(`/council-chat/${data.id}`);
    },
    onError: (error: any) => {
      toast({
        variant: "destructive",
        title: "Erro ao criar conversa",
        description: error?.message || "Não foi possível iniciar a conversa com o conselho",
      });
    },
  });

  if (!showResults) {
    // Mostrar skeleton se estiver analisando, senão mostrar estado vazio
    if (isStreaming) {
      return (
        <div className="lg:col-span-3 mt-8">
          <Card className="rounded-2xl">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Loader2 className="h-5 w-5 animate-spin text-accent" />
                <CardTitle className="font-semibold">Analisando problema...</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Skeleton className="h-6 w-32 mb-4" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-5/6" />
                </div>

                <Separator className="my-4" />

                <Skeleton className="h-6 w-48" />
                {Array.from({ length: 3 }).map((_, i) => (
                  <Card key={i} className="rounded-xl">
                    <CardContent className="pt-4">
                      <div className="flex items-center gap-3 mb-3">
                        <Skeleton className="h-10 w-10 rounded-full" />
                        <Skeleton className="h-5 w-32" />
                      </div>
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-4/5" />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      );
    }
    
    return (
      <div className="lg:col-span-3 mt-8">
        <Card className="border-dashed rounded-2xl">
          <CardContent className="pt-6">
            <div className="text-center text-muted-foreground py-12">
              <Users className="h-12 w-12 mx-auto mb-4 opacity-30" />
              <p className="text-sm">Envie um problema para ver a análise do conselho</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div ref={resultsRef} className="lg:col-span-3 mt-8">
      {/* Confetti Effect */}
      {showConfetti && (
        <Confetti
          width={window.innerWidth}
          height={window.innerHeight}
          recycle={false}
          numberOfPieces={200}
          gravity={0.3}
        />
      )}
      
      {/* Success Banner */}
      <AnimatePresence>
        {showSuccessBanner && analysis && !isStreaming && (
          <motion.div
            initial={{ opacity: 0, y: -50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -50, scale: 0.9 }}
            transition={{ type: "spring", bounce: 0.4, duration: 0.6 }}
            className="fixed top-20 left-1/2 -translate-x-1/2 z-50 w-full max-w-md px-4"
          >
            <Card className="bg-gradient-to-r from-green-500 to-emerald-500 text-white border-none shadow-2xl">
              <CardContent className="pt-6 pb-6">
                <div className="flex items-center gap-4">
                  <motion.div
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ delay: 0.2, type: "spring", bounce: 0.6 }}
                  >
                    <CheckCircle className="h-12 w-12" />
                  </motion.div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold mb-1">Análise Concluída! 🎉</h3>
                    <div className="flex flex-wrap gap-2 text-sm opacity-90">
                      <span className="flex items-center gap-1">
                        <Users className="h-3 w-3" />
                        {analysis.contributions.length} especialistas
                      </span>
                      <span className="flex items-center gap-1">
                        <TrendingUp className="h-3 w-3" />
                        {analysis.actionPlan?.phases?.length || 0} fases
                      </span>
                      <span className="flex items-center gap-1">
                        <Target className="h-3 w-3" />
                        Plano completo gerado
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <Card className="rounded-2xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-semibold">
              <TrendingUp className="h-5 w-5 text-accent" />
              Insights do Conselho
            </CardTitle>
            <CardDescription>
              Análise de {analysis.contributions.length} especialista{analysis.contributions.length !== 1 ? 's' : ''}
            </CardDescription>
          </CardHeader>
          <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full max-w-md grid-cols-3 mb-6">
              <TabsTrigger value="consensus" className="gap-2">
                <Target className="h-4 w-4" />
                Consenso
              </TabsTrigger>
              <TabsTrigger value="contributions" className="gap-2">
                <Users className="h-4 w-4" />
                Contribuições
              </TabsTrigger>
              <TabsTrigger value="summary" className="gap-2">
                <FileText className="h-4 w-4" />
                Resumo
              </TabsTrigger>
            </TabsList>
            
            {/* Tab: Consenso */}
            <TabsContent value="consensus" className="mt-6">
            <div className="space-y-4">
                <h3 className="font-semibold mb-4 text-lg flex items-center gap-2">
                  <Target className="h-5 w-5 text-primary" />
                  Consenso Estratégico
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                  {consensusText}
                </p>
            </div>
            </TabsContent>
            
            {/* Tab: Contribuições */}
            <TabsContent value="contributions" className="mt-6">
            <div className="space-y-4">
                <h3 className="font-semibold mb-4 text-lg flex items-center gap-2">
                  <Users className="h-5 w-5 text-primary" />
                  Contribuições dos Especialistas
                </h3>
                <ScrollArea className="h-[600px] pr-4">
                  <div className="space-y-3">
                    {analysis.contributions.map((contrib, idx) => {
                      const avatarColors = getExpertAvatarColor(contrib.expertName);
                      const initials = getExpertInitials(contrib.expertName);
                      
                      return (
                        <motion.div
                          key={idx}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                        >
                        <Card className="rounded-xl bg-muted/30 hover:shadow-md transition-shadow duration-200 hover:border-primary/20">
                          <CardHeader className="pb-3">
                            <div className="flex items-center gap-3">
                              <Avatar className={`h-10 w-10 ${avatarColors.bg} ring-2 ring-border/50`}>
                                <AvatarFallback className={`${avatarColors.text} font-semibold text-sm`}>
                                  {initials}
                                </AvatarFallback>
                              </Avatar>
                              <CardTitle className="text-base font-semibold">
                                {contrib.expertName}
                              </CardTitle>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-3">
                            {contrib.keyInsights.length > 0 && (
                              <div>
                                <p className="text-sm font-medium mb-1">Principais Insights:</p>
                                <ul className="text-sm text-muted-foreground space-y-1 list-disc pl-5">
                                  {contrib.keyInsights.map((insight, i) => (
                                    <li key={i}>{insight}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {contrib.recommendations.length > 0 && (
                              <div>
                                <p className="text-sm font-medium mb-1">
                                  Recomendações:
                                </p>
                                <ul className="text-sm text-muted-foreground space-y-1 list-disc pl-5">
                                  {contrib.recommendations.map((rec, i) => (
                                    <li key={i}>{rec}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                        </motion.div>
                      );
                    })}
                  </div>
                </ScrollArea>
            </div>
            </TabsContent>
            
            {/* Tab: Resumo Executivo */}
            <TabsContent value="summary" className="mt-6">
            <div className="space-y-6">
                {/* Quick Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 rounded-lg bg-primary/5 border border-primary/20">
                    <div className="text-2xl font-bold text-primary">{analysis.contributions.length}</div>
                    <div className="text-xs text-muted-foreground">Especialistas</div>
                  </div>
                  <div className="p-4 rounded-lg bg-green-500/5 border border-green-500/20">
                    <div className="text-2xl font-bold text-green-600">
                      {analysis.contributions.reduce((sum, c) => sum + c.keyInsights.length, 0)}
                    </div>
                    <div className="text-xs text-muted-foreground">Insights</div>
                  </div>
                  <div className="p-4 rounded-lg bg-blue-500/5 border border-blue-500/20">
                    <div className="text-2xl font-bold text-blue-600">
                      {analysis.contributions.reduce((sum, c) => sum + c.recommendations.length, 0)}
                    </div>
                    <div className="text-xs text-muted-foreground">Recomendações</div>
                  </div>
                  <div className="p-4 rounded-lg bg-purple-500/5 border border-purple-500/20">
                    <div className="text-2xl font-bold text-purple-600">
                      {analysis.actionPlan?.phases?.length || 0}
                    </div>
                    <div className="text-xs text-muted-foreground">Fases do Plano</div>
                  </div>
                </div>
                
                {/* Resumo do Consenso */}
                <div>
                  <h4 className="font-semibold mb-2 flex items-center gap-2">
                    <Target className="h-4 w-4" />
                    Consenso em uma Linha
                  </h4>
                  <p className="text-sm text-muted-foreground line-clamp-3">
                    {analysis.consensus}
                  </p>
                </div>
                
                {/* Top 3 Insights */}
                <div>
                  <h4 className="font-semibold mb-2 flex items-center gap-2">
                    <Lightbulb className="h-4 w-4" />
                    Top 3 Insights
                  </h4>
                  <div className="space-y-2">
                    {analysis.contributions.slice(0, 3).map((contrib, idx) => (
                      contrib.keyInsights.length > 0 && (
                        <div key={idx} className="flex gap-2">
                          <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 text-primary text-xs flex items-center justify-center font-semibold">
                            {idx + 1}
                          </div>
                          <p className="text-sm text-muted-foreground flex-1">
                            <span className="font-medium">{contrib.expertName}:</span> {contrib.keyInsights[0]}
                          </p>
                        </div>
                      )
                    ))}
                  </div>
                </div>
                
                {/* Quick Actions */}
                <div className="flex flex-wrap gap-2 pt-4 border-t">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setActiveTab("consensus")}
                  >
                    Ver Consenso Completo
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setActiveTab("contributions")}
                  >
                    Ver Todas Contribuições
                  </Button>
                </div>
            </div>
            </TabsContent>
          </Tabs>
          </CardContent>
        </Card>
      </motion.div>

      {/* Action Plan Display */}
      {analysis.actionPlan && (
        <ActionPlanDisplay actionPlan={analysis.actionPlan} />
      )}

      {/* Continue Chat Button */}
      {analysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="mt-6"
        >
          <Card className="border-2 border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold mb-1">Quer continuar a conversa?</h3>
                  <p className="text-sm text-muted-foreground">
                    Converse diretamente com os especialistas em tempo real para detalhar o plano de ação
                  </p>
                </div>
                <Button
                  onClick={() => createConversationMutation.mutate()}
                  disabled={createConversationMutation.isPending}
                  className="ml-4"
                >
                  {createConversationMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Criando...
                    </>
                  ) : (
                    <>
                      <Users className="h-4 w-4 mr-2" />
                      Continuar Conversando
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
