import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { MessageSquare, Star, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { useRipple } from "@/hooks/use-ripple";
import { cn } from "@/lib/utils";

// Apple-style: Single accent color, neutral categories
const CATEGORY_COLORS: Record<string, { text: string; bg: string }> = {
  marketing: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  growth: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  content: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  positioning: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  creative: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  direct_response: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  seo: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  social: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  viral: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  product: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  psychology: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  branding: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  analytics: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  sales: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
  sales_enablement: { text: "text-muted-foreground", bg: "bg-muted/50 border-border" },
};

const CATEGORY_NAMES: Record<string, string> = {
  marketing: "Marketing",
  growth: "Growth",
  content: "Content",
  positioning: "Positioning",
  creative: "Creative",
  direct_response: "Direct Response",
  seo: "SEO",
  social: "Social",
  viral: "Viral",
  product: "Product",
  psychology: "Psychology",
  branding: "Branding",
  analytics: "Analytics",
  sales: "Sales",
  sales_enablement: "Sales Enablement",
};

export interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  avatar: string;
  category: string;
}

interface ExpertCardProps {
  expert: Expert;
  onConsult?: (expert: Expert) => void;
  recommendationScore?: number;
  recommendationStars?: number;
  recommendationJustification?: string;
  showRecommendation?: boolean;
}

export function ExpertCard({ 
  expert, 
  onConsult, 
  recommendationScore,
  recommendationStars,
  recommendationJustification,
  showRecommendation = false
}: ExpertCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  const { createRipple } = useRipple();
  
  const initials = expert.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const isHighlyRecommended = showRecommendation && recommendationStars && recommendationStars >= 4;

  return (
    <motion.div
      whileHover={{ 
        y: -2,
        transition: { duration: 0.2, ease: [0.25, 0.1, 0.25, 1] }
      }}
      whileTap={{ scale: 0.98 }}
      className="relative group press-effect"
      onClick={createRipple}
    >
      <Card 
        className={`
          flex flex-col p-8 gap-6 relative rounded-2xl border border-border/50
          transition-shadow duration-200
          ${isHighlyRecommended ? 'border-accent/30' : ''}
          hover:shadow-md
        `}
        data-testid={`card-expert-${expert.id}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Recommended Badge */}
        {isHighlyRecommended && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2 }}
            className="absolute -top-2 -right-2 z-10"
          >
            <Badge className="gap-1 rounded-full px-3 py-1 bg-accent text-white shadow-sm text-xs" data-testid={`badge-recommended-${expert.id}`}>
              <Sparkles className="h-3 w-3" />
              Recomendado
            </Badge>
          </motion.div>
        )}
        
        <div className="flex items-start gap-4">
          {/* Avatar */}
          <Avatar className={`h-20 w-20 ring-2 transition-all duration-200 ${
            isHovered 
              ? 'ring-accent/30' 
              : 'ring-border/50'
          }`}>
            <AvatarImage src={expert.avatar} alt={expert.name} />
            <AvatarFallback className="text-lg font-medium bg-accent/10 text-accent">
              {initials}
            </AvatarFallback>
          </Avatar>

          <div className="flex-1 min-w-0">
            <h3 className="text-xl font-medium tracking-tight" data-testid={`text-expert-name-${expert.id}`}>
              {expert.name}
            </h3>
            <p className="text-sm text-muted-foreground">{expert.title}</p>
            
            {/* Star Rating */}
            {showRecommendation && recommendationStars && (
              <div className="flex items-center gap-1 mt-2">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    className={`h-4 w-4 ${
                      i < recommendationStars
                        ? 'fill-accent text-accent'
                        : 'fill-gray-200 text-gray-200 dark:fill-gray-700 dark:text-gray-700'
                    }`}
                    data-testid={`star-${expert.id}-${i}`}
                  />
                ))}
                <span className="text-xs text-muted-foreground ml-1 font-medium">
                  ({recommendationScore}/100)
                </span>
              </div>
            )}

            {/* Category Badge */}
            {expert.category && CATEGORY_COLORS[expert.category] && (
              <div className="mt-2">
                <Badge 
                  className={cn(
                    "text-xs rounded-full px-3 py-0.5 border font-medium",
                    CATEGORY_COLORS[expert.category].bg,
                    CATEGORY_COLORS[expert.category].text
                  )}
                  data-testid={`badge-category-${expert.id}`}
                >
                  {CATEGORY_NAMES[expert.category] || expert.category}
                </Badge>
              </div>
            )}
          </div>
        </div>

        {/* Expertise Tags */}
        <div className="flex flex-wrap gap-2">
          {expert.expertise.map((skill, index) => (
            <Badge 
              key={index}
              variant="secondary" 
              className="text-xs rounded-full px-3 py-0.5" 
              data-testid={`badge-expertise-${expert.id}-${index}`}
            >
              {skill}
            </Badge>
          ))}
        </div>

        {/* Bio */}
        <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
          {expert.bio}
        </p>

        {/* Recommendation Justification */}
        {showRecommendation && recommendationJustification && (
          <div className="bg-accent/5 border border-accent/10 rounded-xl p-4">
            <p className="text-xs leading-relaxed">
              <span className="font-medium text-accent flex items-center gap-1 mb-1">
                <Sparkles className="h-3 w-3" />
                Por que recomendamos
              </span>
              <span className="text-muted-foreground">
                {recommendationJustification}
              </span>
            </p>
          </div>
        )}

        {/* CTA Button */}
        <Button 
          className="w-full gap-2 mt-2 rounded-xl shadow-sm" 
          onClick={() => onConsult?.(expert)}
          data-testid={`button-consult-${expert.id}`}
        >
          <MessageSquare className="h-4 w-4" />
          Consultar Especialista
        </Button>
      </Card>
    </motion.div>
  );
}
