# AdvisorIA - Replit Agent Guide

## Overview

AdvisorIA is a premium AI consultancy platform that democratizes access to elite strategic expertise. The platform enables users to consult with digital clones of renowned experts or create custom AI consultants to solve complex business challenges. Built with a focus on professional aesthetics and sophisticated user experience, it combines TypeScript/React frontend with Express.js backend and Anthropic's Claude AI for intelligent consultations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework & Tooling**
- **React 18** with TypeScript for type-safe component development
- **Vite** as the build tool and development server
- **Wouter** for lightweight client-side routing (not React Router)
- **TanStack Query** for server state management and API calls

**UI Component System**
- **shadcn/ui** components built on Radix UI primitives (New York style variant)
- **Tailwind CSS** for utility-first styling with custom design tokens
- **CVA (Class Variance Authority)** for component variant management
- Components follow a professional, premium aesthetic inspired by Linear, Notion, and LinkedIn

**Design System**
- Dark mode as primary theme with comprehensive light mode support
- Custom color palette focused on professional blues and purples
- Typography using Inter (primary) and JetBrains Mono (monospace)
- Consistent spacing system using Tailwind's scale (2, 4, 6, 8, 12, 16, 20, 24)

**State Management Pattern**
- Server state managed via TanStack Query with custom query client
- Theme state managed through React Context (ThemeProvider)
- Form state handled by react-hook-form with Zod validation
- No global application state library (Redux/Zustand) - component-level state preferred

### Backend Architecture

**Server Framework**
- **Express.js** with TypeScript for type-safe API development
- RESTful API design pattern for all endpoints
- Custom middleware for request logging and JSON parsing
- Vite integration for development mode with HMR support

**API Structure**
- `/api/experts` - Expert CRUD operations
- `/api/conversations` - Conversation management
- `/api/messages` - Message history and creation
- All endpoints follow consistent error handling patterns

**Storage Layer**
- **In-memory storage** (MemStorage class) currently used for development
- Designed to support database migration (Drizzle ORM schema already defined)
- UUID-based identifiers for all entities
- Schema definitions in `shared/schema.ts` using Drizzle ORM and Zod

### External Dependencies

**AI Integration**
- **Anthropic Claude API** (claude-sonnet-4-20250514 model)
- System prompts define expert personalities and consultation styles
- Streaming chat support available but not yet implemented in UI
- Each expert has a custom systemPrompt stored in database

**Database**
- **PostgreSQL** via Neon serverless driver (configured but not yet actively used)
- **Drizzle ORM** for type-safe database operations
- Migration system configured via `drizzle-kit`
- Schema includes: users, experts, conversations, messages tables

**Third-Party UI Libraries**
- **Radix UI** primitives for accessible components
- **Lucide Icons** for consistent iconography
- **date-fns** for date formatting
- **react-markdown** with remark-gfm for rendering expert responses

**Session Management**
- **connect-pg-simple** configured for PostgreSQL session storage
- Currently not actively used (authentication system pending)

### Key Architectural Decisions

**Monorepo Structure**
- `/client` - React frontend application
- `/server` - Express backend application  
- `/shared` - Shared types and schemas (Drizzle + Zod)
- Path aliases configured for clean imports (`@/`, `@shared/`, `@assets/`)

**Data Flow Pattern**
1. User interacts with UI components
2. TanStack Query manages API calls via custom queryClient
3. Express routes handle requests and validate with Zod schemas
4. Storage layer (currently in-memory, designed for database)
5. Anthropic API called for AI responses
6. Response streamed back through storage to client

**Development vs Production**
- Development: Vite dev server with HMR, in-memory storage
- Production: Built static files served by Express, ready for database integration
- Environment variables for Anthropic API key and database URL

**Migration Path**
- Application ready to migrate from MemStorage to PostgreSQL
- Drizzle schema and migrations directory already configured
- Simply connect storage.ts to database instead of in-memory maps