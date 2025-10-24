import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Info, CheckCircle2, AlertCircle } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { ActivityEvent } from "@/hooks/useCouncilStream";

interface ActivityFeedProps {
  activities: ActivityEvent[];
  className?: string;
}

const eventConfig = {
  info: {
    icon: Info,
    color: "text-accent",
    bgColor: "bg-accent/10",
  },
  success: {
    icon: CheckCircle2,
    color: "text-accent",
    bgColor: "bg-accent/10",
  },
  error: {
    icon: AlertCircle,
    color: "text-destructive",
    bgColor: "bg-destructive/10",
  },
};

export function ActivityFeed({ activities, className = "" }: ActivityFeedProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new activity added
  useEffect(() => {
    if (scrollRef.current) {
      const scrollElement = scrollRef.current.querySelector("[data-radix-scroll-area-viewport]");
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight;
      }
    }
  }, [activities]);

  return (
    <div className={`space-y-2 ${className}`} data-testid="activity-feed">
      <div className="flex items-center justify-between px-1">
        <h3 className="font-semibold text-sm">Feed de Atividades</h3>
        <span className="text-xs text-muted-foreground">
          {activities.length} evento{activities.length !== 1 ? 's' : ''}
        </span>
      </div>

      <ScrollArea ref={scrollRef} className="h-[400px] rounded-xl border p-4">
        <AnimatePresence mode="popLayout">
          {activities.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center justify-center h-full text-muted-foreground text-sm"
            >
              Nenhuma atividade ainda...
            </motion.div>
          ) : (
            <div className="space-y-3">
              {activities.map((activity, index) => {
                const config = eventConfig[activity.type];
                const Icon = config.icon;

                return (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ delay: index * 0.05, duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
                    className={`flex gap-3 p-3 rounded-xl ${config.bgColor}`}
                    data-testid={`activity-event-${activity.id}`}
                  >
                    <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${config.color}`} />
                    
                    <div className="flex-1 min-w-0">
                      {activity.expertName && (
                        <p className="font-semibold text-sm">{activity.expertName}</p>
                      )}
                      <p className="text-sm text-foreground/90">{activity.message}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {new Date(activity.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </AnimatePresence>
      </ScrollArea>
    </div>
  );
}
