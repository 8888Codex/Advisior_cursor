# AdvisorIA - Replit Agent Guide

## Overview
AdvisorIA is a premium AI consultancy platform offering expert advice through cognitive clones of 18 specialists across 15 disciplines. It leverages the "Framework EXTRACT de 12 Camadas" with Anthropic's Claude to create ultra-realistic AI personalities. The platform features a React/TypeScript frontend, an Express.js proxy, and a Python/FastAPI backend with asynchronous AI integration, aiming to provide a specialized multi-category consulting experience.

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
- **UX/UI Decisions ("Disney-Level Premium" & "Apple Store Sofisticado")**:
    - **Color Palette**: Vibrante roxo (primary), dourado (accent), cyan (accent-cyan), deep dark mode.
    - **Visual Effects**: Glassmorphism (backdrop-blur-lg), subtle glow effects, text gradients, animated background gradients (mesh).
    - **Animations**: Shimmer, 3D hover transforms for cards, pulse-glow, animated gradient borders, coordinated stagger animations with `Framer Motion`.
    - **Micro-Interactions**: Press effects, ripple animations, skeleton loaders, cinematic toasts, parallax hero, badge spring animations, avatar breathing effect, smooth page transitions.
    - **Design System**: Standardized border-radius, optimized grid layouts (2-column desktop), refined typography weights, generous spacing, and consistent animation timings (e.g., 0.6s for page transitions).
- **Multi-Category Navigation System**:
    - **Categories**: 15 distinct categories (marketing, growth, psychology, etc.) with dedicated styling and icons.
    - **Category Page**: Grid layout with glassmorphism cards and coordinated entry animations.
    - **Expert Filtering**: Dropdown filter, category badges on cards, and "Limpar Filtros" button.
    - **URL Sync**: Custom `useURLSearchParam` hook with polling and event listeners for robust UI-URL synchronization.
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