import { useState } from "react";
import { ExpertCard, type Expert } from "@/components/ExpertCard";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import strategistAvatar from "@assets/generated_images/Business_strategist_expert_avatar_ef5e30a4.png";
import marketingAvatar from "@assets/generated_images/Marketing_expert_avatar_608db140.png";
import financialAvatar from "@assets/generated_images/Financial_advisor_avatar_b42774d1.png";
import techAvatar from "@assets/generated_images/Technology_consultant_avatar_afb33655.png";
import operationsAvatar from "@assets/generated_images/Operations_expert_avatar_380f05da.png";
import leadershipAvatar from "@assets/generated_images/Leadership_coach_avatar_b49e344d.png";
import { useLocation } from "wouter";

const mockExperts: Expert[] = [
  {
    id: "1",
    name: "Dr. Michael Thompson",
    title: "Estrategista de Negócios Sênior",
    expertise: ["Estratégia Corporativa", "M&A", "Transformação Organizacional"],
    bio: "Com 25 anos de experiência em consultoria estratégica para Fortune 500, Dr. Thompson especializou-se em transformações organizacionais e fusões & aquisições complexas.",
    avatar: strategistAvatar,
  },
  {
    id: "2",
    name: "Ana Costa",
    title: "Especialista em Marketing Digital",
    expertise: ["Marketing Digital", "Branding", "Growth Hacking"],
    bio: "Líder em estratégias de marketing digital que impulsionaram o crescimento de startups unicórnios e marcas globais estabelecidas.",
    avatar: marketingAvatar,
  },
  {
    id: "3",
    name: "Patricia Almeida",
    title: "Consultora Financeira Estratégica",
    expertise: ["Finanças Corporativas", "Valuation", "Reestruturação"],
    bio: "Especialista em modelagem financeira e reestruturação empresarial, com histórico de sucesso em turnarounds corporativos.",
    avatar: financialAvatar,
  },
  {
    id: "4",
    name: "Ricardo Santos",
    title: "Consultor de Inovação Tecnológica",
    expertise: ["Transformação Digital", "IA & Automação", "Cloud Strategy"],
    bio: "Pioneiro em implementações de IA empresarial e arquiteturas cloud que transformaram operações de empresas globais.",
    avatar: techAvatar,
  },
  {
    id: "5",
    name: "Mariana Silva",
    title: "Especialista em Excelência Operacional",
    expertise: ["Lean & Six Sigma", "Process Optimization", "Supply Chain"],
    bio: "Black Belt Six Sigma com expertise em otimização de processos e cadeia de suprimentos para indústrias complexas.",
    avatar: operationsAvatar,
  },
  {
    id: "6",
    name: "Dr. Carlos Mendes",
    title: "Coach de Liderança Executiva",
    expertise: ["Liderança", "Cultura Organizacional", "Change Management"],
    bio: "Mentor de CEOs e líderes C-level com foco em desenvolvimento de liderança transformacional e gestão de mudanças culturais.",
    avatar: leadershipAvatar,
  },
];

export default function Experts() {
  const [search, setSearch] = useState("");
  const [, setLocation] = useLocation();

  const filteredExperts = mockExperts.filter(
    (expert) =>
      expert.name.toLowerCase().includes(search.toLowerCase()) ||
      expert.title.toLowerCase().includes(search.toLowerCase()) ||
      expert.expertise.some((e) => e.toLowerCase().includes(search.toLowerCase()))
  );

  const handleConsult = (expert: Expert) => {
    console.log("Consulting expert:", expert.name);
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
        </div>
      </div>
    </div>
  );
}
