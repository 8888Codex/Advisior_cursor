import { useEffect } from "react";
import { useLocation } from "wouter";
import { useQuery } from "@tanstack/react-query";
import { Hero } from "@/components/Hero";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AnimatedPage } from "@/components/AnimatedPage";
import { TrendingUp, Clock, Award, Lightbulb, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const [, setLocation] = useLocation();

  // Check if user has completed onboarding
  const { data: profile } = useQuery({
    queryKey: ["/api/profile"],
    retry: false,
  });

  // Fetch personalized business insights
  const { data: insightsData } = useQuery<{
    hasProfile: boolean;
    insights: Array<{ category: string; content: string }>;
    profileSummary?: {
      companyName: string;
      industry: string;
      primaryGoal: string;
    };
  }>({
    queryKey: ["/api/insights"],
    enabled: !!profile,
    retry: false,
  });

  useEffect(() => {
    // Check if onboarding has been completed
    const onboardingComplete = localStorage.getItem("onboarding_complete");
    
    // If no localStorage flag and no profile, redirect to welcome
    if (!onboardingComplete && !profile) {
      setLocation("/welcome");
    }
  }, [profile, setLocation]);

  return (
    <AnimatedPage>
      <div className="min-h-screen">
      <Hero />

      {/* Personalized Insights Section - Apple Minimalist */}
      {insightsData?.hasProfile && insightsData.insights.length > 0 && (
        <section className="relative w-full py-20 md:py-24">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="text-center mb-12"
            >
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.25, delay: 0.05 }}
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-muted/50 border border-border/50 mb-8"
              >
                <Sparkles className="h-4 w-4 text-accent" />
                <span className="text-sm font-medium text-foreground">
                  Personalizado para {insightsData.profileSummary?.companyName}
                </span>
              </motion.div>
              
              <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: 0.1 }}
                className="text-4xl md:text-5xl font-semibold mb-4"
              >
                Insights para Seu Negócio
              </motion.h2>
              
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="text-muted-foreground max-w-2xl mx-auto text-lg"
              >
                Dicas estratégicas baseadas no seu perfil e tendências atuais do mercado
              </motion.p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
              {insightsData.insights.map((insight, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileHover={{ y: -2 }}
                  transition={{
                    duration: 0.25,
                    delay: 0.15 + index * 0.05,
                    ease: [0.25, 0.1, 0.25, 1],
                  }}
                >
                  <Card className="p-8 h-full rounded-2xl hover:shadow-md transition-all duration-200 group">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 w-14 h-14 rounded-full bg-accent/10 flex items-center justify-center">
                        <Lightbulb className="h-6 w-6 text-accent" />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <Badge 
                          variant="secondary" 
                          className="mb-3 rounded-full px-3 py-0.5 text-xs"
                        >
                          {insight.category}
                        </Badge>
                        <p className="text-sm leading-relaxed text-muted-foreground">
                          {insight.content}
                        </p>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.5 }}
              className="text-center mt-8"
            >
              <p className="text-sm text-muted-foreground">
                Quer análises mais profundas? Consulte nossos especialistas
              </p>
              <Button
                variant="outline"
                className="mt-3"
                onClick={() => setLocation("/experts")}
                data-testid="button-view-experts"
              >
                Ver Especialistas
              </Button>
            </motion.div>
          </div>
        </section>
      )}

      <section className="w-full py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Por Que AdvisorIA?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Transforme a forma como você acessa conhecimento estratégico de elite
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="p-6 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <TrendingUp className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Resultados Rápidos</h3>
              <p className="text-sm text-muted-foreground">
                Obtenha insights estratégicos instantaneamente, sem esperar semanas por reuniões de consultoria
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <Clock className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Disponível 24/7</h3>
              <p className="text-sm text-muted-foreground">
                Acesso ilimitado a expertise estratégica a qualquer hora, de qualquer lugar
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <Award className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Expertise Customizada</h3>
              <p className="text-sm text-muted-foreground">
                Crie consultores especializados nas suas necessidades específicas de negócio
              </p>
            </Card>
          </div>

          <div className="text-center mt-12">
            <p className="text-lg mb-6 text-muted-foreground">
              Pronto para elevar suas decisões estratégicas?
            </p>
            <Button size="lg" data-testid="button-get-started">
              Começar Agora
            </Button>
          </div>
        </div>
      </section>
      </div>
    </AnimatedPage>
  );
}
