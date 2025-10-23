import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { Building2, Target, TrendingUp, CheckCircle2 } from "lucide-react";
import { insertBusinessProfileSchema, type InsertBusinessProfile } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Progress } from "@/components/ui/progress";

const STEPS = [
  { id: 1, title: "Informações da Empresa", icon: Building2 },
  { id: 2, title: "Contexto de Marketing", icon: TrendingUp },
  { id: 3, title: "Objetivos e Desafios", icon: Target },
];

const CHANNEL_OPTIONS = [
  { id: "online", label: "E-commerce / Online" },
  { id: "retail", label: "Varejo Físico" },
  { id: "b2b", label: "B2B / Vendas Corporativas" },
  { id: "marketplace", label: "Marketplace" },
  { id: "social", label: "Redes Sociais" },
  { id: "direct", label: "Vendas Diretas" },
];

export default function Onboarding() {
  const [step, setStep] = useState(1);
  const [, navigate] = useLocation();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const form = useForm<InsertBusinessProfile>({
    resolver: zodResolver(insertBusinessProfileSchema),
    defaultValues: {
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
    },
  });

  const saveMutation = useMutation({
    mutationFn: async (data: InsertBusinessProfile) => {
      return await apiRequest("/api/profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/profile"] });
      toast({
        title: "Perfil criado com sucesso!",
        description: "Seu perfil foi salvo. O Conselho de Clones estará disponível em breve!",
      });
      navigate("/experts");
    },
    onError: (error: Error) => {
      toast({
        title: "Erro ao salvar perfil",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const onSubmit = async (data: InsertBusinessProfile) => {
    await saveMutation.mutateAsync(data);
  };

  const handleNext = async () => {
    const fieldsToValidate = getStepFields(step);
    const isValid = await form.trigger(fieldsToValidate);
    
    if (isValid) {
      if (step < 3) {
        setStep(step + 1);
      } else {
        form.handleSubmit(onSubmit)();
      }
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const getStepFields = (currentStep: number): (keyof InsertBusinessProfile)[] => {
    switch (currentStep) {
      case 1:
        return ["companyName", "industry", "companySize"];
      case 2:
        return ["targetAudience", "mainProducts", "channels", "budgetRange"];
      case 3:
        return ["primaryGoal", "mainChallenge", "timeline"];
      default:
        return [];
    }
  };

  const progress = (step / STEPS.length) * 100;

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <div>
              <CardTitle className="text-2xl">Bem-vindo ao AdvisorIA</CardTitle>
              <CardDescription className="mt-2">
                Configure seu perfil para receber análises personalizadas do nosso Conselho de Clones
              </CardDescription>
            </div>
          </div>
          
          <div className="space-y-4 mt-6">
            <Progress value={progress} className="h-2" data-testid="progress-onboarding" />
            <div className="flex justify-between">
              {STEPS.map((s) => {
                const Icon = s.icon;
                const isActive = step === s.id;
                const isCompleted = step > s.id;
                
                return (
                  <div key={s.id} className="flex items-center gap-2">
                    <div
                      className={`flex items-center justify-center w-8 h-8 rounded-full ${
                        isCompleted
                          ? "bg-primary text-primary-foreground"
                          : isActive
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5" />
                      ) : (
                        <Icon className="w-4 h-4" />
                      )}
                    </div>
                    <span className={`text-sm hidden md:inline ${isActive ? "font-semibold" : ""}`}>
                      {s.title}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              {step === 1 && (
                <div className="space-y-4">
                  <FormField
                    control={form.control}
                    name="companyName"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Nome da Empresa</FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="Ex: Minha Empresa Ltda" 
                            {...field} 
                            data-testid="input-company-name"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="industry"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Setor / Indústria</FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="Ex: E-commerce de moda, SaaS, Consultoria..." 
                            {...field} 
                            data-testid="input-industry"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="companySize"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Tamanho da Empresa</FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger data-testid="select-company-size">
                              <SelectValue placeholder="Selecione..." />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="1-10">1-10 funcionários</SelectItem>
                            <SelectItem value="11-50">11-50 funcionários</SelectItem>
                            <SelectItem value="51-200">51-200 funcionários</SelectItem>
                            <SelectItem value="201-1000">201-1000 funcionários</SelectItem>
                            <SelectItem value="1000+">Mais de 1000 funcionários</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              )}

              {step === 2 && (
                <div className="space-y-4">
                  <FormField
                    control={form.control}
                    name="targetAudience"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Público-Alvo Principal</FormLabel>
                        <FormControl>
                          <Textarea 
                            placeholder="Ex: Mulheres 25-35 anos, classe A/B, interessadas em moda sustentável..." 
                            {...field} 
                            data-testid="textarea-target-audience"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="mainProducts"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Principais Produtos / Serviços</FormLabel>
                        <FormControl>
                          <Textarea 
                            placeholder="Ex: Roupas femininas, acessórios de moda, consultoria de estilo..." 
                            {...field} 
                            data-testid="textarea-main-products"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="channels"
                    render={() => (
                      <FormItem>
                        <FormLabel>Canais de Venda (selecione todos aplicáveis)</FormLabel>
                        <div className="grid grid-cols-2 gap-3 mt-2">
                          {CHANNEL_OPTIONS.map((option) => (
                            <FormField
                              key={option.id}
                              control={form.control}
                              name="channels"
                              render={({ field }) => {
                                return (
                                  <FormItem className="flex items-center space-x-2 space-y-0">
                                    <FormControl>
                                      <Checkbox
                                        checked={field.value?.includes(option.id)}
                                        onCheckedChange={(checked) => {
                                          return checked
                                            ? field.onChange([...field.value, option.id])
                                            : field.onChange(
                                                field.value?.filter((value) => value !== option.id)
                                              );
                                        }}
                                        data-testid={`checkbox-channel-${option.id}`}
                                      />
                                    </FormControl>
                                    <FormLabel className="font-normal cursor-pointer">
                                      {option.label}
                                    </FormLabel>
                                  </FormItem>
                                );
                              }}
                            />
                          ))}
                        </div>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="budgetRange"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Orçamento de Marketing (mensal)</FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger data-testid="select-budget-range">
                              <SelectValue placeholder="Selecione..." />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="< $10k/month">Menos de R$ 10k/mês</SelectItem>
                            <SelectItem value="$10k-$50k/month">R$ 10k - R$ 50k/mês</SelectItem>
                            <SelectItem value="$50k-$100k/month">R$ 50k - R$ 100k/mês</SelectItem>
                            <SelectItem value="> $100k/month">Mais de R$ 100k/mês</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              )}

              {step === 3 && (
                <div className="space-y-4">
                  <FormField
                    control={form.control}
                    name="primaryGoal"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Objetivo Principal</FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger data-testid="select-primary-goal">
                              <SelectValue placeholder="Selecione..." />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="growth">Crescimento / Aquisição</SelectItem>
                            <SelectItem value="positioning">Posicionamento de Marca</SelectItem>
                            <SelectItem value="retention">Retenção de Clientes</SelectItem>
                            <SelectItem value="launch">Lançamento de Produto</SelectItem>
                            <SelectItem value="awareness">Awareness / Reconhecimento</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="mainChallenge"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Maior Desafio Atual</FormLabel>
                        <FormControl>
                          <Textarea 
                            placeholder="Ex: Alto CAC, baixa conversão, competição agressiva, falta de diferenciação..." 
                            {...field} 
                            data-testid="textarea-main-challenge"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="timeline"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Prazo para Resultados</FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger data-testid="select-timeline">
                              <SelectValue placeholder="Selecione..." />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="immediate">Imediato (0-3 meses)</SelectItem>
                            <SelectItem value="3-6 months">Curto prazo (3-6 meses)</SelectItem>
                            <SelectItem value="6-12 months">Médio prazo (6-12 meses)</SelectItem>
                            <SelectItem value="long-term">Longo prazo (12+ meses)</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              )}

              <div className="flex justify-between pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleBack}
                  disabled={step === 1}
                  data-testid="button-back"
                >
                  Voltar
                </Button>
                <Button
                  type="button"
                  onClick={handleNext}
                  disabled={saveMutation.isPending}
                  data-testid="button-next"
                >
                  {step === 3 ? (saveMutation.isPending ? "Salvando..." : "Finalizar") : "Próximo"}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
