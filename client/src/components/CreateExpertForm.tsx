import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Sparkles, X, Plus } from "lucide-react";

export function CreateExpertForm() {
  const [name, setName] = useState("");
  const [title, setTitle] = useState("");
  const [bio, setBio] = useState("");
  const [expertiseInput, setExpertiseInput] = useState("");
  const [expertise, setExpertise] = useState<string[]>([]);

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
    console.log("Creating expert:", { name, title, bio, expertise });
  };

  const initials = name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "??";

  return (
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

          <Button type="submit" className="w-full gap-2" size="lg" data-testid="button-create-expert">
            <Sparkles className="h-4 w-4" />
            Criar Especialista
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
  );
}
