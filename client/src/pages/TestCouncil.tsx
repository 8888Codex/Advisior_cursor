import { useState, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Switch } from "@/components/ui/switch";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Loader2, Users, Sparkles, TrendingUp, Zap, Star, Lightbulb, Settings } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { useCouncilStream } from "@/hooks/useCouncilStream";
import { useDebounce } from "@/hooks/useDebounce";
import { CouncilAnimation } from "@/components/council/CouncilAnimation";
import { motion } from "framer-motion";
import { ExpertSelector } from "@/components/council/ExpertSelector";
import { CouncilResultDisplay } from "@/components/council/CouncilResultDisplay";
import { PreferencesSettings } from "@/components/settings/PreferencesSettings";
import { useToast } from "@/hooks/use-toast";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import { useNavigate } from "@tanstack/react-router";

interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  avatar?: string;
  category?: string;
}

interface ExpertRecommendation {
  expertId: string;
  expertName: string;
  relevanceScore: number;  // 1-5 stars
  justification: string;
}

interface CouncilAnalysis {
  id: string;
  problem: string;
  personaId?: string;
  contributions: Array<{
    expertId: string;
    expertName: string;
    analysis: string;
    keyInsights: string[];
    recommendations: string[];
  }>;
  consensus: string;
  actionPlan?: any;
}

interface Persona {
  id: string;
  name: string;
  researchMode: "quick" | "strategic";
}

export default function TestCouncil() {
  const [problem, setProblem] = useState("");
  const [selectedExperts, setSelectedExperts] = useState<string[]>([]);
  const [selectedPersonaId, setSelectedPersonaId] = useState<string>("");
  const [useStreaming, setUseStreaming] = useState(true); // Auto-enable for 2+ experts

  const { data: experts = [], isLoading: loadingExperts } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  // Buscar personas
  const { data: personas = [], isLoading: loadingPersonas } = useQuery<Persona[]>({
    queryKey: ["/api/personas"],
  });

  // Debounce problem input for recommendations (800ms delay)
  const debouncedProblem = useDebounce(problem, 800);

  // Get expert recommendations based on problem
  const { data: recommendationsData, isLoading: loadingRecommendations } = useQuery<{ recommendations: ExpertRecommendation[] }>({
    queryKey: ["/api/recommend-experts", debouncedProblem],
    queryFn: async () => {
      if (!debouncedProblem.trim() || debouncedProblem.trim().length < 10) {
        return { recommendations: [] };
      }
      
      const response = await apiRequest("/api/recommend-experts", {
        method: "POST",
        body: JSON.stringify({ problem: debouncedProblem }),
        headers: { "Content-Type": "application/json" },
      });
      return response.json();
    },
    enabled: debouncedProblem.trim().length >= 10,
  });

  const recommendations = recommendationsData?.recommendations || [];

  // SSE Streaming hook
  const [streamingEnabled, setStreamingEnabled] = useState(false);
  const streamState = useCouncilStream({
    problem: problem.trim(),
    expertIds: selectedExperts,
    personaId: selectedPersonaId,  // NOVO: passar personaId
    enabled: streamingEnabled,
  });

  // Traditional mutation (non-streaming)
  const analyzeMutation = useMutation({
    mutationFn: async (data: { problem: string; personaId: string; expertIds: string[] }) => {
      const response = await apiRequest("/api/council/analyze", {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      });
      return response.json();
    },
  });

  // Start streaming when enabled
  useEffect(() => {
    if (streamingEnabled && !streamState.isStreaming && !streamState.finalAnalysis) {
      streamState.startStreaming();
    }
  }, [streamingEnabled]);

  const handleToggleExpert = (expertId: string) => {
    setSelectedExperts((prev) =>
      prev.includes(expertId)
        ? prev.filter((id) => id !== expertId)
        : [...prev, expertId]
    );
  };

  const handleSelectAll = () => {
    if (selectedExperts.length === experts.length) {
      setSelectedExperts([]);
    } else {
      setSelectedExperts(experts.map((e) => e.id));
    }
  };

  const handleApplySuggestions = () => {
    const recommendedIds = recommendations.map(r => r.expertId);
    setSelectedExperts(recommendedIds);
  };

  const handleSubmit = async () => {
    if (!problem.trim()) return;
    if (selectedExperts.length === 0) return;
    
    // Validar persona (OBRIGATÓRIA)
    if (!selectedPersonaId) {
      toast({
        title: "Persona obrigatória",
        description: "Você precisa selecionar uma persona antes de usar o conselho. Crie uma persona na página de Personas.",
        variant: "destructive",
      });
      return;
    }

    if (useStreaming) {
      // Use SSE streaming (TODO: adicionar personaId ao streaming também)
      setStreamingEnabled(true);
    } else {
      // Use traditional mutation
      analyzeMutation.mutate({
        problem: problem.trim(),
        personaId: selectedPersonaId,
        expertIds: selectedExperts,
      });
    }
  };

  const analysis = streamState.finalAnalysis || (analyzeMutation.data as CouncilAnalysis | undefined);
  const isAnalyzing = useStreaming ? streamState.isStreaming : analyzeMutation.isPending;

  return (
    <div className="container mx-auto py-8 px-4 max-w-7xl">
      <motion.div 
        className="mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
      >
        <h1 className="text-4xl font-semibold mb-2 flex items-center gap-3">
          <Users className="h-10 w-10 text-muted-foreground" />
          Teste de Análise do Conselho
        </h1>
        <p className="text-muted-foreground">
          Teste a funcionalidade do conselho de IA com lendas do marketing
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Forms on the left */}
        <div className="lg:col-span-3 space-y-6">
          {/* Persona Selection - OBRIGATÓRIA */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.05, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <Card className="rounded-2xl">
              <CardHeader>
                <CardTitle className="font-semibold flex items-center gap-2">
                  Cliente Ideal (Persona)
                  <Badge variant="destructive" className="text-xs">Obrigatório</Badge>
                </CardTitle>
                <CardDescription>
                  Selecione a persona do seu cliente ideal. As recomendações serão personalizadas para este perfil.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {loadingPersonas ? (
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Carregando personas...</span>
                  </div>
                ) : personas.length === 0 ? (
                  <Alert>
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription className="flex items-center justify-between">
                      <span>Você precisa criar uma persona antes de usar o conselho.</span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate({ to: "/personas" })}
                      >
                        Criar Persona
                      </Button>
                    </AlertDescription>
                  </Alert>
                ) : (
                  <Select value={selectedPersonaId} onValueChange={setSelectedPersonaId}>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Selecione uma persona..." />
                    </SelectTrigger>
                    <SelectContent>
                      {personas.map((persona) => (
                        <SelectItem key={persona.id} value={persona.id}>
                          {persona.name} ({persona.researchMode === "quick" ? "Rápida" : "Estratégica"})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <Card className="rounded-2xl">
              <CardHeader>
                <CardTitle className="font-semibold">Seu Desafio de Negócio</CardTitle>
                <CardDescription>
                  Descreva o problema que você gostaria que o conselho analisasse
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Textarea
                  placeholder="Exemplo: Estamos lançando uma marca de moda sustentável para a Geração Z. Como devemos nos posicionar contra gigantes do fast fashion mantendo valores autênticos?"
                  value={problem}
                  onChange={(e) => setProblem(e.target.value)}
                  className="min-h-[150px] text-base"
                  disabled={analyzeMutation.isPending || !selectedPersonaId}
                  data-testid="input-problem"
                />
                <div className="flex items-center justify-between mt-2">
                  <div className="text-xs text-muted-foreground">
                    {problem.trim().length < 10 ? (
                      <span className="text-destructive">
                        Mínimo 10 caracteres ({problem.length}/10)
                      </span>
                    ) : (
                      <span className="text-green-600">
                        ✓ {problem.length} caracteres
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {problem.length > 0 && `${problem.length} caracteres`}
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* AI Recommendations Section */}
          {loadingRecommendations && debouncedProblem.trim().length >= 10 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
            >
              <Card className="border-accent/20 bg-muted/30 rounded-2xl">
                <CardContent className="pt-6 pb-6">
                  <div className="flex items-center gap-3">
                    <Loader2 className="h-5 w-5 animate-spin text-accent" />
                    <p className="text-sm text-muted-foreground">
                      Analisando seu problema para recomendar especialistas...
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {recommendations.length > 0 && !loadingRecommendations && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
            >
              <Card className="border-accent/20 bg-muted/30 rounded-2xl">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Lightbulb className="h-5 w-5 text-accent" />
                      <CardTitle className="text-lg font-semibold">Sugestões da IA</CardTitle>
                    </div>
                    <Button
                      variant="default"
                      size="sm"
                      onClick={handleApplySuggestions}
                      disabled={analyzeMutation.isPending || loadingRecommendations}
                      data-testid="button-apply-suggestions"
                    >
                      Usar Sugestões ({recommendations.length})
                    </Button>
                  </div>
                  <CardDescription>
                    Recomendamos estes especialistas com base no seu problema
                  </CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          )}

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <ExpertSelector
              experts={experts}
              selectedExperts={selectedExperts}
              recommendations={recommendations}
              loadingExperts={loadingExperts}
              isAnalyzing={isAnalyzing}
              onToggleExpert={handleToggleExpert}
              onSelectAll={handleSelectAll}
            />
          </motion.div>

          {/* Streaming Toggle */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <Card className="rounded-2xl">
            <CardContent className="pt-6 pb-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="streaming-mode" className="flex items-center gap-2 cursor-pointer font-semibold">
                    <Zap className="h-4 w-4 text-accent" />
                    Modo Streaming ao Vivo
                  </Label>
                  <p className="text-sm text-muted-foreground">
                    Veja os especialistas trabalhando em tempo real
                  </p>
                </div>
                <Switch
                  id="streaming-mode"
                  checked={useStreaming}
                  onCheckedChange={setUseStreaming}
                  disabled={isAnalyzing}
                  data-testid="switch-streaming"
                />
              </div>
            </CardContent>
            </Card>
          </motion.div>

          {/* Preferences Settings */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.35, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline" className="w-full gap-2">
                  <Settings className="h-4 w-4" />
                  Configurar Preferências de Conversa
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>Preferências de Conversa</DialogTitle>
                </DialogHeader>
                <PreferencesSettings isAuthenticated={false} />
              </DialogContent>
            </Dialog>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <Button
              onClick={handleSubmit}
            disabled={
              !problem.trim() ||
              !selectedPersonaId ||
              selectedExperts.length === 0 ||
              isAnalyzing
            }
            className="w-full"
            size="lg"
            data-testid="button-analyze"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analisando... (pode levar 1-3 minutos)
              </>
            ) : (
              <>
                {useStreaming ? <Zap className="mr-2 h-5 w-5" /> : <Sparkles className="mr-2 h-5 w-5" />}
                Consultar Conselho ({selectedExperts.length} especialista{selectedExperts.length !== 1 ? 's' : ''})
              </>
            )}
            </Button>
          </motion.div>

          {analyzeMutation.isError && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="border-destructive bg-destructive/5">
                <CardContent className="pt-6">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="h-5 w-5 text-destructive mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <p className="font-semibold text-destructive mb-1">Erro na análise</p>
                      <p className="text-sm text-destructive/80 mb-3">
                        {(analyzeMutation.error as Error).message || "Ocorreu um erro inesperado"}
                      </p>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => analyzeMutation.reset()}
                      >
                        Tentar Novamente
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>

        {/* Show CouncilAnimation when streaming */}
        {useStreaming && (streamState.isStreaming || streamState.expertStatusArray.length > 0) && (
          <div className="lg:col-span-3 mt-8">
            <CouncilAnimation
              expertStatuses={streamState.expertStatusArray}
              activityFeed={streamState.activityFeed}
              isStreaming={streamState.isStreaming}
            />
          </div>
        )}

        {/* Show results (for both streaming and non-streaming after completion) */}
        <CouncilResultDisplay analysis={analysis} isStreaming={useStreaming && (streamState.isStreaming || !streamState.finalAnalysis)} />

      </div>
    </div>
  );
}
