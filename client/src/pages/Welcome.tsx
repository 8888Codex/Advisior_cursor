import { useState } from "react";
import { useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronRight,
  ChevronLeft,
  Sparkles,
  Building2,
  Target,
  TrendingUp,
  Users,
  Package,
  DollarSign,
  Calendar,
  AlertCircle,
  MessageSquare,
  Zap,
  Award,
  Check,
  X,
} from "lucide-react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { apiRequestJson, queryClient } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

type WelcomeStep = "hero" | "tour" | "profile";

interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  avatar?: string;
}

interface ProfileFormData {
  companyName: string;
  industry: string;
  companySize: string;
  targetAudience: string;
  mainProducts: string;
  channels: string[];
  budgetRange: string;
  primaryGoal: string;
  mainChallenge: string;
  timeline: string;
}

export default function Welcome() {
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  const [step, setStep] = useState<WelcomeStep>("hero");
  const [tourIndex, setTourIndex] = useState(0);
  const [profileData, setProfileData] = useState<ProfileFormData>({
    companyName: "",
    industry: "",
    companySize: "",
    targetAudience: "",
    mainProducts: "",
    channels: [],
    budgetRange: "",
    primaryGoal: "",
    mainChallenge: "",
    timeline: "",
  });

  // Fetch experts for the tour
  const { data: experts = [], isLoading: expertsLoading } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  // Show ALL high-fidelity experts (18 marketing legends)
  const legends = experts.filter((e) => e.expertise && e.expertise.length > 0);

  const saveProfileMutation = useMutation({
    mutationFn: async (data: ProfileFormData) => {
      return await apiRequestJson("/api/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/profile"] });
      localStorage.setItem("onboarding_complete", "true");
      toast({
        title: "Perfil Salvo",
        description: "Bem-vindo ao AdvisorIA! Sua consultoria personalizada aguarda.",
      });
      setLocation("/");
    },
    onError: () => {
      toast({
        title: "Erro ao salvar perfil",
        description: "Tente novamente.",
        variant: "destructive",
      });
    },
  });

  const handleStartTour = () => {
    // Always start tour when button is clicked (loading/empty states handled inside tour)
    setStep("tour");
  };

  const handleNextExpert = () => {
    if (tourIndex < legends.length - 1) {
      setTourIndex(tourIndex + 1);
    } else {
      setStep("profile");
    }
  };

  const handlePreviousExpert = () => {
    if (tourIndex > 0) {
      setTourIndex(tourIndex - 1);
    }
  };

  const handleSkipToProfile = () => {
    setStep("profile");
  };

  const handleProfileSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    saveProfileMutation.mutate(profileData);
  };

  const updateProfileField = (field: keyof ProfileFormData, value: any) => {
    setProfileData((prev) => ({ ...prev, [field]: value }));
  };

  const toggleChannel = (channel: string) => {
    setProfileData((prev) => ({
      ...prev,
      channels: prev.channels.includes(channel)
        ? prev.channels.filter((c) => c !== channel)
        : [...prev.channels, channel],
    }));
  };

  const currentExpert = legends[tourIndex];
  const expertInitials = currentExpert
    ? currentExpert.name
        .split(" ")
        .map((n: string) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : "";

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-background to-muted/20">
      <AnimatePresence mode="wait">
        {step === "hero" && (
          <motion.div
            key="hero"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="max-w-3xl w-full text-center space-y-8"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.3 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-muted border border-border/50"
            >
              <Sparkles className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium text-muted-foreground">
                Framework EXTRACT™ • Fidelidade Cognitiva 19/20
              </span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="space-y-6"
            >
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight leading-tight">
                Consulte Philip Kotler,
                <br />
                Seth Godin e Mais <span className="text-accent">16 Lendas</span>
                <br />
                do Marketing. A Qualquer Hora.
              </h1>
              <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                450+ anos de expertise combinada. Respostas tão precisas que você esquece 
                que está falando com IA. Em português, instantaneamente.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.5 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Button
                size="lg"
                onClick={handleStartTour}
                disabled={expertsLoading}
                className="gap-2 text-lg px-8 py-6"
                data-testid="button-start-tour"
              >
                {expertsLoading ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <Sparkles className="h-5 w-5" />
                    </motion.div>
                    Carregando Especialistas...
                  </>
                ) : (
                  <>
                    Explorar os 18 Especialistas
                    <ChevronRight className="h-5 w-5" />
                  </>
                )}
              </Button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8, duration: 0.5 }}
              className="flex items-center justify-center gap-4 text-sm text-muted-foreground"
            >
              <span>18 Especialistas</span>
              <span className="text-border">•</span>
              <span>15 Disciplinas</span>
              <span className="text-border">•</span>
              <span>Respostas em 30 segundos</span>
            </motion.div>

            {/* Como Funciona Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1, duration: 0.5 }}
              className="w-full max-w-5xl mt-24 space-y-12"
            >
              <div className="text-center space-y-4">
                <h2 className="text-3xl md:text-4xl font-semibold">
                  Como Funciona a Clonagem Cognitiva?
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  3 passos simples separam você das maiores mentes do marketing mundial
                </p>
              </div>

              {/* 3 Steps */}
              <div className="grid md:grid-cols-3 gap-8">
                {[
                  {
                    step: "1",
                    icon: Users,
                    title: "Escolha Sua Lenda",
                    description: "Navegue por 18 especialistas. De Philip Kotler a Gary Vaynerchuk."
                  },
                  {
                    step: "2",
                    icon: MessageSquare,
                    title: "Faça Sua Pergunta",
                    description: "Descreva seu desafio real. Em português, naturalmente."
                  },
                  {
                    step: "3",
                    icon: Zap,
                    title: "Receba Insight Perfeito",
                    description: "Resposta em 30s com fidelidade cognitiva 19-20/20."
                  }
                ].map((item, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.1 + index * 0.1, duration: 0.3 }}
                    className="text-center space-y-4"
                  >
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted">
                      <item.icon className="h-8 w-8 text-muted-foreground" />
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-accent">Passo {item.step}</div>
                      <h3 className="text-xl font-semibold">{item.title}</h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {item.description}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* IA Genérica vs Clone Perfeito */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.4, duration: 0.5 }}
                className="grid md:grid-cols-2 gap-6 mt-16"
              >
                {/* IA Genérica */}
                <Card className="p-6 rounded-2xl bg-background border-border">
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center justify-center w-10 h-10 rounded-full bg-destructive/10">
                        <X className="h-5 w-5 text-destructive" />
                      </div>
                      <h4 className="text-lg font-semibold">IA Genérica</h4>
                    </div>
                    <ul className="space-y-3 text-sm text-muted-foreground">
                      <li className="flex gap-2">
                        <span className="text-destructive flex-shrink-0">×</span>
                        <span>Respostas superficiais e genéricas</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="text-destructive flex-shrink-0">×</span>
                        <span>Ignora contexto histórico e nuances</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="text-destructive flex-shrink-0">×</span>
                        <span>Não reflete estilo de pensamento único</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="text-destructive flex-shrink-0">×</span>
                        <span>Sem terminologia autêntica do especialista</span>
                      </li>
                    </ul>
                  </div>
                </Card>

                {/* Clone Perfeito */}
                <Card className="p-6 rounded-2xl bg-accent/5 border-accent/20">
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center justify-center w-10 h-10 rounded-full bg-accent/20">
                        <Check className="h-5 w-5 text-accent" />
                      </div>
                      <h4 className="text-lg font-semibold">Clone Cognitivo EXTRACT</h4>
                    </div>
                    <ul className="space-y-3 text-sm text-muted-foreground">
                      <li className="flex gap-2">
                        <span className="text-accent flex-shrink-0">✓</span>
                        <span>20 camadas de personalidade e expertise</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="text-accent flex-shrink-0">✓</span>
                        <span>Cita casos reais e controvérsias históricas</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="text-accent flex-shrink-0">✓</span>
                        <span>Usa padrões de raciocínio autênticos</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="text-accent flex-shrink-0">✓</span>
                        <span>Fidelidade cognitiva validada 19-20/20</span>
                      </li>
                    </ul>
                  </div>
                </Card>
              </motion.div>

              {/* Framework EXTRACT Badge */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.6, duration: 0.5 }}
                className="text-center pt-8"
              >
                <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-muted border border-border/50">
                  <Award className="h-5 w-5 text-accent" />
                  <span className="text-sm font-medium">
                    Desenvolvido com Framework EXTRACT™ de 20 Pontos
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mt-4 max-w-2xl mx-auto">
                  Cada especialista inclui: Identidade Central, Terminologia, Padrões de Raciocínio,
                  Estilo de Comunicação, Contextos de Expertise, Técnicas & Métodos, Limitações,
                  Meta-Consciência, Citações Famosas, Casos Reais, Posições Controversas, Contexto Temporal
                </p>
              </motion.div>
            </motion.div>
          </motion.div>
        )}

        {step === "tour" && (
          <motion.div
            key={`tour-${tourIndex}`}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.4 }}
            className="max-w-4xl w-full"
          >
            {/* Loading state */}
            {expertsLoading && (
              <Card className="p-8 space-y-6">
                <div className="flex flex-col items-center justify-center py-12 space-y-4">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  >
                    <Sparkles className="h-12 w-12 text-accent" />
                  </motion.div>
                  <p className="text-lg text-muted-foreground">
                    Preparando os especialistas...
                  </p>
                </div>
              </Card>
            )}

            {/* Empty state */}
            {!expertsLoading && legends.length === 0 && (
              <Card className="p-8 space-y-6">
                <div className="flex flex-col items-center justify-center py-12 space-y-4">
                  <AlertCircle className="h-12 w-12 text-muted-foreground" />
                  <p className="text-lg text-muted-foreground">
                    Nenhum especialista disponível no momento
                  </p>
                  <Button onClick={handleSkipToProfile} variant="outline">
                    Pular para Perfil
                  </Button>
                </div>
              </Card>
            )}

            {/* Expert showcase */}
            {!expertsLoading && currentExpert && (
              <Card className="p-8 space-y-6">
                {/* Progress indicator */}
                <div className="flex items-center gap-2 mb-6">
                {legends.map((_, idx) => (
                  <div
                    key={idx}
                    className={`h-1.5 flex-1 rounded-full transition-colors ${
                      idx <= tourIndex ? "bg-accent" : "bg-muted"
                    }`}
                  />
                ))}
                </div>

                {/* Expert content */}
                <div className="flex flex-col md:flex-row gap-8 items-start">
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.1, duration: 0.4 }}
                  className="flex-shrink-0"
                >
                  <Avatar className="h-32 w-32 border-4 border-accent/20">
                    <AvatarImage src={currentExpert.avatar} alt={currentExpert.name} />
                    <AvatarFallback className="text-3xl font-semibold bg-accent/10">
                      {expertInitials}
                    </AvatarFallback>
                  </Avatar>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2, duration: 0.4 }}
                  className="flex-1 space-y-4"
                >
                  <div>
                    <h2 className="text-3xl font-semibold mb-2">
                      {currentExpert.name}
                    </h2>
                    <p className="text-lg text-muted-foreground mb-4">
                      {currentExpert.title}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {currentExpert.expertise.slice(0, 4).map((skill: string, idx: number) => (
                        <Badge key={idx} variant="secondary">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {currentExpert.bio}
                  </p>
                </motion.div>
                </div>

                {/* Navigation */}
                <div className="flex items-center justify-between pt-6 border-t">
                <Button
                  variant="ghost"
                  onClick={handlePreviousExpert}
                  disabled={tourIndex === 0}
                  className="gap-2"
                  data-testid="button-previous-expert"
                >
                  <ChevronLeft className="h-4 w-4" />
                  Anterior
                </Button>

                <Button
                  variant="outline"
                  onClick={handleSkipToProfile}
                  data-testid="button-skip-tour"
                >
                  Pular Tour
                </Button>

                <Button
                  onClick={handleNextExpert}
                  className="gap-2"
                  data-testid="button-next-expert"
                >
                  {tourIndex < legends.length - 1 ? "Próximo" : "Começar"}
                  <ChevronRight className="h-4 w-4" />
                </Button>
                </div>
              </Card>
            )}
          </motion.div>
        )}

        {step === "profile" && (
          <motion.div
            key="profile"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
            className="max-w-3xl w-full"
          >
            <Card className="p-8">
              <form onSubmit={handleProfileSubmit} className="space-y-6">
                <div className="text-center space-y-3 mb-8">
                  <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
                    Últimas Perguntas para Personalizar
                    <br />
                    <span className="text-accent">Sua Consultoria Exclusiva</span>
                  </h2>
                  <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                    Quanto mais soubermos, melhores serão as recomendações. 
                    Cada especialista ajustará suas respostas ao seu contexto real.
                  </p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {/* Company Name */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="companyName" className="flex items-center gap-2">
                      <Building2 className="h-4 w-4 text-muted-foreground" />
                      Nome da Empresa
                    </Label>
                    <Input
                      id="companyName"
                      value={profileData.companyName}
                      onChange={(e) =>
                        updateProfileField("companyName", e.target.value)
                      }
                      placeholder="Ex: Tech Innovators Inc."
                      required
                      data-testid="input-company-name"
                    />
                  </div>

                  {/* Industry */}
                  <div className="space-y-2">
                    <Label htmlFor="industry">Indústria</Label>
                    <Input
                      id="industry"
                      value={profileData.industry}
                      onChange={(e) =>
                        updateProfileField("industry", e.target.value)
                      }
                      placeholder="Ex: SaaS, E-commerce, Consultoria"
                      required
                      data-testid="input-industry"
                    />
                  </div>

                  {/* Company Size */}
                  <div className="space-y-2">
                    <Label htmlFor="companySize">Tamanho da Empresa</Label>
                    <Select
                      value={profileData.companySize}
                      onValueChange={(value) =>
                        updateProfileField("companySize", value)
                      }
                      required
                    >
                      <SelectTrigger id="companySize" data-testid="select-company-size">
                        <SelectValue placeholder="Selecione" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1-10">1-10 funcionários</SelectItem>
                        <SelectItem value="11-50">11-50 funcionários</SelectItem>
                        <SelectItem value="51-200">51-200 funcionários</SelectItem>
                        <SelectItem value="201-1000">201-1000 funcionários</SelectItem>
                        <SelectItem value="1000+">1000+ funcionários</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Target Audience */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="targetAudience" className="flex items-center gap-2">
                      <Users className="h-4 w-4 text-muted-foreground" />
                      Público-Alvo
                    </Label>
                    <Input
                      id="targetAudience"
                      value={profileData.targetAudience}
                      onChange={(e) =>
                        updateProfileField("targetAudience", e.target.value)
                      }
                      placeholder="Ex: C-level executivos de empresas B2B"
                      required
                      data-testid="input-target-audience"
                    />
                  </div>

                  {/* Main Products */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="mainProducts" className="flex items-center gap-2">
                      <Package className="h-4 w-4 text-muted-foreground" />
                      Principais Produtos/Serviços
                    </Label>
                    <Textarea
                      id="mainProducts"
                      value={profileData.mainProducts}
                      onChange={(e) =>
                        updateProfileField("mainProducts", e.target.value)
                      }
                      placeholder="Descreva brevemente seus produtos ou serviços principais"
                      rows={3}
                      required
                      data-testid="input-main-products"
                    />
                  </div>

                  {/* Channels */}
                  <div className="md:col-span-2 space-y-2">
                    <Label>Canais de Venda</Label>
                    <div className="flex flex-wrap gap-2">
                      {["online", "retail", "b2b", "marketplace"].map((channel) => (
                        <Badge
                          key={channel}
                          variant={
                            profileData.channels.includes(channel)
                              ? "default"
                              : "outline"
                          }
                          className="cursor-pointer hover-elevate"
                          onClick={() => toggleChannel(channel)}
                          data-testid={`badge-channel-${channel}`}
                        >
                          {channel === "online" && "Online"}
                          {channel === "retail" && "Varejo Físico"}
                          {channel === "b2b" && "B2B Direto"}
                          {channel === "marketplace" && "Marketplace"}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Budget Range */}
                  <div className="space-y-2">
                    <Label htmlFor="budgetRange" className="flex items-center gap-2">
                      <DollarSign className="h-4 w-4 text-muted-foreground" />
                      Orçamento de Marketing (mensal)
                    </Label>
                    <Select
                      value={profileData.budgetRange}
                      onValueChange={(value) =>
                        updateProfileField("budgetRange", value)
                      }
                      required
                    >
                      <SelectTrigger id="budgetRange" data-testid="select-budget-range">
                        <SelectValue placeholder="Selecione" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="< $10k/month">Menos de $10k</SelectItem>
                        <SelectItem value="$10k-$50k/month">$10k - $50k</SelectItem>
                        <SelectItem value="$50k-$100k/month">$50k - $100k</SelectItem>
                        <SelectItem value="> $100k/month">Mais de $100k</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Primary Goal */}
                  <div className="space-y-2">
                    <Label htmlFor="primaryGoal" className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-muted-foreground" />
                      Objetivo Principal
                    </Label>
                    <Select
                      value={profileData.primaryGoal}
                      onValueChange={(value) =>
                        updateProfileField("primaryGoal", value)
                      }
                      required
                    >
                      <SelectTrigger id="primaryGoal" data-testid="select-primary-goal">
                        <SelectValue placeholder="Selecione" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="growth">Crescimento</SelectItem>
                        <SelectItem value="positioning">Posicionamento</SelectItem>
                        <SelectItem value="retention">Retenção</SelectItem>
                        <SelectItem value="launch">Lançamento</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Main Challenge */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="mainChallenge" className="flex items-center gap-2">
                      <AlertCircle className="h-4 w-4 text-muted-foreground" />
                      Principal Desafio de Marketing
                    </Label>
                    <Textarea
                      id="mainChallenge"
                      value={profileData.mainChallenge}
                      onChange={(e) =>
                        updateProfileField("mainChallenge", e.target.value)
                      }
                      placeholder="Qual é o maior desafio que você enfrenta atualmente?"
                      rows={3}
                      required
                      data-testid="input-main-challenge"
                    />
                  </div>

                  {/* Timeline */}
                  <div className="md:col-span-2 space-y-2">
                    <Label htmlFor="timeline" className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      Prazo para Resultados
                    </Label>
                    <Select
                      value={profileData.timeline}
                      onValueChange={(value) =>
                        updateProfileField("timeline", value)
                      }
                      required
                    >
                      <SelectTrigger id="timeline" data-testid="select-timeline">
                        <SelectValue placeholder="Selecione" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="immediate">Imediato (este mês)</SelectItem>
                        <SelectItem value="3-6 months">3-6 meses</SelectItem>
                        <SelectItem value="6-12 months">6-12 meses</SelectItem>
                        <SelectItem value="long-term">Longo prazo (1+ ano)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="pt-6 space-y-4">
                  <Button
                    type="submit"
                    size="lg"
                    className="w-full gap-2"
                    disabled={saveProfileMutation.isPending || profileData.channels.length === 0}
                    data-testid="button-save-profile"
                  >
                    {saveProfileMutation.isPending ? (
                      <>
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        >
                          <TrendingUp className="h-5 w-5" />
                        </motion.div>
                        Salvando...
                      </>
                    ) : (
                      <>
                        Começar Minha Consultoria Gratuita
                        <ChevronRight className="h-5 w-5" />
                      </>
                    )}
                  </Button>
                  <p className="text-center text-sm text-muted-foreground">
                    Sem cartão de crédito necessário • Perguntas ilimitadas • Cancele quando quiser
                  </p>
                </div>
              </form>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
