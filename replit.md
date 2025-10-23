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
- **UX/UI Decisions**: Disney-level animations for onboarding, chat interactions, expert cards, suggested questions, and page transitions. Consistent timing (0.3s for micro, 0.5s for macro) and easing function (cubic-bezier(0.4, 0, 0.2, 1)).
- **Personalization**: Expert recommendation system based on user profile (goal, industry, challenge, keywords) and automatic injection of profile context into AI system prompts.

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