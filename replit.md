# AdvisorIA - Replit Agent Guide

## Overview

AdvisorIA is a premium AI consultancy platform featuring cognitive clones of **18 specialists** across **15 disciplines**. It uses the **Framework EXTRACT de 12 Camadas** to create ultra-realistic AI personalities via Anthropic's Claude. The platform is built with a React/TypeScript frontend, an Express.js proxy, and a Python/FastAPI backend with async AI integration. Its purpose is to provide expert advice through AI-powered cognitive clones, offering a specialized multi-category consulting experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework & Tooling**: React 18 with TypeScript, Vite, Wouter for routing, TanStack Query v5 for server state.
- **UI Component System**: shadcn/ui components on Radix UI, Tailwind CSS for styling. Professional aesthetic inspired by Linear, Notion, and LinkedIn, with dark mode primary and light mode support.
- **State Management**: TanStack Query for server state, React Context for theme, react-hook-form with Zod for forms. No global state library.
- **Routing**: Wouter with custom `useURLSearchParam` hook for reliable URL query parameter synchronization (see URL Sync Solution below).

### Backend Architecture (Hybrid Proxy + Python)
- **Express.js Proxy Server (Port 5000)**: Lightweight TypeScript proxy forwarding `/api` requests to Python backend, automatic Python backend startup, Vite integration, serves static frontend in production.
- **Python/FastAPI Backend (Port 5001)**: FastAPI for async API routes, AsyncAnthropic client for non-blocking AI calls.
- **API Endpoints**: 
  - `GET /api/experts` (supports `?category=` filter)
  - `GET /api/categories` (metadata: id, name PT-BR, description, icon, color, expertCount)
  - `GET /api/experts/{id}/suggested-questions` (Perplexity-powered personalization)
  - `POST /api/chat` (streaming AI responses)
  - `POST /api/auto-clone` (research + prompt generation)
  - `GET /api/profile` (user business profile)
  - `GET /api/insights` (Perplexity industry tips)
- **Storage Layer**: In-memory Python storage (MemStorage) using Pydantic models for Expert (with CategoryType enum), Conversation, and Message entities.

### AI Integration - Cognitive Cloning (Enhanced)
- **Framework EXTRACT de 12 Camadas**: Each specialist has an ultra-realistic system prompt with 12 cognitive layers:
  1. **Identity Core**: Name, role, historical context
  2. **Terminology**: Domain-specific vocabulary
  3. **Reasoning Patterns**: How they think and solve problems
  4. **Communication Style**: Tone, formality, linguistic quirks
  5. **Expertise Contexts**: Where they excel
  6. **Techniques & Methods**: Proprietary frameworks (ICE, STEPPS, AIDA)
  7. **Limitations**: What they DON'T do
  8. **Meta-Awareness**: Self-reference behavior
  9. **Famous Quotes**: Authentic quotes from books/speeches
  10. **Real Cases**: Documented campaigns/strategies
  11. **Controversial Takes**: Polarizing opinions
  12. **Temporal Context**: 2025 awareness with maintained philosophy
- **Implementation**: Uses AsyncAnthropic Claude API (claude-sonnet-4-20250514) for non-blocking calls. System prompts stored in `python_backend/prompts/legends.py`.
- **Current Specialists (18)**: Philip Kotler, David Ogilvy, Seth Godin, Al Ries, Bill Bernbach, Dan Kennedy, Ann Handley, Neil Patel, Robert Cialdini, Simon Sinek, Byron Sharp, Sean Ellis, Brian Balfour, Andrew Chen, Jonah Berger, Hiten Shah, Elena Verna, Casey Winters.
- **Cross-References**: Each specialist can recommend other specialists when appropriate (e.g., Sean Ellis → Brian Balfour for growth systems)
- **Socratic Questioning**: Each specialist asks diagnostic questions before advising (e.g., Dan Kennedy asks about CAC/LTV before strategy recommendations)

### Key Architectural Decisions
- **Monorepo Structure**: `/client` (React), `/server` (Express), `/python_backend` (FastAPI), and `/shared` (TypeScript types).
- **Data Flow**: User interaction -> React UI -> TanStack Query -> Express proxy -> FastAPI -> Storage/AsyncAnthropic -> FastAPI -> Express -> React.
- **Proxy Configuration**: Proxy middleware configured before `express.json()` to preserve request bodies.
- **Development Workflow**: `npm run dev` starts Express, which spawns the auto-reloading Python backend.
- **Production Readiness**: AsyncAnthropic prevents event loop blocking. Auto-clone feature complete. In-memory storage is a known limitation for production persistence.
- **UX/UI Decisions - Disney-Level Premium**: 
  - **Color Palette**: Vibrante roxo 270°100%65% (primary) + dourado 45°100%58% (accent) + cyan 190°100%55% (accent-cyan), dark mode profundo 250°40%6%
  - **Glassmorphism System**: backdrop-blur-xl/2xl nos cards, glass e glass-strong utilities
  - **Glow Effects**: glow-primary, glow-accent, glow-subtle com multi-layered box-shadows
  - **Text Gradients**: text-gradient-primary, text-gradient-gold, text-gradient-premium para headlines impactantes
  - **Background Gradients**: bg-gradient-mesh (hero), bg-gradient-card, bg-gradient-hero com mesh animado
  - **Premium Animations**: shimmer (2s loop), card-3d-hover (translateY + scale + glow), pulse-glow, gradient-border animado
  - **Timing**: Micro 150-250ms, médio 300-400ms, page transitions 500ms, easing cubic-bezier(0.4, 0, 0.2, 1)
  - **Stagger Animations**: 0.1s delay entre cards, entry animations coordenadas
  - **Hero Section**: Mesh gradient animado com 3 blobs pulsantes, glassmorphism badges, text gradients, glow CTAs
  - **Expert Cards**: 3D hover transform, avatar ring glow, gradient borders para recomendados, shimmer badges
  - **Page Transitions**: Fade + scale coordenados (0.98→1) entry/exit 500ms
- **Visual Refinement "Apple Store Sofisticado" (Completo)**:
  - Border-radius system: cards rounded-3xl (24px), badges rounded-full, buttons rounded-xl (12px)
  - Hover animations: translateY(-2px) scale(1.01) duration-600ms type:"tween" (ultra-sutis e cinematográficos)
  - Grid layout: 2 colunas desktop (md:grid-cols-2) com gap-8, nunca 3 colunas
  - Spacing generous: cards p-8 gap-6, sections py-20/24, avatars w-24 h-24
  - Typography weights: font-bold apenas títulos principais, resto font-medium/semibold/normal
  - Glassmorphism: backdrop-blur-lg bg-card/30 (reduzido de xl/40), borders /30
  - Glow effects: opacidades 0.12-0.15 (reduzidas de 0.3-0.4), spreads 8-30px
  - Stagger animations: 0.15s delays (aumentado de 0.05s-0.1s)
  - Avatar photos: todos os 8 especialistas com fotos reais (/attached_assets/generated_images/)
  - AnimatedPage transitions: 0.6s duration com stagger coordenado
  - Expert cards: p-8 gap-6 rounded-3xl com hover suave e fotos visíveis
- **Personalization System (Fase 4 - Completa)**:
  - Expert recommendation engine scores 8 experts (0-100) based on user profile alignment, displays 5-star badges for top matches (stars >= 4)
  - Contextual AI prompt enrichment injects business profile into system prompts for all chat interactions
  - Perplexity-powered suggested questions: GET /api/experts/{expert_id}/suggested-questions generates 5 personalized questions (temperature 0.3, sonar-pro model) with defensive fallbacks
  - Business insights section on home: GET /api/insights generates 3-4 industry-specific tips (temperature 0.4, month recency filter) with category badges
  - Smart filters on /experts page: search, sort by relevance/name, filter by expertise category, toggle "Apenas Recomendados" (stars >= 4), active filter count
  - All personalized features conditional on hasProfile=true, graceful fallbacks to generic content when Perplexity API fails or profile missing

### Multi-Category Navigation System (NEW)
- **15 Categories**: marketing, growth, psychology, branding, sales, content, seo, analytics, sales_enablement, media_buying, virality, product_strategy, retention, conversion_optimization, network_effects
- **Category Page** (`/categories`): Grid layout with glassmorphism cards, Lucide icons, theme colors (purple for marketing, emerald for growth, cyan for psychology, etc.), stagger animations (0.15s delay)
- **Expert Filtering** (`/experts?category={id}`): Dropdown filter, category badges on ExpertCards, "Limpar Filtros" button
- **Design System**: 
  - `CATEGORY_COLORS`: bg/text/glow/border variants for all 15 categories
  - `CATEGORY_ICONS`: Brain, Rocket, Award, Handshake, BarChart3, etc.
  - `CATEGORY_NAMES`: PT-BR labels ("Marketing Tradicional", "Growth Hacking", etc.)
- **URL Sync Solution**: Custom `useURLSearchParam` hook with polling fallback (100ms) + event listeners (popstate, hashchange) ensures UI syncs with URL across ALL navigation types (dropdown selection, browser back/forward, category card clicks, direct URLs)
- **Mobile Accessibility**: Touch targets corrected to 44px minimum (`min-h-11`) for all interactive buttons
- **Hover Effects**: `overflow-visible` on Cards to enable `translateY(-2px) scale(1.01)` 3D animations

## Recent Updates

### October 24, 2025 - Multi-Category System: URL Sync Fix + Production-Ready
- **Custom Hook `useURLSearchParam`**: Created `client/src/hooks/use-url-search-params.ts` to solve URL ↔ UI synchronization bug
- **Polling Fallback**: 100ms polling catches programmatic navigation when Wouter location hook doesn't trigger (e.g., dropdown selection, setLocation calls)
- **Event Listeners**: popstate (browser back/forward) + hashchange (URL changes) + wouter location dependency
- **Architecture**: Simplified `Experts.tsx` from manual useState sync to single `const selectedCategory = useURLSearchParam("category", "all")` line
- **E2E Testing PASS**: All navigation flows validated (dropdown, browser history, category cards, direct URLs)
- **Architect Review PASS**: Production-ready with recommendations to monitor polling if hook reused widely, evaluate wouter built-in search handling, add regression tests
- **Bug Fixes Applied**:
  - Touch targets: `min-h-11` (44px) on "Consultar Especialista" and "Ver Especialistas" buttons
  - Hover effects: Removed `overflow-hidden` from ExpertCard, added `overflow-visible` to enable 3D transform animations
  - URL sync: Custom hook with polling eliminates all sync issues across navigation methods
- **Specialist Count**: 18/25+ (all with 12-layer EXTRACT prompts, cross-references, socratic questioning)

### October 24, 2025 - Disney-Level Polish: Micro-Interações Mágicas (Fase 1-4 Completa)
- **Press Effects & Ripple**: Scale(0.98) ao clicar em cards/botões, ripple animation expandindo ao click com hook useRipple
- **Skeleton Loaders**: ExpertGridSkeleton e ChatLoadingSkeleton com pulse orgânico para estados de loading
- **Toasts Cinematográficos**: Slide-in from right, duration 400ms, glassmorphism background, saída coordenada
- **Cascade Animations**: Expert cards entram com stagger 0.15s, motion parent com staggerChildren coordenado
- **Parallax Hero**: Background mesh move 20% mais devagar ao scroll usando useScroll/useTransform
- **Badges Spring**: Pop animation com stiffness 300/damping 20, rotate -5deg→0deg em badges de expertise/recomendação
- **Estados Elegantes**: EmptyState, PulseLoader (glow roxo/dourado pulsante), ErrorState components criados e integrados
- **Avatar Breathing**: Ring glow ultra-sutil pulsando primary/30→primary/50 a cada 3s nos avatares
- **Page Transitions**: AnimatedPage com blur(0px→4px→0px) + fade + scale coordenados (duration 600ms)
- **Tailwind Durations**: Adicionado duration-400 e duration-600 para timing consistente
- **Design Philosophy**: "Menos é mais" → "Disney-level polish" com micro-interações que encantam

### October 24, 2025 - Visual Refinement "Apple Store Sofisticado"
- **Avatar Photos Fixed**: Added AvatarImage component to Welcome.tsx onboarding tour - all 8 expert photos now display correctly instead of initials
- **Hover Animations Refined**: Updated to ultra-subtle translateY(-2px) scale(1.01) with 600ms duration and type:"tween" for smooth, cinematographic feel (previously -4px/-6px and 1.02-1.05 with faster 300-500ms timing)
- **Border-Radius Systemized**: Cards rounded-3xl (24px), badges rounded-full, buttons rounded-xl (12px) for organic, flowing design
- **Grid Layout Optimized**: Changed from 3 to 2 columns on desktop (md:grid-cols-2) with gap-8 for generous breathing room
- **Typography Weights Lightened**: Removed excessive font-bold, using font-medium/semibold/normal throughout (bold only on main headings)
- **Spacing Increased**: Cards p-8 gap-6 (was p-6 gap-4), sections py-20/24 (was py-16/20), avatars w-24 h-24 (was w-20)
- **Glassmorphism Refined**: backdrop-blur-lg bg-card/30 (was xl/40), more subtle transparency and lighter borders /30
- **Glow Effects Reduced**: Opacities 0.12-0.15 (was 0.3-0.4), spreads 8-30px (was 20-60px) for understated elegance
- **Stagger Timing Extended**: Animation delays 0.15s (was 0.05s-0.1s) for better visual rhythm
- **AnimatedPage Duration**: Increased to 0.6s (was 0.5s) for smoother page transitions
- **design_guidelines.md Updated**: Complete documentation of "Apple Store Sofisticado" philosophy with all refined values

## External Dependencies

- **Anthropic Claude API**: For AI model interactions and cognitive cloning.
- **Perplexity API**: Used for researching target individuals for the auto-cloning feature.
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