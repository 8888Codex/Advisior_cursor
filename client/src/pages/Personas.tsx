import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { queryClient, apiRequest } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Loader2, Download, Trash2, Edit, Sparkles, Check, X, Wand2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ResourceExhaustedError } from "@/components/ResourceExhaustedError";

interface Persona {
  id: string;
  userId: string;
  name: string;
  researchMode: "quick" | "strategic";
  job_statement: string;
  situational_contexts: string[];
  functional_jobs: string[];
  emotional_jobs: string[];
  social_jobs: string[];
  behaviors: Record<string, any>;
  aspirations: string[];
  goals: any[]; // Can be strings or objects
  pain_points_quantified: any[];
  decision_criteria: Record<string, any>;
  demographics: Record<string, any>;
  psychographics?: Record<string, any>;
  painPoints?: string[]; // Legacy field
  values: string[];
  touchpoints: any[];
  contentPreferences: Record<string, any>;
  communities: string[];
  behavioralPatterns?: Record<string, any>;
  researchData: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export default function Personas() {
  const { toast } = useToast();
  const [mode, setMode] = useState<"quick" | "strategic">("quick");
  const [targetDescription, setTargetDescription] = useState("");
  const [industry, setIndustry] = useState("");
  const [additionalContext, setAdditionalContext] = useState("");
  const [selectedPersona, setSelectedPersona] = useState<Persona | null>(null);
  const [resourceExhaustedError, setResourceExhaustedError] = useState(false);
  
  // 🆕 Estados para enhancement de descrição
  const [enhancedSuggestion, setEnhancedSuggestion] = useState<string>("");
  const [suggestedIndustry, setSuggestedIndustry] = useState<string>("");
  const [suggestedContext, setSuggestedContext] = useState<string>("");
  const [showEnhancedSuggestion, setShowEnhancedSuggestion] = useState(false);

  // Fetch personas
  const { data: personas = [], isLoading: loadingPersonas } = useQuery<Persona[]>({
    queryKey: ["/api/personas"],
  });

  // Create persona mutation
  const createPersonaMutation = useMutation({
    mutationFn: async (data: {
      mode: "quick" | "strategic";
      targetDescription: string;
      industry?: string;
      additionalContext?: string;
    }) => {
      const response = await apiRequest("/api/personas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        timeout: 120000, // 120 segundos (2 minutos) para modo estratégico
      });
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/personas"] });
      toast({
        title: "Persona criada!",
        description: "Sua persona foi gerada com sucesso.",
      });
      // Reset form
      setTargetDescription("");
      setIndustry("");
      setAdditionalContext("");
    },
    onError: (error: any) => {
      // Verificar se é um erro de recursos esgotados
      if (error.message && (
          error.message.includes('resource_exhausted') || 
          error.message.includes('Limite de recursos') ||
          error.message.includes('Connection failed')
      )) {
        setResourceExhaustedError(true);
        return;
      }
      
      toast({
        title: "Erro ao criar persona",
        description: error.message || "Tente novamente mais tarde.",
        variant: "destructive",
      });
    },
  });

  // 🆕 Enhance description mutation
  const enhanceDescriptionMutation = useMutation({
    mutationFn: async () => {
      const response = await apiRequest("/api/personas/enhance-description", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: targetDescription,
          industry: industry || undefined,
          context: additionalContext || undefined,
        }),
      });
      return response.json();
    },
    onSuccess: (data) => {
      setEnhancedSuggestion(data.enhanced);
      setSuggestedIndustry(data.suggested_industry || "");
      setSuggestedContext(data.suggested_context || "");
      setShowEnhancedSuggestion(true);
      toast({
        title: "✨ Descrição melhorada!",
        description: "A IA enriqueceu sua descrição e sugeriu indústria e contexto.",
        duration: 5000,
      });
    },
    onError: (error: any) => {
      toast({
        title: "Erro ao melhorar descrição",
        description: error.message || "Tente novamente.",
        variant: "destructive",
      });
    },
  });
  
  const handleEnhanceDescription = () => {
    if (!targetDescription.trim() || targetDescription.trim().length < 10) {
      toast({
        title: "Descrição muito curta",
        description: "Digite pelo menos 10 caracteres para a IA melhorar.",
        variant: "destructive",
      });
      return;
    }
    enhanceDescriptionMutation.mutate();
  };
  
  const handleApplyEnhanced = () => {
    setTargetDescription(enhancedSuggestion);
    if (suggestedIndustry) setIndustry(suggestedIndustry);
    if (suggestedContext) setAdditionalContext(suggestedContext);
    setShowEnhancedSuggestion(false);
    toast({
      title: "Sugestões aplicadas!",
      description: "Descrição, indústria e contexto foram preenchidos automaticamente.",
    });
  };
  
  const handleRejectEnhanced = () => {
    setShowEnhancedSuggestion(false);
    setEnhancedSuggestion("");
    setSuggestedIndustry("");
    setSuggestedContext("");
  };

  // Delete persona mutation
  const deletePersonaMutation = useMutation({
    mutationFn: async (personaId: string) => {
      await apiRequest(`/api/personas/${personaId}`, {
        method: "DELETE",
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/personas"] });
      setSelectedPersona(null);
      toast({
        title: "Persona deletada",
        description: "A persona foi removida com sucesso.",
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!targetDescription.trim()) {
      toast({
        title: "Campo obrigatório",
        description: "Descreva seu público-alvo.",
        variant: "destructive",
      });
      return;
    }

    createPersonaMutation.mutate({
      mode,
      targetDescription,
      industry: industry || undefined,
      additionalContext: additionalContext || undefined,
    });
  };

  const handleDownload = async (persona: Persona) => {
    try {
      const response = await fetch(`/api/personas/${persona.id}/download`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `persona_${persona.id}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      toast({
        title: "Erro ao baixar",
        description: "Não foi possível baixar a persona.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="container mx-auto py-8 max-w-7xl px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold mb-2">Persona Builder</h1>
        <p className="text-muted-foreground">
          Crie personas detalhadas usando pesquisa estratégica em comunidades do Reddit
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Column */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Nova Persona</CardTitle>
              <CardDescription>
                Pesquisa {mode === "quick" ? "rápida (1-2 min)" : "estratégica (5-10 min)"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Mode Selection */}
                <div className="space-y-2">
                  <Label>Modo de Pesquisa</Label>
                  <RadioGroup
                    value={mode}
                    onValueChange={(value) => setMode(value as "quick" | "strategic")}
                    data-testid="radio-mode"
                  >
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="quick" id="quick" data-testid="radio-quick" />
                      <Label htmlFor="quick" className="font-normal cursor-pointer">
                        Rápida (1-2 min)
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="strategic" id="strategic" data-testid="radio-strategic" />
                      <Label htmlFor="strategic" className="font-normal cursor-pointer">
                        Estratégica (5-10 min)
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                {/* Target Description */}
                <div className="space-y-3">
                  <Label htmlFor="target">Público-Alvo *</Label>
                  <Textarea
                    id="target"
                    data-testid="input-target"
                    placeholder="Ex: Profissionais B2B que investem em marketing digital"
                    value={targetDescription}
                    onChange={(e) => setTargetDescription(e.target.value)}
                    rows={3}
                    className="resize-none"
                  />
                  
                  {/* 🆕 Botão "Melhorar com IA" */}
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={handleEnhanceDescription}
                    disabled={!targetDescription.trim() || targetDescription.trim().length < 10 || enhanceDescriptionMutation.isPending}
                    className="w-full sm:w-auto gap-2"
                  >
                    {enhanceDescriptionMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Melhorando com IA...
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-4 w-4" />
                        Melhorar Descrição com IA
                      </>
                    )}
                  </Button>
                  
                  {/* 🆕 Card de Sugestão Melhorada */}
                  {showEnhancedSuggestion && enhancedSuggestion && (
                    <Card className="border-accent/50 bg-accent/5">
                      <CardContent className="pt-4 space-y-4">
                        <div className="flex items-start gap-2">
                          <Wand2 className="h-5 w-5 text-accent mt-0.5 flex-shrink-0" />
                          <div className="flex-1 space-y-3">
                            <div>
                              <p className="text-sm font-semibold text-foreground mb-2">
                                ✨ Sugestões da IA (mais específicas):
                            </p>
                              
                              {/* Descrição Melhorada */}
                              <div className="mb-3">
                                <p className="text-xs font-medium text-muted-foreground mb-1">
                                  📝 Descrição:
                                </p>
                                <p className="text-sm text-foreground leading-relaxed bg-background/50 p-3 rounded-lg border border-border/50">
                              {enhancedSuggestion}
                            </p>
                              </div>
                              
                              {/* Indústria Sugerida */}
                              {suggestedIndustry && (
                                <div className="mb-3">
                                  <p className="text-xs font-medium text-muted-foreground mb-1">
                                    🏢 Indústria:
                                  </p>
                                  <p className="text-sm text-foreground bg-background/50 p-2 rounded-lg border border-border/50">
                                    {suggestedIndustry}
                                  </p>
                                </div>
                              )}
                              
                              {/* Contexto Sugerido */}
                              {suggestedContext && (
                                <div>
                                  <p className="text-xs font-medium text-muted-foreground mb-1">
                                    💡 Contexto Adicional:
                                  </p>
                                  <p className="text-sm text-foreground bg-background/50 p-2 rounded-lg border border-border/50">
                                    {suggestedContext}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button
                            type="button"
                            size="sm"
                            onClick={handleApplyEnhanced}
                            className="gap-2"
                          >
                            <Check className="h-4 w-4" />
                            Usar Todas as Sugestões
                          </Button>
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={handleRejectEnhanced}
                            className="gap-2"
                          >
                            <X className="h-4 w-4" />
                            Manter Original
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>

                {/* Industry */}
                <div className="space-y-2">
                  <Label htmlFor="industry">Indústria (opcional)</Label>
                  <Input
                    id="industry"
                    data-testid="input-industry"
                    placeholder="Ex: E-commerce, SaaS, Marketing"
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                  />
                </div>

                {/* Additional Context (Strategic only) */}
                {mode === "strategic" && (
                  <div className="space-y-2">
                    <Label htmlFor="context">Contexto Adicional</Label>
                    <Textarea
                      id="context"
                      data-testid="input-context"
                      placeholder="Informações adicionais que podem ajudar na pesquisa..."
                      value={additionalContext}
                      onChange={(e) => setAdditionalContext(e.target.value)}
                      rows={3}
                    />
                  </div>
                )}

                {resourceExhaustedError ? (
                  <ResourceExhaustedError 
                    onRetry={() => {
                      setResourceExhaustedError(false);
                      handleSubmit(new Event('submit') as any);
                    }} 
                  />
                ) : (
                  <Button
                    type="submit"
                    data-testid="button-create-persona"
                    className="w-full"
                    disabled={createPersonaMutation.isPending}
                  >
                    {createPersonaMutation.isPending ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        {mode === "quick" ? "Pesquisando..." : "Analisando..."}
                      </>
                    ) : (
                      "Criar Persona"
                    )}
                  </Button>
                )}

                {!resourceExhaustedError && createPersonaMutation.isPending && (
                  <p className="text-sm text-muted-foreground text-center">
                    {mode === "quick"
                      ? "Pesquisando comunidades e extraindo insights..."
                      : "Conduzindo análise profunda em múltiplas frentes..."}
                  </p>
                )}
              </form>
            </CardContent>
          </Card>
        </div>

        {/* Personas List + Details */}
        <div className="lg:col-span-2 space-y-4">
          {loadingPersonas ? (
            <Card>
              <CardContent className="py-8 text-center">
                <Loader2 className="h-8 w-8 animate-spin mx-auto mb-2" />
                <p className="text-muted-foreground">Carregando personas...</p>
              </CardContent>
            </Card>
          ) : personas.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-muted-foreground">
                  Nenhuma persona criada ainda. Use o formulário ao lado para começar.
                </p>
              </CardContent>
            </Card>
          ) : (
            <>
              {/* Personas Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {personas.map((persona) => (
                  <Card
                    key={persona.id}
                    className={`cursor-pointer transition hover-elevate ${
                      selectedPersona?.id === persona.id ? "ring-2 ring-primary" : ""
                    }`}
                    onClick={() => setSelectedPersona(persona)}
                    data-testid={`card-persona-${persona.id}`}
                  >
                    <CardHeader>
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <CardTitle className="text-base truncate">
                            {persona.name}
                          </CardTitle>
                          <CardDescription className="text-xs">
                            {persona.researchMode === "quick" ? "Rápida" : "Estratégica"}
                            {" · "}
                            {new Date(persona.createdAt).toLocaleDateString("pt-BR")}
                          </CardDescription>
                        </div>
                        <div className="flex gap-1">
                          <Button
                            size="icon"
                            variant="ghost"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDownload(persona);
                            }}
                            data-testid={`button-download-${persona.id}`}
                          >
                            <Download className="h-4 w-4" />
                          </Button>
                          <Button
                            size="icon"
                            variant="ghost"
                            onClick={(e) => {
                              e.stopPropagation();
                              deletePersonaMutation.mutate(persona.id);
                            }}
                            data-testid={`button-delete-${persona.id}`}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2 text-sm">
                        <div>
                          <span className="text-muted-foreground">Job Statement:</span>{" "}
                          {persona.job_statement ? "Sim" : "Não"}
                        </div>
                        <div>
                          <span className="text-muted-foreground">Pain Points:</span>{" "}
                          {persona.pain_points_quantified?.length || persona.painPoints?.length || 0}
                        </div>
                        <div>
                          <span className="text-muted-foreground">Goals:</span>{" "}
                          {persona.goals?.length || 0}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Selected Persona Details */}
              {selectedPersona && (
                <Card data-testid="card-persona-details">
                  <CardHeader>
                    <CardTitle>{selectedPersona.name}</CardTitle>
                    <CardDescription>
                      Criada em {new Date(selectedPersona.createdAt).toLocaleDateString("pt-BR")} ·{" "}
                      Modo {selectedPersona.researchMode === "quick" ? "Rápido" : "Estratégico"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Job Statement */}
                    {selectedPersona.job_statement && (
                      <div>
                        <h3 className="font-semibold mb-2">Job Statement</h3>
                        <div className="bg-muted/50 p-4 rounded-md text-sm">
                          <p className="text-muted-foreground">{selectedPersona.job_statement}</p>
                        </div>
                      </div>
                    )}

                    {/* Demographics */}
                    {selectedPersona.demographics && Object.keys(selectedPersona.demographics).length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-2">Demografia</h3>
                        <div className="bg-muted/50 p-4 rounded-md space-y-1 text-sm">
                          {Object.entries(selectedPersona.demographics).map(([key, value]) => (
                            <div key={key}>
                              <span className="text-muted-foreground capitalize">
                                {key.replace(/([A-Z])/g, " $1").trim()}:
                              </span>{" "}
                              {String(value)}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Pain Points */}
                    {((selectedPersona.pain_points_quantified && selectedPersona.pain_points_quantified.length > 0) || (selectedPersona.painPoints && selectedPersona.painPoints.length > 0)) && (
                      <div>
                        <h3 className="font-semibold mb-2">Pain Points</h3>
                        <ul className="list-disc list-inside space-y-2 text-sm">
                          {selectedPersona.pain_points_quantified?.map((point: any, idx: number) => (
                            <li key={idx} className="text-muted-foreground">
                              <strong>{typeof point === 'object' ? point.description : point}</strong>
                              {typeof point === 'object' && point.impact && (
                                <span className="block text-xs mt-1">Impacto: {point.impact}</span>
                              )}
                            </li>
                          )) || selectedPersona.painPoints?.map((point, idx) => (
                            <li key={idx} className="text-muted-foreground">
                              {point}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Goals */}
                    {selectedPersona.goals?.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-2">Objetivos</h3>
                        <ul className="list-disc list-inside space-y-1 text-sm">
                          {selectedPersona.goals.map((goal: any, idx: number) => (
                            <li key={idx} className="text-muted-foreground">
                              {typeof goal === 'string' ? goal : goal.description || JSON.stringify(goal)}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Values */}
                    {selectedPersona.values.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-2">Valores</h3>
                        <div className="flex flex-wrap gap-2">
                          {selectedPersona.values.map((value, idx) => (
                            <span
                              key={idx}
                              className="bg-muted px-3 py-1 rounded-full text-sm"
                            >
                              {value}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Communities */}
                    {selectedPersona.communities.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-2">Comunidades Reddit</h3>
                        <div className="flex flex-wrap gap-2">
                          {selectedPersona.communities.map((community, idx) => (
                            <span
                              key={idx}
                              className="bg-muted px-3 py-1 rounded-full text-sm font-mono"
                            >
                              {community}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Behavioral Patterns (Strategic only) */}
                    {selectedPersona.researchMode === "strategic" &&
                      selectedPersona.behavioralPatterns &&
                      Object.keys(selectedPersona.behavioralPatterns).length > 0 && (
                        <div>
                          <h3 className="font-semibold mb-2">Padrões Comportamentais</h3>
                          <div className="bg-muted/50 p-4 rounded-md space-y-2 text-sm">
                            {Object.entries(selectedPersona.behavioralPatterns).map(
                              ([key, value]) => (
                                <div key={key}>
                                  <span className="font-medium capitalize">
                                    {key.replace(/([A-Z])/g, " $1").trim()}:
                                  </span>
                                  <div className="text-muted-foreground mt-1">
                                    {Array.isArray(value)
                                      ? value.join(", ")
                                      : String(value)}
                                  </div>
                                </div>
                              )
                            )}
                          </div>
                        </div>
                      )}

                    {/* Content Preferences (Strategic only) */}
                    {selectedPersona.researchMode === "strategic" &&
                      selectedPersona.contentPreferences &&
                      Object.keys(selectedPersona.contentPreferences).length > 0 && (
                        <div>
                          <h3 className="font-semibold mb-2">Preferências de Conteúdo</h3>
                          <div className="bg-muted/50 p-4 rounded-md space-y-2 text-sm">
                            {Object.entries(selectedPersona.contentPreferences).map(
                              ([key, value]) => (
                                <div key={key}>
                                  <span className="font-medium capitalize">
                                    {key.replace(/([A-Z])/g, " $1").trim()}:
                                  </span>
                                  <div className="text-muted-foreground mt-1">
                                    {Array.isArray(value)
                                      ? value.join(", ")
                                      : String(value)}
                                  </div>
                                </div>
                              )
                            )}
                          </div>
                        </div>
                      )}
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
