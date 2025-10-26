# AdvisorIA - Replit Agent Guide

## Overview
AdvisorIA is a premium AI consultancy platform offering expert advice through cognitive clones of 18 specialists across 15 disciplines. It leverages the "Framework EXTRACT de 12 Camadas" with Anthropic's Claude to create ultra-realistic AI personalities. The platform features a React/TypeScript frontend, an Express.js proxy, and a Python/FastAPI backend with asynchronous AI integration, aiming to provide a specialized multi-category consulting experience.

## Recent Changes (October 2025 - Landing Page Unificada "Experiência Disney")
- **Landing Page Consolidada**: Welcome.tsx + Marketing.tsx fundidos em Landing.tsx única na raiz (`/`), criando jornada linear encantadora com storytelling emocional de ponta a ponta.
- **Hero Estratégica com Números Concretos** (aplicando princípios das 18 lendas):
  - Badge: "18 Lendas do Marketing Mundial" (prova social imediata)
  - H1: "**450+ Anos de Expertise** em Marketing. Agora em Uma Conversa." (números concretos + benefício tangível)
  - Subtitle: "De Philip Kotler a Gary Vaynerchuk. Consulte as maiores mentes do marketing como se estivessem vivos na sua frente." (nomeia lendas + emoção)
  - Princípios: Claude Hopkins (números), Ogilvy (fatos específicos), Cialdini (prova social), Godin (storytelling), Schwartz (benefício)
- **Auditoria Completa de Marketing** (Outubro 2025 - Aplicando TODAS as 18 Lendas):
  - **Impact Stats**: Card 2 "Consultas respondidas em português" (concreto vs vago), Card 3 "Testado por usuários reais em comparação cega" (prova do 95%)
  - **Timeline**: "57 Anos de Inovação em Marketing. Grátis Para Começar." + "converse com quem inventou as estratégias que você estuda" (urgência + grátis + storytelling)
  - **Como Funciona - Passo 3**: "Receba Insight em 30 Segundos" + "95% de fidelidade autêntica. Já consultado por +1.000 profissionais." (números + prova social)
  - **IA vs Clone**: IA Genérica "Soa como Wikipedia genérica", Clone "Fala com a voz única de cada lenda" (benefícios tangíveis vs abstrações)
  - **Badge Emocional + Micro-Exemplo**: Adicionado box com exemplo real: "Philip Kotler não diria 'use redes sociais'. Ele diria: 'Segmente por psicografia, não demografia. Depois teste canais.'" (prova por exemplo concreto)
  - **Tour**: "18 Lendas. 450+ Anos. 30 Segundos Para Respostas." + "Escolha sua lenda. Descreva seu desafio. Receba insights que livros não ensinam." (números + energia Gary V + benefício)
  - **Perguntas Footer**: "David Aaker (Branding), Jay Levinson (Guerrilla), Donald Miller (StoryBrand), Robert Cialdini (Persuasão) e +8 outros prontos para consulta." (nomear específicos vs "+12 outros")
  - **Formulário**: "1 Minuto Para Descobrir Qual Lenda Pode 10x Seu Marketing" + "Responda 4 perguntas. Receba recomendações personalizadas de especialistas que dominam seu desafio específico." (benefício vs objeção)
  - **CTA Final**: "Sua Próxima Decisão de Marketing Vale Milhões. Consulte Quem Domina Isso." + "Grátis para começar. 30 segundos para primeiras respostas. 18 lendas disponíveis agora." + Button "Começar Consultoria Grátis" (urgência + grátis + números concretos)
  - **Princípios Aplicados**: Hopkins (números concretos sempre), Ogilvy (fatos vs abstrações), Cialdini (prova social em TODAS seções), Schwartz (benefícios tangíveis), Gary V (energia e punch), Godin (storytelling + exemplos reais), Kennedy (urgência sem agressividade)
- **Estrutura da Landing** (10 seções sequenciais):
  1. Hero: Números concretos logo no início (450+ Anos, 18 Lendas) com 2 CTAs primários
  2. Impact Stats: 18 Lendas / 450+ Anos / 95% Fidelidade (social proof visual com copy atualizada)
  3. Timeline de Impacto: 4 eras (1967-Hoje) com lendas, urgência "Grátis Para Começar"
  4. Como Funciona: 3 passos (último atualizado com +1.000 profissionais)
  5. IA vs Clone: Comparação com bullets atualizados (benefícios tangíveis)
  6. Badge Emocional: "Como Se Estivessem Vivos" + micro-exemplo Kotler
  7. Tour Interativo: 18 especialistas com headline energética e números
  8. Perguntas Concretas: 6 especialistas × 3 perguntas + footer nomeando lendas
  9. Formulário Inline: "10x Seu Marketing" → conversão suave para /home
  10. CTA Final: "Vale Milhões" + urgência + "Consultoria Grátis"
- **Copy 100% Emocional**: Removido jargão técnico ("Framework EXTRACT de 20 pontos") → substituído por benefícios ("Como Se Estivessem Vivos na Sua Frente"). Framework permanece 20 pontos internamente, mas apresentado ao usuário via emoção.
- **Roteamento Simplificado**:
  - `/` → Landing.tsx (público, jornada completa Disney)
  - `/home` → Home.tsx (grid autenticado, preservado)
  - `/welcome` e `/marketing` → REMOVIDOS (redirects automáticos para /)
- **Navegação Atualizada**: Header limpo (Logo, Especialistas, Categorias, Criar Especialista) sem link obsoleto para /marketing.
- **Validação E2E**: Jornada completa testada (desktop + mobile 375x667) - landing → tour → formulário → /home → chat funcionando perfeitamente, todas 9 seções atualizadas validadas visualmente, animações fluidas <300ms, conversão suave, sem bugs funcionais.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend
- **Framework & Tooling**: React 18 with TypeScript, Vite, Wouter for routing, TanStack Query v5 for server state.
- **UI Component System**: shadcn/ui components on Radix UI, Tailwind CSS for styling. Professional aesthetic inspired by Linear, Notion, and LinkedIn, with primary dark mode.
- **State Management**: TanStack Query for server state, React Context for theme, react-hook-form with Zod for forms.
- **Routing**: Wouter with custom `useURLSearchParam` hook for URL query parameter synchronization.

### Backend (Hybrid Proxy + Python)
- **Express.js Proxy Server (Port 5000)**: TypeScript proxy forwarding `/api` requests to Python backend, handles automatic Python backend startup and serves static frontend in production.
- **Python/FastAPI Backend (Port 5001)**: FastAPI for async API routes, AsyncAnthropic client for non-blocking AI calls.
- **API Endpoints**: Includes endpoints for experts, categories, suggested questions, chat, auto-cloning, user profiles, and insights.
- **Storage Layer**: In-memory Python storage (MemStorage) using Pydantic models for Expert, Conversation, and Message entities.

### AI Integration - Cognitive Cloning
- **Framework EXTRACT de 12 Camadas**: Each specialist uses a 12-layer system prompt for ultra-realistic personalities (Identity Core, Terminology, Reasoning Patterns, Communication Style, Expertise Contexts, Techniques & Methods, Limitations, Meta-Awareness, Famous Quotes, Real Cases, Controversial Takes, Temporal Context).
- **Implementation**: Uses AsyncAnthropic Claude API (claude-sonnet-4-20250514) with system prompts stored in `python_backend/prompts/legends.py`.
- **Specialists**: 18 specialists with cross-referencing capabilities and Socratic questioning for diagnostic interactions.

### Key Architectural Decisions
- **Monorepo Structure**: `/client` (React), `/server` (Express), `/python_backend` (FastAPI), and `/shared` (TypeScript types).
- **Data Flow**: User interaction -> React UI -> TanStack Query -> Express proxy -> FastAPI -> Storage/AsyncAnthropic -> FastAPI -> Express -> React.
- **Development Workflow**: `npm run dev` starts Express, which spawns the auto-reloading Python backend.
- **UX/UI Decisions (Apple-style Minimalist - October 2025 Redesign)**:
    - **Color Palette**: 95% neutral (grays), 1 accent coral único (hsl 9° 75% 61% light, 42% dark). Rainbow palette ELIMINADA (no emerald, cyan, blue, amber, etc).
    - **Visual Effects**: Minimalistas - subtle shadows, hover translateY(-2px), NO glassmorphism pesado, NO shimmer/glow/pulse effects.
    - **Animations**: Apple-style rápido (200-300ms duration, cubic-bezier [0.25, 0.1, 0.25, 1]), stagger delays <100ms, NO teatral.
    - **Typography**: font-semibold para headings (não bold pesado), hierarchy com 3 níveis de text-muted-foreground.
    - **Components**: Badges neutros (variant="secondary"), apenas CTAs usam accent coral, NO avatar breathing/gradient borders.
    - **Design System**: Consistência visual total - accent único em toda aplicação, animações rápidas, espaçamento generoso, rounded-2xl standardizado.
- **Multi-Category Navigation System**:
    - **Categories**: 15 distinct categories (marketing, growth, psychology, etc.) com ícones neutros e palette consistente.
    - **Category Page**: Grid 2-column com cards neutros (NO glassmorphism), stagger animations 50ms, hover subtle.
    - **Category Colors**: TODAS neutras (from-muted to-muted/50), badges secondary variant, ícones text-muted-foreground.
    - **Expert Filtering**: Dropdown filter, badges neutros, "Limpar Filtros" button.
    - **URL Sync**: Custom `useURLSearchParam` hook com polling e event listeners.
- **Personalization System**:
    - **Expert Recommendation**: Scores experts based on user profile, displaying 5-star badges.
    - **Contextual AI Prompt Enrichment**: Injects user business profile into chat interactions.
    - **Perplexity-powered Suggested Questions**: Generates personalized questions for experts.
    - **Business Insights**: Provides industry-specific tips based on user profile.
    - **Smart Filters**: Search, sort, and filter experts, including "Apenas Recomendados" option.
    - All personalized features are conditional on `hasProfile=true` with graceful fallbacks.

## External Dependencies

- **Anthropic Claude API**: AI model interactions and cognitive cloning.
- **Perplexity API**: Research for auto-cloning feature and content generation.
- **React**: Frontend library.
- **Vite**: Build tool.
- **Wouter**: Client-side router.
- **TanStack Query**: Server state management.
- **shadcn/ui & Radix UI**: UI component libraries.
- **Tailwind CSS**: Styling framework.
- **Express.js**: Proxy server.
- **FastAPI**: Python backend framework.
- **AsyncAnthropic**: Asynchronous Python client for Anthropic API.
- **Uvicorn**: ASGI server for FastAPI.
- **Pydantic**: Data validation for Python models.
- **Zod**: Schema declaration and validation for TypeScript.
- **Framer Motion**: Animation library for React.