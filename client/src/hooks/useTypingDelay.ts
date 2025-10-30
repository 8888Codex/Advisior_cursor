import { useState, useEffect, useRef } from "react";

interface UseTypingDelayOptions {
  text: string;
  speed?: number; // Characters per second (default: 30)
  enabled?: boolean; // Enable/disable typing effect
  delay?: number; // Delay before starting (ms)
}

/**
 * Hook que simula efeito de digitação (typing delay) para texto longo.
 * Útil para tornar respostas de IA mais naturais e menos abruptas.
 */
export function useTypingDelay({
  text,
  speed = 30,
  enabled = true,
  delay = 0,
}: UseTypingDelayOptions): string {
  const [displayedText, setDisplayedText] = useState("");
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!enabled || !text) {
      setDisplayedText(text);
      return;
    }

    setDisplayedText("");

    const delayTimeout = setTimeout(() => {
      let currentIndex = 0;
      // Ajustar chunks baseado na velocidade para animação mais suave
      // Para velocidades menores, usar chunks menores para ser mais fluido
      const optimalInterval = Math.max(16, Math.min(100, 1000 / speed)); // Entre 16ms (60fps) e 100ms
      const charsPerTick = Math.max(1, Math.ceil(speed / (1000 / optimalInterval)));

      intervalRef.current = setInterval(() => {
        if (currentIndex < text.length) {
          // Avançar em chunks otimizados para velocidade natural
          const nextChunk = text.slice(0, currentIndex + charsPerTick);
          setDisplayedText(nextChunk);
          currentIndex = nextChunk.length;
        } else {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
        }
      }, optimalInterval);
    }, delay);

    return () => {
      clearTimeout(delayTimeout);
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [text, speed, enabled, delay]);

  return displayedText;
}

