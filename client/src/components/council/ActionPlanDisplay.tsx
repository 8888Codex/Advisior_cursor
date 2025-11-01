import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { CheckCircle2, Clock, Target, AlertCircle, TrendingUp, Users, Calendar, DollarSign, List, LayoutGrid, Search, Download } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

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

interface ActionPlanDisplayProps {
  actionPlan: ActionPlan;
}

const priorityColors = {
  alta: "destructive",
  média: "default",
  baixa: "secondary",
} as const;

const priorityLabels = {
  alta: "Alta Prioridade",
  média: "Média Prioridade",
  baixa: "Baixa Prioridade",
} as const;

export function ActionPlanDisplay({ actionPlan }: ActionPlanDisplayProps) {
  const [viewMode, setViewMode] = useState<"detailed" | "summary">("detailed");
  const [searchTerm, setSearchTerm] = useState("");
  
  if (!actionPlan || !actionPlan.phases || actionPlan.phases.length === 0) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          Plano de ação não disponível.
        </AlertDescription>
      </Alert>
    );
  }

  const totalActions = actionPlan.phases.reduce((sum, phase) => sum + phase.actions.length, 0);
  
  // Filtrar fases/ações baseado na busca
  const filteredPhases = searchTerm.trim() === "" 
    ? actionPlan.phases 
    : actionPlan.phases.map(phase => ({
        ...phase,
        actions: phase.actions.filter(action =>
          action.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          action.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
          action.responsible.toLowerCase().includes(searchTerm.toLowerCase())
        )
      })).filter(phase => phase.actions.length > 0);
  
  // Função para exportar para Markdown
  const exportToMarkdown = () => {
    let md = `# Plano de Ação Completo\n\n`;
    md += `**Duração Total:** ${actionPlan.totalDuration}\n`;
    md += `**Fases:** ${actionPlan.phases.length}\n`;
    md += `**Ações Totais:** ${totalActions}\n\n`;
    md += `---\n\n`;
    
    actionPlan.phases.forEach(phase => {
      md += `## Fase ${phase.phaseNumber}: ${phase.name}\n\n`;
      md += `**Duração:** ${phase.duration}\n\n`;
      
      if (phase.objectives.length > 0) {
        md += `### Objetivos:\n`;
        phase.objectives.forEach(obj => md += `- ${obj}\n`);
        md += `\n`;
      }
      
      md += `### Ações:\n\n`;
      phase.actions.forEach((action, idx) => {
        md += `#### ${idx + 1}. ${action.title}\n\n`;
        md += `**Descrição:** ${action.description}\n\n`;
        md += `**Responsável:** ${action.responsible}  \n`;
        md += `**Tempo Estimado:** ${action.estimatedTime}  \n`;
        md += `**Prioridade:** ${action.priority}\n\n`;
        
        if (action.steps.length > 0) {
          md += `**Passos:**\n`;
          action.steps.forEach((step, i) => md += `${i + 1}. ${step}\n`);
          md += `\n`;
        }
      });
      
      md += `---\n\n`;
    });
    
    // Criar e download
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `plano-de-acao-${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="mt-8"
    >
      <Card className="rounded-2xl border-2">
        <CardHeader className="pb-4">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <CardTitle className="text-2xl font-semibold mb-2 flex items-center gap-2">
                <Target className="h-6 w-6 text-primary" />
                Plano de Ação Completo
              </CardTitle>
              <CardDescription className="text-base">
                Plano estruturado e executável baseado no consenso dos especialistas
              </CardDescription>
            </div>
            
            {/* Controls */}
            <div className="flex items-center gap-2">
              {/* View Toggle */}
              <div className="flex items-center gap-1 border rounded-lg p-1">
                <Button
                  variant={viewMode === "summary" ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setViewMode("summary")}
                  className="h-8"
                >
                  <List className="h-4 w-4 mr-1" />
                  Resumo
                </Button>
                <Button
                  variant={viewMode === "detailed" ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setViewMode("detailed")}
                  className="h-8"
                >
                  <LayoutGrid className="h-4 w-4 mr-1" />
                  Detalhado
                </Button>
              </div>
              
              {/* Export Button */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" className="h-8">
                    <Download className="h-4 w-4 mr-1" />
                    Exportar
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem onClick={exportToMarkdown}>
                    📝 Markdown (.md)
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => window.print()}>
                    🖨️ Imprimir / PDF
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
          
          {/* Search */}
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar no plano de ação..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9"
            />
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Duração Total</p>
                <p className="text-sm font-medium">{actionPlan.totalDuration}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
              <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Fases</p>
                <p className="text-sm font-medium">{actionPlan.phases.length}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Ações</p>
                <p className="text-sm font-medium">{totalActions}</p>
              </div>
            </div>
            {actionPlan.estimatedBudget && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
                <DollarSign className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-xs text-muted-foreground">Budget Estimado</p>
                  <p className="text-sm font-medium">{actionPlan.estimatedBudget}</p>
                </div>
              </div>
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Summary View */}
          {viewMode === "summary" && (
            <div className="space-y-4">
              <h4 className="font-semibold text-lg mb-4">📋 Resumo Executivo</h4>
              
              {/* Timeline Visual */}
              <div className="relative">
                {filteredPhases.map((phase, idx) => (
                  <div key={phase.phaseNumber} className="flex gap-4 pb-6 last:pb-0">
                    <div className="flex flex-col items-center">
                      <div className={`flex items-center justify-center w-10 h-10 rounded-full ${idx === 0 ? 'bg-primary' : 'bg-muted'} ${idx === 0 ? 'text-white' : 'text-muted-foreground'} font-semibold`}>
                        {phase.phaseNumber}
                      </div>
                      {idx < filteredPhases.length - 1 && (
                        <div className="w-0.5 h-full bg-border my-1 flex-1" />
                      )}
                    </div>
                    <div className="flex-1 pb-2">
                      <h5 className="font-semibold mb-1">{phase.name}</h5>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                        <Clock className="h-3 w-3" />
                        {phase.duration}
                        <span>•</span>
                        {phase.actions.length} ação{phase.actions.length !== 1 ? "ões" : ""}
                      </div>
                      {phase.objectives.length > 0 && (
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {phase.objectives[0]}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Detailed View */}
          {viewMode === "detailed" && (
          <Accordion type="multiple" className="w-full" defaultValue={["phase-0"]}>
            {filteredPhases.map((phase, phaseIndex) => (
              <AccordionItem
                key={phase.phaseNumber}
                value={`phase-${phaseIndex}`}
                className="border rounded-lg px-4 mb-4"
              >
                <AccordionTrigger className="hover:no-underline">
                  <div className="flex items-center gap-3 flex-1 text-left">
                    <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary/10 text-primary font-semibold">
                      {phase.phaseNumber}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold">{phase.name}</h3>
                      <div className="flex items-center gap-3 mt-1">
                        <Badge variant="outline" className="text-xs">
                          <Clock className="h-3 w-3 mr-1" />
                          {phase.duration}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {phase.actions.length} ação{phase.actions.length !== 1 ? "ões" : ""}
                        </span>
                      </div>
                    </div>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pt-4 pb-6">
                  <div className="space-y-6">
                    {/* Objectives */}
                    {phase.objectives && phase.objectives.length > 0 && (
                      <div>
                        <h4 className="font-semibold mb-2 flex items-center gap-2">
                          <Target className="h-4 w-4" />
                          Objetivos da Fase
                        </h4>
                        <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-2">
                          {phase.objectives.map((objective, idx) => (
                            <li key={idx}>{objective}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Dependencies */}
                    {phase.dependencies && phase.dependencies.length > 0 && (
                      <Alert>
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>
                          <span className="font-medium">Dependências:</span>{" "}
                          {phase.dependencies.join(", ")}
                        </AlertDescription>
                      </Alert>
                    )}

                    {/* Actions */}
                    <div className="space-y-4">
                      <h4 className="font-semibold flex items-center gap-2">
                        <CheckCircle2 className="h-4 w-4" />
                        Ações ({phase.actions.length})
                      </h4>
                      {phase.actions.map((action, actionIndex) => (
                        <Card key={action.id} className="border-l-4 border-l-primary/30 hover:shadow-md transition-all duration-200 hover:border-l-primary">
                          <CardContent className="pt-4">
                            <div className="flex items-start justify-between mb-2">
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                  <h5 className="font-semibold">{action.title}</h5>
                                  <Badge variant={priorityColors[action.priority]}>
                                    {priorityLabels[action.priority]}
                                  </Badge>
                                </div>
                                <p className="text-sm text-muted-foreground mb-3">
                                  {action.description}
                                </p>
                              </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                              <div className="flex items-center gap-2">
                                <Users className="h-4 w-4 text-muted-foreground" />
                                <span className="text-muted-foreground">Responsável:</span>
                                <span className="font-medium">{action.responsible}</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <Clock className="h-4 w-4 text-muted-foreground" />
                                <span className="text-muted-foreground">Tempo:</span>
                                <span className="font-medium">{action.estimatedTime}</span>
                              </div>
                            </div>

                            {/* Tools */}
                            {action.tools && action.tools.length > 0 && (
                              <div className="mt-3">
                                <p className="text-xs text-muted-foreground mb-1">Ferramentas:</p>
                                <div className="flex flex-wrap gap-1">
                                  {action.tools.map((tool, toolIndex) => (
                                    <Badge key={toolIndex} variant="secondary" className="text-xs">
                                      {tool}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Steps */}
                            {action.steps && action.steps.length > 0 && (
                              <div className="mt-4 pt-3 border-t">
                                <p className="text-xs font-medium mb-2">Passos Detalhados:</p>
                                <ol className="list-decimal list-inside space-y-1 text-xs text-muted-foreground ml-2">
                                  {action.steps.map((step, stepIndex) => (
                                    <li key={stepIndex}>{step}</li>
                                  ))}
                                </ol>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </div>

                    {/* Deliverables */}
                    {phase.deliverables && phase.deliverables.length > 0 && (
                      <div className="mt-4 pt-4 border-t">
                        <h4 className="font-semibold mb-2 flex items-center gap-2">
                          <CheckCircle2 className="h-4 w-4" />
                          Entregáveis
                        </h4>
                        <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-2">
                          {phase.deliverables.map((deliverable, idx) => (
                            <li key={idx}>{deliverable}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
          )}
          
          {/* No Results Message */}
          {filteredPhases.length === 0 && searchTerm && (
            <div className="text-center py-8">
              <p className="text-muted-foreground">
                Nenhuma ação encontrada para "{searchTerm}"
              </p>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSearchTerm("")}
                className="mt-2"
              >
                Limpar busca
              </Button>
            </div>
          )}

          <Separator />

          {/* Success Metrics */}
          {actionPlan.successMetrics && actionPlan.successMetrics.length > 0 && (
            <div>
              <h4 className="font-semibold mb-3 flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Métricas de Sucesso (SMART)
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {actionPlan.successMetrics.map((metric, idx) => (
                  <Card key={idx} className="border-l-4 border-l-success">
                    <CardContent className="pt-3 pb-3">
                      <p className="text-sm">{metric}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

