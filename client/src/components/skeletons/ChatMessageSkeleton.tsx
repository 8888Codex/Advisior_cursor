import { motion } from "framer-motion";

export function ChatMessageSkeleton({ isUser = false }: { isUser?: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {!isUser && (
        <div className="h-8 w-8 rounded-full bg-muted shimmer flex-shrink-0" />
      )}
      
      <div className={`flex flex-col gap-2 max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`space-y-2 ${isUser ? 'bg-primary/10' : 'bg-muted'} rounded-2xl p-4 shimmer`}>
          <div className="h-4 w-48 bg-muted/50 rounded-xl" />
          <div className="h-4 w-36 bg-muted/50 rounded-xl" />
        </div>
      </div>

      {isUser && (
        <div className="h-8 w-8 rounded-full bg-muted shimmer flex-shrink-0" />
      )}
    </motion.div>
  );
}

export function ChatLoadingSkeleton() {
  return (
    <div className="space-y-6 p-6">
      <ChatMessageSkeleton isUser={false} />
      <ChatMessageSkeleton isUser={true} />
      <ChatMessageSkeleton isUser={false} />
    </div>
  );
}
