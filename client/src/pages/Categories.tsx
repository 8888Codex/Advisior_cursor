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

const CATEGORY_COLORS: Record<string, { bg: string; text: string; glow: string; border: string }> = {
  marketing: {
    bg: "bg-primary/10",
    text: "text-primary",
    glow: "shadow-[0_0_30px_rgba(168,85,247,0.15)]",
    border: "border-primary/30",
  },
  growth: {
    bg: "bg-emerald-500/10",
    text: "text-emerald-400",
    glow: "shadow-[0_0_30px_rgba(52,211,153,0.15)]",
    border: "border-emerald-500/30",
  },
  content: {
    bg: "bg-cyan-500/10",
    text: "text-cyan-400",
    glow: "shadow-[0_0_30px_rgba(6,182,212,0.15)]",
    border: "border-cyan-500/30",
  },
  positioning: {
    bg: "bg-blue-500/10",
    text: "text-blue-400",
    glow: "shadow-[0_0_30px_rgba(59,130,246,0.15)]",
    border: "border-blue-500/30",
  },
  creative: {
    bg: "bg-amber-500/10",
    text: "text-amber-400",
    glow: "shadow-[0_0_30px_rgba(251,191,36,0.15)]",
    border: "border-amber-500/30",
  },
  direct_response: {
    bg: "bg-orange-500/10",
    text: "text-orange-400",
    glow: "shadow-[0_0_30px_rgba(251,146,60,0.15)]",
    border: "border-orange-500/30",
  },
  seo: {
    bg: "bg-lime-500/10",
    text: "text-lime-400",
    glow: "shadow-[0_0_30px_rgba(132,204,22,0.15)]",
    border: "border-lime-500/30",
  },
  social: {
    bg: "bg-fuchsia-500/10",
    text: "text-fuchsia-400",
    glow: "shadow-[0_0_30px_rgba(217,70,239,0.15)]",
    border: "border-fuchsia-500/30",
  },
  viral: {
    bg: "bg-pink-500/10",
    text: "text-pink-400",
    glow: "shadow-[0_0_30px_rgba(236,72,153,0.15)]",
    border: "border-pink-500/30",
  },
  product: {
    bg: "bg-violet-500/10",
    text: "text-violet-400",
    glow: "shadow-[0_0_30px_rgba(139,92,246,0.15)]",
    border: "border-violet-500/30",
  },
  psychology: {
    bg: "bg-indigo-500/10",
    text: "text-indigo-400",
    glow: "shadow-[0_0_30px_rgba(99,102,241,0.15)]",
    border: "border-indigo-500/30",
  },
  branding: {
    bg: "bg-rose-500/10",
    text: "text-rose-400",
    glow: "shadow-[0_0_30px_rgba(244,63,94,0.15)]",
    border: "border-rose-500/30",
  },
  analytics: {
    bg: "bg-teal-500/10",
    text: "text-teal-400",
    glow: "shadow-[0_0_30px_rgba(20,184,166,0.15)]",
    border: "border-teal-500/30",
  },
  sales: {
    bg: "bg-green-500/10",
    text: "text-green-400",
    glow: "shadow-[0_0_30px_rgba(34,197,94,0.15)]",
    border: "border-green-500/30",
  },
  sales_enablement: {
    bg: "bg-sky-500/10",
    text: "text-sky-400",
    glow: "shadow-[0_0_30px_rgba(14,165,233,0.15)]",
    border: "border-sky-500/30",
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
        duration: 0.6,
        delay: index * 0.15,
        ease: [0.4, 0, 0.2, 1],
      }}
    >
      <Link href={`/experts?category=${category.id}`} data-testid={`link-category-${category.id}`}>
        <motion.div
          className={cn(
            "group relative overflow-visible rounded-3xl p-8",
            "bg-card/30 backdrop-blur-lg border border-border/30",
            "hover:shadow-xl transition-all duration-600 cursor-pointer",
            colors.glow
          )}
          whileHover={{
            y: -2,
            scale: 1.01,
            transition: { duration: 0.6, ease: [0.4, 0, 0.2, 1] },
          }}
          whileTap={{ scale: 0.98 }}
        >
          {/* Icon Circle */}
          <div
            className={cn(
              "w-16 h-16 rounded-full flex items-center justify-center mb-6",
              colors.bg,
              `border-2 ${colors.border}`,
              "group-hover:scale-110 transition-transform duration-600"
            )}
            data-testid={`icon-category-${category.id}`}
          >
            <Icon className={cn("w-8 h-8", colors.text)} />
          </div>

          {/* Category Name */}
          <h3 className="text-xl font-semibold tracking-tight mb-2" data-testid={`text-category-name-${category.id}`}>
            {category.name}
          </h3>

          {/* Description */}
          <p className="text-sm text-muted-foreground/80 leading-relaxed mb-6" data-testid={`text-category-description-${category.id}`}>
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
              className={cn("rounded-xl min-h-11", colors.text)}
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
        <div key={i} className="rounded-3xl p-8 bg-card/30 backdrop-blur-lg border border-border/30">
          <Skeleton className="w-16 h-16 rounded-full mb-6" />
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
      <div className="min-h-screen bg-gradient-mesh">
        <div className="max-w-7xl mx-auto px-6 py-24">
          {/* Header */}
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 text-gradient-primary" data-testid="heading-categories">
              Explore por Área de Expertise
            </h1>
            <p className="text-lg text-muted-foreground/80 max-w-3xl mx-auto leading-relaxed" data-testid="text-categories-subtitle">
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
