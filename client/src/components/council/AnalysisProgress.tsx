import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

interface AnalysisStage {
  id: string;
  label: string;
  status: "pending" | "active" | "completed";
}

interface AnalysisProgressProps {
  stages: AnalysisStage[];
  currentStage: string | null;
  progress: number; // 0-100
  estimatedTimeRemaining?: string;
}

export function AnalysisProgress({
  stages,
  currentStage,
  progress,
  estimatedTimeRemaining,
}: AnalysisProgressProps) {
  return (
    <Card className="rounded-2xl border-primary/20 bg-primary/5">
      <CardHeader>
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
          Análise em Andamento
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Barra de progresso */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Progresso</span>
            <span className="font-semibold">{progress}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Tempo estimado */}
        {estimatedTimeRemaining && (
          <div className="text-sm text-muted-foreground">
            ⏱️ Tempo estimado: {estimatedTimeRemaining}
          </div>
        )}

        {/* Etapas */}
        <div className="space-y-3 pt-2">
          {stages.map((stage, index) => {
            const isActive = stage.status === "active" || stage.id === currentStage;
            const isCompleted = stage.status === "completed";

            return (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-3"
              >
                <div className="flex-shrink-0">
                  {isCompleted ? (
                    <CheckCircle2 className="h-5 w-5 text-green-600" />
                  ) : isActive ? (
                    <Loader2 className="h-5 w-5 animate-spin text-primary" />
                  ) : (
                    <Circle className="h-5 w-5 text-muted-foreground" />
                  )}
                </div>
                <span
                  className={`text-sm ${
                    isActive
                      ? "font-semibold text-primary"
                      : isCompleted
                      ? "text-green-600"
                      : "text-muted-foreground"
                  }`}
                >
                  {stage.label}
                </span>
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

