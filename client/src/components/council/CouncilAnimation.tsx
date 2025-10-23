import { motion } from "framer-motion";
import { ExpertAvatar } from "./ExpertAvatar";
import { ActivityFeed } from "./ActivityFeed";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users } from "lucide-react";
import type { ExpertStatus, ActivityEvent } from "@/hooks/useCouncilStream";

interface CouncilAnimationProps {
  expertStatuses: ExpertStatus[];
  activityFeed: ActivityEvent[];
  isStreaming: boolean;
}

export function CouncilAnimation({
  expertStatuses,
  activityFeed,
  isStreaming,
}: CouncilAnimationProps) {
  const completedCount = expertStatuses.filter((s) => s.status === "completed").length;
  const totalCount = expertStatuses.length;

  return (
    <div className="space-y-6" data-testid="council-animation">
      {/* Header with progress */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="flex items-center justify-center gap-2 mb-2">
          <Users className="h-6 w-6 text-primary" />
          <h2 className="text-2xl font-bold">Conselho em Sessão</h2>
        </div>
        <p className="text-muted-foreground">
          {isStreaming
            ? `Analisando... (${completedCount}/${totalCount} especialista${totalCount !== 1 ? 's' : ''} concluído${completedCount !== 1 ? 's' : ''})`
            : `Análise completa (${completedCount}/${totalCount} especialista${totalCount !== 1 ? 's' : ''})`}
        </p>
      </motion.div>

      {/* Grid + Feed Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Expert Avatars Grid */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Painel de Especialistas</CardTitle>
              <CardDescription>
                Lendas do marketing analisando seu desafio
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {expertStatuses.map((status, index) => (
                  <ExpertAvatar key={status.expertId} status={status} index={index} />
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Activity Feed */}
        <div className="lg:col-span-1">
          <ActivityFeed activities={activityFeed} />
        </div>
      </div>
    </div>
  );
}
