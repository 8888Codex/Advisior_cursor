import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { type Expert } from "@/components/ExpertCard";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Loader2, Upload } from "lucide-react";
import { AvatarUploadModal } from "@/components/AvatarUploadModal";

export default function AdminExperts() {
  const [selectedExpert, setSelectedExpert] = useState<Expert | null>(null);

  const { data: experts = [], isLoading } = useQuery<Expert[]>({
    queryKey: ["/api/experts"],
  });

  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4">Gerenciar Experts</h1>
            <p className="text-muted-foreground">
              Atualize os avatares dos especialistas
            </p>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {experts.map((expert) => (
                <Card key={expert.id} data-testid={`card-expert-${expert.id}`}>
                  <CardHeader>
                    <div className="flex items-center gap-4">
                      <Avatar className="h-16 w-16 ring-2 ring-primary/20">
                        <AvatarImage src={expert.avatar} alt={expert.name} />
                        <AvatarFallback className="text-lg">
                          {expert.name.split(" ").map((n) => n[0]).join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <CardTitle className="text-lg">{expert.name}</CardTitle>
                        <CardDescription className="text-sm">
                          {expert.title}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <Button
                      onClick={() => setSelectedExpert(expert)}
                      variant="outline"
                      className="w-full"
                      data-testid={`button-edit-avatar-${expert.id}`}
                    >
                      <Upload className="h-4 w-4 mr-2" />
                      Editar Avatar
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {selectedExpert && (
        <AvatarUploadModal
          expert={selectedExpert}
          onClose={() => setSelectedExpert(null)}
        />
      )}
    </div>
  );
}
