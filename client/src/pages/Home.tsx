import { useEffect } from "react";
import { useLocation } from "wouter";
import { useQuery } from "@tanstack/react-query";
import { Hero } from "@/components/Hero";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AnimatedPage } from "@/components/AnimatedPage";
import { TrendingUp, Clock, Award } from "lucide-react";

export default function Home() {
  const [, setLocation] = useLocation();

  // Check if user has completed onboarding
  const { data: profile } = useQuery({
    queryKey: ["/api/profile"],
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
