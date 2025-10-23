import { motion } from "framer-motion";
import { Check, X, Loader2, Search, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";
import type { ExpertStatus } from "@/hooks/useCouncilStream";

interface ExpertAvatarProps {
  status: ExpertStatus;
  index: number;
}

const statusConfig = {
  waiting: {
    icon: null,
    color: "text-muted-foreground",
    bgColor: "bg-muted",
    label: "Waiting",
  },
  researching: {
    icon: Search,
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
    label: "Researching",
  },
  analyzing: {
    icon: Sparkles,
    color: "text-primary",
    bgColor: "bg-primary/10",
    label: "Analyzing",
  },
  completed: {
    icon: Check,
    color: "text-green-500",
    bgColor: "bg-green-500/10",
    label: "Completed",
  },
  failed: {
    icon: X,
    color: "text-destructive",
    bgColor: "bg-destructive/10",
    label: "Failed",
  },
};

export function ExpertAvatar({ status, index }: ExpertAvatarProps) {
  const config = statusConfig[status.status];
  const Icon = config.icon;
  const isActive = status.status === "analyzing" || status.status === "researching";

  // Get initials from expert name
  const initials = status.expertName
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .substring(0, 2)
    .toUpperCase() || "?";

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.1 }}
      data-testid={`expert-avatar-${status.expertId}`}
    >
      <Card className={`p-4 relative overflow-hidden ${isActive ? "ring-2 ring-primary" : ""}`}>
        {/* Animated background pulse for active experts */}
        {isActive && (
          <motion.div
            className="absolute inset-0 bg-primary/5"
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        )}

        <div className="relative space-y-3">
          {/* Avatar with progress ring */}
          <div className="relative mx-auto w-20 h-20">
            {/* Progress ring */}
            <svg className="absolute inset-0 w-full h-full -rotate-90">
              {/* Background ring */}
              <circle
                cx="40"
                cy="40"
                r="36"
                fill="none"
                stroke="currentColor"
                strokeWidth="4"
                className="text-muted"
                opacity="0.2"
              />
              {/* Progress ring */}
              <motion.circle
                cx="40"
                cy="40"
                r="36"
                fill="none"
                stroke="currentColor"
                strokeWidth="4"
                className={config.color}
                strokeLinecap="round"
                strokeDasharray={226} // 2 * π * 36
                initial={{ strokeDashoffset: 226 }}
                animate={{ strokeDashoffset: 226 - (226 * status.progress) / 100 }}
                transition={{ duration: 0.5 }}
              />
            </svg>

            {/* Avatar circle */}
            <div
              className={`absolute inset-2 rounded-full flex items-center justify-center text-lg font-bold ${config.bgColor} ${config.color}`}
            >
              {initials}
            </div>

            {/* Status icon overlay */}
            {Icon && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className={`absolute -bottom-1 -right-1 w-7 h-7 rounded-full ${config.bgColor} ${config.color} flex items-center justify-center border-2 border-background`}
              >
                {isActive ? (
                  <Icon className="w-4 h-4 animate-pulse" />
                ) : (
                  <Icon className="w-4 h-4" />
                )}
              </motion.div>
            )}
          </div>

          {/* Expert name */}
          <div className="text-center">
            <p className="font-semibold text-sm line-clamp-2">
              {status.expertName || "Expert"}
            </p>
            <p className={`text-xs mt-1 ${config.color}`}>{config.label}</p>
          </div>

          {/* Stats (when completed) */}
          {status.status === "completed" && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-xs text-center space-y-1 text-muted-foreground"
            >
              {status.insightCount !== undefined && (
                <div>{status.insightCount} insights</div>
              )}
              {status.recommendationCount !== undefined && (
                <div>{status.recommendationCount} recommendations</div>
              )}
            </motion.div>
          )}

          {/* Error message */}
          {status.status === "failed" && status.error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xs text-destructive text-center line-clamp-2"
            >
              {status.error}
            </motion.div>
          )}
        </div>
      </Card>
    </motion.div>
  );
}
