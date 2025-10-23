import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { User } from "lucide-react";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
  expertName?: string;
  expertAvatar?: string;
}

export function ChatMessage({ message, expertName, expertAvatar }: ChatMessageProps) {
  const isUser = message.role === "user";
  const initials = expertName
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "AI";

  return (
    <div
      className={cn(
        "flex gap-3 mb-4",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
      data-testid={`message-${message.id}`}
    >
      <Avatar className="h-8 w-8 flex-shrink-0">
        {isUser ? (
          <>
            <AvatarFallback>
              <User className="h-4 w-4" />
            </AvatarFallback>
          </>
        ) : (
          <>
            <AvatarImage src={expertAvatar} alt={expertName} />
            <AvatarFallback className="text-xs">{initials}</AvatarFallback>
          </>
        )}
      </Avatar>

      <div className={cn("flex flex-col gap-1 max-w-[80%]", isUser ? "items-end" : "items-start")}>
        {!isUser && expertName && (
          <span className="text-xs font-medium text-muted-foreground px-3">
            {expertName}
          </span>
        )}
        <div
          className={cn(
            "rounded-xl px-4 py-3 text-sm leading-relaxed",
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-card border"
          )}
        >
          {message.content}
        </div>
      </div>
    </div>
  );
}
