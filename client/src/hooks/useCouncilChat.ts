import { useState, useCallback, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiRequest, apiRequestJson } from "@/lib/queryClient";

interface CouncilMessage {
  id: string;
  conversationId: string;
  expertId?: string;
  expertName?: string;
  content: string;
  role: "user" | "expert" | "system";
  timestamp: string;
  reactions: Array<{
    expertId: string;
    expertName: string;
    type: "agree" | "disagree" | "add" | "question";
    content?: string;
  }>;
}

interface CouncilConversation {
  id: string;
  userId: string;
  personaId: string;
  problem: string;
  expertIds: string[];
  createdAt: string;
  updatedAt: string;
}

interface SendMessageResponse {
  status?: string;
  message?: string;
  userMessage: CouncilMessage;
  expertMessages?: CouncilMessage[];
  conversationId?: string;
}

export function useCouncilChat(conversationId: string | null) {
  const queryClient = useQueryClient();
  const [isSending, setIsSending] = useState(false);

  // Buscar conversa
  const { data: conversation, isLoading: loadingConversation } = useQuery<CouncilConversation>({
    queryKey: ["/api/council/conversations", conversationId],
    enabled: !!conversationId,
    queryFn: async () => {
      if (!conversationId) return null;
      const response = await apiRequest(`/api/council/conversations/${conversationId}`);
      return response.json();
    },
  });

  // Estado para controlar polling
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Buscar mensagens com polling automático quando processando
  const { data: messages = [], isLoading: loadingMessages, refetch: refetchMessages } = useQuery<CouncilMessage[]>({
    queryKey: ["/api/council/conversations", conversationId, "messages"],
    enabled: !!conversationId,
    queryFn: async () => {
      if (!conversationId) return [];
      const response = await apiRequest(`/api/council/conversations/${conversationId}/messages`);
      return response.json();
    },
    refetchInterval: (query) => {
      // Polling enquanto processando ou enviando
      if (isProcessing || isSending) {
        return 2000; // Poll a cada 2 segundos
      }
      return false;
    },
  });

  // Mutation para enviar mensagem
  const sendMessageMutation = useMutation({
    mutationFn: async (content: string) => {
      if (!conversationId) throw new Error("Conversa não encontrada");
      
      setIsSending(true);
      setIsProcessing(true);
      
      try {
        const response = await apiRequestJson<SendMessageResponse>(
          `/api/council/conversations/${conversationId}/messages`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content }),
            timeout: 5000, // Timeout menor agora (endpoint retorna rápido)
          }
        );
        
        // Se status é "processing", significa que está em background
        if (response.status === "processing") {
          // Iniciar polling - a query já vai fazer isso automaticamente
          // Salvar no localStorage para continuar mesmo se mudar de página
          const activeTasks = JSON.parse(localStorage.getItem("council_chat_active_tasks") || "[]");
          if (!activeTasks.includes(conversationId)) {
            activeTasks.push(conversationId);
            localStorage.setItem("council_chat_active_tasks", JSON.stringify(activeTasks));
          }
        }
        
        return response;
      } finally {
        setIsSending(false);
        // isProcessing será false quando as mensagens chegarem
      }
    },
    onSuccess: (data) => {
      // Se já recebeu as mensagens, invalidar cache
      if (data.expertMessages && data.expertMessages.length > 0) {
        setIsProcessing(false);
        queryClient.invalidateQueries({
          queryKey: ["/api/council/conversations", conversationId, "messages"],
        });
      }
    },
  });
  
  // Verificar se há novas mensagens de especialistas quando polling
  useEffect(() => {
    if (!conversationId || !isProcessing) return;
    
    // Contar mensagens de especialistas
    const expertMessagesCount = messages.filter(m => m.role === "expert").length;
    
    // Se encontrou novas mensagens de especialistas, pode parar o processing
    // Verificar se temos pelo menos uma mensagem de cada especialista esperado
    const expectedExpertCount = conversation?.expertIds?.length || 0;
    const lastUserMessageTime = messages
      .filter(m => m.role === "user")
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())[0]?.timestamp;
    
    // Contar mensagens de especialistas após a última mensagem do usuário
    const recentExpertMessages = messages.filter(
      m => m.role === "expert" && lastUserMessageTime && new Date(m.timestamp) > new Date(lastUserMessageTime)
    ).length;
    
    // Se temos respostas de todos os especialistas esperados, parar processing
    if (recentExpertMessages >= expectedExpertCount && expectedExpertCount > 0) {
      setIsProcessing(false);
      // Remover do localStorage
      const activeTasks = JSON.parse(localStorage.getItem("council_chat_active_tasks") || "[]");
      const updated = activeTasks.filter((id: string) => id !== conversationId);
      localStorage.setItem("council_chat_active_tasks", JSON.stringify(updated));
    }
  }, [messages, isProcessing, conversationId, conversation]);
  
  // Verificar tasks ativas no localStorage ao montar
  useEffect(() => {
    if (!conversationId) return;
    
    const activeTasks = JSON.parse(localStorage.getItem("council_chat_active_tasks") || "[]");
    if (activeTasks.includes(conversationId)) {
      setIsProcessing(true);
    }
  }, [conversationId]);

  const sendMessage = useCallback(
    (content: string) => {
      if (!conversationId || !content.trim()) return;
      sendMessageMutation.mutate(content.trim());
    },
    [conversationId, sendMessageMutation]
  );

  return {
    conversation,
    messages,
    loadingConversation,
    loadingMessages,
    isSending: isSending || sendMessageMutation.isPending,
    isProcessing,
    sendMessage,
    error: sendMessageMutation.error,
  };
}

