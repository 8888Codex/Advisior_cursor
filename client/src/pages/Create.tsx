import { CreateExpertForm } from "@/components/CreateExpertForm";
import { Sparkles } from "lucide-react";

export default function Create() {
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

          <CreateExpertForm />
        </div>
      </div>
    </div>
  );
}
