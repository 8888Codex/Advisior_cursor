import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { ExpertCard, type Expert } from "@/components/ExpertCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { AnimatedPage } from "@/components/AnimatedPage";
import { Search, Loader2, SlidersHorizontal, Star, X } from "lucide-react";
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

type SortOption = "relevance" | "name-asc" | "name-desc";

export default function Experts() {
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState<SortOption>("relevance");
  const [filterExpertise, setFilterExpertise] = useState<string>("all");
  const [showRecommendedOnly, setShowRecommendedOnly] = useState(false);
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

  // Extract unique expertise categories
  const expertiseCategories = useMemo(() => {
    const categories = new Set<string>();
    experts.forEach(expert => {
      expert.expertise.forEach(exp => categories.add(exp));
    });
    return Array.from(categories).sort();
  }, [experts]);

  const expertsWithRecommendations = useMemo(() => {
    return experts.map(expert => ({
      expert,
      recommendation: expertRecommendationMap.get(expert.id)
    }));
  }, [experts, expertRecommendationMap]);

  // Apply filters and sorting
  const filteredAndSortedExperts = useMemo(() => {
    let result = [...expertsWithRecommendations];

    // Text search filter
    if (search) {
      result = result.filter(({ expert }) =>
        expert.name.toLowerCase().includes(search.toLowerCase()) ||
        expert.title.toLowerCase().includes(search.toLowerCase()) ||
        expert.expertise.some((e) => e.toLowerCase().includes(search.toLowerCase()))
      );
    }

    // Expertise category filter
    if (filterExpertise !== "all") {
      result = result.filter(({ expert }) =>
        expert.expertise.includes(filterExpertise)
      );
    }

    // Recommended only filter
    if (showRecommendedOnly) {
      result = result.filter(({ recommendation }) =>
        recommendation && recommendation.stars >= 4
      );
    }

    // Sorting
    result.sort((a, b) => {
      switch (sortBy) {
        case "relevance":
          if (hasProfile && a.recommendation && b.recommendation) {
            return b.recommendation.score - a.recommendation.score;
          }
          return 0;
        case "name-asc":
          return a.expert.name.localeCompare(b.expert.name);
        case "name-desc":
          return b.expert.name.localeCompare(a.expert.name);
        default:
          return 0;
      }
    });

    return result;
  }, [expertsWithRecommendations, search, filterExpertise, showRecommendedOnly, sortBy, hasProfile]);

  const activeFiltersCount = 
    (filterExpertise !== "all" ? 1 : 0) + 
    (showRecommendedOnly ? 1 : 0);

  const clearAllFilters = () => {
    setFilterExpertise("all");
    setShowRecommendedOnly(false);
  };

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

            <div className="flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1 max-w-md">
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

            {/* Filters & Sorting */}
            <div className="mt-4 flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2">
                <SlidersHorizontal className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-medium">Filtros:</span>
              </div>

              {/* Sort Dropdown */}
              <Select value={sortBy} onValueChange={(v) => setSortBy(v as SortOption)}>
                <SelectTrigger className="w-[180px]" data-testid="select-sort-by">
                  <SelectValue placeholder="Ordenar por" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="relevance">
                    Relevância
                    {hasProfile && <span className="ml-1 text-xs text-muted-foreground">(Match)</span>}
                  </SelectItem>
                  <SelectItem value="name-asc">Nome (A-Z)</SelectItem>
                  <SelectItem value="name-desc">Nome (Z-A)</SelectItem>
                </SelectContent>
              </Select>

              {/* Expertise Filter Dropdown */}
              {expertiseCategories.length > 0 && (
                <Select value={filterExpertise} onValueChange={setFilterExpertise}>
                  <SelectTrigger className="w-[200px]" data-testid="select-filter-expertise">
                    <SelectValue placeholder="Especialidade" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todas Especialidades</SelectItem>
                    {expertiseCategories.map(category => (
                      <SelectItem key={category} value={category}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}

              {/* Recommended Only Toggle (only show when hasProfile) */}
              {hasProfile && (
                <Button
                  variant={showRecommendedOnly ? "default" : "outline"}
                  size="sm"
                  onClick={() => setShowRecommendedOnly(!showRecommendedOnly)}
                  className="gap-2"
                  data-testid="toggle-recommended"
                >
                  <Star className="h-4 w-4" />
                  Apenas Recomendados
                </Button>
              )}

              {/* Clear Filters Button */}
              {activeFiltersCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearAllFilters}
                  className="gap-1 text-muted-foreground hover:text-foreground"
                  data-testid="button-clear-filters"
                >
                  <X className="h-4 w-4" />
                  Limpar ({activeFiltersCount})
                </Button>
              )}
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
              
              <div className="grid md:grid-cols-2 gap-8">
                {filteredAndSortedExperts.map(({ expert, recommendation }) => (
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

              {filteredAndSortedExperts.length === 0 && (
                <div className="text-center py-16">
                  <p className="text-muted-foreground">
                    {search || filterExpertise !== "all" || showRecommendedOnly
                      ? "Nenhum especialista encontrado com os filtros aplicados"
                      : "Nenhum especialista disponível"}
                  </p>
                  {activeFiltersCount > 0 && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={clearAllFilters}
                      className="mt-4"
                    >
                      Limpar Filtros
                    </Button>
                  )}
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
