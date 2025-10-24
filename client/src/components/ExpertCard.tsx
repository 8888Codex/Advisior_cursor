import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { MessageSquare, Star, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { useRipple } from "@/hooks/use-ripple";
import { cn } from "@/lib/utils";

// Category color mapping (matching Categories page) - covers ALL schema categories
const CATEGORY_COLORS: Record<string, { text: string; bg: string }> = {
  marketing: { text: "text-primary", bg: "bg-primary/10 border-primary/30" },
  growth: { text: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30" },
  content: { text: "text-cyan-400", bg: "bg-cyan-500/10 border-cyan-500/30" },
  positioning: { text: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/30" },
  creative: { text: "text-amber-400", bg: "bg-amber-500/10 border-amber-500/30" },
  direct_response: { text: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30" },
  seo: { text: "text-lime-400", bg: "bg-lime-500/10 border-lime-500/30" },
  social: { text: "text-fuchsia-400", bg: "bg-fuchsia-500/10 border-fuchsia-500/30" },
  viral: { text: "text-pink-400", bg: "bg-pink-500/10 border-pink-500/30" },
  product: { text: "text-violet-400", bg: "bg-violet-500/10 border-violet-500/30" },
  psychology: { text: "text-indigo-400", bg: "bg-indigo-500/10 border-indigo-500/30" },
  branding: { text: "text-rose-400", bg: "bg-rose-500/10 border-rose-500/30" },
  analytics: { text: "text-teal-400", bg: "bg-teal-500/10 border-teal-500/30" },
  sales: { text: "text-green-400", bg: "bg-green-500/10 border-green-500/30" },
  sales_enablement: { text: "text-sky-400", bg: "bg-sky-500/10 border-sky-500/30" },
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
        scale: 1.01, 
        y: -2,
        transition: { type: "tween", duration: 0.6, ease: [0.4, 0, 0.2, 1] }
      }}
      whileTap={{ scale: 0.98 }}
      className="relative group press-effect"
      onClick={createRipple}
    >
      <Card 
        className={`
          flex flex-col p-8 gap-6 relative overflow-hidden rounded-3xl
          transition-all duration-600
          ${isHighlyRecommended ? 'gradient-border glow-subtle' : ''}
          hover:shadow-lg
        `}
        data-testid={`card-expert-${expert.id}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Ultra subtle gradient overlay on hover */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary/3 via-transparent to-accent/3 opacity-0 group-hover:opacity-100 transition-opacity duration-600 pointer-events-none"
          initial={false}
        />

        {/* Highly Recommended Badge */}
        {isHighlyRecommended && (
          <motion.div
            initial={{ opacity: 0, scale: 0, rotate: -5 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 20, delay: 0.2 }}
            className="absolute -top-2 -right-2 z-10"
          >
            <Badge className="gap-1 rounded-full px-3 py-0.5 bg-gradient-to-r from-primary/90 to-accent-cyan/90 text-white shadow-sm pulse-glow text-xs hover:bg-primary/8" data-testid={`badge-recommended-${expert.id}`}>
              <Sparkles className="h-3 w-3" />
              Recomendado
            </Badge>
          </motion.div>
        )}
        
        <div className="flex items-start gap-4 relative z-10">
          {/* Avatar with Premium Hover Effect */}
          <motion.div
            animate={{
              scale: isHovered ? 1.01 : 1,
              y: isHovered ? -2 : 0,
            }}
            transition={{ type: "tween", duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
            className="relative"
          >
            <Avatar className={`h-24 w-24 ring-2 transition-all duration-600 avatar-breathe ${
              isHovered 
                ? 'ring-primary/40 shadow-md shadow-primary/15' 
                : 'ring-primary/15'
            }`}>
              <AvatarImage src={expert.avatar} alt={expert.name} />
              <AvatarFallback className="text-lg font-semibold bg-gradient-to-br from-primary to-accent-cyan text-white">
                {initials}
              </AvatarFallback>
            </Avatar>
            {isHovered && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="absolute inset-0 rounded-full border-2 border-primary/40 blur-sm"
              />
            )}
          </motion.div>

          <div className="flex-1 min-w-0">
            <h3 className="text-xl font-semibold tracking-tight" data-testid={`text-expert-name-${expert.id}`}>
              {expert.name}
            </h3>
            <p className="text-sm text-muted-foreground font-normal">{expert.title}</p>
            
            {/* Star Rating */}
            {showRecommendation && recommendationStars && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="flex items-center gap-1 mt-2"
              >
                {Array.from({ length: 5 }).map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.4 + i * 0.15 }}
                  >
                    <Star
                      className={`h-4 w-4 transition-all ${
                        i < recommendationStars
                          ? 'fill-accent text-accent drop-shadow-sm'
                          : 'fill-gray-200 text-gray-200 dark:fill-gray-700 dark:text-gray-700'
                      }`}
                      data-testid={`star-${expert.id}-${i}`}
                    />
                  </motion.div>
                ))}
                <span className="text-xs text-muted-foreground ml-1 font-medium">
                  ({recommendationScore}/100)
                </span>
              </motion.div>
            )}

            {/* Category Badge */}
            {expert.category && CATEGORY_COLORS[expert.category] && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="mt-2"
              >
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
              </motion.div>
            )}
          </div>
        </div>

        {/* Expertise Tags with Spring Pop Animation */}
        <div className="flex flex-wrap gap-2 relative z-10">
          {expert.expertise.map((skill, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0, rotate: -5 }}
              animate={{ opacity: 1, scale: 1, rotate: 0 }}
              transition={{ 
                type: "spring",
                stiffness: 300,
                damping: 20,
                delay: 0.1 + index * 0.08
              }}
              whileHover={{ scale: 1.05, rotate: 2 }}
            >
              <Badge 
                variant="secondary" 
                className="text-xs rounded-full px-3 py-0.5 shimmer hover:bg-primary/8 hover:text-primary transition-colors duration-300" 
                data-testid={`badge-expertise-${expert.id}-${index}`}
              >
                {skill}
              </Badge>
            </motion.div>
          ))}
        </div>

        {/* Bio */}
        <p className="text-sm text-muted-foreground/80 leading-relaxed line-clamp-3 relative z-10 font-normal">
          {expert.bio}
        </p>

        {/* Recommendation Justification */}
        {showRecommendation && recommendationJustification && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass rounded-xl p-4 border border-primary/15 relative z-10"
          >
            <p className="text-xs leading-relaxed">
              <span className="font-medium text-primary flex items-center gap-1 mb-1">
                <Sparkles className="h-3 w-3" />
                Por que recomendamos
              </span>
              <span className="text-muted-foreground">
                {recommendationJustification}
              </span>
            </p>
          </motion.div>
        )}

        {/* CTA Button with Ultra-Subtle Hover */}
        <motion.div
          whileHover={{ scale: 1.01, y: -2 }}
          whileTap={{ scale: 0.98 }}
          transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
          className="relative z-10"
        >
          <Button 
            className="w-full gap-2 mt-2 rounded-xl shadow-sm hover:shadow-md hover:shadow-primary/10 transition-all duration-600" 
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
