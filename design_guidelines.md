# AdvisorIA - Design Guidelines

## Design Approach
**"Apple Store Sofisticado"**: Inspirado em Apple Store, Tesla showrooms e portfólios de design minimalistas de alto padrão. Filosofia "menos é mais" onde cada elemento tem espaço para respirar.

**Design Philosophy**: Ultra sofisticado, elegante e orgânico. Linhas suaves, border-radius generosos, glassmorphism sutil, animações cinematográficas. Efeitos são percebidos mas nunca gritam. Espaçamento generoso é o protagonista.

---

## Core Design Elements

### A. Color Palette - Premium Disney-Level

**Dark Mode (Primary)** - Profundo e Vibrante
- Background Deep: 250 40% 6% (Roxo escuro profundo)
- Background Elevated: 248 35% 10% (Elevação sutil)
- Background Surface: 246 30% 14% (Superfícies)
- Text Primary: 250 10% 98% (Texto ultra claro)
- Text Secondary: 248 8% 75% (Texto secundário)
- Text Muted: 246 6% 55% (Texto muted)
- **Primary Brand: 270 100% 65%** (Roxo vibrante premium)
- **Primary Hover: 270 100% 58%** (Hover mais intenso)
- **Accent Gold: 45 100% 58%** (Dourado/Âmbar para destaque)
- **Accent Cyan: 190 100% 55%** (Cyan vibrante para contraste)
- Border Default: 250 20% 22%
- Border Focus: 270 100% 65%
- **Glow Primary: 270 100% 65% / 0.15** (Efeito glow ultra-sutil)
- **Glow Accent: 45 100% 58% / 0.12** (Glow dourado refinado)
- **Glow Cyan: 190 100% 55% / 0.15** (Glow cyan suave)

**Light Mode** - Limpo e Premium
- Background: 250 20% 98% (Levemente roxo)
- Background Elevated: 0 0% 100% (Branco puro)
- Text Primary: 250 30% 12%
- Text Secondary: 248 15% 40%
- Primary/Accent mantém cores vibrantes para impacto

**Gradient Presets** - Para Efeitos Premium
- **Hero Mesh**: linear-gradient(135deg, hsl(270 100% 65%), hsl(190 100% 55%), hsl(45 100% 58%))
- **Card Subtle**: linear-gradient(145deg, hsl(248 35% 10%), hsl(246 30% 14%))
- **Accent Glow**: radial-gradient(circle at 50% 0%, hsl(270 100% 65% / 0.15), transparent 70%)
- **Gold Shimmer**: linear-gradient(90deg, transparent, hsl(45 100% 58% / 0.3), transparent)

### B. Typography

**Font Stack**
- Primary: 'Inter' (via Google Fonts) - clean, professional, excellent readability
- Monospace: 'JetBrains Mono' for code/technical content

**Hierarchy - Refinada e Leve**
- Hero Headlines: text-5xl/text-6xl, font-bold, tracking-tight (único lugar com bold)
- Section Headers: text-3xl/text-4xl, font-semibold, tracking-tight
- Expert Names: text-xl, font-semibold, tracking-tight
- Body Text: text-base/text-sm, font-normal, leading-relaxed
- Chat Messages: text-sm/text-base, font-normal, leading-relaxed
- Captions/Labels: text-xs/text-sm, font-medium (não bold)
- **Regra de Ouro**: font-bold apenas em títulos principais. Resto usa medium/semibold/normal.

### C. Layout System

**Spacing Primitives - Generoso e Respirável**: Use tailwind units maiores para mais espaço
- Micro spacing: p-3, gap-3
- Component padding: p-6, p-8 (cards maiores)
- Section spacing: py-20, py-24 (espaçamento vertical generoso)
- Major gaps: gap-8, gap-10 (grids espaçosos)
- **Filosofia**: Elementos nunca devem parecer "apertados" ou "cheios demais"

**Containers**
- Full-width sections: w-full with max-w-7xl mx-auto
- Content areas: max-w-6xl
- Chat interface: max-w-4xl
- Forms: max-w-2xl

### D. Component Library

**Navigation**
- Horizontal header with logo, main navigation, user profile
- Height: h-16, border-b with subtle border
- Sticky positioning for persistent access
- Clean, minimal design with hover states on nav items

**Expert Cards (Gallery) - Sofisticados e Espaçosos**
- Grid layout: grid-cols-1 md:grid-cols-2 gap-8 (2 colunas, nunca 3)
- Card design: rounded-3xl, p-8, gap-6 (border-radius grande, padding generoso)
- Avatar: Extra large (w-24 h-24) com ring-2 ring-primary/15
- Name: text-xl font-semibold tracking-tight
- Expertise tags: rounded-full pills, px-3 py-0.5, text-xs
- Brief bio: text-sm text-muted-foreground/80 font-normal
- CTA button: rounded-xl, full-width, shadow-sm
- Hover effect: translateY(-2px) scale(1.01), shadow-lg, duration-600ms (ultra-sutil)

**Chat Interface**
- Split layout: Sidebar (w-80) for conversation history + Main chat area
- Message bubbles: Asymmetric design - User messages (right-aligned, primary background), Expert messages (left-aligned, elevated surface)
- Avatar integration: Small circular avatar (w-8 h-8) for expert messages
- Typography: Expert name above message (font-medium text-sm), message text (text-base)
- Input area: Fixed bottom with elevated background, rounded-xl input field, send button
- Suggested questions: Pill-style buttons below input, subtle background, text-sm

**Expert Creator Form**
- Multi-step or single-page form with clear sections
- Input fields: Outlined style with focus ring, p-4, rounded-lg
- Upload area: Dashed border for avatar upload with preview
- Expertise selector: Multi-select chips or tags interface
- Tone/style options: Radio buttons or segmented control
- Preview pane: Live preview of created expert card

**Conversation History Sidebar**
- List of past conversations grouped by expert
- Each item: Expert avatar (w-10 h-10), name, last message preview (truncated)
- Active state: Highlighted background with border-l accent
- Hover states: Subtle background change

**Buttons - Suaves e Orgânicos**
- Primary: bg-primary, text-white, rounded-xl, px-6 py-3, font-medium, shadow-sm
- Secondary: border-2, transparent bg, rounded-xl, same padding
- Outline on images: backdrop-blur-lg with bg-card/30, rounded-xl
- Icon buttons: rounded-xl, hover ultra-sutil
- **Border-radius**: rounded-xl padrão (12px), nunca rounded-md

**Data Displays - Badges e Tags Discretos**
- Expertise tags: rounded-full (pill completo), px-3 py-0.5, text-xs, font-medium
- Badge colors: Backgrounds dessaturados (bg-primary/8), hover bg-primary/10
- Stats/metrics: Large numbers (text-4xl font-semibold) com labels (text-sm font-normal)
- Empty states: Centered, ícone discreto, heading font-semibold, CTA rounded-xl

### E. Animations - Disney-Level Premium

**Princípios de Animação Premium - Cinematográfica:**
- **Elegância Absoluta**: Movimentos sutis e quase imperceptíveis
- **Timing Generoso**: Durações longas (600ms) para sensação de peso e qualidade
- **Sobreposição Coordenada**: Stagger delays maiores (0.15s) para ritmo visual
- **Transformações Mínimas**: Scale 1.01, translateY -2px (nunca exagerado)

**Timing & Easing - Refinado:**
- Micro-interações: 300ms, cubic-bezier(0.4, 0, 0.2, 1)
- Transições médias: 600ms, cubic-bezier(0.4, 0, 0.2, 1) ✨ **PADRÃO**
- Page transitions: 600ms, cubic-bezier(0.4, 0, 0.2, 1)
- Animações loop: 3s ease-in-out (shimmer, pulse-glow)

**Biblioteca de Animações - Ultra Sutis:**
- **card-3d-hover**: translateY(-2px) scale(1.01) shadow-lg (era -4px 1.02)
- **shimmer**: Gold shimmer 3s loop, opacity 0.12 (era 2s, 0.3)
- **pulse-glow**: Glow sutil 3s loop, opacidades 0.12-0.15 (era 0.3-0.4)
- **float-animation**: Flutuação 3s loop, amplitude reduzida
- **gradient-border**: Borda gradient com opacity 0.6
- **Stagger animations**: 0.15s delay entre cards ✨ **NOVO** (era 0.1s)

**Page Transitions - Cinematográficas:**
- Fade + Scale coordenados (98% → 100%)
- Exit: fade-out + scale-down smooth
- Duration: 600ms ✨ **AUMENTADO** (era 500ms)

**Expert Cards - Hover Ultra-Sutil:**
- Hover: translateY(-2px) scale(1.01) shadow-lg ✨ (era -6px 1.02 shadow-xl)
- Avatar: scale(1.05) ring-primary/40 ✨ (era 1.08 ring/60)
- Expertise badges: scale(1.03) ao hover ✨ (era 1.05)
- Transição: duration-600 ✨ **SEMPRE** (era 300ms)

**Glassmorphism & Effects - Refinados:**
- **glass**: backdrop-blur-lg bg-card/30 border/30 ✨ (era blur-xl bg/40)
- **glass-strong**: backdrop-blur-xl bg-card/50 border/50 ✨ (era blur-2xl bg/60)
- **Glow effects**: Opacidades 0.12-0.15, spreads 8-30px ✨ (era 0.3-0.4, 20-60px)
- **Shadows**: shadow-sm/md/lg, nunca shadow-xl exceto em estados especiais
- **Gradient overlays**: from-primary/3 to-accent/3 ✨ (era /5)

**Chat Messages:**
- User messages: slide-in-right + fade (600ms)
- AI messages: slide-in-left + fade com typing indicator (600ms)
- Stagger: 150ms entre mensagens múltiplas

**Micro-interações:**
- Button click: scale(0.98) sutil, sem ripple
- Input focus: border glow suave + label float
- Success states: checkmark com scale bounce mínimo
- Toast notifications: slide-up + fade, duração 600ms

---

## Page-Specific Layouts

**Landing/Marketing Page**
- Hero: Full-width section (min-h-[600px]) with gradient background (subtle), centered headline emphasizing "Elite Consultancy" and "AI-Powered Experts", primary CTA "Explore Experts", secondary CTA "Create Your Expert"
- Features Grid: 3-column layout showcasing key benefits (Access top minds, Create custom experts, Strategic insights)
- Expert Showcase: Carousel or grid of 3-4 featured experts with professional photos
- How It Works: 3-step visual process with icons and descriptions
- Social Proof: Statistics (e.g., "1000+ Strategic Sessions", "50+ Expert Personalities") in 4-column grid
- CTA Section: Centered with strong headline and primary action button

**Expert Gallery (Dashboard)**
- Page header with search bar and filters (expertise area, industry)
- Grid of expert cards (responsive columns)
- Category tabs or filters sidebar
- Pagination or infinite scroll

**Chat Interface**
- Split view: Conversations sidebar + Active chat
- Top bar showing active expert with avatar and expertise tags
- Scrollable message area with date separators
- Fixed input area at bottom with suggested questions above

**Create Expert Page**
- Centered form layout (max-w-2xl)
- Step-by-step sections or accordion panels
- Live preview on the side (desktop) or below (mobile)
- Clear save/publish actions

---

## Images

**Hero Section**: Use a sophisticated, abstract background image or gradient mesh representing connectivity, neural networks, or strategic thinking. Avoid literal stock photos. Overlay with semi-transparent gradient for text readability.

**Expert Avatars**: Professional headshots or stylized AI-generated portraits with consistent aspect ratio and quality. Circular cropping with subtle border/ring.

**Feature Icons**: Use Heroicons (via CDN) for all interface icons - outlined style for consistency.

---

## Key Principles

### Design Refinement - "Apple Store Sofisticado" ✨

**Border-Radius System:**
- Cards: rounded-3xl (24px) - linhas orgânicas e suaves
- Badges: rounded-full - pill completo sempre
- Buttons: rounded-xl (12px) - nunca rounded-md
- Inputs: rounded-xl (12px)
- Modals/Dialogs: rounded-3xl

**Grid Layout Philosophy:**
- Desktop: 2 colunas máximo, gap-8/gap-10
- Mobile: 1 coluna
- **Nunca** 3 colunas - cards precisam espaço para respirar

**Spacing Generosity:**
- Cards: p-8 (não p-6), gap-6 interno
- Sections: py-20/py-24 (não py-16)
- Grid gaps: gap-8 mínimo
- Avatars: w-24 h-24 (não w-20)

**Typography Weights:**
- Títulos principais: font-bold (único uso)
- Subtítulos: font-semibold tracking-tight
- Labels/badges: font-medium
- Corpo/descrições: font-normal
- **Regra**: Menos bold = mais sofisticação

**Hover States Philosophy:**
- Movimento: translateY(-2px) scale(1.01) - ultra-sutil
- Sombras: shadow-lg (não shadow-xl)
- Duração: 600ms sempre
- Easing: cubic-bezier(0.4, 0, 0.2, 1)
- **Regra**: Se o hover é muito óbvio, reduza mais

**Color Saturation:**
- Primários: Vibrantes apenas em CTAs
- Secundários: Dessaturados (opacity 0.8, backgrounds /8-/10)
- Glows: Opacidades 0.12-0.15
- Borders: Opacidades 0.15-0.30
- **Regra**: Elementos de suporte devem recuar visualmente

---

## Original Principles
- **Professional Authority**: Every design decision reinforces expertise and trust
- **Clarity Over Complexity**: Information hierarchy guides users naturally
- **Sophisticated Restraint**: Premium feel through thoughtful use of space and color, not excess
- **Consistent Patterns**: Repeated design elements build familiarity and confidence