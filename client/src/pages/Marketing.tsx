import { useQuery } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { AnimatedPage } from "@/components/AnimatedPage";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { motion } from "framer-motion";
import { 
  Sparkles, 
  TrendingUp, 
  Users, 
  Award,
  ChevronRight,
  MessageSquare,
  Calendar
} from "lucide-react";
import type { Expert } from "@shared/schema";

export default function Marketing() {
  const [, setLocation] = useLocation();

  const { data: experts = [], isLoading } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  const marketingLegends = experts.filter(e => e.expertise && e.expertise.length > 0);
  const totalYearsExperience = marketingLegends.length * 25;

  const impactStats = [
    { 
      icon: Users, 
      value: "18", 
      label: "Lendas do Marketing",
      description: "De Philip Kotler a Gary Vaynerchuk"
    },
    { 
      icon: Calendar, 
      value: `${totalYearsExperience}+`, 
      label: "Anos de Expertise",
      description: "Conhecimento combinado sem precedentes"
    },
    { 
      icon: Award, 
      value: "19-20/20", 
      label: "Fidelidade Cognitiva",
      description: "Framework EXTRACT de 20 pontos"
    },
  ];

  return (
    <AnimatedPage>
      <div className="min-h-screen">
        {/* Hero Section */}
        <section className="relative w-full py-20 md:py-28 bg-gradient-to-b from-muted/30 to-background">
          <div className="container mx-auto px-4">
            <div className="max-w-5xl mx-auto text-center space-y-8">
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-muted border border-border/50"
              >
                <Sparkles className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-medium text-muted-foreground">
                  As Maiores Mentes do Marketing Mundial
                </span>
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.05 }}
                className="text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight leading-tight"
              >
                {totalYearsExperience}+ Anos de Sabedoria.
                <br />
                <span className="text-accent">Um Clique de Distância.</span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.1 }}
                className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed"
              >
                Cada especialista foi recriado com o Framework EXTRACT™ de 20 pontos.
                O resultado? Conversas tão autênticas que você esquece que está falando com IA.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.15 }}
                className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4"
              >
                <Button 
                  size="lg" 
                  className="gap-2"
                  onClick={() => setLocation("/experts")}
                  data-testid="button-start-consulting"
                >
                  Começar Consultoria Agora
                  <ChevronRight className="h-5 w-5" />
                </Button>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Impact Stats */}
        <section className="w-full py-16 bg-background">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {impactStats.map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: 0.2 + index * 0.05 }}
                >
                  <Card className="p-8 text-center rounded-2xl">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted mb-4">
                      <stat.icon className="h-8 w-8 text-muted-foreground" />
                    </div>
                    <div className="text-4xl font-semibold mb-2">{stat.value}</div>
                    <h3 className="text-lg font-medium mb-2">{stat.label}</h3>
                    <p className="text-sm text-muted-foreground">{stat.description}</p>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Timeline de Impacto */}
        <section className="w-full py-20 bg-background">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="text-4xl md:text-5xl font-semibold mb-4"
              >
                Décadas de Impacto. Agora Acessível.
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.05 }}
                className="text-lg text-muted-foreground max-w-2xl mx-auto"
              >
                De 1967 até hoje: as mentes que moldaram o marketing moderno,
                disponíveis para consulta instantânea.
              </motion.p>
            </div>

            <div className="max-w-5xl mx-auto space-y-6">
              {[
                {
                  decade: "1967-1980",
                  title: "Fundações do Marketing Moderno",
                  experts: ["Philip Kotler", "Al Ries", "Jack Trout"],
                  impact: "Criaram os conceitos fundamentais: 4Ps, posicionamento, segmentação de mercado"
                },
                {
                  decade: "1980-2000",
                  title: "Era da Marca e Identidade",
                  experts: ["David Ogilvy", "Guy Kawasaki", "Jay Conrad Levinson"],
                  impact: "Revolucionaram branding, evangelismo de marca e guerrilla marketing para pequenas empresas"
                },
                {
                  decade: "2000-2015",
                  title: "Revolução Digital",
                  experts: ["Seth Godin", "Neil Patel", "Tim Ferriss"],
                  impact: "Transformaram marketing com tribos, SEO/growth hacking e produtividade estratégica"
                },
                {
                  decade: "2015-Hoje",
                  title: "Marketing de Conteúdo e Social",
                  experts: ["Gary Vaynerchuk", "Ann Handley", "Rand Fishkin"],
                  impact: "Dominaram conteúdo, mídias sociais e SEO transparente na era da atenção"
                }
              ].map((era, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.08 }}
                >
                  <Card className="p-6 rounded-2xl hover:shadow-md transition-all duration-200">
                    <div className="flex items-start gap-6">
                      <div className="flex-shrink-0 text-center">
                        <Badge variant="secondary" className="rounded-full px-4 py-1 mb-2">
                          {era.decade}
                        </Badge>
                      </div>
                      <div className="flex-1 space-y-2">
                        <h3 className="text-xl font-semibold">{era.title}</h3>
                        <p className="text-sm text-muted-foreground">
                          <span className="font-medium">Lendas: </span>
                          {era.experts.join(", ")}
                        </p>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {era.impact}
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
              transition={{ duration: 0.3, delay: 0.4 }}
              className="text-center mt-12"
            >
              <p className="text-muted-foreground mb-4">
                Mais de 50 anos de inovação em marketing, agora em conversas instantâneas
              </p>
            </motion.div>
          </div>
        </section>

        {/* Perguntas que Cada Lenda Responde */}
        <section className="w-full py-20 bg-muted/20">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="text-4xl md:text-5xl font-semibold mb-4"
              >
                Perguntas Que Cada Lenda Responde
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.05 }}
                className="text-lg text-muted-foreground max-w-2xl mx-auto"
              >
                Exemplos reais de como consultar cada especialista.
                Faça suas próprias perguntas ou use essas como inspiração.
              </motion.p>
            </div>

            <div className="grid md:grid-cols-2 gap-6 max-w-6xl mx-auto">
              {[
                {
                  expert: "Philip Kotler",
                  title: "Pai do Marketing Moderno",
                  questions: [
                    "Como segmentar meu mercado B2B de forma eficaz?",
                    "Qual estratégia de precificação maximiza valor percebido?",
                    "Como aplicar os 4Ps em produtos digitais?"
                  ]
                },
                {
                  expert: "Seth Godin",
                  title: "Visionário das Tribos",
                  questions: [
                    "Como criar uma tribo engajada ao redor da minha marca?",
                    "Qual a diferença entre marketing de permissão e interrupção?",
                    "Como ser notável (remarkable) num mercado saturado?"
                  ]
                },
                {
                  expert: "Gary Vaynerchuk",
                  title: "Rei do Marketing de Conteúdo",
                  questions: [
                    "Qual plataforma social devo priorizar em 2025?",
                    "Como produzir conteúdo autêntico que vende sem ser vendedor?",
                    "Estratégia de 'jab, jab, jab, right hook' para meu nicho?"
                  ]
                },
                {
                  expert: "Neil Patel",
                  title: "Growth Hacker Legendário",
                  questions: [
                    "Como rankear no Google para palavras-chave competitivas?",
                    "Qual estratégia de link building funciona hoje?",
                    "Como otimizar taxa de conversão do meu funil?"
                  ]
                },
                {
                  expert: "Al Ries",
                  title: "Mestre do Posicionamento",
                  questions: [
                    "Como posicionar minha startup em mercado dominado?",
                    "Lei da categoria: devo criar nova categoria ou competir?",
                    "Como simplificar mensagem para ocupar mente do consumidor?"
                  ]
                },
                {
                  expert: "Ann Handley",
                  title: "Rainha do Content Marketing",
                  questions: [
                    "Como escrever emails que convertem sem parecer spam?",
                    "Qual estrutura de storytelling funciona para B2B?",
                    "Como criar conteúdo que educa e vende simultaneamente?"
                  ]
                }
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.25, delay: index * 0.05 }}
                >
                  <Card className="p-6 h-full rounded-2xl hover:shadow-md transition-all duration-200">
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-semibold text-lg mb-1">{item.expert}</h3>
                        <p className="text-sm text-muted-foreground">{item.title}</p>
                      </div>
                      <div className="space-y-2">
                        {item.questions.map((question, qIndex) => (
                          <div 
                            key={qIndex}
                            className="flex gap-2 text-sm"
                          >
                            <span className="text-accent flex-shrink-0">•</span>
                            <span className="text-muted-foreground leading-relaxed">
                              "{question}"
                            </span>
                          </div>
                        ))}
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="w-full gap-2 mt-2"
                        onClick={() => {
                          const expert = marketingLegends.find(e => e.name === item.expert);
                          if (expert) setLocation(`/chat/${expert.id}`);
                        }}
                        data-testid={`button-ask-${item.expert.toLowerCase().replace(/\s+/g, '-')}`}
                      >
                        <MessageSquare className="h-4 w-4" />
                        Perguntar para {item.expert.split(' ')[0]}
                      </Button>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.4 }}
              className="text-center mt-12"
            >
              <p className="text-sm text-muted-foreground mb-4">
                + 12 outros especialistas respondendo perguntas sobre branding, PR, copywriting, analytics e mais
              </p>
              <Button 
                variant="outline"
                onClick={() => setLocation("/experts")}
                data-testid="button-view-all-experts"
              >
                Ver Todos os 18 Especialistas
              </Button>
            </motion.div>
          </div>
        </section>

        {/* Legends Grid */}
        <section className="w-full py-20 bg-background">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="text-4xl md:text-5xl font-semibold mb-4"
              >
                Conheça as 18 Lendas
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.05 }}
                className="text-lg text-muted-foreground max-w-2xl mx-auto"
              >
                Cada especialista domina décadas de conhecimento estratégico.
                Todos disponíveis 24/7 para resolver seus desafios.
              </motion.p>
            </div>

            {isLoading ? (
              <div className="text-center py-12">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="inline-block"
                >
                  <Sparkles className="h-8 w-8 text-accent" />
                </motion.div>
                <p className="text-muted-foreground mt-4">Carregando especialistas...</p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
                {marketingLegends.map((expert, index) => {
                  const initials = expert.name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")
                    .toUpperCase()
                    .slice(0, 2);

                  return (
                    <motion.div
                      key={expert.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      whileHover={{ y: -2 }}
                      transition={{
                        duration: 0.25,
                        delay: index * 0.03,
                        ease: [0.25, 0.1, 0.25, 1],
                      }}
                    >
                      <Card className="p-6 h-full rounded-2xl group hover:shadow-md transition-all duration-200">
                        <div className="flex items-start gap-4 mb-4">
                          <Avatar className="h-16 w-16 ring-2 ring-border/50">
                            <AvatarImage src={expert.avatar || undefined} alt={expert.name} />
                            <AvatarFallback>{initials}</AvatarFallback>
                          </Avatar>
                          <div className="flex-1 min-w-0">
                            <h3 className="font-semibold text-lg mb-1 leading-tight">
                              {expert.name}
                            </h3>
                            <p className="text-sm text-muted-foreground leading-snug">
                              {expert.title}
                            </p>
                          </div>
                        </div>

                        <div className="flex flex-wrap gap-2 mb-4">
                          {expert.expertise.slice(0, 3).map((skill, idx) => (
                            <Badge 
                              key={idx}
                              variant="secondary" 
                              className="text-xs rounded-full px-3 py-0.5"
                            >
                              {skill}
                            </Badge>
                          ))}
                        </div>

                        <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3 mb-4">
                          {expert.bio}
                        </p>

                        <Button
                          variant="outline"
                          size="sm"
                          className="w-full gap-2"
                          onClick={() => setLocation(`/chat/${expert.id}`)}
                          data-testid={`button-consult-${expert.id}`}
                        >
                          <MessageSquare className="h-4 w-4" />
                          Iniciar Conversa
                        </Button>
                      </Card>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </div>
        </section>

        {/* Framework EXTRACT Highlight */}
        <section className="w-full py-20 bg-background">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <Card className="p-8 md:p-12 rounded-2xl bg-gradient-to-br from-muted/50 to-muted/20 border-border/50">
                <div className="text-center space-y-6">
                  <div className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-background border border-border/50">
                    <TrendingUp className="h-4 w-4 text-accent" />
                    <span className="text-sm font-medium">Framework EXTRACT™ de 20 Pontos</span>
                  </div>

                  <h2 className="text-3xl md:text-4xl font-semibold">
                    A Diferença Entre IA Genérica
                    <br />
                    <span className="text-accent">e Clone Cognitivo Perfeito</span>
                  </h2>

                  <p className="text-lg text-muted-foreground leading-relaxed max-w-2xl mx-auto">
                    Cada especialista foi recriado com 20 camadas de personalidade, conhecimento e
                    estilo de pensamento. De terminologia específica até controvérsias que defendem.
                    O resultado? Fidelidade cognitiva de 19-20/20.
                  </p>

                  <div className="grid md:grid-cols-2 gap-4 pt-4">
                    <div className="text-left p-6 rounded-xl bg-background/50">
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <span className="text-destructive">✗</span> IA Genérica
                      </h4>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        Respostas superficiais sem profundidade. Ignora contexto histórico e nuances.
                        Não reflete estilo de pensamento único.
                      </p>
                    </div>
                    <div className="text-left p-6 rounded-xl bg-accent/5 border border-accent/10">
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <span className="text-accent">✓</span> Clone EXTRACT
                      </h4>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        Respostas profundas com casos reais. Usa terminologia autêntica do especialista.
                        Reflete décadas de expertise e posicionamento único.
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="w-full py-20 bg-muted/20">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center space-y-6">
              <h2 className="text-4xl md:text-5xl font-semibold">
                Pronto para Consultar as Lendas?
              </h2>
              <p className="text-lg text-muted-foreground">
                18 especialistas esperando para resolver seus desafios de marketing mais complexos.
                Gratuito. Ilimitado. Sem cartão de crédito.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
                <Button 
                  size="lg" 
                  className="gap-2"
                  onClick={() => setLocation("/experts")}
                  data-testid="button-final-cta"
                >
                  Ver Todos os 18 Especialistas
                  <ChevronRight className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </AnimatedPage>
  );
}
