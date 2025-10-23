import { ThemeProvider } from "../ThemeProvider";
import { CreateExpertForm } from "../CreateExpertForm";

export default function CreateExpertFormExample() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold mb-8">Criar Novo Especialista</h2>
          <CreateExpertForm />
        </div>
      </div>
    </ThemeProvider>
  );
}
