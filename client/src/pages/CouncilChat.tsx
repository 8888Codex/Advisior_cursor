import { useState, useEffect, useRef } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useRoute, useLocation } from "wouter";
import { useToast } from "@/hooks/use-toast";
import { apiRequest, apiRequestJson, queryClient } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, Users, ArrowLeft } from "lucide-react";
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
                    initial={{ opacity: 0, x: -20, y: 10 }}
                    animate={{ opacity: 1, x: 0, y: 0 }}
                    exit={{ opacity: 0 }}
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
                      <Card className="bg-muted/30">
                        <CardContent className="pt-4">
                          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                          {message.reactions && message.reactions.length > 0 && (
                            <div className="mt-3 pt-3 border-t space-y-1">
                              {message.reactions.map((reaction, idx) => (
                                <div key={idx} className="text-xs text-muted-foreground">
                                  <Badge variant="secondary" className="text-xs mr-2">
                                    {reaction.type === "agree" ? "✓" : reaction.type === "disagree" ? "✗" : reaction.type === "add" ? "+" : "?"}
                                  </Badge>
                                  <span className="font-medium">{reaction.expertName}:</span> {reaction.content || reaction.type}
                                </div>
                              ))}
                            </div>
                          )}
                          <p className="text-xs text-muted-foreground mt-2">
                            {new Date(message.timestamp).toLocaleTimeString("pt-BR", {
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </p>
                        </CardContent>
                      </Card>
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

