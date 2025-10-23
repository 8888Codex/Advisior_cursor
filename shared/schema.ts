import { sql } from "drizzle-orm";
import { pgTable, text, varchar, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

export const experts = pgTable("experts", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: text("name").notNull(),
  title: text("title").notNull(),
  expertise: text("expertise").array().notNull(),
  bio: text("bio").notNull(),
  avatar: text("avatar"),
  systemPrompt: text("system_prompt").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertExpertSchema = createInsertSchema(experts).omit({
  id: true,
  createdAt: true,
});

export type InsertExpert = z.infer<typeof insertExpertSchema>;
export type Expert = typeof experts.$inferSelect;

export const conversations = pgTable("conversations", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  expertId: varchar("expert_id").notNull(),
  title: text("title").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const insertConversationSchema = createInsertSchema(conversations).omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

export type InsertConversation = z.infer<typeof insertConversationSchema>;
export type Conversation = typeof conversations.$inferSelect;

export const messages = pgTable("messages", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  conversationId: varchar("conversation_id").notNull(),
  role: text("role").notNull(),
  content: text("content").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertMessageSchema = createInsertSchema(messages).omit({
  id: true,
  createdAt: true,
});

export type InsertMessage = z.infer<typeof insertMessageSchema>;
export type Message = typeof messages.$inferSelect;

// Business Profile (Python backend)
export const businessProfileSchema = z.object({
  id: z.string(),
  userId: z.string(),
  companyName: z.string(),
  industry: z.string(),
  companySize: z.string(),
  targetAudience: z.string(),
  mainProducts: z.string(),
  channels: z.array(z.string()),
  budgetRange: z.string(),
  primaryGoal: z.string(),
  mainChallenge: z.string(),
  timeline: z.string(),
  createdAt: z.string(),
  updatedAt: z.string(),
});

export const insertBusinessProfileSchema = z.object({
  companyName: z.string().min(1, "Nome da empresa é obrigatório"),
  industry: z.string().min(1, "Setor é obrigatório"),
  companySize: z.string().min(1, "Tamanho da empresa é obrigatório"),
  targetAudience: z.string().min(1, "Público-alvo é obrigatório"),
  mainProducts: z.string().min(1, "Produtos/serviços são obrigatórios"),
  channels: z.array(z.string()).min(1, "Selecione pelo menos um canal"),
  budgetRange: z.string().min(1, "Faixa de orçamento é obrigatória"),
  primaryGoal: z.string().min(1, "Objetivo principal é obrigatório"),
  mainChallenge: z.string().min(1, "Maior desafio é obrigatório"),
  timeline: z.string().min(1, "Prazo é obrigatório"),
});

export type BusinessProfile = z.infer<typeof businessProfileSchema>;
export type InsertBusinessProfile = z.infer<typeof insertBusinessProfileSchema>;
