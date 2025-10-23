import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ExpertCard, type Expert } from "@/components/ExpertCard";
import { Input } from "@/components/ui/input";
import { Search, Loader2 } from "lucide-react";
import { useLocation } from "wouter";

export default function Experts() {
  const [search, setSearch] = useState("");
  const [, setLocation] = useLocation();

  const { data: experts = [], isLoading } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  const filteredExperts = experts.filter(
    (expert) =>
      expert.name.toLowerCase().includes(search.toLowerCase()) ||
      expert.title.toLowerCase().includes(search.toLowerCase()) ||
      expert.expertise.some((e) => e.toLowerCase().includes(search.toLowerCase()))
  );

  const handleConsult = async (expert: Expert) => {
    setLocation(`/chat/${expert.id}`);
  };

  return (
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
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredExperts.map((expert) => (
                  <ExpertCard key={expert.id} expert={expert} onConsult={handleConsult} />
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
  );
}
