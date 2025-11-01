import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CheckCircle2, Circle, AlertCircle, TrendingUp, Users, MessageSquare, FileText, Sparkles } from "lucide-react";
import { PageSkeleton } from "@/components/PageSkeleton";
import { LoadingSpinner } from "@/components/LoadingSpinner";

interface Feature {
  id: string;
  name: string;
  description: string;
  status: "completed" | "in_progress" | "pending";
  category: string;
  endpoint?: string;
  frontend?: string;
  backend?: string;
}

export default function FeaturesAnalysis() {
  // Simular dados de funcionalidades (pode ser substituído por API real)
  const features: Feature[] = [
    // Frontend Core
    {
      id: "shell-layout",
      name: "Shell Layout Component",
      description: "Componente wrapper reutilizável para páginas internas",
      status: "completed",
      category: "Frontend Core",
      frontend: "client/src/components/Shell.tsx",
    },
    {
      id: "sidebar-nav",
      name: "Sidebar Navigation",
      description: "Navegação lateral com highlight de rota ativa",
      status: "completed",
      category: "Frontend Core",
      frontend: "client/src/components/Sidebar.tsx",
    },
    {
      id: "loading-components",
      name: "Loading Components",
      description: "LoadingSpinner, PageSkeleton padronizados",
      status: "completed",
      category: "Frontend Core",
      frontend: "client/src/components/LoadingSpinner.tsx, PageSkeleton.tsx",
    },
    {
      id: "error-banner",
      name: "Global Error Banner",
      description: "Banner global para erros críticos com contexto React",
      status: "completed",
      category: "Frontend Core",
      frontend: "client/src/components/ErrorBanner.tsx, hooks/useGlobalError.tsx",
    },
    
    // Personas
    {
      id: "personas-page",
      name: "Persona Builder Page",
      description: "Página completa para criação e gerenciamento de personas",
      status: "completed",
      category: "Personas",
      frontend: "client/src/pages/Personas.tsx",
      endpoint: "POST /api/personas",
    },
    {
      id: "personas-form",
      name: "Persona Creation Form",
      description: "Formulário com modos quick/strategic, validações e toasts",
      status: "completed",
      category: "Personas",
      frontend: "client/src/pages/Personas.tsx",
    },
    {
      id: "personas-list",
      name: "Personas List & Actions",
      description: "Lista de personas com download JSON e delete",
      status: "completed",
      category: "Personas",
      frontend: "client/src/pages/Personas.tsx",
      endpoint: "GET /api/personas, DELETE /api/personas/:id",
    },
    
    // API & Integration
    {
      id: "api-wrapper",
      name: "API Request Wrapper",
      description: "apiRequest com timeout (30s), parse de erros robusto",
      status: "completed",
      category: "API & Integration",
      frontend: "client/src/lib/queryClient.ts",
    },
    {
      id: "query-client",
      name: "React Query Integration",
      description: "QueryClient configurado com timeout e tratamento de erros",
      status: "completed",
      category: "API & Integration",
      frontend: "client/src/lib/queryClient.ts",
    },
    {
      id: "proxy-middleware",
      name: "Express Proxy Middleware",
      description: "Proxy /api → Python backend com reescrita de paths",
      status: "completed",
      category: "API & Integration",
      backend: "server/index.ts",
    },
    
    // Backend Python
    {
      id: "health-endpoint",
      name: "Health Check Endpoint",
      description: "GET /api/health para monitoramento e CI/CD",
      status: "completed",
      category: "Backend Python",
      endpoint: "GET /api/health",
      backend: "python_backend/main.py",
    },
    {
      id: "council-consensus",
      name: "Council Consensus Synthesis",
      description: "Síntese de consenso entre especialistas usando Claude",
      status: "completed",
      category: "Backend Python",
      endpoint: "POST /api/council/analyze",
      backend: "python_backend/crew_council.py",
    },
    {
      id: "personas-api",
      name: "Personas API Endpoints",
      description: "CRUD completo de personas com pesquisa estratégica",
      status: "completed",
      category: "Backend Python",
      endpoint: "GET/POST/DELETE /api/personas",
      backend: "python_backend/personas_modern.py",
    },
    
    // Logging & Observability
    {
      id: "structured-logs",
      name: "Structured Logging",
      description: "Logs estruturados com request-id, latência, indicadores visuais",
      status: "completed",
      category: "Logging & Observability",
      backend: "server/index.ts",
    },
    {
      id: "error-tracking",
      name: "Error Tracking",
      description: "Log JSON estruturado para erros 5xx com request-id",
      status: "completed",
      category: "Logging & Observability",
      backend: "server/index.ts",
    },
    
    // Type Safety
    {
      id: "zod-schemas",
      name: "Zod Shared Schemas",
      description: "Schemas Zod compartilhados para Persona, Goals, PainPoints",
      status: "completed",
      category: "Type Safety",
      frontend: "shared/schema.ts",
      backend: "shared/schema.ts",
    },
    
    // CI/CD & Deploy
    {
      id: "github-actions",
      name: "GitHub Actions CI",
      description: "CI/CD com type-check e smoke tests",
      status: "completed",
      category: "CI/CD & Deploy",
      backend: ".github/workflows/ci.yml",
    },
    {
      id: "smoke-tests",
      name: "Smoke Tests Script",
      description: "Script de validação básica (build, health checks)",
      status: "completed",
      category: "CI/CD & Deploy",
      backend: "scripts/smoke-test.sh",
    },
    {
      id: "deploy-docs",
      name: "Deploy Documentation",
      description: "Documentação completa de deploy (DEPLOY.md)",
      status: "completed",
      category: "CI/CD & Deploy",
      backend: "DEPLOY.md",
    },
    
    // Exports
    {
      id: "agent-exports",
      name: "Agent Exports",
      description: "Exportação de agentes em JSON/Python para outras plataformas",
      status: "completed",
      category: "Exports",
      backend: "exports/agent_*.json, exports/agent_*.py",
    },
    
    // Pending/In Progress
    {
      id: "personas-types",
      name: "Personas Type Migration",
      description: "Migrar Personas.tsx para usar tipos de shared/schema",
      status: "pending",
      category: "Type Safety",
      frontend: "client/src/pages/Personas.tsx",
    },
    {
      id: "proxy-types",
      name: "Proxy Types Fix",
      description: "Tipar corretamente handler onProxyReq",
      status: "pending",
      category: "API & Integration",
      backend: "server/index.ts",
    },
    {
      id: "py-error-codes",
      name: "Python Error Codes Standardization",
      description: "Padronizar códigos e mensagens de erro no backend Python",
      status: "pending",
      category: "Backend Python",
      backend: "python_backend/",
    },
  ];

  const categories = Array.from(new Set(features.map(f => f.category)));
  const statusCounts = {
    completed: features.filter(f => f.status === "completed").length,
    in_progress: features.filter(f => f.status === "in_progress").length,
    pending: features.filter(f => f.status === "pending").length,
  };

  const getStatusIcon = (status: Feature["status"]) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="h-4 w-4 text-green-500" />;
      case "in_progress":
        return <TrendingUp className="h-4 w-4 text-yellow-500" />;
      case "pending":
        return <Circle className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusBadge = (status: Feature["status"]) => {
    switch (status) {
      case "completed":
        return <Badge variant="default" className="bg-green-500">Completo</Badge>;
      case "in_progress":
        return <Badge variant="default" className="bg-yellow-500">Em Progresso</Badge>;
      case "pending":
        return <Badge variant="secondary">Pendente</Badge>;
    }
  };

  return (
    <div className="container mx-auto py-8 max-w-7xl px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold mb-2">Análise de Funcionalidades</h1>
        <p className="text-muted-foreground">
          Visão completa de todas as funcionalidades implementadas e pendentes
        </p>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Completas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-8 w-8 text-green-500" />
              <span className="text-3xl font-bold">{statusCounts.completed}</span>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Em Progresso</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-8 w-8 text-yellow-500" />
              <span className="text-3xl font-bold">{statusCounts.in_progress}</span>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Pendentes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Circle className="h-8 w-8 text-gray-400" />
              <span className="text-3xl font-bold">{statusCounts.pending}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Features by Category */}
      <Tabs defaultValue={categories[0]} className="space-y-4">
        <TabsList className="grid w-full grid-cols-2 md:grid-cols-4 lg:grid-cols-6">
          {categories.map((category) => (
            <TabsTrigger key={category} value={category} className="text-xs">
              {category}
            </TabsTrigger>
          ))}
        </TabsList>

        {categories.map((category) => (
          <TabsContent key={category} value={category} className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              {features
                .filter((f) => f.category === category)
                .map((feature) => (
                  <Card key={feature.id}>
                    <CardHeader>
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            {getStatusIcon(feature.status)}
                            <CardTitle className="text-base">{feature.name}</CardTitle>
                          </div>
                          {getStatusBadge(feature.status)}
                        </div>
                      </div>
                      <CardDescription className="mt-2">{feature.description}</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm">
                      {feature.endpoint && (
                        <div>
                          <span className="text-muted-foreground font-medium">Endpoint:</span>
                          <code className="ml-2 text-xs bg-muted px-2 py-1 rounded">
                            {feature.endpoint}
                          </code>
                        </div>
                      )}
                      {feature.frontend && (
                        <div>
                          <span className="text-muted-foreground font-medium">Frontend:</span>
                          <code className="ml-2 text-xs bg-muted px-2 py-1 rounded">
                            {feature.frontend}
                          </code>
                        </div>
                      )}
                      {feature.backend && (
                        <div>
                          <span className="text-muted-foreground font-medium">Backend:</span>
                          <code className="ml-2 text-xs bg-muted px-2 py-1 rounded">
                            {feature.backend}
                          </code>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
            </div>
          </TabsContent>
        ))}
      </Tabs>

      {/* Summary Stats */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Estatísticas Gerais</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold">{features.length}</div>
              <div className="text-sm text-muted-foreground">Total de Funcionalidades</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{categories.length}</div>
              <div className="text-sm text-muted-foreground">Categorias</div>
            </div>
            <div>
              <div className="text-2xl font-bold">
                {Math.round((statusCounts.completed / features.length) * 100)}%
              </div>
              <div className="text-sm text-muted-foreground">Taxa de Conclusão</div>
            </div>
            <div>
              <div className="text-2xl font-bold">
                {features.filter(f => f.endpoint).length}
              </div>
              <div className="text-sm text-muted-foreground">Endpoints API</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

