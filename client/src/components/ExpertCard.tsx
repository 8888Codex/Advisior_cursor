import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { MessageSquare } from "lucide-react";

export interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  avatar: string;
}

interface ExpertCardProps {
  expert: Expert;
  onConsult?: (expert: Expert) => void;
}

export function ExpertCard({ expert, onConsult }: ExpertCardProps) {
  const initials = expert.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <Card className="flex flex-col p-6 gap-4 hover-elevate transition-all duration-200" data-testid={`card-expert-${expert.id}`}>
      <div className="flex items-start gap-4">
        <Avatar className="h-20 w-20 ring-2 ring-primary/20">
          <AvatarImage src={expert.avatar} alt={expert.name} />
          <AvatarFallback className="text-lg font-semibold">{initials}</AvatarFallback>
        </Avatar>
        <div className="flex-1 min-w-0">
          <h3 className="text-xl font-semibold" data-testid={`text-expert-name-${expert.id}`}>
            {expert.name}
          </h3>
          <p className="text-sm text-muted-foreground">{expert.title}</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {expert.expertise.map((skill, index) => (
          <Badge key={index} variant="secondary" className="text-xs" data-testid={`badge-expertise-${expert.id}-${index}`}>
            {skill}
          </Badge>
        ))}
      </div>

      <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
        {expert.bio}
      </p>

      <Button 
        className="w-full gap-2 mt-2" 
        onClick={() => onConsult?.(expert)}
        data-testid={`button-consult-${expert.id}`}
      >
        <MessageSquare className="h-4 w-4" />
        Consultar Especialista
      </Button>
    </Card>
  );
}
