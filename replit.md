# AdvisorIA - Replit Agent Guide

## Overview

AdvisorIA is a premium AI consultancy platform featuring cognitive clones of 8 legendary marketing figures. It uses the Framework EXTRACT methodology to create high-fidelity AI personalities via Anthropic's Claude. The platform is built with a React/TypeScript frontend, an Express.js proxy, and a Python/FastAPI backend with async AI integration. Its purpose is to provide expert marketing advice through AI-powered cognitive clones, offering a unique and specialized consulting experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework & Tooling**: React 18 with TypeScript, Vite, Wouter for routing, TanStack Query v5 for server state.
- **UI Component System**: shadcn/ui components on Radix UI, Tailwind CSS for styling. Professional aesthetic inspired by Linear, Notion, and LinkedIn, with dark mode primary and light mode support.
- **State Management**: TanStack Query for server state, React Context for theme, react-hook-form with Zod for forms. No global state library.

### Backend Architecture (Hybrid Proxy + Python)
- **Express.js Proxy Server (Port 5000)**: Lightweight TypeScript proxy forwarding `/api` requests to Python backend, automatic Python backend startup, Vite integration, serves static frontend in production.
- **Python/FastAPI Backend (Port 5001)**: FastAPI for async API routes, AsyncAnthropic client for non-blocking AI calls.
- **API Endpoints**: CRUD operations for experts and conversations, including `auto-clone` and `test-chat` functionalities.
- **Storage Layer**: In-memory Python storage (MemStorage) using Pydantic models for Expert, Conversation, and Message entities.

### AI Integration - Cognitive Cloning
- **Framework EXTRACT Methodology**: Each marketing legend has a detailed system prompt with 8 cognitive layers (Identity Core, Terminology, Reasoning Patterns, Communication Style, Expertise Contexts, Techniques & Methods, Limitations, Meta-Awareness).
- **Implementation**: Uses AsyncAnthropic Claude API (claude-sonnet-4-20250514) for non-blocking calls. System prompts are stored in `python_backend/prompts/legends.py`.
- **Pre-Seeded Legends**: Includes 8 marketing legends like Philip Kotler, David Ogilvy, and Seth Godin, each responding with authentic personality and expertise.

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

## Recent Updates

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