# AdvisorIA - Design Guidelines

## Design Approach
**Hybrid Approach**: Drawing from premium professional platforms (Linear's typography + Notion's clean interfaces + LinkedIn's professional aesthetics) combined with custom consultancy-specific patterns.

**Design Philosophy**: Elite, sophisticated, and trustworthy. The platform should convey expertise, authority, and premium quality while remaining accessible and intuitive.

---

## Core Design Elements

### A. Color Palette

**Dark Mode (Primary)**
- Background Deep: 220 25% 8%
- Background Elevated: 220 20% 12%
- Background Surface: 220 18% 15%
- Text Primary: 220 10% 95%
- Text Secondary: 220 8% 70%
- Text Muted: 220 6% 50%
- Primary Brand: 210 100% 56% (Professional blue conveying trust)
- Primary Hover: 210 100% 48%
- Accent Subtle: 280 45% 58% (Purple for premium features)
- Border Default: 220 15% 22%
- Border Focus: 210 100% 56%

**Light Mode**
- Background: 220 10% 98%
- Background Elevated: 0 0% 100%
- Text Primary: 220 20% 15%
- Text Secondary: 220 12% 40%
- Primary remains consistent for brand recognition

### B. Typography

**Font Stack**
- Primary: 'Inter' (via Google Fonts) - clean, professional, excellent readability
- Monospace: 'JetBrains Mono' for code/technical content

**Hierarchy**
- Hero Headlines: text-5xl/text-6xl, font-bold, tracking-tight
- Section Headers: text-3xl/text-4xl, font-semibold
- Expert Names: text-2xl, font-semibold
- Body Text: text-base, font-normal, leading-relaxed
- Chat Messages: text-sm/text-base, leading-relaxed
- Captions/Labels: text-xs/text-sm, font-medium, uppercase tracking-wide

### C. Layout System

**Spacing Primitives**: Use tailwind units of 2, 4, 6, 8, 12, 16, 20, 24 consistently
- Micro spacing: p-2, gap-2
- Component padding: p-4, p-6
- Section spacing: py-12, py-16, py-20
- Major gaps: gap-8, gap-12, gap-16

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

**Expert Cards (Gallery)**
- Grid layout: grid-cols-1 md:grid-cols-2 lg:grid-cols-3
- Card design: Elevated surface with subtle border, rounded-xl
- Avatar: Large circular image (w-20 h-20) with ring-2 in brand color
- Name: text-xl font-semibold
- Expertise tags: Small pills with background-subtle and text-xs
- Brief bio: text-sm text-muted, 2-3 lines with line-clamp
- CTA button: "Consult Expert" - primary button, full-width
- Hover effect: Subtle lift (shadow-lg) and border glow

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

**Buttons**
- Primary: bg-primary, text-white, rounded-lg, px-6 py-3, font-medium, shadow-sm
- Secondary: border-2 border-current, transparent background, same padding
- Outline on images: backdrop-blur-md with semi-transparent background
- Icon buttons: p-2, rounded-lg, hover:bg-surface

**Data Displays**
- Expertise tags: Rounded-full, px-3 py-1, text-xs, font-medium, subtle backgrounds
- Stats/metrics: Large numbers (text-4xl font-bold) with labels (text-sm text-muted)
- Empty states: Centered content with icon, heading, description, CTA

### E. Animations
Use sparingly and purposefully:
- Page transitions: Subtle fade-in (200ms)
- Card hover: Transform scale(1.02) with shadow transition (150ms)
- Button interactions: Built-in states only
- Chat messages: Gentle slide-in from appropriate side (300ms)
- Loading states: Subtle pulse on skeleton screens

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
- **Professional Authority**: Every design decision reinforces expertise and trust
- **Clarity Over Complexity**: Information hierarchy guides users naturally
- **Sophisticated Restraint**: Premium feel through thoughtful use of space and color, not excess
- **Consistent Patterns**: Repeated design elements build familiarity and confidence