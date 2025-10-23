import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Sparkles } from "lucide-react";
import { ChatMessage, type Message } from "./ChatMessage";
import { Badge } from "@/components/ui/badge";
import type { Expert } from "./ExpertCard";

interface ChatInterfaceProps {
  expert: Expert;
  suggestedQuestions?: string[];
}

export function ChatInterface({ expert, suggestedQuestions = [] }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: `Olá! Sou ${expert.name}, ${expert.title}. Como posso ajudá-lo hoje com seus desafios estratégicos?`,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Esta é uma resposta simulada do especialista. Na versão completa, aqui virá a resposta real da IA com insights estratégicos profundos.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }, 1000);
  };

  const handleSuggestedQuestion = (question: string) => {
    setInput(question);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            expertName={expert.name}
            expertAvatar={expert.avatar}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {suggestedQuestions.length > 0 && messages.length <= 1 && (
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
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Digite sua pergunta estratégica..."
            className="flex-1"
            data-testid="input-chat-message"
          />
          <Button onClick={handleSend} size="icon" data-testid="button-send-message">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
