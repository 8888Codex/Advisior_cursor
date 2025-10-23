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
- `POST /api/experts` - Create custom cognitive clone (future: guided EXTRACT process)
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
- ⚠️ In-memory storage: Replace with PostgreSQL/Drizzle for persistence
- ⚠️ No authentication system yet (planned: Replit Auth)
- ⚠️ Custom clone creation endpoint exists but lacks guided EXTRACT process
- ⚠️ No streaming responses yet (frontend and backend support needed)
- ⚠️ Error handling could be more granular (distinguish API errors, timeouts, etc.)

**Migration Path**
- Storage: Swap MemStorage for PostgreSQL via Drizzle ORM
- Auth: Integrate Replit Auth for user sessions
- Custom Clones: Add guided multi-step EXTRACT interview process
- Streaming: Implement Server-Sent Events (SSE) for real-time AI responses
- Monitoring: Add logging, metrics, error tracking (e.g., Sentry)

## Recent Changes (October 23, 2025)

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

**Testing**
- End-to-end Playwright tests confirm full user flow working
- AI responses authentic to each legend's personality (verified manually and via tests)
- Concurrent request support confirmed via async client architecture
