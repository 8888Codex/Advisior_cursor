import { ThemeProvider } from "../ThemeProvider";
import { ChatInterface } from "../ChatInterface";
import strategistAvatar from "@assets/generated_images/Business_strategist_expert_avatar_ef5e30a4.png";

export default function ChatInterfaceExample() {
  const expert = {
    id: "1",
    name: "Dr. Michael Thompson",
    title: "Estrategista de Negócios Sênior",
    expertise: ["Estratégia Corporativa", "M&A", "Transformação"],
    bio: "Especialista em transformações organizacionais",
    avatar: strategistAvatar,
    category: "marketing" as const,
  };

  const suggestions = [
    "Como estruturar uma estratégia de expansão internacional?",
    "Quais métricas devo acompanhar para M&A?",
    "Como liderar uma transformação digital?",
  ];

  return (
    <ThemeProvider>
      <div className="h-screen bg-background flex items-center justify-center p-4">
        <div className="w-full max-w-4xl h-[600px] border rounded-xl overflow-hidden bg-card">
          <ChatInterface expert={expert} suggestedQuestions={suggestions} />
        </div>
      </div>
    </ThemeProvider>
  );
}
