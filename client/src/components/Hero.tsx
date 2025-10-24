import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Brain, Users, Zap } from "lucide-react";
import { Link } from "wouter";
import { motion } from "framer-motion";
import { useRipple } from "@/hooks/use-ripple";

export function Hero() {
  const { createRipple } = useRipple();
  
  return (
    <section className="relative w-full py-24 md:py-32">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto gap-8">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="inline-flex items-center gap-2 bg-muted/50 rounded-full px-6 py-2.5 text-sm border border-border/50"
          >
            <Sparkles className="h-4 w-4 text-accent" />
            <span className="font-medium text-foreground">
              Consultoria Estratégica de Elite com IA
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.05 }}
            className="text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight leading-tight"
          >
            Democratizando o Acesso a{" "}
            <span className="text-accent">
              Mentalidades Estratégicas
            </span>{" "}
            de Alto Nível
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
            className="text-lg md:text-xl text-muted-foreground max-w-2xl leading-relaxed"
          >
            Consulte clones digitais de especialistas renomados ou crie seus próprios consultores de IA personalizados para resolver seus desafios de negócios mais complexos.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.15 }}
            className="flex flex-col sm:flex-row gap-4 mt-4"
          >
            <Link href="/experts">
              <Button 
                size="lg" 
                className="gap-2 rounded-xl press-effect" 
                data-testid="button-explore-experts"
                onClick={createRipple}
              >
                <Zap className="h-5 w-5" />
                Explorar Especialistas
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/create">
              <Button 
                size="lg" 
                variant="outline" 
                className="gap-2 rounded-xl press-effect" 
                data-testid="button-create-expert"
                onClick={createRipple}
              >
                <Brain className="h-4 w-4" />
                Criar Seu Especialista
              </Button>
            </Link>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-20 w-full max-w-4xl mx-auto">
            {[
              {
                icon: Brain,
                title: "Expertise de Elite",
                description: "Acesse conhecimento estratégico de consultores de alto nível",
                delay: 0.2
              },
              {
                icon: Users,
                title: "Consultores Personalizados",
                description: "Crie especialistas customizados para suas necessidades específicas",
                delay: 0.25
              },
              {
                icon: Sparkles,
                title: "Insights Estratégicos",
                description: "Obtenha análises profundas e soluções inovadoras instantaneamente",
                delay: 0.3
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  duration: 0.3, 
                  delay: feature.delay,
                  ease: [0.25, 0.1, 0.25, 1]
                }}
                className="flex flex-col items-center gap-4 p-8 bg-card/50 border border-border/50 rounded-2xl card-hover"
              >
                <div className="rounded-full bg-accent/10 p-4 border border-accent/20">
                  <feature.icon className="h-8 w-8 text-accent" />
                </div>
                <h3 className="font-medium text-lg tracking-tight">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
