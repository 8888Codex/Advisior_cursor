import { useState, useEffect, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { apiRequestJson } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { AnimatedPage } from "@/components/AnimatedPage";
import { Sparkles, Loader2, Brain, Search, Wand2, Check, MessageSquare, Send, Clock, Eye, EyeOff } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import type { Expert } from "@shared/schema";

type CloneStep = "idle" | "researching" | "analyzing" | "synthesizing" | "complete";

interface TestMessage {
  role: "user" | "assistant";
  content: string;
}

export default function Create() {
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  
  // Auto-clone form state
  const [targetName, setTargetName] = useState("");
  const [context, setContext] = useState("");
  const [cloneStep, setCloneStep] = useState<CloneStep>("idle");
  const [generatedExpert, setGeneratedExpert] = useState<any | null>(null); // ExpertCreate data, not persisted yet
  
  // Test chat state
  const [showTestChat, setShowTestChat] = useState(false);
  const [testMessages, setTestMessages] = useState<TestMessage[]>([]);
  const [testInput, setTestInput] = useState("");
  
  // Timer para mostrar tempo decorrido (usa Date.now para funcionar em background)
  const [elapsedTime, setElapsedTime] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [wasInBackground, setWasInBackground] = useState(false);
  const visibilityRef = useRef(false);
  
  // Calcular isProcessing ANTES do useEffect
  const isProcessing = ["researching", "analyzing", "synthesizing"].includes(cloneStep);
  
  // Timer effect - usa Date.now() ao invés de contador para funcionar mesmo em background
  useEffect(() => {
    if (isProcessing && !startTime) {
      setStartTime(Date.now());
    } else if (!isProcessing) {
      setStartTime(null);
      setElapsedTime(0);
    }
  }, [isProcessing, startTime]);
  
  // Atualizar tempo decorrido baseado em Date.now() (funciona mesmo em background)
  useEffect(() => {
    if (!startTime) return;
    
    const updateElapsed = () => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      setElapsedTime(elapsed);
    };
    
    // Atualizar imediatamente
    updateElapsed();
    
    // Usar requestAnimationFrame para melhor performance
    let animationId: number;
    const animate = () => {
      updateElapsed();
      animationId = requestAnimationFrame(animate);
    };
    animationId = requestAnimationFrame(animate);
    
    return () => {
      if (animationId) cancelAnimationFrame(animationId);
    };
  }, [startTime]);
  
  // 🆕 Detectar quando usuário volta para a aba
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        // Aba ficou em background
        visibilityRef.current = true;
        if (isProcessing) {
          console.log('[Create] Aba em background - requisição continua rodando');
        }
      } else {
        // Usuário voltou para a aba
        if (visibilityRef.current && isProcessing) {
          console.log('[Create] Usuário voltou - sincronizando estado');
          setWasInBackground(true);
          
          // Limpar flag após 3 segundos
          setTimeout(() => setWasInBackground(false), 3000);
        }
        visibilityRef.current = false;
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isProcessing]);

  const autoCloneMutation = useMutation({
    mutationFn: async (data: { targetName: string; context?: string }) => {
      // Simulate step progression com tempos mais realistas
      setCloneStep("researching");
      await new Promise((resolve) => setTimeout(resolve, 2000));  // 2s
      
      setCloneStep("analyzing");
      await new Promise((resolve) => setTimeout(resolve, 2000));  // 2s
      
      setCloneStep("synthesizing");
      // Não esperar aqui - deixa a API rodar
      
      // Timeout maior para auto-clone (180 segundos - Claude pode demorar gerando EXTRACT completo)
      return await apiRequestJson<any>("/api/experts/auto-clone", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        timeout: 180000, // 180 segundos (3 minutos) para auto-clone - EXTRACT é complexo
      });
    },
    onSuccess: (expertData) => {
      setCloneStep("complete");
      setGeneratedExpert(expertData);
      
      toast({
        title: "Clone Cognitivo Criado",
        description: `${expertData.name} foi sintetizado com sucesso.`,
      });
    },
    onError: (error: any) => {
      setCloneStep("idle");
      
      const errorMessage = error?.message || "Tente novamente mais tarde.";
      
      toast({
        title: "Erro ao criar clone",
        description: errorMessage,
        variant: "destructive",
      });
    },
  });

  const handleAutoClone = (e: React.FormEvent) => {
    e.preventDefault();
    autoCloneMutation.mutate({ 
      targetName, 
      context: context.trim() || undefined 
    });
  };

  const saveExpertMutation = useMutation({
    mutationFn: async (expertData: any) => {
      return await apiRequestJson<Expert>("/api/experts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(expertData),
      });
    },
    onSuccess: (expert) => {
      queryClient.invalidateQueries({ queryKey: ["/api/experts"] });
      setLocation("/");
      toast({
        title: "Especialista Salvo",
        description: `${expert.name} está pronto para consultas.`,
      });
    },
    onError: () => {
      toast({
        title: "Erro ao salvar",
        description: "Não foi possível salvar o especialista.",
        variant: "destructive",
      });
    },
  });

  const handleSaveExpert = () => {
    if (generatedExpert) {
      saveExpertMutation.mutate(generatedExpert);
    }
  };

  const handleRegenerate = () => {
    setGeneratedExpert(null);
    setCloneStep("idle");
    setShowTestChat(false);
    setTestMessages([]);
    autoCloneMutation.reset();
  };

  const testChatMutation = useMutation({
    mutationFn: async (message: string) => {
      if (!generatedExpert) throw new Error("No expert to test");
      
      // For testing, we'll use Claude directly with the generated system prompt
      // This avoids persisting temporary conversations
      // Timeout maior para test-chat (120 segundos - respostas longas do EXTRACT)
      const response = await apiRequestJson<{ response: string }>("/api/experts/test-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          systemPrompt: generatedExpert.systemPrompt,
          message: message,
          history: testMessages
        }),
        timeout: 120000, // 120 segundos (2 minutos) para test-chat
      });
      
      return response.response;
    },
    onSuccess: (response) => {
      setTestMessages((prev) => [
        ...prev,
        { role: "assistant", content: response }
      ]);
    },
    onError: () => {
      toast({
        title: "Erro no chat de teste",
        description: "Tente novamente.",
        variant: "destructive",
      });
    },
  });

  const handleTestSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!testInput.trim()) return;
    
    const userMessage = testInput.trim();
    setTestMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setTestInput("");
    testChatMutation.mutate(userMessage);
  };

  const initials = generatedExpert
    ? generatedExpert.name
        .split(" ")
        .map((n: string) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : "??";

  const getStepIcon = (step: CloneStep) => {
    switch (step) {
      case "researching":
        return <Search className="h-4 w-4" />;
      case "analyzing":
        return <Brain className="h-4 w-4" />;
      case "synthesizing":
        return <Wand2 className="h-4 w-4" />;
      case "complete":
        return <Check className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const getStepText = (step: CloneStep) => {
    switch (step) {
      case "researching":
        return "Pesquisando biografia, filosofia e métodos... (30-60s)";
      case "analyzing":
        return "Analisando padrões cognitivos e expertise... (30-60s)";
      case "synthesizing":
        return "Sintetizando clone EXTRACT de alta fidelidade (20 pontos)... Pode demorar 1-3 minutos. Não atualize a página! 🎯";
      case "complete":
        return "Clone cognitivo pronto!";
      default:
        return "";
    }
  };

  return (
    <AnimatedPage>
      <div className="min-h-screen py-12">
      <div className="container mx-auto px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <div className="inline-flex items-center gap-2 rounded-full bg-muted px-4 py-1.5 text-sm mb-4">
              <Sparkles className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Clonagem Cognitiva Automática - Framework EXTRACT</span>
            </div>
            <h1 className="text-4xl font-semibold mb-3 tracking-tight">Criar Seu Especialista</h1>
            <p className="text-muted-foreground max-w-2xl leading-relaxed">
              Digite o nome de quem você quer clonar. Nosso sistema cria um clone cognitivo de 
              <strong className="text-foreground"> ALTA FIDELIDADE (20/20)</strong> usando Framework EXTRACT de 20 pontos.
            </p>
            <div className="mt-3 p-3 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900 rounded-lg">
              <p className="text-sm text-amber-900 dark:text-amber-200">
                ⏱️ <strong>Tempo estimado:</strong> 1-3 minutos para máxima qualidade (Framework EXTRACT completo de 20 pontos)
              </p>
            </div>
          </div>

          {!generatedExpert && (
            <Card className="p-8 rounded-2xl">
              <form onSubmit={handleAutoClone} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="targetName" className="text-sm font-medium">Quem você quer clonar?</Label>
                  <Input
                    id="targetName"
                    value={targetName}
                    onChange={(e) => setTargetName(e.target.value)}
                    placeholder="Ex: Steve Jobs, Elon Musk, Warren Buffett..."
                    required
                    disabled={isProcessing}
                    data-testid="input-target-name"
                    className="text-base"
                  />
                  <p className="text-sm text-muted-foreground">
                    Pode ser qualquer pessoa pública com informação disponível online
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="context" className="text-sm font-medium">Contexto Adicional (Opcional)</Label>
                  <Textarea
                    id="context"
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    placeholder="Ex: fundador da Apple, foco em design e inovação..."
                    rows={3}
                    disabled={isProcessing}
                    data-testid="input-context"
                    className="resize-none"
                  />
                  <p className="text-sm text-muted-foreground">
                    Adicione contexto para refinar a pesquisa
                  </p>
                </div>

                {wasInBackground && isProcessing && (
                  <Card className="mb-4 p-4 rounded-2xl bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-900">
                    <div className="flex items-center gap-2">
                      <Eye className="h-4 w-4 text-green-600 dark:text-green-400" />
                      <p className="text-sm text-green-900 dark:text-green-200">
                        <strong>Bem-vindo de volta!</strong> O processo continuou rodando em segundo plano enquanto você estava em outra aba.
                      </p>
                    </div>
                  </Card>
                )}
                
                {isProcessing && (
                  <Card className="p-6 rounded-2xl bg-gradient-to-br from-accent/10 to-accent/5 border-accent/20">
                    <div className="space-y-4">
                      <div className="flex items-center gap-3">
                        <div className="text-accent flex-shrink-0">
                          <Loader2 className="h-5 w-5 animate-spin" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-foreground mb-1">
                            {cloneStep === "researching" ? "Pesquisando..." :
                             cloneStep === "analyzing" ? "Analisando..." :
                             cloneStep === "synthesizing" ? "Gerando Framework EXTRACT..." : "Processando..."}
                          </p>
                          <p className="text-xs text-muted-foreground leading-relaxed">{getStepText(cloneStep)}</p>
                        </div>
                      </div>
                      
                      <div className="w-full bg-background/50 rounded-full h-2 overflow-hidden">
                        <div 
                          className="bg-accent h-2 rounded-full transition-all duration-500 ease-out"
                          style={{
                            width: cloneStep === "researching" ? "20%" :
                                   cloneStep === "analyzing" ? "40%" :
                                   cloneStep === "synthesizing" ? "75%" : "0%"
                          }}
                        />
                      </div>
                      
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span>Tempo decorrido: {Math.floor(elapsedTime / 60)}:{(elapsedTime % 60).toString().padStart(2, '0')}</span>
                        <span className="text-accent">Estimado: 1-3 minutos</span>
                      </div>
                      
                      {cloneStep === "synthesizing" && (
                        <div className="mt-3 space-y-2">
                          <div className="p-3 bg-background/80 rounded-lg border border-border/50">
                            <p className="text-xs text-muted-foreground leading-relaxed mb-2">
                              💡 <strong className="text-foreground">Estamos gerando um clone de MÁXIMA QUALIDADE (20/20)</strong> com Framework EXTRACT completo de 20 pontos.
                            </p>
                            <ul className="text-xs text-muted-foreground space-y-1 ml-4">
                              <li>✓ Experiências formativas e padrões decisórios</li>
                              <li>✓ Terminologia própria e axiomas pessoais</li>
                              <li>✓ Story banks e callbacks icônicos</li>
                              <li>✓ Limitações e áreas de especialidade</li>
                              <li className="text-accent">⏳ Sintetizando... {elapsedTime > 60 ? "Quase lá!" : "Isso vale a pena!"}</li>
                            </ul>
                          </div>
                          
                          {elapsedTime > 90 && (
                            <div className="p-3 bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900 rounded-lg">
                              <p className="text-xs text-blue-900 dark:text-blue-200">
                                🔄 <strong>Ainda processando...</strong> Clone complexo pode demorar até 3 minutos. Não atualize a página!
                              </p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </Card>
                )}

                <Button 
                  type="submit" 
                  className="w-full gap-2" 
                  size="lg" 
                  disabled={isProcessing}
                  data-testid="button-auto-clone"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Criando Clone Cognitivo...
                    </>
                  ) : (
                    <>
                      <Brain className="h-4 w-4" />
                      Criar Clone Automático
                    </>
                  )}
                </Button>
              </form>
            </Card>
          )}

          {generatedExpert && cloneStep === "complete" && (
            <div className="space-y-6">
              <Card className="p-8 rounded-2xl hover-elevate transition-all duration-200">
                <div className="flex items-center gap-2 text-muted-foreground mb-6">
                  <Check className="h-5 w-5" />
                  <h3 className="text-lg font-medium">Clone Cognitivo Gerado com Sucesso!</h3>
                </div>

                <div className="space-y-6">
                  <div className="flex items-start gap-6">
                    <Avatar className="h-24 w-24 ring-1 ring-border/50">
                      <AvatarFallback className="text-xl font-medium">{initials}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-2xl font-semibold mb-2 tracking-tight">{generatedExpert.name}</h3>
                      <p className="text-muted-foreground mb-4 leading-relaxed">{generatedExpert.title}</p>
                      
                      {generatedExpert.expertise && generatedExpert.expertise.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {generatedExpert.expertise.map((skill: string, index: number) => (
                            <Badge key={index} variant="secondary" className="font-normal">
                              {skill}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {generatedExpert.bio}
                  </p>

                  <details className="group">
                    <summary className="cursor-pointer text-sm font-medium text-foreground hover-elevate active-elevate-2 p-4 rounded-xl transition-all duration-200">
                      Ver System Prompt EXTRACT Completo
                    </summary>
                    <Card className="mt-3 p-6 bg-muted/30 rounded-2xl">
                      <pre className="text-xs whitespace-pre-wrap font-mono overflow-x-auto leading-relaxed">
                        {generatedExpert.systemPrompt}
                      </pre>
                    </Card>
                  </details>
                </div>
              </Card>

              <Card className="p-6 rounded-2xl">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-5 w-5 text-muted-foreground" />
                    <h3 className="text-lg font-medium">Testar Clone</h3>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowTestChat(!showTestChat)}
                    data-testid="button-toggle-test-chat"
                  >
                    {showTestChat ? "Ocultar" : "Mostrar"} Chat
                  </Button>
                </div>

                {showTestChat && (
                  <div className="space-y-4">
                    <div className="border border-border/50 rounded-2xl p-4 space-y-3 min-h-[200px] max-h-[400px] overflow-y-auto">
                      {testMessages.length === 0 ? (
                        <p className="text-sm text-muted-foreground text-center py-12 leading-relaxed">
                          Faça uma pergunta para testar a personalidade do clone
                        </p>
                      ) : (
                        testMessages.map((msg, index) => (
                          <div
                            key={index}
                            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                          >
                            <div
                              className={`max-w-[80%] rounded-2xl p-4 transition-all duration-200 ${
                                msg.role === "user"
                                  ? "bg-accent text-accent-foreground"
                                  : "bg-muted"
                              }`}
                            >
                              <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                            </div>
                          </div>
                        ))
                      )}
                      {testChatMutation.isPending && (
                        <div className="flex justify-start">
                          <div className="bg-muted rounded-2xl p-4">
                            <Loader2 className="h-4 w-4 animate-spin" />
                          </div>
                        </div>
                      )}
                    </div>

                    <form onSubmit={handleTestSend} className="flex gap-3">
                      <Input
                        value={testInput}
                        onChange={(e) => setTestInput(e.target.value)}
                        placeholder="Digite sua pergunta..."
                        disabled={testChatMutation.isPending}
                        data-testid="input-test-message"
                        className="flex-1"
                      />
                      <Button
                        type="submit"
                        size="icon"
                        disabled={testChatMutation.isPending || !testInput.trim()}
                        data-testid="button-send-test-message"
                      >
                        <Send className="h-4 w-4" />
                      </Button>
                    </form>
                  </div>
                )}
              </Card>

              <div className="flex gap-4">
                <Button 
                  onClick={handleSaveExpert}
                  size="lg"
                  className="flex-1 gap-2"
                  disabled={saveExpertMutation.isPending}
                  data-testid="button-save-expert"
                >
                  {saveExpertMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Salvando...
                    </>
                  ) : (
                    <>
                      <Check className="h-4 w-4" />
                      Salvar Especialista
                    </>
                  )}
                </Button>
                <Button 
                  onClick={handleRegenerate}
                  variant="outline"
                  size="lg"
                  className="gap-2"
                  data-testid="button-regenerate"
                >
                  <Wand2 className="h-4 w-4" />
                  Regenerar
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
    </AnimatedPage>
  );
}
