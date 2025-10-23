import { motion, AnimatePresence } from "framer-motion";
import { ReactNode } from "react";

interface AnimatedPageProps {
  children: ReactNode;
}

export function AnimatedPage({ children }: AnimatedPageProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98, y: -10 }}
      transition={{ 
        duration: 0.6, 
        ease: [0.4, 0, 0.2, 1],
        opacity: { duration: 0.5 }
      }}
    >
      {children}
    </motion.div>
  );
}
