import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { MessageSquare } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

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
  const [isHovered, setIsHovered] = useState(false);
  
  const initials = expert.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
    >
      <Card 
        className="flex flex-col p-6 gap-4 hover-elevate transition-all duration-200" 
        data-testid={`card-expert-${expert.id}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <div className="flex items-start gap-4">
          <motion.div
            animate={{
              scale: isHovered ? 1.05 : 1,
              rotate: isHovered ? [0, -2, 2, 0] : 0
            }}
            transition={{ duration: 0.3 }}
          >
            <Avatar className="h-20 w-20 ring-2 ring-primary/20">
              <AvatarImage src={expert.avatar} alt={expert.name} />
              <AvatarFallback className="text-lg font-semibold">{initials}</AvatarFallback>
            </Avatar>
          </motion.div>
        <div className="flex-1 min-w-0">
          <h3 className="text-xl font-semibold" data-testid={`text-expert-name-${expert.id}`}>
            {expert.name}
          </h3>
          <p className="text-sm text-muted-foreground">{expert.title}</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {expert.expertise.map((skill, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ 
              duration: 0.2, 
              delay: 0.1 + index * 0.05,
              ease: [0.4, 0, 0.2, 1]
            }}
          >
            <Badge variant="secondary" className="text-xs" data-testid={`badge-expertise-${expert.id}-${index}`}>
              {skill}
            </Badge>
          </motion.div>
        ))}
      </div>

      <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
        {expert.bio}
      </p>

        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Button 
            className="w-full gap-2 mt-2" 
            onClick={() => onConsult?.(expert)}
            data-testid={`button-consult-${expert.id}`}
          >
            <MessageSquare className="h-4 w-4" />
            Consultar Especialista
          </Button>
        </motion.div>
      </Card>
    </motion.div>
  );
}
