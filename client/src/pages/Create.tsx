import { useState } from "react";
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
import { Sparkles, Loader2, Brain, Search, Wand2, Check, MessageSquare, Send } from "lucide-react";
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

  const autoCloneMutation = useMutation({
    mutationFn: async (data: { targetName: string; context?: string }) => {
      // Simulate step progression
      setCloneStep("researching");
      await new Promise((resolve) => setTimeout(resolve, 1000));
      
      setCloneStep("analyzing");
      await new Promise((resolve) => setTimeout(resolve, 1000));
      
      setCloneStep("synthesizing");
      
      return await apiRequestJson<any>("/api/experts/auto-clone", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
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
      const response = await apiRequestJson<{ response: string }>("/api/experts/test-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          systemPrompt: generatedExpert.systemPrompt,
          message: message,
          history: testMessages
        }),
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
        return <Search className="h-5 w-5 animate-pulse" />;
      case "analyzing":
        return <Brain className="h-5 w-5 animate-pulse" />;
      case "synthesizing":
        return <Wand2 className="h-5 w-5 animate-pulse" />;
      case "complete":
        return <Check className="h-5 w-5" />;
      default:
        return null;
    }
  };

  const getStepText = (step: CloneStep) => {
    switch (step) {
      case "researching":
        return "Pesquisando biografia, filosofia e métodos...";
      case "analyzing":
        return "Analisando padrões cognitivos e expertise...";
      case "synthesizing":
        return "Sintetizando clone de alta fidelidade...";
      case "complete":
        return "Clone cognitivo pronto!";
      default:
        return "";
    }
  };

  const isProcessing = ["researching", "analyzing", "synthesizing"].includes(cloneStep);

  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <div className="inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm mb-4">
              <Sparkles className="h-4 w-4 text-primary" />
              <span className="text-muted-foreground">Clonagem Cognitiva Automática</span>
            </div>
            <h1 className="text-4xl font-bold mb-4">Criar Seu Especialista</h1>
            <p className="text-muted-foreground max-w-2xl">
              Digite o nome de quem você quer clonar. Nosso sistema pesquisa automaticamente 
              e cria um clone cognitivo de alta fidelidade usando Framework EXTRACT.
            </p>
          </div>

          {!generatedExpert && (
            <Card className="p-6">
              <form onSubmit={handleAutoClone} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="targetName">Quem você quer clonar?</Label>
                  <Input
                    id="targetName"
                    value={targetName}
                    onChange={(e) => setTargetName(e.target.value)}
                    placeholder="Ex: Steve Jobs, Elon Musk, Warren Buffett..."
                    required
                    disabled={isProcessing}
                    data-testid="input-target-name"
                    className="text-lg"
                  />
                  <p className="text-sm text-muted-foreground">
                    Pode ser qualquer pessoa pública com informação disponível online
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="context">Contexto Adicional (Opcional)</Label>
                  <Textarea
                    id="context"
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    placeholder="Ex: fundador da Apple, foco em design e inovação..."
                    rows={3}
                    disabled={isProcessing}
                    data-testid="input-context"
                  />
                  <p className="text-sm text-muted-foreground">
                    Adicione contexto para refinar a pesquisa
                  </p>
                </div>

                {isProcessing && (
                  <Card className="p-4 bg-primary/5 border-primary/20">
                    <div className="flex items-center gap-3">
                      <div className="text-primary">
                        {getStepIcon(cloneStep)}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">{getStepText(cloneStep)}</p>
                        <div className="w-full bg-muted rounded-full h-1.5 mt-2">
                          <div 
                            className="bg-primary h-1.5 rounded-full transition-all duration-1000"
                            style={{
                              width: cloneStep === "researching" ? "33%" :
                                     cloneStep === "analyzing" ? "66%" :
                                     cloneStep === "synthesizing" ? "90%" : "0%"
                            }}
                          />
                        </div>
                      </div>
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
              <Card className="p-6">
                <div className="flex items-center gap-2 text-primary mb-4">
                  <Check className="h-5 w-5" />
                  <h3 className="text-lg font-semibold">Clone Cognitivo Gerado com Sucesso!</h3>
                </div>

                <div className="space-y-4">
                  <div className="flex items-start gap-4">
                    <Avatar className="h-24 w-24 ring-2 ring-primary/20">
                      <AvatarFallback className="text-xl font-semibold">{initials}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-2xl font-bold mb-1">{generatedExpert.name}</h3>
                      <p className="text-muted-foreground mb-3">{generatedExpert.title}</p>
                      
                      {generatedExpert.expertise && generatedExpert.expertise.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {generatedExpert.expertise.map((skill: string, index: number) => (
                            <Badge key={index} variant="secondary">
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
                    <summary className="cursor-pointer text-sm font-medium text-primary hover-elevate p-3 rounded-md">
                      Ver System Prompt EXTRACT Completo
                    </summary>
                    <Card className="mt-2 p-4 bg-muted/50">
                      <pre className="text-xs whitespace-pre-wrap font-mono overflow-x-auto">
                        {generatedExpert.systemPrompt}
                      </pre>
                    </Card>
                  </details>
                </div>
              </Card>

              <Card className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-5 w-5 text-primary" />
                    <h3 className="text-lg font-semibold">Testar Clone</h3>
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
                    <div className="border rounded-lg p-4 space-y-3 min-h-[200px] max-h-[400px] overflow-y-auto">
                      {testMessages.length === 0 ? (
                        <p className="text-sm text-muted-foreground text-center py-8">
                          Faça uma pergunta para testar a personalidade do clone
                        </p>
                      ) : (
                        testMessages.map((msg, index) => (
                          <div
                            key={index}
                            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                          >
                            <div
                              className={`max-w-[80%] rounded-lg p-3 ${
                                msg.role === "user"
                                  ? "bg-primary text-primary-foreground"
                                  : "bg-muted"
                              }`}
                            >
                              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                            </div>
                          </div>
                        ))
                      )}
                      {testChatMutation.isPending && (
                        <div className="flex justify-start">
                          <div className="bg-muted rounded-lg p-3">
                            <Loader2 className="h-4 w-4 animate-spin" />
                          </div>
                        </div>
                      )}
                    </div>

                    <form onSubmit={handleTestSend} className="flex gap-2">
                      <Input
                        value={testInput}
                        onChange={(e) => setTestInput(e.target.value)}
                        placeholder="Digite sua pergunta..."
                        disabled={testChatMutation.isPending}
                        data-testid="input-test-message"
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
  );
}
