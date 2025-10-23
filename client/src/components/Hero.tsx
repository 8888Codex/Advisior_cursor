import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Brain, Users } from "lucide-react";
import { Link } from "wouter";

export function Hero() {
  return (
    <section className="relative w-full py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto gap-8">
          <div className="inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm">
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="text-muted-foreground">Consultoria Estratégica de Elite</span>
          </div>

          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight">
            Democratizando o Acesso a{" "}
            <span className="text-primary">Mentalidades Estratégicas</span> de Alto Nível
          </h1>

          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl leading-relaxed">
            Consulte clones digitais de especialistas renomados ou crie seus próprios consultores de IA personalizados para resolver seus desafios de negócios mais complexos.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mt-4">
            <Link href="/experts">
              <Button size="lg" className="gap-2" data-testid="button-explore-experts">
                Explorar Especialistas
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/create">
              <Button size="lg" variant="outline" className="gap-2" data-testid="button-create-expert">
                Criar Seu Especialista
                <Brain className="h-4 w-4" />
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 w-full">
            <div className="flex flex-col items-center gap-3 p-6">
              <div className="rounded-full bg-primary/10 p-4">
                <Brain className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-semibold text-lg">Expertise de Elite</h3>
              <p className="text-sm text-muted-foreground">
                Acesse conhecimento estratégico de consultores de alto nível
              </p>
            </div>

            <div className="flex flex-col items-center gap-3 p-6">
              <div className="rounded-full bg-primary/10 p-4">
                <Users className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-semibold text-lg">Consultores Personalizados</h3>
              <p className="text-sm text-muted-foreground">
                Crie especialistas customizados para suas necessidades específicas
              </p>
            </div>

            <div className="flex flex-col items-center gap-3 p-6">
              <div className="rounded-full bg-primary/10 p-4">
                <Sparkles className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-semibold text-lg">Insights Estratégicos</h3>
              <p className="text-sm text-muted-foreground">
                Obtenha análises profundas e soluções inovadoras instantaneamente
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
