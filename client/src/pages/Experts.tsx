import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { ExpertCard, type Expert } from "@/components/ExpertCard";
import { Input } from "@/components/ui/input";
import { AnimatedPage } from "@/components/AnimatedPage";
import { Search, Loader2 } from "lucide-react";
import { useLocation } from "wouter";

interface Recommendation {
  expertId: string;
  expertName: string;
  score: number;
  stars: number;
  justification: string;
  breakdown: Record<string, number>;
}

interface RecommendationsResponse {
  hasProfile: boolean;
  recommendations: Recommendation[];
}

export default function Experts() {
  const [search, setSearch] = useState("");
  const [, setLocation] = useLocation();

  const { data: experts = [], isLoading } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  const { data: recommendationsData } = useQuery<RecommendationsResponse>({
    queryKey: ["/api/experts/recommendations"],
  });

  const expertRecommendationMap = useMemo(() => {
    if (!recommendationsData?.recommendations) return new Map();
    
    const map = new Map();
    recommendationsData.recommendations.forEach(rec => {
      map.set(rec.expertId, rec);
    });
    return map;
  }, [recommendationsData]);

  const hasProfile = recommendationsData?.hasProfile ?? false;

  const expertsWithRecommendations = useMemo(() => {
    return experts.map(expert => ({
      expert,
      recommendation: expertRecommendationMap.get(expert.id)
    })).sort((a, b) => {
      if (hasProfile && a.recommendation && b.recommendation) {
        return b.recommendation.score - a.recommendation.score;
      }
      return 0;
    });
  }, [experts, expertRecommendationMap, hasProfile]);

  const filteredExperts = expertsWithRecommendations.filter(
    ({ expert }) =>
      expert.name.toLowerCase().includes(search.toLowerCase()) ||
      expert.title.toLowerCase().includes(search.toLowerCase()) ||
      expert.expertise.some((e) => e.toLowerCase().includes(search.toLowerCase()))
  );

  const handleConsult = async (expert: Expert) => {
    setLocation(`/chat/${expert.id}`);
  };

  return (
    <AnimatedPage>
      <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4">Especialistas Disponíveis</h1>
            <p className="text-muted-foreground mb-6">
              Consulte especialistas de elite em diversas áreas estratégicas
            </p>

            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Buscar por nome, especialidade..."
                className="pl-10"
                data-testid="input-search-experts"
              />
            </div>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : (
            <>
              {hasProfile && (
                <div className="mb-6 bg-primary/5 border border-primary/20 rounded-lg p-4">
                  <p className="text-sm text-muted-foreground">
                    <span className="font-medium text-foreground">Personalizado para você:</span> Os especialistas estão ordenados por relevância com base no seu perfil de negócio.
                  </p>
                </div>
              )}
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredExperts.map(({ expert, recommendation }) => (
                  <ExpertCard 
                    key={expert.id} 
                    expert={expert} 
                    onConsult={handleConsult}
                    showRecommendation={hasProfile}
                    recommendationScore={recommendation?.score}
                    recommendationStars={recommendation?.stars}
                    recommendationJustification={recommendation?.justification}
                  />
                ))}
              </div>

              {filteredExperts.length === 0 && (
                <div className="text-center py-16">
                  <p className="text-muted-foreground">
                    Nenhum especialista encontrado para "{search}"
                  </p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
      </div>
    </AnimatedPage>
  );
}
