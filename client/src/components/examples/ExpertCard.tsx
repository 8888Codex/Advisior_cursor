import { ThemeProvider } from "../ThemeProvider";
import { ExpertCard } from "../ExpertCard";
import strategistAvatar from "@assets/generated_images/Business_strategist_expert_avatar_ef5e30a4.png";

export default function ExpertCardExample() {
  const expert = {
    id: "1",
    name: "Dr. Michael Thompson",
    title: "Estrategista de Negócios Sênior",
    expertise: ["Estratégia Corporativa", "M&A", "Transformação"],
    bio: "Com 25 anos de experiência em consultoria estratégica para Fortune 500, Dr. Thompson especializou-se em transformações organizacionais e fusões & aquisições complexas.",
    avatar: strategistAvatar,
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-md mx-auto">
          <ExpertCard expert={expert} onConsult={(e) => console.log("Consulting:", e.name)} />
        </div>
      </div>
    </ThemeProvider>
  );
}
