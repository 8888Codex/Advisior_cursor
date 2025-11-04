import { useState, useEffect, useRef } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useRoute, useLocation } from "wouter";
import { useToast } from "@/hooks/use-toast";
import { apiRequest, apiRequestJson, queryClient } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, Users, ArrowLeft, Sparkles, Lightbulb, Target } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { motion, AnimatePresence } from "framer-motion";
import { AnimatedPage } from "@/components/AnimatedPage";
import { useCouncilChat } from "@/hooks/useCouncilChat";

interface Persona {
  id: string;
  name: string;
}

interface Expert {
  id: string;
  name: string;
  avatar?: string;
}

interface CouncilConversation {
  id: string;
  personaId: string;
  problem: string;
  expertIds: string[];
}

// Função helper para gerar cores dos avatares
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
];

function getExpertAvatarColor(expertName: string): { bg: string; text: string } {
  if (EXPERT_COLOR_MAP[expertName]) {
    return EXPERT_COLOR_MAP[expertName];
  }
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

// Parser para extrair ações executáveis da resposta
interface ActionItem {
  title: string;
  steps: string[];
  resultado: string;
  tempo: string;
}

function parseExecutableResponse(content: string): {
  diagnostico: string;
  acoes: ActionItem[];
  template: string;
  metrica: string;
  armadilha: string;
  rawContent: string;
} {
  // Regex patterns
  const diagnosticoMatch = content.match(/##\s*🎯\s*DIAGNÓSTICO RÁPIDO\s*([\s\S]*?)(?=##|$)/i);
  const templateMatch = content.match(/##\s*📋\s*TEMPLATE PRONTO[\s\S]*?\n([\s\S]*?)(?=##|$)/i);
  const metricaMatch = content.match(/##\s*📊\s*COMO MEDIR[\s\S]*?\n([\s\S]*?)(?=##|⚠️|$)/i);
  const armadilhaMatch = content.match(/##\s*⚠️\s*ARMADILHA[\s\S]*?\n([\s\S]*?)$/i);
  
  // Parse ações
  const acoes: ActionItem[] = [];
  const acoesSection = content.match(/##\s*⚡.*?(?=##\s*📋|$)/is)?.[0] || '';
  const acaoMatches = acoesSection.matchAll(/\*\*AÇÃO\s+(\d+):\*\*\s*(.*?)\n-\s*\*\*Fazer agora:\*\*(.*?)\n-\s*\*\*Resultado:\*\*(.*?)\n-\s*\*\*Tempo:\*\*(.*?)(?=\*\*AÇÃO|\n\n|##|$)/gis);
  
  for (const match of acaoMatches) {
    acoes.push({
      title: match[2].trim(),
      steps: match[3].split('\n-').map(s => s.trim()).filter(Boolean),
      resultado: match[4].trim(),
      tempo: match[5].trim(),
    });
  }

  return {
    diagnostico: diagnosticoMatch?.[1]?.trim() || '',
    acoes,
    template: templateMatch?.[1]?.trim() || '',
    metrica: metricaMatch?.[1]?.trim() || '',
    armadilha: armadilhaMatch?.[1]?.trim() || '',
    rawContent: content,
  };
}

// Componente ExecutableMessage - Formato Executável
interface ExecutableMessageProps {
  message: any;
  expertName: string;
  expertColors: { bg: string; text: string };
}

function ExecutableMessage({ message, expertName, expertColors }: ExecutableMessageProps) {
  const { toast } = useToast();
  const parsed = parseExecutableResponse(message.content);
  const [checkedActions, setCheckedActions] = useState<Record<number, boolean>>({});
  const [showTemplate, setShowTemplate] = useState(false);
  
  const toggleAction = (idx: number) => {
    setCheckedActions(prev => ({ ...prev, [idx]: !prev[idx] }));
  };
  
  const completedCount = Object.values(checkedActions).filter(Boolean).length;
  
  return (
    <Card className="bg-muted/30 relative overflow-hidden border-l-4 border-l-primary/50">
      {/* Shimmer Effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/10 to-transparent -translate-x-full animate-shimmer pointer-events-none" />
      
      <CardContent className="pt-4 relative z-10 space-y-4">
        {/* Diagnóstico */}
        {parsed.diagnostico && (
          <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <p className="text-sm font-medium text-blue-700 dark:text-blue-300">
              🎯 {parsed.diagnostico}
            </p>
          </div>
        )}
        
        {/* Ações Executáveis */}
        {parsed.acoes.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-sm">⚡ Ações Imediatas</h4>
              {parsed.acoes.length > 0 && (
                <Badge variant={completedCount === parsed.acoes.length ? "default" : "secondary"}>
                  {completedCount}/{parsed.acoes.length} completas
                </Badge>
              )}
            </div>
            
            {parsed.acoes.map((acao, idx) => (
              <Card key={idx} className={`p-3 transition-all ${checkedActions[idx] ? 'opacity-50 bg-green-500/5' : ''}`}>
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    checked={checkedActions[idx] || false}
                    onChange={() => toggleAction(idx)}
                    className="mt-1 h-5 w-5 rounded border-2 cursor-pointer"
                  />
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-2">
                      <p className="font-semibold text-sm">{acao.title}</p>
                      <Badge variant="outline" className="text-xs">{acao.tempo}</Badge>
                    </div>
                    <div className="space-y-1">
                      {acao.steps.map((step, sidx) => (
                        <p key={sidx} className="text-xs text-muted-foreground pl-3 border-l-2 border-primary/30">
                          {step}
                        </p>
                      ))}
                    </div>
                    <p className="text-xs text-green-700 dark:text-green-400">
                      ✓ Resultado: {acao.resultado}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
        
        {/* Template Pronto */}
        {parsed.template && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-sm">📋 Template Pronto</h4>
              <Button
                size="sm"
                variant="outline"
                onClick={() => setShowTemplate(!showTemplate)}
              >
                {showTemplate ? 'Ocultar' : 'Ver Template'}
              </Button>
            </div>
            
            {showTemplate && (
              <Card className="p-3 bg-accent/5 border-accent/20">
                <pre className="text-xs whitespace-pre-wrap font-mono">
                  {parsed.template}
                </pre>
                <Button
                  size="sm"
                  className="mt-3"
                  onClick={() => {
                    navigator.clipboard.writeText(parsed.template);
                    toast({ title: "✅ Template copiado!" });
                  }}
                >
                  Copiar Template
                </Button>
              </Card>
            )}
          </div>
        )}
        
        {/* Métrica + Armadilha */}
        <div className="grid grid-cols-2 gap-3">
          {parsed.metrica && (
            <div className="p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
              <p className="text-xs font-medium text-green-700 dark:text-green-300">
                📊 {parsed.metrica}
              </p>
            </div>
          )}
          {parsed.armadilha && (
            <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
              <p className="text-xs font-medium text-red-700 dark:text-red-300">
                ⚠️ {parsed.armadilha}
              </p>
            </div>
          )}
        </div>
        
        {/* Fallback: se não parseou, mostrar raw */}
        {parsed.acoes.length === 0 && !parsed.diagnostico && (
          <p className="text-sm whitespace-pre-wrap">{parsed.rawContent}</p>
        )}
        
        {/* Timestamp */}
        <p className="text-xs text-muted-foreground mt-2">
          {new Date(message.timestamp).toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </CardContent>
    </Card>
  );
}

// Componente InsightsPanel - "Efeito Disney" 🎭
interface InsightsPanelProps {
  analysis: any;
}

function InsightsPanel({ analysis }: InsightsPanelProps) {
  if (!analysis) return null;
  
  const allInsights = analysis.contributions.flatMap((c: any) => 
    c.keyInsights.map((insight: string) => ({
      expert: c.expertName,
      insight,
    }))
  );
  
  const allRecommendations = analysis.contributions.flatMap((c: any) =>
    c.recommendations.map((rec: string) => ({
      expert: c.expertName,
      recommendation: rec,
    }))
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="mb-4 bg-gradient-to-br from-primary/5 via-accent/5 to-primary/5 border-2 border-primary/20 shadow-lg">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-accent animate-pulse" />
              <CardTitle className="text-lg">💎 Insights do Conselho</CardTitle>
            </div>
            <Badge variant="secondary" className="font-semibold">
              {allInsights.length + allRecommendations.length} descobertas
            </Badge>
          </div>
          <CardDescription>
            Conhecimento acumulado dos especialistas — sempre disponível
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="insights" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="insights">
                <Lightbulb className="h-4 w-4 mr-2" />
                Insights ({allInsights.length})
              </TabsTrigger>
              <TabsTrigger value="recommendations">
                <Target className="h-4 w-4 mr-2" />
                Ações ({allRecommendations.length})
              </TabsTrigger>
              <TabsTrigger value="consensus">
                <Users className="h-4 w-4 mr-2" />
                Consenso
              </TabsTrigger>
            </TabsList>
          
            <TabsContent value="insights" className="space-y-2 mt-4 max-h-64 overflow-y-auto pr-2">
              {allInsights.map((item, idx) => {
                const colors = getExpertAvatarColor(item.expert);
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex gap-3 items-start p-3 rounded-lg bg-background/60 hover:bg-background/90 transition-all duration-200 border border-border/50"
                  >
                    <Avatar className={`h-7 w-7 ${colors.bg} shrink-0`}>
                      <AvatarFallback className={`${colors.text} text-xs font-semibold`}>
                        {getExpertInitials(item.expert)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-muted-foreground mb-1">{item.expert}</p>
                      <p className="text-sm leading-relaxed">{item.insight}</p>
                    </div>
                  </motion.div>
                );
              })}
            </TabsContent>
          
            <TabsContent value="recommendations" className="space-y-2 mt-4 max-h-64 overflow-y-auto pr-2">
              {allRecommendations.map((item, idx) => {
                const colors = getExpertAvatarColor(item.expert);
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex gap-3 items-start p-3 rounded-lg bg-background/60 hover:bg-background/90 transition-all duration-200 border border-border/50"
                  >
                    <Avatar className={`h-7 w-7 ${colors.bg} shrink-0`}>
                      <AvatarFallback className={`${colors.text} text-xs font-semibold`}>
                        {getExpertInitials(item.expert)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-muted-foreground mb-1">{item.expert}</p>
                      <p className="text-sm leading-relaxed">{item.recommendation}</p>
                    </div>
                  </motion.div>
                );
              })}
            </TabsContent>
          
            <TabsContent value="consensus" className="mt-4 max-h-64 overflow-y-auto pr-2">
              <div className="p-4 rounded-lg bg-background/60 border border-border/50">
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{analysis.consensus}</p>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export default function CouncilChat() {
  const [, params] = useRoute("/council-chat/:id");
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  
  // Obter conversationId da URL
  const conversationId = params?.id || null;
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Hook do chat
  const { conversation, messages, loadingMessages, isSending, isProcessing, sendMessage, error } = useCouncilChat(conversationId);

  // Buscar informações dos especialistas
  const { data: experts = [] } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
    enabled: !!conversation?.expertIds,
    select: (data) => {
      if (!conversation) return [];
      return data.filter((e) => conversation.expertIds.includes(e.id));
    },
  });

  // Buscar persona (buscar da lista)
  const { data: personas = [] } = useQuery<Persona[]>({
    queryKey: ["/api/personas"],
    enabled: !!conversation?.personaId,
  });
  const persona = personas.find((p) => p.id === conversation?.personaId);

  // Buscar análise inicial se disponível (para painel de insights)
  const { data: analysisData } = useQuery({
    queryKey: [`/api/council/analysis/${conversation?.analysisId}`],
    enabled: !!conversation?.analysisId,
  });

  // Auto-scroll para última mensagem
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
      } else if (messagesContainerRef.current) {
        messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
      }
    }, 100);
    return () => clearTimeout(timeoutId);
  }, [messages.length, isSending]);

  // Tratamento de erros
  useEffect(() => {
    if (error) {
      toast({
        variant: "destructive",
        title: "Erro ao enviar mensagem",
        description: error instanceof Error ? error.message : "Erro desconhecido",
      });
    }
  }, [error, toast]);

  const handleSend = () => {
    if (!input.trim() || isSending || !conversationId) return;
    sendMessage(input);
    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!conversationId) {
    return (
      <AnimatedPage>
        <div className="container mx-auto py-8 px-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-muted-foreground mb-4">Nenhuma conversa selecionada</p>
                <Button onClick={() => setLocation("/test-council")}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar para o Conselho
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </AnimatedPage>
    );
  }

  if (loadingMessages && messages.length === 0) {
    return (
      <AnimatedPage>
        <div className="container mx-auto py-8 px-4">
          <div className="flex items-center justify-center h-64">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        </div>
      </AnimatedPage>
    );
  }

  // Filtrar mensagens do sistema (opcional)
  const displayMessages = messages.filter((m) => m.role !== "system");

  return (
    <AnimatedPage>
      <div className="flex flex-col h-screen">
        {/* Header */}
        <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto px-4 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setLocation("/test-council")}
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar
                </Button>
                <div>
                  <h1 className="text-lg font-semibold flex items-center gap-2">
                    <Users className="h-5 w-5" />
                    Chat com Conselho
                  </h1>
                  {persona && (
                    <p className="text-xs text-muted-foreground">
                      Persona: {persona.name} • {experts.length} especialista(s)
                    </p>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {experts.map((expert) => {
                  const colors = getExpertAvatarColor(expert.name);
                  return (
                    <Avatar key={expert.id} className={`h-8 w-8 ${colors.bg}`}>
                      <AvatarFallback className={colors.text}>
                        {getExpertInitials(expert.name)}
                      </AvatarFallback>
                    </Avatar>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div
          ref={messagesContainerRef}
          className="flex-1 overflow-y-auto p-6 pb-6 space-y-4 min-h-0"
        >
          {/* Painel de Insights "Disney" - sempre visível */}
          {analysisData && (
            <InsightsPanel analysis={analysisData} />
          )}
          
          {displayMessages.length === 0 ? (
            <div className="text-center py-12 px-4">
              <Users className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
              <h3 className="text-lg font-semibold mb-2">Comece a conversa!</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Faça uma pergunta para os especialistas. Você pode perguntar sobre o plano de ação, detalhar estratégias ou pedir recomendações específicas.
              </p>
              
              {conversation?.problem && (
                <Card className="mt-6 max-w-2xl mx-auto mb-6">
                  <CardContent className="pt-4">
                    <p className="text-sm font-medium mb-2">📋 Problema Inicial:</p>
                    <p className="text-sm text-muted-foreground">{conversation.problem}</p>
                  </CardContent>
                </Card>
              )}
              
              {/* Perguntas sugeridas */}
              <div className="max-w-2xl mx-auto space-y-3">
                <p className="text-sm font-medium text-muted-foreground mb-3">
                  💡 Exemplos de perguntas:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-left">
                  {[
                    "Como podemos começar a implementar o plano de ação?",
                    "Quais são os principais desafios que devemos esperar?",
                    "Me explique a Fase 1 do plano em mais detalhes",
                    "Quais métricas devemos acompanhar primeiro?",
                  ].map((suggestion, idx) => (
                    <Button
                      key={idx}
                      variant="outline"
                      className="justify-start text-left h-auto py-2 px-3 text-xs"
                      onClick={() => setInput(suggestion)}
                    >
                      {suggestion}
                    </Button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <AnimatePresence>
              {displayMessages.map((message) => {
                const isUser = message.role === "user";
                const isSystem = message.role === "system";

                if (isSystem) return null;

                if (isUser) {
                  return (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, x: 20, y: 10 }}
                      animate={{ opacity: 1, x: 0, y: 0 }}
                      exit={{ opacity: 0 }}
                      className="flex justify-end"
                    >
                      <Card className="max-w-3xl bg-primary text-primary-foreground">
                        <CardContent className="pt-4">
                          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                          <p className="text-xs opacity-70 mt-2">
                            {new Date(message.timestamp).toLocaleTimeString("pt-BR", {
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </p>
                        </CardContent>
                      </Card>
                    </motion.div>
                  );
                }

                // Mensagem de especialista
                const colors = getExpertAvatarColor(message.expertName || "");
                const initials = getExpertInitials(message.expertName || "");

                return (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, scale: 0.95, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{
                      type: "spring",
                      stiffness: 120,
                      damping: 20,
                    }}
                    className="flex gap-3"
                  >
                    <Avatar className={`h-10 w-10 ${colors.bg} ring-2 ring-border/50 flex-shrink-0`}>
                      <AvatarFallback className={colors.text}>{initials}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center gap-2">
                        <p className="text-sm font-semibold">{message.expertName}</p>
                        <Badge variant="outline" className="text-xs">
                          Especialista
                        </Badge>
                      </div>
                      <ExecutableMessage 
                        message={message}
                        expertName={message.expertName || ''}
                        expertColors={colors}
                      />
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          )}

          {/* Loading indicator quando enviando ou processando */}
          {(isSending || isProcessing) && (
            <motion.div
              className="flex gap-3"
              initial={{ opacity: 0, x: -20, y: 10 }}
              animate={{ opacity: 1, x: 0, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="h-10 w-10 flex items-center justify-center">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
              <Card className="bg-muted/30">
                <CardContent className="pt-4">
                  <p className="text-sm text-muted-foreground">
                    {isSending ? "Enviando mensagem..." : "Os especialistas estão analisando sua mensagem em segundo plano..."}
                  </p>
                  {isProcessing && (
                    <p className="text-xs text-muted-foreground mt-1">
                      Você pode navegar para outras páginas. As respostas aparecerão automaticamente quando prontas.
                    </p>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto px-4 py-4">
            <div className="flex gap-2 items-end">
              <Textarea
                placeholder="Digite sua mensagem para o conselho..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                disabled={isSending || !conversationId}
                className="min-h-[60px] max-h-[200px] resize-none"
                rows={2}
              />
              <Button
                onClick={handleSend}
                disabled={!input.trim() || isSending || !conversationId}
                size="lg"
                className="shrink-0"
              >
                {isSending ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Send className="h-5 w-5" />
                )}
              </Button>
            </div>
            <div className="flex items-center justify-between mt-2">
              <p className="text-xs text-muted-foreground">
                {isSending
                  ? "Enviando mensagem..."
                  : isProcessing
                  ? "Processando respostas em segundo plano..."
                  : "Pressione Enter para enviar, Shift+Enter para nova linha"}
              </p>
              {isProcessing && (
                <Badge variant="secondary" className="text-xs">
                  <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                  Processando
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>
    </AnimatedPage>
  );
}

