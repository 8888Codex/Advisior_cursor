import { motion } from "framer-motion";
import { AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ResourceExhaustedErrorProps {
  onRetry?: () => void;
}

export function ResourceExhaustedError({ onRetry }: ResourceExhaustedErrorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
      className="flex flex-col items-center justify-center py-16 px-4 text-center bg-muted/30 rounded-lg border border-muted"
      data-testid="resource-exhausted-error"
    >
      <motion.div
        initial={{ scale: 0, rotate: -10 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ 
          type: "spring", 
          stiffness: 260, 
          damping: 20, 
          delay: 0.1 
        }}
        className="mb-6 p-6 rounded-full bg-amber-500/10 border border-amber-500/20"
      >
        <AlertCircle className="h-12 w-12 text-amber-500" />
      </motion.div>
      
      <motion.h3
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-xl font-semibold mb-2"
      >
        Limite de recursos atingido
      </motion.h3>
      
      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-muted-foreground mb-6 max-w-md"
      >
        As APIs externas (Claude ou Perplexity) estão temporariamente indisponíveis ou atingiram seu limite de uso. 
        Por favor, aguarde um momento e tente novamente.
      </motion.p>
      
      {onRetry && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Button 
            onClick={onRetry}
            className="gap-2"
            variant="outline"
          >
            <RefreshCw className="h-4 w-4" />
            Tentar Novamente
          </Button>
        </motion.div>
      )}
    </motion.div>
  );
}
