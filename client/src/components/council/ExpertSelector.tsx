import { TooltipProvider, Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Loader2, Star } from "lucide-react";
import { motion } from "framer-motion";
import { ExpertListSkeleton } from "@/components/skeletons/CouncilSkeleton";

// Types need to be imported or defined here as well
interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  avatar?: string;
  category?: string;
}

interface ExpertRecommendation {
  expertId: string;
  relevanceScore: number;
  justification: string;
}

interface ExpertSelectorProps {
  experts: Expert[];
  selectedExperts: string[];
  recommendations: ExpertRecommendation[];
  loadingExperts: boolean;
  isAnalyzing: boolean;
  onToggleExpert: (id: string) => void;
  onSelectAll: () => void;
}

export function ExpertSelector({
  experts,
  selectedExperts,
  recommendations,
  loadingExperts,
  isAnalyzing,
  onToggleExpert,
  onSelectAll,
}: ExpertSelectorProps) {
  return (
    <Card className="rounded-2xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="font-semibold">Selecionar Especialistas</CardTitle>
            <CardDescription>
              Escolha quais lendas do marketing consultar ({selectedExperts.length}{" "}
              selecionado{selectedExperts.length !== 1 ? 's' : ''})
            </CardDescription>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={onSelectAll}
            disabled={loadingExperts || isAnalyzing}
            data-testid="button-select-all"
          >
            {selectedExperts.length === experts.length ? "Desmarcar Todos" : "Selecionar Todos"}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {loadingExperts ? (
          <ExpertListSkeleton />
        ) : (
          <TooltipProvider>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {experts.map((expert, index) => {
                const recommendation = recommendations.find(r => r.expertId === expert.id);
                const isRecommended = !!recommendation;
                
                return (
                  <Tooltip key={expert.id}>
                    <TooltipTrigger asChild>
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.05, ease: [0.25, 0.1, 0.25, 1] }}
                        className={`flex items-start space-x-3 p-3 rounded-xl border hover-elevate active-elevate-2 cursor-pointer transition-all ${
                          isRecommended ? 'border-accent/30 bg-muted/40' : ''
                        }`}
                        onClick={() => onToggleExpert(expert.id)}
                        data-testid={`expert-card-${expert.id}`}
                      >
                        <Checkbox
                          checked={selectedExperts.includes(expert.id)}
                          disabled={isAnalyzing}
                          data-testid={`checkbox-expert-${expert.id}`}
                        />
                        <Avatar className="h-10 w-10 flex-shrink-0 ring-2 ring-accent/20">
                          <AvatarImage src={expert.avatar} alt={expert.name} className="object-cover" />
                          <AvatarFallback className="text-xs font-semibold">
                            {expert.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <Label className="font-semibold cursor-pointer">
                              {expert.name}
                            </Label>
                            {isRecommended && (
                              <Badge variant="secondary" className="text-xs px-1.5 py-0">
                                Recomendado
                              </Badge>
                            )}
                          </div>
                          {isRecommended && recommendation && (
                            <div className="flex items-center gap-0.5 mb-1">
                              {Array.from({ length: 5 }).map((_, i) => (
                                <Star
                                  key={i}
                                  className={`h-3 w-3 ${
                                    i < recommendation.relevanceScore
                                      ? 'fill-accent text-accent'
                                      : 'text-muted-foreground/30'
                                  }`}
                                />
                              ))}
                            </div>
                          )}
                          <p className="text-sm text-muted-foreground line-clamp-2">
                            {expert.title}
                          </p>
                          {expert.expertise && expert.expertise.length > 0 && (
                            <Badge variant="secondary" className="mt-1 text-xs">
                              {expert.expertise.slice(0, 2).join(", ")}
                            </Badge>
                          )}
                        </div>
                      </motion.div>
                    </TooltipTrigger>
                    {isRecommended && recommendation && (
                      <TooltipContent className="max-w-xs">
                        <p className="text-sm">{recommendation.justification}</p>
                      </TooltipContent>
                    )}
                  </Tooltip>
                );
              })}
            </div>
          </TooltipProvider>
        )}
      </CardContent>
    </Card>
  );
}
