import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Settings, Save, RotateCcw } from "lucide-react";
import { useUserPreferences, type UserPreferences } from "@/hooks/useUserPreferences.ts";
import { useToast } from "@/hooks/use-toast";

interface PreferencesSettingsProps {
  userId?: string;
  isAuthenticated?: boolean;
  onClose?: () => void;
}

export function PreferencesSettings({ 
  userId, 
  isAuthenticated = false,
  onClose 
}: PreferencesSettingsProps) {
  const { preferences, savePreferences, clearPreferences, isLoading } = useUserPreferences(
    userId,
    isAuthenticated
  );
  const { toast } = useToast();
  
  const [localPrefs, setLocalPrefs] = useState<UserPreferences>(preferences);
  const [hasChanges, setHasChanges] = useState(false);

  // Sincronizar quando preferências mudarem do hook
  useEffect(() => {
    setLocalPrefs(preferences);
    setHasChanges(false);
  }, [preferences]);

  const handleChange = <K extends keyof UserPreferences>(
    key: K,
    value: UserPreferences[K]
  ) => {
    setLocalPrefs((prev) => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  const handleSave = () => {
    savePreferences(localPrefs);
    setHasChanges(false);
    toast({
      title: "Preferências salvas",
      description: "Suas preferências foram salvas com sucesso.",
    });
    onClose?.();
  };

  const handleReset = () => {
    setLocalPrefs(preferences);
    setHasChanges(false);
    toast({
      title: "Alterações descartadas",
      description: "As alterações foram revertidas.",
    });
  };

  const handleClear = () => {
    if (confirm("Tem certeza que deseja limpar todas as preferências?")) {
      clearPreferences();
      setLocalPrefs({});
      setHasChanges(false);
      toast({
        title: "Preferências limpas",
        description: "Todas as preferências foram removidas.",
      });
    }
  };

  return (
    <Card className="rounded-2xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Settings className="h-5 w-5 text-accent" />
            <CardTitle className="font-semibold">Preferências de Conversa</CardTitle>
          </div>
          {hasChanges && (
            <span className="text-xs text-muted-foreground">Alterações não salvas</span>
          )}
        </div>
        <CardDescription>
          Configure como você prefere receber análises e recomendações dos especialistas.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Estilo de Resposta */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Estilo de Resposta</Label>
          <RadioGroup
            value={localPrefs.style_preference || ""}
            onValueChange={(value) => handleChange("style_preference", value as "objetivo" | "detalhado")}
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="objetivo" id="style-objetivo" />
              <Label htmlFor="style-objetivo" className="font-normal cursor-pointer">
                Objetivo - Respostas diretas e concisas
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="detalhado" id="style-detalhado" />
              <Label htmlFor="style-detalhado" className="font-normal cursor-pointer">
                Detalhado - Explicações completas e contexto
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Foco */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Foco Principal</Label>
          <RadioGroup
            value={localPrefs.focus_preference || ""}
            onValueChange={(value) => handleChange("focus_preference", value as "ROI-first" | "brand-first")}
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="ROI-first" id="focus-roi" />
              <Label htmlFor="focus-roi" className="font-normal cursor-pointer">
                ROI-first - Foco em resultados mensuráveis e conversão
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="brand-first" id="focus-brand" />
              <Label htmlFor="focus-brand" className="font-normal cursor-pointer">
                Brand-first - Foco em marca, posicionamento e reputação
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Tom */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Tom de Comunicação</Label>
          <RadioGroup
            value={localPrefs.tone_preference || ""}
            onValueChange={(value) => handleChange("tone_preference", value as "prático" | "estratégico")}
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="prático" id="tone-pratico" />
              <Label htmlFor="tone-pratico" className="font-normal cursor-pointer">
                Prático - Ações imediatas e implementação
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="estratégico" id="tone-estrategico" />
              <Label htmlFor="tone-estrategico" className="font-normal cursor-pointer">
                Estratégico - Visão de longo prazo e planejamento
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Formato de Comunicação */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Formato de Comunicação</Label>
          <RadioGroup
            value={localPrefs.communication_preference || ""}
            onValueChange={(value) => handleChange("communication_preference", value as "bullets" | "blocos")}
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="bullets" id="comm-bullets" />
              <Label htmlFor="comm-bullets" className="font-normal cursor-pointer">
                Bullets - Listas e pontos destacados
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="blocos" id="comm-blocos" />
              <Label htmlFor="comm-blocos" className="font-normal cursor-pointer">
                Blocos - Parágrafos e texto completo
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Estilo Conversacional */}
        <div className="space-y-3">
          <Label htmlFor="conversation-style" className="text-sm font-medium">
            Estilo Conversacional
          </Label>
          <Select
            value={localPrefs.conversation_style || ""}
            onValueChange={(value) => handleChange("conversation_style", value as "coach" | "consultor" | "direto")}
          >
            <SelectTrigger id="conversation-style">
              <SelectValue placeholder="Selecione um estilo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="coach">Coach - Mais perguntas, empoderamento</SelectItem>
              <SelectItem value="consultor">Consultor - Balanceado (padrão)</SelectItem>
              <SelectItem value="direto">Direto - Mais ações, menos perguntas</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-4 border-t">
          <Button 
            onClick={handleSave} 
            disabled={!hasChanges || isLoading}
            className="flex-1 gap-2"
          >
            <Save className="h-4 w-4" />
            Salvar Preferências
          </Button>
          {hasChanges && (
            <Button 
              variant="outline" 
              onClick={handleReset}
              className="gap-2"
            >
              <RotateCcw className="h-4 w-4" />
              Descartar
            </Button>
          )}
          <Button 
            variant="ghost" 
            onClick={handleClear}
            className="text-destructive hover:text-destructive"
          >
            Limpar Tudo
          </Button>
        </div>

        {isAuthenticated && (
          <p className="text-xs text-muted-foreground text-center">
            Suas preferências são sincronizadas automaticamente quando você está autenticado.
          </p>
        )}
      </CardContent>
    </Card>
  );
}

