import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

interface PulseLoaderProps {
  size?: "sm" | "md" | "lg";
  text?: string;
}

export function PulseLoader({ size = "md", text }: PulseLoaderProps) {
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-6 w-6",
    lg: "h-8 w-8"
  };

  return (
    <div className="flex items-center gap-3">
      <motion.div
        animate={{
          filter: [
            "drop-shadow(0 0 8px hsl(var(--primary) / 0.3))",
            "drop-shadow(0 0 12px hsl(var(--accent) / 0.4))",
            "drop-shadow(0 0 8px hsl(var(--primary) / 0.3))"
          ],
          scale: [1, 1.05, 1]
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <Loader2 className={`${sizeClasses[size]} animate-spin text-primary`} />
      </motion.div>
      {text && (
        <motion.span
          animate={{
            opacity: [0.6, 1, 0.6]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="text-sm text-muted-foreground"
        >
          {text}
        </motion.span>
      )}
    </div>
  );
}
