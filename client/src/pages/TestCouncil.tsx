import { useState, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Loader2, Users, Sparkles, TrendingUp, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useCouncilStream } from "@/hooks/useCouncilStream";
import { CouncilAnimation } from "@/components/council/CouncilAnimation";

interface Expert {
  id: string;
  name: string;
  tagline: string;
  specialty: string;
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
}

export default function TestCouncil() {
  const [problem, setProblem] = useState("");
  const [selectedExperts, setSelectedExperts] = useState<string[]>([]);
  const [useStreaming, setUseStreaming] = useState(true); // Auto-enable for 2+ experts

  const { data: experts = [], isLoading: loadingExperts } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  // SSE Streaming hook
  const [streamingEnabled, setStreamingEnabled] = useState(false);
  const streamState = useCouncilStream({
    problem: problem.trim(),
    expertIds: selectedExperts,
    enabled: streamingEnabled,
  });

  // Traditional mutation (non-streaming)
  const analyzeMutation = useMutation({
    mutationFn: async (data: { problem: string; expertIds: string[] }) => {
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

  const handleSubmit = async () => {
    if (!problem.trim()) return;
    if (selectedExperts.length === 0) return;

    if (useStreaming) {
      // Use SSE streaming
      setStreamingEnabled(true);
    } else {
      // Use traditional mutation
      analyzeMutation.mutate({
        problem: problem.trim(),
        expertIds: selectedExperts,
      });
    }
  };

  const analysis = streamState.finalAnalysis || (analyzeMutation.data as CouncilAnalysis | undefined);
  const isAnalyzing = useStreaming ? streamState.isStreaming : analyzeMutation.isPending;

  return (
    <div className="container mx-auto py-8 px-4 max-w-7xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
          <Users className="h-10 w-10" />
          Teste de Análise do Conselho
        </h1>
        <p className="text-muted-foreground">
          Teste a funcionalidade do conselho de IA com lendas do marketing
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Seu Desafio de Negócio</CardTitle>
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
                disabled={analyzeMutation.isPending}
                data-testid="input-problem"
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Selecionar Especialistas</CardTitle>
                  <CardDescription>
                    Escolha quais lendas do marketing consultar ({selectedExperts.length}{" "}
                    selecionado{selectedExperts.length !== 1 ? 's' : ''})
                  </CardDescription>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleSelectAll}
                  disabled={loadingExperts || analyzeMutation.isPending}
                  data-testid="button-select-all"
                >
                  {selectedExperts.length === experts.length ? "Desmarcar Todos" : "Selecionar Todos"}
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {loadingExperts ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {experts.map((expert) => (
                    <div
                      key={expert.id}
                      className="flex items-start space-x-3 p-3 rounded-lg border hover-elevate cursor-pointer"
                      onClick={() => handleToggleExpert(expert.id)}
                      data-testid={`expert-card-${expert.id}`}
                    >
                      <Checkbox
                        checked={selectedExperts.includes(expert.id)}
                        onCheckedChange={() => handleToggleExpert(expert.id)}
                        disabled={analyzeMutation.isPending}
                        data-testid={`checkbox-expert-${expert.id}`}
                      />
                      <div className="flex-1 min-w-0">
                        <Label className="font-semibold cursor-pointer">
                          {expert.name}
                        </Label>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {expert.tagline}
                        </p>
                        <Badge variant="secondary" className="mt-1 text-xs">
                          {expert.specialty}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Streaming Toggle */}
          <Card>
            <CardContent className="pt-6 pb-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="streaming-mode" className="flex items-center gap-2 cursor-pointer">
                    <Zap className="h-4 w-4 text-primary" />
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

          <Button
            onClick={handleSubmit}
            disabled={
              !problem.trim() ||
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

          {analyzeMutation.isError && (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <p className="text-destructive">
                  ❌ Erro: {(analyzeMutation.error as Error).message}
                </p>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Show CouncilAnimation when streaming */}
        {useStreaming && (streamState.isStreaming || streamState.expertStatusArray.length > 0) && (
          <div className="lg:col-span-3">
            <CouncilAnimation
              expertStatuses={streamState.expertStatusArray}
              activityFeed={streamState.activityFeed}
              isStreaming={streamState.isStreaming}
            />
          </div>
        )}

        {/* Show results (for both streaming and non-streaming after completion) */}
        <div className={`lg:col-span-1 ${useStreaming && (streamState.isStreaming || !streamState.finalAnalysis) ? "hidden" : ""}`}>
          {analysis ? (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Insights do Conselho
                </CardTitle>
                <CardDescription>
                  Análise de {analysis.contributions.length} especialista{analysis.contributions.length !== 1 ? 's' : ''}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[600px] pr-4">
                  <div className="space-y-6">
                    <div>
                      <h3 className="font-semibold mb-2">📋 Consenso Estratégico</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                        {analysis.consensus}
                      </p>
                    </div>

                    <div className="space-y-4">
                      <h3 className="font-semibold">💡 Contribuições dos Especialistas</h3>
                      {analysis.contributions.map((contrib, idx) => (
                        <Card key={idx}>
                          <CardHeader className="pb-3">
                            <CardTitle className="text-base">
                              {contrib.expertName}
                            </CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-3">
                            {contrib.keyInsights.length > 0 && (
                              <div>
                                <p className="text-sm font-medium mb-1">Principais Insights:</p>
                                <ul className="text-sm text-muted-foreground space-y-1">
                                  {contrib.keyInsights.map((insight, i) => (
                                    <li key={i} className="flex gap-2">
                                      <span>•</span>
                                      <span>{insight}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {contrib.recommendations.length > 0 && (
                              <div>
                                <p className="text-sm font-medium mb-1">
                                  Recomendações:
                                </p>
                                <ul className="text-sm text-muted-foreground space-y-1">
                                  {contrib.recommendations.map((rec, i) => (
                                    <li key={i} className="flex gap-2">
                                      <span>→</span>
                                      <span>{rec}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-dashed">
              <CardContent className="pt-6">
                <div className="text-center text-muted-foreground py-12">
                  <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Envie um problema para ver a análise do conselho</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
