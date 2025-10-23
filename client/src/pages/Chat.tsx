import { useState, useEffect } from "react";
import { useRoute, useLocation } from "wouter";
import { useQuery, useMutation } from "@tanstack/react-query";
import { queryClient, apiRequestJson } from "@/lib/queryClient";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Send, Sparkles, Loader2 } from "lucide-react";
import { ChatMessage } from "@/components/ChatMessage";
import type { Expert, Conversation, Message } from "@shared/schema";

export default function Chat() {
  const [, params] = useRoute("/chat/:id");
  const [, setLocation] = useLocation();
  const expertId = params?.id || "";
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [input, setInput] = useState("");

  const { data: expert, isLoading: expertLoading } = useQuery<Expert>({
    queryKey: ["/api/experts", expertId],
    enabled: !!expertId,
  });

  const { data: messages = [], isLoading: messagesLoading } = useQuery<Message[]>({
    queryKey: ["/api/conversations", conversationId, "messages"],
    enabled: !!conversationId,
  });

  const createConversationMutation = useMutation({
    mutationFn: async (data: { expertId: string; title: string }) => {
      return await apiRequestJson<Conversation>("/api/conversations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
    },
    onSuccess: (conversation) => {
      setConversationId(conversation.id);
    },
  });

  const sendMessageMutation = useMutation({
    mutationFn: async (data: { conversationId: string; content: string }) => {
      return await apiRequestJson<{ userMessage: Message; assistantMessage: Message }>(
        `/api/conversations/${data.conversationId}/messages`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: data.content }),
        }
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations", conversationId, "messages"] });
      setInput("");
    },
  });

  useEffect(() => {
    if (expert && !conversationId && !createConversationMutation.isPending) {
      createConversationMutation.mutate({
        expertId: expert.id,
        title: `Conversa com ${expert.name}`,
      });
    }
  }, [expert, conversationId]);

  const handleSend = () => {
    if (!input.trim() || !conversationId) return;
    sendMessageMutation.mutate({ conversationId, content: input });
  };

  const handleSuggestedQuestion = (question: string) => {
    setInput(question);
  };

  const suggestedQuestions = expert
    ? [
        `Como posso melhorar ${expert.expertise[0]?.toLowerCase() || "minha estratégia"}?`,
        `Quais são as melhores práticas em ${expert.expertise[1]?.toLowerCase() || "minha área"}?`,
        `Como resolver desafios de ${expert.expertise[2]?.toLowerCase() || "negócios"}?`,
      ]
    : [];

  if (expertLoading) {
    return (
      <div className="h-[calc(100vh-4rem)] flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!expert) {
    return (
      <div className="h-[calc(100vh-4rem)] flex items-center justify-center">
        <p className="text-muted-foreground">Especialista não encontrado</p>
      </div>
    );
  }

  const initials = expert.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      <div className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setLocation("/experts")}
              data-testid="button-back"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <Avatar className="h-12 w-12 ring-2 ring-primary/20">
              <AvatarImage src={expert.avatar || undefined} alt={expert.name} />
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <h2 className="text-lg font-semibold">{expert.name}</h2>
              <p className="text-sm text-muted-foreground">{expert.title}</p>
            </div>
            <div className="hidden md:flex gap-2">
              {expert.expertise.slice(0, 3).map((skill, index) => (
                <Badge key={index} variant="secondary" className="text-xs">
                  {skill}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messagesLoading ? (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : (
          <>
            <ChatMessage
              message={{
                id: "welcome",
                role: "assistant",
                content: `Olá! Sou ${expert.name}, ${expert.title}. Como posso ajudá-lo hoje com seus desafios estratégicos?`,
                timestamp: new Date(),
              }}
              expertName={expert.name}
              expertAvatar={expert.avatar || undefined}
            />
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={{
                  id: message.id,
                  role: message.role as "user" | "assistant",
                  content: message.content,
                  timestamp: message.createdAt,
                }}
                expertName={expert.name}
                expertAvatar={expert.avatar || undefined}
              />
            ))}
            {sendMessageMutation.isPending && (
              <div className="flex gap-3">
                <Avatar className="h-8 w-8 flex-shrink-0">
                  <AvatarImage src={expert.avatar || undefined} alt={expert.name} />
                  <AvatarFallback className="text-xs">{initials}</AvatarFallback>
                </Avatar>
                <div className="flex items-center gap-2 px-4 py-3 bg-card border rounded-xl">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm text-muted-foreground">Pensando...</span>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {suggestedQuestions.length > 0 && messages.length === 0 && !sendMessageMutation.isPending && (
        <div className="px-6 pb-4">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium text-muted-foreground">Perguntas Sugeridas</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question, index) => (
              <Badge
                key={index}
                variant="outline"
                className="cursor-pointer hover-elevate active-elevate-2 py-2 px-3"
                onClick={() => handleSuggestedQuestion(question)}
                data-testid={`badge-suggestion-${index}`}
              >
                {question}
              </Badge>
            ))}
          </div>
        </div>
      )}

      <div className="border-t bg-card p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !sendMessageMutation.isPending && handleSend()}
            placeholder="Digite sua pergunta estratégica..."
            className="flex-1"
            disabled={sendMessageMutation.isPending}
            data-testid="input-chat-message"
          />
          <Button 
            onClick={handleSend} 
            size="icon" 
            disabled={sendMessageMutation.isPending || !input.trim()}
            data-testid="button-send-message"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
