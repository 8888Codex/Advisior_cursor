import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { apiRequestJson } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Sparkles, X, Plus, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import type { Expert } from "@shared/schema";

export default function Create() {
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  const [name, setName] = useState("");
  const [title, setTitle] = useState("");
  const [bio, setBio] = useState("");
  const [expertiseInput, setExpertiseInput] = useState("");
  const [expertise, setExpertise] = useState<string[]>([]);

  const createExpertMutation = useMutation({
    mutationFn: async (data: {
      name: string;
      title: string;
      bio: string;
      expertise: string[];
    }) => {
      const systemPrompt = `Você é ${data.name}, ${data.title}.

${data.bio}

Suas áreas de expertise incluem: ${data.expertise.join(", ")}.

Forneça consultoria estratégica profunda e insights acionáveis. Mantenha um tom profissional e consultivo.`;

      return await apiRequestJson<Expert>("/api/experts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...data,
          systemPrompt,
          avatar: null,
        }),
      });
    },
    onSuccess: (expert) => {
      toast({
        title: "Especialista criado!",
        description: `${expert.name} foi criado com sucesso.`,
      });
      setLocation(`/chat/${expert.id}`);
    },
    onError: () => {
      toast({
        title: "Erro ao criar especialista",
        description: "Tente novamente mais tarde.",
        variant: "destructive",
      });
    },
  });

  const addExpertise = () => {
    if (expertiseInput.trim() && !expertise.includes(expertiseInput.trim())) {
      setExpertise([...expertise, expertiseInput.trim()]);
      setExpertiseInput("");
    }
  };

  const removeExpertise = (item: string) => {
    setExpertise(expertise.filter((e) => e !== item));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (expertise.length === 0) {
      toast({
        title: "Expertise necessária",
        description: "Adicione pelo menos uma área de expertise.",
        variant: "destructive",
      });
      return;
    }
    createExpertMutation.mutate({ name, title, bio, expertise });
  };

  const initials = name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "??";

  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <div className="inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm mb-4">
              <Sparkles className="h-4 w-4 text-primary" />
              <span className="text-muted-foreground">Personalização Total</span>
            </div>
            <h1 className="text-4xl font-bold mb-4">Criar Seu Especialista</h1>
            <p className="text-muted-foreground max-w-2xl">
              Defina as características, expertise e personalidade do seu consultor de IA personalizado.
              Quanto mais detalhes você fornecer, mais preciso e útil será o especialista.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="name">Nome do Especialista</Label>
                  <Input
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Ex: Dr. Carlos Silva"
                    required
                    data-testid="input-expert-name"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="title">Título Profissional</Label>
                  <Input
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Ex: Especialista em Transformação Digital"
                    required
                    data-testid="input-expert-title"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bio">Biografia / Contexto</Label>
                  <Textarea
                    id="bio"
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    placeholder="Descreva o background, experiência e estilo de consultoria deste especialista..."
                    rows={5}
                    required
                    data-testid="input-expert-bio"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="expertise">Áreas de Expertise</Label>
                  <div className="flex gap-2">
                    <Input
                      id="expertise"
                      value={expertiseInput}
                      onChange={(e) => setExpertiseInput(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addExpertise())}
                      placeholder="Ex: Estratégia, Inovação, Marketing"
                      data-testid="input-expertise"
                    />
                    <Button type="button" onClick={addExpertise} size="icon" data-testid="button-add-expertise">
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                  {expertise.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3">
                      {expertise.map((item, index) => (
                        <Badge key={index} variant="secondary" className="gap-1 py-1.5" data-testid={`badge-expertise-${index}`}>
                          {item}
                          <button
                            type="button"
                            onClick={() => removeExpertise(item)}
                            className="hover-elevate rounded-full p-0.5"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>

                <Button 
                  type="submit" 
                  className="w-full gap-2" 
                  size="lg" 
                  disabled={createExpertMutation.isPending}
                  data-testid="button-create-expert"
                >
                  {createExpertMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Criando...
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-4 w-4" />
                      Criar Especialista
                    </>
                  )}
                </Button>
              </form>
            </div>

            <div>
              <div className="sticky top-24">
                <h3 className="text-lg font-semibold mb-4">Preview do Especialista</h3>
                <Card className="p-6 space-y-4">
                  <div className="flex items-start gap-4">
                    <Avatar className="h-20 w-20 ring-2 ring-primary/20">
                      <AvatarFallback className="text-lg font-semibold">{initials}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-xl font-semibold">
                        {name || "Nome do Especialista"}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        {title || "Título Profissional"}
                      </p>
                    </div>
                  </div>

                  {expertise.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {expertise.map((skill, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  )}

                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {bio || "A biografia do especialista aparecerá aqui..."}
                  </p>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
