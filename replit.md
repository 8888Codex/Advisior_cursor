# AdvisorIA - Replit Agent Guide

## Overview

AdvisorIA is a premium AI consultancy platform featuring cognitive clones of 8 legendary marketing figures (Philip Kotler, David Ogilvy, Claude Hopkins, John Wanamaker, Mary Wells Lawrence, Seth Godin, Gary Vaynerchuk, Leo Burnett). The platform uses Framework EXTRACT methodology to create high-fidelity AI personalities via Anthropic's Claude. Built with React/TypeScript frontend, Express.js proxy, and Python/FastAPI backend with async AI integration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture (Updated: October 23, 2025)

### Frontend Architecture

**Framework & Tooling**
- **React 18** with TypeScript for type-safe component development
- **Vite** as the build tool and development server
- **Wouter** for lightweight client-side routing
- **TanStack Query v5** for server state management and API calls

**UI Component System**
- **shadcn/ui** components built on Radix UI primitives
- **Tailwind CSS** for utility-first styling
- Professional aesthetic inspired by Linear, Notion, and LinkedIn
- Dark mode primary with comprehensive light mode support

**State Management Pattern**
- Server state: TanStack Query with custom query client
- Theme: React Context (ThemeProvider)
- Forms: react-hook-form with Zod validation
- No global state library (component-level state preferred)

### Backend Architecture (Hybrid Proxy + Python)

**Express.js Proxy Server (Port 5000)**
- Lightweight TypeScript proxy that forwards all `/api` requests to Python backend
- Automatic Python backend startup via `child_process.spawn`
- Proxy configured BEFORE `express.json()` middleware to preserve request bodies
- Vite integration for development HMR
- Serves static frontend in production

**Python/FastAPI Backend (Port 5001)**
- **FastAPI** for async API routes
- **AsyncAnthropic** client for non-blocking AI calls (critical for production concurrency)
- RESTful API matching frontend expectations
- In-memory storage (MemStorage) for development
- Auto-reload enabled via uvicorn --reload

**API Endpoints**
- `GET /api/experts` - List all marketing legend experts
- `GET /api/experts/:id` - Get specific expert details
- `POST /api/experts` - Save cognitive clone to storage
- `POST /api/experts/auto-clone` - Auto-generate clone from person name (Perplexity research + Claude synthesis)
- `POST /api/experts/test-chat` - Test clone preview without persistence
- `POST /api/conversations` - Create conversation with an expert
- `GET /api/conversations/:id/messages` - Get conversation message history
- `POST /api/conversations/:id/messages` - Send message and get AI response

**Storage Layer**
- In-memory Python storage (MemStorage class) in `python_backend/storage.py`
- UUID-based identifiers for all entities
- Schema: Expert, Conversation, Message models (Pydantic)
- Conversation history maintained across messages

### AI Integration - Cognitive Cloning

**Framework EXTRACT Methodology**
Each marketing legend has a detailed system prompt with 8 cognitive layers:
1. **Identity Core**: Formative experiences, mental models, personal axioms
2. **Terminology**: Signature phrases and concepts
3. **Reasoning Patterns**: Typical decision frameworks
4. **Communication Style**: Tone, structure, references
5. **Expertise Contexts**: Specialty domains
6. **Techniques & Methods**: Specific approaches and tools
7. **Limitations**: Acknowledged boundaries
8. **Meta-Awareness**: Self-reflection on biases

**Implementation**
- **AsyncAnthropic Claude API** (claude-sonnet-4-20250514)
- Non-blocking async calls to avoid event loop starvation
- System prompts stored in `python_backend/prompts/legends.py`
- Each legend responds with authentic personality and expertise

**8 Pre-Seeded Marketing Legends**
1. Philip Kotler - "O Pai do Marketing Moderno" (4Ps, Segmentation, Brand Positioning)
2. David Ogilvy - "O Pai da Publicidade" (Copywriting, Direct Response, Luxury Marketing)
3. Claude C. Hopkins - "Pioneiro do Marketing Científico" (A/B Testing, ROI, Scientific Advertising)
4. John Wanamaker - "Revolucionário do Varejo Moderno" (Retail Strategy, Customer Trust)
5. Mary Wells Lawrence - "Pioneira do Branding Emocional" (Lifestyle Marketing, I ♥ NY)
6. Seth Godin - "Visionário do Permission Marketing" (Purple Cow, Tribes, Storytelling Digital)
7. Gary Vaynerchuk - "Rei do Marketing Digital e Hustle" (Social Media, Personal Branding)
8. Leo Burnett - "O Rei do Storytelling Publicitário" (Archetypal Characters, Marlboro Man)

### Key Architectural Decisions

**Monorepo Structure**
- `/client` - React frontend
- `/server` - Express.js proxy (TypeScript)
- `/python_backend` - FastAPI AI backend (Python)
  - `main.py` - API routes and startup
  - `models.py` - Pydantic data models
  - `storage.py` - In-memory storage layer
  - `crew_agent.py` - AsyncAnthropic wrapper for AI responses
  - `seed.py` - Marketing legends seeding
  - `prompts/legends.py` - Framework EXTRACT system prompts
- `/shared` - Shared TypeScript types (Drizzle + Zod schemas)
- Path aliases: `@/`, `@shared/`, `@assets/`

**Data Flow Pattern**
1. User interacts with React UI
2. TanStack Query makes API call to Express (port 5000)
3. Express proxy forwards to Python FastAPI (port 5001)
4. FastAPI validates with Pydantic, queries storage
5. For messages: AsyncAnthropic client calls Claude with legend's system prompt
6. Response flows back: FastAPI → Express → React
7. TanStack Query caches and updates UI

**Proxy Configuration (Critical)**
- Proxy middleware MUST be configured BEFORE `express.json()` middleware
- Otherwise request bodies are consumed and not forwarded to Python backend
- Target: `http://localhost:5001/api` (includes /api prefix in target)
- `changeOrigin: true` for proper header forwarding

**Development Workflow**
- Single command: `npm run dev` starts Express server (port 5000)
- Express automatically spawns Python backend process (port 5001)
- Python backend auto-reloads on file changes via uvicorn --reload
- Frontend HMR via Vite integration
- All logs visible in Express console (both servers)

**Production Readiness Notes**
- ✅ AsyncAnthropic prevents event loop blocking (supports concurrent requests)
- ✅ Auto-clone feature complete: Perplexity research + Claude EXTRACT synthesis
- ✅ Preview→test→save workflow prevents unwanted clones in storage
- ⚠️ In-memory storage: Replace with PostgreSQL/Drizzle for persistence
- ⚠️ No authentication system yet (planned: Replit Auth)
- ⚠️ No streaming responses yet (frontend and backend support needed)
- ⚠️ Error handling could be more granular (distinguish API errors, timeouts, etc.)

**Migration Path**
- Storage: Swap MemStorage for PostgreSQL via Drizzle ORM
- Auth: Integrate Replit Auth for user sessions
- Streaming: Implement Server-Sent Events (SSE) for real-time AI responses
- Monitoring: Add logging, metrics, error tracking (e.g., Sentry)
- Disney-Level UX: Complete phases 2-6 (onboarding, micro-moments, personalization, export, gamification)

## Recent Changes (October 23, 2025)

**Fase 1: Auto-Clone Cognitivo (COMPLETED)**
- **Backend Auto-Clone System**:
  - `POST /api/experts/auto-clone`: Accepts only `targetName` (required) and `context` (optional)
  - Uses Perplexity API to research target person (biography, philosophy, methods, iconic phrases)
  - Claude synthesizes research into complete EXTRACT system prompt (8 cognitive layers)
  - Second Claude call extracts metadata (title, expertise, bio)
  - Returns `ExpertCreate` data WITHOUT persisting (preview-first workflow)
- **Frontend UX Refinements**:
  - Minimalist form on `/create` page (2 inputs: name + context)
  - 3-stage animated loading (Pesquisando → Analisando → Sintetizando)
  - Preview screen with expandable system prompt
  - Test chat uses dedicated endpoint (`/api/experts/test-chat`) without persistence
  - Save/Regenerate buttons: only Save persists to storage
- **Workflow Guarantee**: Preview→test→save prevents unwanted clones and storage pollution
- **Design Compliance**: All emojis removed from UI (toast titles, descriptions)

**Backend Migration to Python/FastAPI**
- Replaced TypeScript backend with Python/FastAPI for AI orchestration
- Maintained API compatibility with existing React frontend
- Express server now acts as lightweight proxy to Python backend

**Cognitive Cloning System**
- Implemented Framework EXTRACT methodology for 8 marketing legends
- Each legend has 1000+ word system prompt capturing cognitive patterns
- High-fidelity personality simulation via Anthropic Claude

**Critical Bug Fixes**
1. **Proxy Middleware Order**: Moved proxy BEFORE express.json() to preserve POST bodies
2. **Async API Calls**: Switched from sync Anthropic to AsyncAnthropic to prevent event loop blocking
3. **Conversation History**: Fixed logic to include all prior messages in AI context
4. **Auto-Clone Persistence**: Fixed to defer storage until explicit save (prevents duplicates)

**Testing**
- End-to-end Playwright tests confirm full user flow working
- AI responses authentic to each legend's personality (verified manually and via tests)
- Concurrent request support confirmed via async client architecture
- Preview→test→save workflow validated by architect review

**Fase 2: Onboarding Cinematográfico (COMPLETED)**
- **Página /welcome com 3 Etapas**:
  - **Hero Section**: Introdução visual com animações Framer Motion, badge "Bem-vindo ao AdvisorIA", título principal, descrição do sistema e botão CTA com loading state
  - **Tour Interativo**: Carrossel cinematográfico apresentando os 8 legendários do marketing com avatars, badges de expertise, biografia e progress bar. Navegação anterior/próximo/pular totalmente funcional
  - **Formulário de Perfil**: Coleta dados do negócio (empresa, indústria, tamanho, público-alvo, produtos, canais, orçamento, objetivo, desafio, prazo) para personalização futura
- **Estados de Loading/Empty Robusto**:
  - Hero CTA desabilitado apenas durante `expertsLoading`, habilitado assim que request termina
  - Tour acessível em QUALQUER cenário: loading (mostra card com Sparkles rotativo), empty (mostra escape hatch "Pular para Perfil"), success (mostra carrossel)
  - Garantia de zero dead-ends: usuário sempre pode progredir independente do payload de experts
- **Animações Disney-Level**:
  - AnimatePresence do Framer Motion para transições suaves entre etapas
  - Entrada/saída com fade e slide (x/y offset)
  - Progress bar animado no tour
  - Loading state no botão de salvar perfil com ícone rotativo
- **Fluxo UX Completo**:
  - Hero → Tour (com skip) → Profile → Save → Redirect para Home
  - localStorage marca `onboarding_complete` após salvar
  - Home verifica localStorage + API profile para redirecionar novos usuários para /welcome automaticamente
- **Integração Backend**:
  - Usa endpoints existentes POST/GET `/api/profile` (BusinessProfile model)
  - Mutation TanStack Query para salvar perfil com invalidação de cache
  - Redirecionamento automático após sucesso

**Fase 3: Micro-Momentos de Interação Disney-Level (COMPLETED)**
- **Animações de Entrada para Mensagens de Chat**:
  - Mensagens deslizam de lados opostos (user: direita, assistant: esquerda)
  - Fade + slide combinados com cubic bezier ease (0.4, 0, 0.2, 1)
  - Animação suave de 0.3s por mensagem via motion.div
- **Feedback Visual Premium ao Enviar Mensagem**:
  - Avatar do especialista pulsa com breathing effect durante "Pensando..." (scale 1.0 → 1.05 loop)
  - Ripple effect no card de mensagem (boxShadow animado com glow)
  - Animação infinita com loop de 2s usando keyframes CSS
- **Expert Cards com Hover/Tap Effects**:
  - Card envolto em motion.div com fade-in + slide-up na entrada inicial
  - Avatar: scale 1.05 + rotate wiggle (-2°, 2°, 0°) ao hover no card parent
  - Badges: staggered animation (0.05s delay entre cada badge)
  - Botão: whileHover scale 1.02, whileTap scale 0.98 para feedback tátil
- **Perguntas Sugeridas com Stagger Animation**:
  - Container fade-in + slide-up na montagem
  - Label "Perguntas Sugeridas" com delay 0.1s
  - Badges aparecem uma após outra (delay: 0.2 + index * 0.1)
  - Animação scale + fade para cada badge (cubic bezier consistente)
- **Transições Suaves Entre Páginas**:
  - Criado componente AnimatedPage wrapper universal
  - Aplicado em Home, Experts, Chat, Create (todas páginas principais)
  - Fade + slide vertical (y: 20 → 0 enter, y: -20 exit) em 0.3s
  - AnimatePresence mode="wait" integrado com wouter router via useLocation
  - Exit animations funcionais: key={location} no Switch trigger rerenders
- **Consistência e Performance**:
  - Todos os timings: 0.3s (micro-momentos), 0.5s (macro-transições)
  - Easing function padronizada: cubic-bezier(0.4, 0, 0.2, 1) "ease-out"
  - Animações sutis para não atrasar percepção de performance
  - Arquiteto validou zero jank ou regressões de performance
