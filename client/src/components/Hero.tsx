import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Brain, Users, Zap } from "lucide-react";
import { Link } from "wouter";
import { motion } from "framer-motion";
import { useRipple } from "@/hooks/use-ripple";

export function Hero() {
  const { createRipple } = useRipple();
  
  return (
    <section className="relative w-full py-20 md:py-32 overflow-hidden">
      {/* Premium Gradient Background */}
      <div className="absolute inset-0 bg-gradient-hero pointer-events-none" />
      
      {/* Animated Mesh Gradient Overlay */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-accent-cyan/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto gap-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 glass rounded-full px-6 py-2.5 text-sm shimmer"
          >
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="font-medium bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent-cyan">
              Consultoria Estratégica de Elite com IA
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-tight"
          >
            Democratizando o Acesso a{" "}
            <span className="text-gradient-premium inline-block">
              Mentalidades Estratégicas
            </span>{" "}
            de Alto Nível
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg md:text-xl text-muted-foreground max-w-2xl leading-relaxed"
          >
            Consulte clones digitais de especialistas renomados ou crie seus próprios consultores de IA personalizados para resolver seus desafios de negócios mais complexos.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 mt-4"
          >
            <Link href="/experts">
              <Button 
                size="lg" 
                className="gap-2 rounded-xl glow-subtle transition-all duration-600 press-effect relative overflow-hidden" 
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
                className="gap-2 rounded-xl glass-strong hover:border-primary/30 transition-all duration-600 press-effect relative overflow-hidden" 
                data-testid="button-create-expert"
                onClick={createRipple}
              >
                <Brain className="h-4 w-4" />
                Criar Seu Especialista
              </Button>
            </Link>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-10 mt-16 w-full max-w-4xl mx-auto">
            {[
              {
                icon: Brain,
                title: "Expertise de Elite",
                description: "Acesse conhecimento estratégico de consultores de alto nível",
                gradient: "from-primary to-accent-cyan",
                delay: 0.4
              },
              {
                icon: Users,
                title: "Consultores Personalizados",
                description: "Crie especialistas customizados para suas necessidades específicas",
                gradient: "from-accent-cyan to-accent",
                delay: 0.5
              },
              {
                icon: Sparkles,
                title: "Insights Estratégicos",
                description: "Obtenha análises profundas e soluções inovadoras instantaneamente",
                gradient: "from-accent to-primary",
                delay: 0.6
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ 
                  duration: 0.5, 
                  delay: feature.delay,
                  ease: [0.4, 0, 0.2, 1]
                }}
                className="flex flex-col items-center gap-4 p-8 glass rounded-3xl hover:glass-strong transition-all duration-600 group hover:scale-[1.01] hover:-translate-y-0.5"
              >
                <div className={`rounded-full bg-gradient-to-br ${feature.gradient} p-4 shadow-md group-hover:shadow-lg transition-all duration-600`}>
                  <feature.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="font-semibold text-lg tracking-tight">{feature.title}</h3>
                <p className="text-sm text-muted-foreground/80 leading-relaxed font-normal">
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
