import { useQuery } from "@tanstack/react-query";
import { Link } from "wouter";
import { motion } from "framer-motion";
import {
  TrendingUp,
  Rocket,
  FileText,
  Target,
  Sparkles,
  BarChart,
  Search,
  Users,
  Share2,
  Package,
  Brain,
  Award,
  BarChart4,
  Handshake,
  TrendingUpDown,
  type LucideIcon,
} from "lucide-react";
import { AnimatedPage } from "@/components/AnimatedPage";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

interface Category {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  expertCount: number;
}

const CATEGORY_ICONS: Record<string, LucideIcon> = {
  marketing: TrendingUp,
  growth: Rocket,
  content: FileText,
  positioning: Target,
  creative: Sparkles,
  direct_response: BarChart,
  seo: Search,
  social: Users,
  viral: Share2,
  product: Package,
  psychology: Brain,
  branding: Award,
  analytics: BarChart4,
  sales: Handshake,
  sales_enablement: TrendingUpDown,
};

// Apple-style: Neutral palette, no rainbow colors
const CATEGORY_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  marketing: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  growth: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  content: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  positioning: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  creative: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  direct_response: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  seo: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  social: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  viral: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  product: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  psychology: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  branding: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  analytics: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  sales: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
  sales_enablement: {
    bg: "bg-muted/50",
    text: "text-foreground",
    border: "border-border/50",
  },
};

function CategoryCard({ category, index }: { category: Category; index: number }) {
  const Icon = CATEGORY_ICONS[category.id] || TrendingUp;
  const colors = CATEGORY_COLORS[category.id] || CATEGORY_COLORS.marketing;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.3,
        delay: index * 0.05,
        ease: [0.25, 0.1, 0.25, 1],
      }}
    >
      <Link href={`/experts?category=${category.id}`} data-testid={`link-category-${category.id}`}>
        <motion.div
          className={cn(
            "group relative rounded-2xl p-8",
            "bg-card border border-border/50",
            "hover:shadow-md transition-shadow duration-200 cursor-pointer"
          )}
          whileHover={{
            y: -2,
            transition: { duration: 0.2, ease: [0.25, 0.1, 0.25, 1] },
          }}
          whileTap={{ scale: 0.98 }}
        >
          {/* Icon Circle */}
          <div
            className={cn(
              "w-14 h-14 rounded-full flex items-center justify-center mb-6",
              colors.bg,
              `border ${colors.border}`,
              "group-hover:scale-105 transition-transform duration-200"
            )}
            data-testid={`icon-category-${category.id}`}
          >
            <Icon className={cn("w-7 h-7", colors.text)} />
          </div>

          {/* Category Name */}
          <h3 className="text-xl font-medium tracking-tight mb-2" data-testid={`text-category-name-${category.id}`}>
            {category.name}
          </h3>

          {/* Description */}
          <p className="text-sm text-muted-foreground leading-relaxed mb-6" data-testid={`text-category-description-${category.id}`}>
            {category.description}
          </p>

          {/* Expert Count + CTA */}
          <div className="flex items-center justify-between gap-4">
            <span className="text-xs font-medium text-muted-foreground" data-testid={`text-expert-count-${category.id}`}>
              {category.expertCount} {category.expertCount === 1 ? "Especialista" : "Especialistas"}
            </span>

            <Button
              variant="ghost"
              size="sm"
              className={cn("rounded-xl", colors.text)}
              data-testid={`button-view-experts-${category.id}`}
            >
              Ver Especialistas →
            </Button>
          </div>
        </motion.div>
      </Link>
    </motion.div>
  );
}

function CategoryGridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="rounded-2xl p-8 bg-card border border-border/50">
          <Skeleton className="w-14 h-14 rounded-full mb-6" />
          <Skeleton className="h-6 w-48 mb-2" />
          <Skeleton className="h-4 w-full mb-2" />
          <Skeleton className="h-4 w-3/4 mb-6" />
          <div className="flex items-center justify-between">
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-8 w-40 rounded-xl" />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function Categories() {
  const { data: categories, isLoading } = useQuery<Category[]>({
    queryKey: ["/api/categories"],
  });

  return (
    <AnimatedPage>
      <div className="min-h-screen">
        <div className="max-w-7xl mx-auto px-6 py-24">
          {/* Header */}
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h1 className="text-5xl md:text-6xl font-semibold tracking-tight mb-6" data-testid="heading-categories">
              Explore por Área de Expertise
            </h1>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed" data-testid="text-categories-subtitle">
              Navegue pelos nossos especialistas organizados por disciplina. Cada categoria reúne os maiores nomes
              em suas respectivas áreas para oferecer consultoria ultra-especializada.
            </p>
          </motion.div>

          {/* Categories Grid */}
          {isLoading ? (
            <CategoryGridSkeleton />
          ) : categories && categories.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8" data-testid="grid-categories">
              {categories.map((category, index) => (
                <CategoryCard key={category.id} category={category} index={index} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-muted-foreground">Nenhuma categoria disponível no momento.</p>
            </div>
          )}
        </div>
      </div>
    </AnimatedPage>
  );
}
