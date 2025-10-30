import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { TrendingUp, Users } from "lucide-react";
import { motion } from "framer-motion";
import { useTypingDelay } from "@/hooks/useTypingDelay";

// Configuração de typing delay
const TYPING_DELAY_CONFIG = {
  speed: 25, // caracteres por segundo (velocidade natural de leitura)
  delay: 500, // delay inicial em ms antes de começar a digitar
} as const;

// Função helper para gerar avatar colorido baseado no nome do expert
// Sistema expandido com mais cores e mapeamento por nome para consistência
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
  { bg: "bg-pink-500", text: "text-white" },
  { bg: "bg-indigo-500", text: "text-white" },
  { bg: "bg-red-500", text: "text-white" },
  { bg: "bg-teal-500", text: "text-white" },
  { bg: "bg-cyan-500", text: "text-white" },
  { bg: "bg-emerald-500", text: "text-white" },
];

function getExpertAvatarColor(expertName: string): { bg: string; text: string } {
  // Verificar se há cor mapeada para este expert
  if (EXPERT_COLOR_MAP[expertName]) {
    return EXPERT_COLOR_MAP[expertName];
  }
  
  // Hash simples do nome para escolher cor consistente
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

interface CouncilResultDisplayProps {
  analysis: CouncilAnalysis | undefined;
  isStreaming: boolean;
}

export function CouncilResultDisplay({ analysis, isStreaming }: CouncilResultDisplayProps) {
  const showResults = analysis && !isStreaming;
  
  // Typing delay para consenso usando configuração centralizada
  const consensusText = useTypingDelay({
    text: analysis?.consensus || "",
    speed: TYPING_DELAY_CONFIG.speed,
    enabled: showResults && !!analysis?.consensus,
    delay: TYPING_DELAY_CONFIG.delay,
  });

  if (!showResults) {
    return (
      <div className="lg:col-span-3 mt-8">
        <Card className="border-dashed rounded-2xl">
          <CardContent className="pt-6">
            <div className="text-center text-muted-foreground py-12">
              <Users className="h-12 w-12 mx-auto mb-4 opacity-30" />
              <p className="text-sm">Envie um problema para ver a análise do conselho</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="lg:col-span-3 mt-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <Card className="rounded-2xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-semibold">
              <TrendingUp className="h-5 w-5 text-accent" />
              Insights do Conselho
            </CardTitle>
            <CardDescription>
              Análise de {analysis.contributions.length} especialista{analysis.contributions.length !== 1 ? 's' : ''}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Consensus on the left */}
              <div className="lg:col-span-1">
                <h3 className="font-semibold mb-2 text-lg">📋 Consenso Estratégico</h3>
                <ScrollArea className="h-[600px] pr-4">
                  <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                    {consensusText}
                    {consensusText.length < (analysis.consensus?.length || 0) && (
                      <span className="inline-block w-2 h-4 bg-accent animate-pulse ml-1" />
                    )}
                  </p>
                </ScrollArea>
              </div>

              {/* Contributions on the right */}
              <div className="lg:col-span-2 space-y-4">
                <h3 className="font-semibold text-lg">💡 Contribuições dos Especialistas</h3>
                <ScrollArea className="h-[600px] pr-4">
                  <div className="space-y-3">
                    {analysis.contributions.map((contrib, idx) => {
                      const avatarColors = getExpertAvatarColor(contrib.expertName);
                      const initials = getExpertInitials(contrib.expertName);
                      
                      return (
                        <Card key={idx} className="rounded-xl bg-muted/30">
                          <CardHeader className="pb-3">
                            <div className="flex items-center gap-3">
                              <Avatar className={`h-10 w-10 ${avatarColors.bg} ring-2 ring-border/50`}>
                                <AvatarFallback className={`${avatarColors.text} font-semibold text-sm`}>
                                  {initials}
                                </AvatarFallback>
                              </Avatar>
                              <CardTitle className="text-base font-semibold">
                                {contrib.expertName}
                              </CardTitle>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-3">
                            {contrib.keyInsights.length > 0 && (
                              <div>
                                <p className="text-sm font-medium mb-1">Principais Insights:</p>
                                <ul className="text-sm text-muted-foreground space-y-1 list-disc pl-5">
                                  {contrib.keyInsights.map((insight, i) => (
                                    <li key={i}>{insight}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {contrib.recommendations.length > 0 && (
                              <div>
                                <p className="text-sm font-medium mb-1">
                                  Recomendações:
                                </p>
                                <ul className="text-sm text-muted-foreground space-y-1 list-disc pl-5">
                                  {contrib.recommendations.map((rec, i) => (
                                    <li key={i}>{rec}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      );
                    })}
                  </div>
                </ScrollArea>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
