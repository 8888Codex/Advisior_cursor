import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { MessageSquare, Star, Sparkles } from "lucide-react";
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
  
  const initials = expert.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const isHighlyRecommended = showRecommendation && recommendationStars && recommendationStars >= 4;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
      whileHover={{ scale: 1.01, y: -2 }}
      className="relative group"
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
            initial={{ opacity: 0, scale: 0, rotate: -10 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
            className="absolute -top-2 -right-2 z-10"
          >
            <Badge className="gap-1 rounded-full px-3 py-1 bg-gradient-to-r from-primary/90 to-accent-cyan/90 text-white shadow-md pulse-glow text-xs" data-testid={`badge-recommended-${expert.id}`}>
              <Sparkles className="h-3 w-3" />
              Recomendado
            </Badge>
          </motion.div>
        )}
        
        <div className="flex items-start gap-4 relative z-10">
          {/* Avatar with Premium Hover Effect */}
          <motion.div
            animate={{
              scale: isHovered ? 1.05 : 1,
            }}
            transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
            className="relative"
          >
            <Avatar className={`h-24 w-24 ring-2 transition-all duration-600 ${
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
                    transition={{ delay: 0.4 + i * 0.05 }}
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
          </div>
        </div>

        {/* Expertise Tags with Stagger Animation */}
        <div className="flex flex-wrap gap-2 relative z-10">
          {expert.expertise.map((skill, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.8, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ 
                duration: 0.3, 
                delay: 0.1 + index * 0.05,
                ease: [0.4, 0, 0.2, 1]
              }}
              whileHover={{ scale: 1.03 }}
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

        {/* CTA Button with Enhanced Hover */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
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
