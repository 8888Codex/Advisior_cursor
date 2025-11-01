import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Lightbulb, MessageSquare } from "lucide-react";
import { motion } from "framer-motion";

interface SuggestedQuestion {
  id: string;
  text: string;
  category?: string;
}

interface SuggestedQuestionsProps {
  questions: SuggestedQuestion[];
  problem?: string;
  onSelectQuestion: (question: string) => void;
}

export function SuggestedQuestions({
  questions,
  problem,
  onSelectQuestion,
}: SuggestedQuestionsProps) {
  if (questions.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-4"
    >
      <div className="flex items-center gap-2 text-sm font-semibold text-muted-foreground">
        <Lightbulb className="h-4 w-4" />
        <span>Perguntas Sugeridas</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {questions.map((question) => (
          <motion.div
            key={question.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Card className="cursor-pointer hover:border-primary/50 transition-colors">
              <CardContent className="pt-4">
                <Button
                  variant="ghost"
                  className="w-full justify-start text-left h-auto p-0"
                  onClick={() => onSelectQuestion(question.text)}
                >
                  <MessageSquare className="h-4 w-4 mr-2 text-muted-foreground flex-shrink-0" />
                  <span className="text-sm">{question.text}</span>
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

