import { useRoute } from "wouter";
import { ChatInterface } from "@/components/ChatInterface";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft } from "lucide-react";
import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import strategistAvatar from "@assets/generated_images/Business_strategist_expert_avatar_ef5e30a4.png";
import marketingAvatar from "@assets/generated_images/Marketing_expert_avatar_608db140.png";
import financialAvatar from "@assets/generated_images/Financial_advisor_avatar_b42774d1.png";
import techAvatar from "@assets/generated_images/Technology_consultant_avatar_afb33655.png";
import operationsAvatar from "@assets/generated_images/Operations_expert_avatar_380f05da.png";
import leadershipAvatar from "@assets/generated_images/Leadership_coach_avatar_b49e344d.png";

const mockExperts = {
  "1": {
    id: "1",
    name: "Dr. Michael Thompson",
    title: "Estrategista de Negócios Sênior",
    expertise: ["Estratégia Corporativa", "M&A", "Transformação Organizacional"],
    bio: "Especialista em transformações organizacionais",
    avatar: strategistAvatar,
    suggestions: [
      "Como estruturar uma estratégia de expansão internacional?",
      "Quais são as melhores práticas em M&A?",
      "Como liderar uma transformação organizacional de sucesso?",
    ],
  },
  "2": {
    id: "2",
    name: "Ana Costa",
    title: "Especialista em Marketing Digital",
    expertise: ["Marketing Digital", "Branding", "Growth Hacking"],
    bio: "Líder em estratégias de marketing digital",
    avatar: marketingAvatar,
    suggestions: [
      "Como construir uma estratégia de marketing digital eficaz?",
      "Quais canais priorizar para growth hacking?",
      "Como medir ROI de campanhas digitais?",
    ],
  },
  "3": {
    id: "3",
    name: "Patricia Almeida",
    title: "Consultora Financeira Estratégica",
    expertise: ["Finanças Corporativas", "Valuation", "Reestruturação"],
    bio: "Especialista em modelagem financeira",
    avatar: financialAvatar,
    suggestions: [
      "Como fazer valuation de uma startup?",
      "Quais métricas financeiras são essenciais?",
      "Como estruturar uma reestruturação financeira?",
    ],
  },
  "4": {
    id: "4",
    name: "Ricardo Santos",
    title: "Consultor de Inovação Tecnológica",
    expertise: ["Transformação Digital", "IA & Automação", "Cloud Strategy"],
    bio: "Pioneiro em implementações de IA",
    avatar: techAvatar,
    suggestions: [
      "Como implementar IA na minha empresa?",
      "Qual a melhor estratégia de cloud?",
      "Como automatizar processos com eficiência?",
    ],
  },
  "5": {
    id: "5",
    name: "Mariana Silva",
    title: "Especialista em Excelência Operacional",
    expertise: ["Lean & Six Sigma", "Process Optimization", "Supply Chain"],
    bio: "Black Belt Six Sigma",
    avatar: operationsAvatar,
    suggestions: [
      "Como otimizar processos operacionais?",
      "Quais são os princípios Lean mais importantes?",
      "Como melhorar a eficiência da supply chain?",
    ],
  },
  "6": {
    id: "6",
    name: "Dr. Carlos Mendes",
    title: "Coach de Liderança Executiva",
    expertise: ["Liderança", "Cultura Organizacional", "Change Management"],
    bio: "Mentor de CEOs e líderes C-level",
    avatar: leadershipAvatar,
    suggestions: [
      "Como desenvolver habilidades de liderança?",
      "Como transformar a cultura organizacional?",
      "Quais são os desafios da liderança executiva?",
    ],
  },
};

export default function Chat() {
  const [, params] = useRoute("/chat/:id");
  const expertId = params?.id || "1";
  const expert = mockExperts[expertId as keyof typeof mockExperts] || mockExperts["1"];

  const initials = expert.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      <div className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link href="/experts">
              <Button variant="ghost" size="icon" data-testid="button-back">
                <ArrowLeft className="h-4 w-4" />
              </Button>
            </Link>
            <Avatar className="h-12 w-12 ring-2 ring-primary/20">
              <AvatarImage src={expert.avatar} alt={expert.name} />
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <h2 className="text-lg font-semibold">{expert.name}</h2>
              <p className="text-sm text-muted-foreground">{expert.title}</p>
            </div>
            <div className="hidden md:flex gap-2">
              {expert.expertise.slice(0, 3).map((skill, index) => (
                <Badge key={index} variant="secondary" className="text-xs">
                  {skill}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <ChatInterface expert={expert} suggestedQuestions={expert.suggestions} />
      </div>
    </div>
  );
}
