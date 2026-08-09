# AI-Powered Adaptive Learning Platform
## Design System (v1.0)

**Prepared by:** Principal Product Designer
**Grounded in:** `PROJECT_BLUEPRINT.md` (v1.0)
**Audience:** Frontend engineers, product designers, QA
**Purpose:** This is the single source of design truth. Any screen, component, or state not explicitly covered here should be resolved by applying the principles in Section 24 — not by improvising a new pattern.

---

## Table of Contents

1. Design Philosophy
2. Color Palette
3. Typography
4. Spacing System
5. Border Radius
6. Shadows
7. Iconography
8. Buttons
9. Inputs
10. Cards
11. Navigation
12. Dashboard Widgets
13. Charts
14. Tables
15. Forms
16. Modals
17. Notifications
18. Loading States
19. Empty States
20. Animations
21. Accessibility
22. Responsive Design
23. Design Tokens
24. UI Principles
25. Things to Avoid

---

## 1. Design Philosophy

### 1.1 The core idea: make partial knowledge *visible*

Every other e-learning product treats "progress" as a single number climbing toward 100%. This platform's entire premise (per the Blueprint's knowledge graph and concept-level mastery model) is that knowledge is **granular, partial, and state-based** — a learner is never simply "50% done," they are *Mastered* on seven concepts, *Partial* on three, *Weak* on two, and haven't touched the rest. The interface's job is to make that texture visible at a glance, everywhere, without needing a report to explain it.

This becomes the platform's one signature visual idea, carried through the whole system:

> **The Mastery Fill.** A single, reusable visual grammar — a segmented, state-colored fill — that appears identically in the knowledge graph, the video scrubber, progress rings, path steps, and even button loading states. Once a learner understands what a green segment vs. an amber segment vs. an outlined segment means in one place, they understand it everywhere.

This is not decoration. It is load-bearing information architecture, and it is the one place we spend visual boldness. Everything else in the system stays quiet and disciplined around it.

### 1.2 Visual identity

- **Professional, not corporate.** Confident typography, restrained color, real content over icons-and-gradients filler — closer to a Stripe dashboard than a marketing site.
- **Minimal, not empty.** Generous whitespace, but every element earns its place; density is used deliberately in data-heavy views (analytics, tables) and never in learning views (assessment, tutor).
- **Premium, not luxurious.** No skeuomorphism, no ornamental gradients, no stock-photo warmth. Premium here means precision: consistent 4px spacing, pixel-aligned icons, deliberate motion.
- **AI-first, not AI-decorated.** AI-generated content (tutor replies, recommendations, insights, auto-generated segments/quizzes) is *visually distinguishable* from human/system content at all times, using a single consistent accent (Section 2.3) — never a sparkle emoji bolted onto everything.
- **Student-friendly, not childish.** Gamification (streaks, XP, badges) is real but restrained — a small gold accent and a calm animation, never confetti-cannon energy on every interaction.

### 1.3 Emotional targets

| We want the learner to feel | We avoid the interface feeling |
|---|---|
| In control of their own time | Like they're being lectured at |
| Respected for what they already know | Punished with review of known material |
| Calm focus during learning, quiet momentum during review | Anxious ("test" framing) or bored (dense text walls) |
| Quiet pride when a concept turns green | Cheap gamified dopamine (badges for badges' sake) |
| Trust in the AI's judgment | Uncertainty about what the AI changed and why |

### 1.4 Why this supports learning

- **Reduced cognitive load:** a consistent fill/state grammar means the learner spends zero effort re-learning what a screen means; all effort goes to the subject matter.
- **Transparency builds trust in skipping:** because AI Video Segmentation auto-skips content (Blueprint §9), the interface must always show *why* — a visible mastery fill on the scrubber turns an opaque AI decision into an obviously fair one.
- **Calm data reduces anxiety:** adaptive assessments (Blueprint §9.1) already carry test-anxiety risk; the UI intentionally hides live scoring during assessments and reveals results only as calm, structured concept breakdowns afterward.
- **Restraint respects the learner's time:** the platform's entire value proposition is "don't waste my time" — a cluttered, over-animated UI would directly contradict the product's promise.

### 1.5 Reference triangulation

| Borrowed from | What we take | What we deliberately don't take |
|---|---|---|
| **Linear** | Speed, keyboard-first affordances, restrained motion, dark-mode-first engineering discipline | Its near-monochrome palette (we need semantic color for mastery states) |
| **Notion** | Calm neutral surfaces, generous content breathing room, quiet iconography | Its block-editor visual looseness (our data views need more structure) |
| **GitHub** | Dense, trustworthy data tables and diffs; clear status chips | Its heavier borders-everywhere grid |
| **Duolingo** | Warmth in streaks/gamification, one confident accent for achievement | Its saturated, cartoon-adjacent palette and mascot energy |
| **Stripe Dashboard** | Precise data visualization, confident use of a single brand blue, exceptional form/table polish | Its marketing-site gradient flourishes |

---

## 2. Color Palette

### 2.1 System principle

The palette has exactly **two brand hues** (Primary, Secondary) and **one gamification accent** — everything else is semantic or neutral. Concept-mastery states reuse the semantic palette directly (Mastered = Success, Partial = Warning, Weak = Danger, Unknown = Muted) rather than inventing a parallel color language. This is a deliberate constraint: it keeps the system small enough that every color in the product means exactly one thing.

### 2.2 Full palette

| Token | Light | Dark | Usage | Rationale |
|---|---|---|---|---|
| **Primary** | `#3B33D6` | `#7C74FF` | Primary buttons, active nav, links, focus rings, selected states | A confident blue-violet — reads as "intelligent/technical" without tipping into generic Tailwind indigo or any AI-lab house color. This is the *user's* action color. |
| **Primary Hover** | `#332BC2` | `#8F88FF` | Hover on primary elements | ~8% darker (light) / lighter (dark) for clear but subtle feedback |
| **Primary Pressed** | `#2A23A3` | `#9FA0FF` | Active/pressed state | ~16% shift for tactile confirmation |
| **Secondary (AI Signal)** | `#0F9E93` | `#3DD9C9` | Anything AI *generated or decided*: tutor bubbles, AI recommendation cards, AI-insight callouts, "AI is thinking" states | A distinct teal, deliberately different from Primary's blue-violet, so learners can tell "I did this" (indigo) from "the AI did this" (teal) at a glance |
| **Accent (Streak Gold)** | `#D98C00` | `#F2B94A` | Gamification only: streak flame, XP counters, badges, celebratory highlights | Warm and earned-feeling without being childish; used sparingly so it retains impact |
| **Success (Mastered)** | `#1A9450` | `#3FCE84` | Mastered concept state, success toasts, positive deltas | Calm, confident green — not neon |
| **Warning (Partial)** | `#B87500` | `#E3A53D` | Partial-mastery concept state, caution banners | Distinguished from Accent gold by being more amber/brown, less bright |
| **Danger (Weak)** | `#C6303E` | `#F0616E` | Weak concept state, destructive actions, validation errors | Never used for anything except a real problem or a real knowledge gap — see §25 |
| **Info** | `#2170D8` | `#5B9BFF` | Neutral informational banners, tooltips | A cooler, calmer blue than Primary so it doesn't compete with action color |
| **Background** | `#F6F7FB` | `#0B0C10` | App canvas | Slightly cool off-white / true near-black, never pure `#FFFFFF`/`#000000` |
| **Surface** | `#FFFFFF` | `#15171E` | Cards, panels, modals | One step lighter than Background, creating layering without shadows alone |
| **Surface Raised** | `#FFFFFF` + shadow-md | `#1C1F29` | Popovers, dropdown menus, floating toolbars | Slightly higher elevation than Surface |
| **Border** | `#E3E5EC` | `#262A35` | Dividers, card outlines, input borders | Low-contrast, structural only — never used to create emphasis |
| **Border Strong** | `#C7CBD6` | `#363B49` | Focus-adjacent borders, active input outlines | Reserved for states that need more definition |
| **Text Primary** | `#12141C` | `#F3F4F7` | Headings, primary body copy | Near-black/near-white ink, not pure for reduced eye strain |
| **Text Secondary** | `#565C6E` | `#A6ACBD` | Supporting copy, descriptions, table secondary columns | |
| **Muted / Unknown state** | `#9AA0B0` | `#6C7284` | Placeholder text, disabled labels, "Unknown" concept state (unfilled outline) | Deliberately the *only* state with no fill — visually communicates "nothing learned yet" |
| **Disabled Surface** | `#EEF0F4` | `#1B1D24` | Disabled buttons/inputs background | |
| **Disabled Text** | `#B7BBC7` | `#4B505F` | Disabled button/input text | |

### 2.3 Concept-mastery color mapping (critical, reused everywhere)

| Mastery State | Color Token | Fill Behavior |
|---|---|---|
| Mastered | Success `#1A9450` | 100% solid fill |
| Partial | Warning `#B87500` | Partial fill proportional to mastery % |
| Weak | Danger `#C6303E` | Low fill (10–30%), always at least a sliver visible — never fully empty, to avoid reading as "broken" |
| Unknown | Muted `#9AA0B0` | Outline only, 0% fill — no color inside |

This exact mapping drives the Knowledge Graph, video scrubber, path steps, and progress rings (Sections 12–13). It is never reassigned to unrelated UI (e.g., Success green must not also mean "form saved" in a context where it could be confused with "concept mastered" — use a distinct toast style instead, per Section 17).

---

## 3. Typography

### 3.1 Typeface roles

| Role | Typeface | Fallback stack | Why |
|---|---|---|---|
| **Display** | Geist | `"Geist", "Inter", system-ui, sans-serif` | A modern grotesk with just enough character in its numerals and terminals to feel technical/premium — used sparingly, only for hero moments and page-level titles |
| **Heading** | Geist | same | Same family as Display at lower weight/size, keeping the system to two families total |
| **Subheading / Body** | Inter | `"Inter", system-ui, sans-serif` | Exceptional legibility at small sizes — essential for dense dashboards, tables, and long-form tutor conversations |
| **Caption / Labels** | Inter | same, uppercase + tracked | Used for eyebrows, table headers, badges |
| **Code / Data / Monospace** | JetBrains Mono | `"JetBrains Mono", ui-monospace, monospace` | Coding exercises, inline code in AI Tutor answers, numeric data in tables where digit alignment matters |

### 3.2 Type scale

| Token | Size | Line Height | Weight | Letter Spacing | Typeface | Example Use |
|---|---|---|---|---|---|---|
| Display XL | 48px | 1.1 | 700 | -0.02em | Geist | Marketing/landing hero only |
| Display L | 36px | 1.15 | 700 | -0.02em | Geist | Dashboard page title (e.g., "Python") |
| Heading 1 | 30px | 1.2 | 600 | -0.01em | Geist | Section titles (e.g., "Knowledge Graph") |
| Heading 2 | 24px | 1.25 | 600 | -0.01em | Geist | Card group titles, modal titles |
| Heading 3 | 20px | 1.3 | 600 | 0 | Geist | Card titles, widget titles |
| Subheading | 18px | 1.4 | 500 | 0 | Inter | Sub-sections within a card |
| Body Large | 16px | 1.6 | 400 | 0 | Inter | Primary reading copy, tutor chat |
| Body | 14px | 1.6 | 400 | 0 | Inter | Default UI text, table cells, form labels |
| Caption | 12px | 1.4 | 500 | +0.04em (uppercase) | Inter | Eyebrows, badges, table headers, timestamps |
| Micro | 11px | 1.3 | 500 | +0.02em | Inter | Chart axis labels, footnotes |
| Code | 14px | 1.6 | 400–500 | 0 | JetBrains Mono | Code blocks, inline code |

### 3.3 Weight usage rules

- **700** — Display only. Never body text.
- **600** — Headings, active nav items, emphasized numbers (e.g., mastery %).
- **500** — Labels, captions, medium emphasis inline text, button labels.
- **400** — All default body copy.

---

## 4. Spacing System

### 4.1 Base unit

All spacing is derived from a **4px base unit**. No arbitrary values (e.g., no 15px or 22px paddings).

| Token | Value |
|---|---|
| `space-1` | 4px |
| `space-2` | 8px |
| `space-3` | 12px |
| `space-4` | 16px |
| `space-5` | 20px |
| `space-6` | 24px |
| `space-8` | 32px |
| `space-10` | 40px |
| `space-12` | 48px |
| `space-16` | 64px |
| `space-20` | 80px |
| `space-24` | 96px |

### 4.2 Applied spacing

| Context | Value |
|---|---|
| Card padding (standard) | `space-6` (24px) |
| Card padding (dense/mobile) | `space-4` (16px) |
| Card internal element gap | `space-3` (12px) |
| Grid gutter (dashboard) | `space-6` (24px) |
| Grid gutter (mobile) | `space-4` (16px) |
| Section spacing (dashboard, between widget groups) | `space-10` (40px) |
| Section spacing (marketing/landing) | `space-20`–`space-24` (80–96px) |
| Form field vertical gap | `space-5` (20px) |
| Sidebar item padding | `space-3` vertical / `space-4` horizontal |
| Page margin (desktop) | `space-8` (32px) |
| Page margin (mobile) | `space-4` (16px) |

### 4.3 Grid & container widths

| Breakpoint context | Max container width | Columns |
|---|---|---|
| Dashboard (default) | 1280px | 12-column, 24px gutter |
| Wide analytics views | 1440px | 12-column, 24px gutter |
| Reading views (AI Tutor, notes, articles) | 760px (optimal line length ~70ch) | Single column |
| Mobile | 100% fluid | 4-column, 16px gutter |

---

## 5. Border Radius

| Element | Radius | Notes |
|---|---|---|
| Buttons | 8px | Consistent across all button variants |
| Inputs | 8px | Matches buttons for visual rhythm |
| Cards | 16px | Slightly larger than inputs — cards are containers, not controls |
| Small cards / widgets | 12px | Dashboard widgets, stat tiles |
| Dialogs / Modals | 20px | Largest radius, reinforces "floating above the page" |
| Dropdowns / Popovers | 12px | |
| Images / video thumbnails | 12px | |
| Avatars | 999px (full circle) | |
| Badges / Pills / Tags | 999px (full pill) | |
| Toasts | 12px | |

**Rule:** radius scales *up* with elevation (buttons < cards < modals). Never mix a sharp 0px element with a 20px element in the same visual group.

---

## 6. Shadows

Shadows use a **brand-tinted neutral** (a very low-opacity indigo, not pure black) to feel premium rather than muddy.

| Token | Value (light mode) | Usage |
|---|---|---|
| `shadow-xs` | `0 1px 2px rgba(29, 27, 84, 0.04)` | Inputs, subtle separation |
| `shadow-sm` | `0 2px 4px rgba(29, 27, 84, 0.06)` | Default card resting state |
| `shadow-md` | `0 6px 16px rgba(29, 27, 84, 0.08)` | Hovered cards, dropdown menus |
| `shadow-lg` | `0 12px 32px rgba(29, 27, 84, 0.12)` | Modals, dialogs |
| `shadow-floating` | `0 16px 48px rgba(29, 27, 84, 0.18)` | FAB, AI Tutor floating launcher, toasts |

In dark mode, shadows are replaced primarily by a 1px `Border` outline plus a reduced-opacity version of the same shadow (elevation in dark UI reads better through contrast than through shadow alone).

---

## 7. Iconography

### 7.1 Library

**Recommendation: Lucide Icons.** Consistent 24×24 grid, 2px stroke, MIT-licensed, actively maintained, and shares the same geometric restraint as Linear/Notion's internal icon sets — avoids the "generic Bootstrap glyph" look explicitly called out to avoid.

### 7.2 Sizes

| Token | Size | Usage |
|---|---|---|
| `icon-sm` | 16px | Inline with Body/Caption text, table rows |
| `icon-md` | 20px | Buttons, form fields, nav items |
| `icon-lg` | 24px | Section headers, empty states |
| `icon-xl` | 32px | Empty-state illustration accents, onboarding |

### 7.3 Color rules

- Default icon color: `Text Secondary`.
- Active/selected icon (e.g., current nav item): `Primary`.
- Destructive icon (e.g., delete): `Danger`.
- AI-context icon (e.g., tutor launcher, "AI generated" tag): `Secondary`.
- Icons are never colored decoratively — color always encodes state or ownership (user vs. AI vs. system).

### 7.4 Filled vs. outlined

- **Outlined = default/inactive state** for all navigation and action icons.
- **Filled = active/selected/completed state only** — e.g., a filled checkmark-circle for a mastered concept, a filled nav icon for the current section, a filled bookmark once saved.
- Never mix filled and outlined icons of the same glyph within one component group (e.g., a tab bar must be all-outlined except the active tab, never a mix within inactive tabs).

---

## 8. Buttons

| Variant | Background | Text | Border | Use |
|---|---|---|---|---|
| **Primary** | `Primary` | White | none | One per screen/section — the single most important action |
| **Secondary** | `Surface` | `Text Primary` | `Border Strong` 1px | Default action button, used liberally |
| **Outline** | transparent | `Primary` | `Primary` 1px | Secondary emphasis on colored/dark surfaces |
| **Ghost** | transparent | `Text Secondary` | none | Low-emphasis actions inside dense UI (table rows, cards) |
| **Danger** | `Danger` | White | none | Destructive confirmation only |
| **AI Action** | `Secondary` (teal) | White | none | Explicit AI-initiated actions ("Ask AI Tutor," "Regenerate quiz") — visually ties the action to the AI signal color |

### 8.1 Sizing & interaction spec

| Property | Small | Default | Large |
|---|---|---|---|
| Height | 32px | 40px | 48px |
| Horizontal padding | 12px | 16px | 20px |
| Radius | 8px | 8px | 8px |
| Font | Body / 500 | Body / 500 | Body Large / 500 |
| Icon gap | 6px | 8px | 8px |

- **Hover:** background shifts to the `-Hover` token (Section 2); transition `120ms ease-out`; no scale change.
- **Active/Pressed:** background shifts to `-Pressed` token; scale `0.98` over `80ms`.
- **Focus (keyboard):** 2px `Primary` outline, 2px offset from the button edge — visible on all variants, including Ghost.
- **Loading:** label is replaced by a 16px spinner in the button's foreground color; button retains its width (no layout shift); button is non-interactive but not visually "disabled" (still full opacity).
- **Disabled:** background → `Disabled Surface`, text → `Disabled Text`, cursor `not-allowed`, no hover/active response.
- **Icon Button:** square, same heights as above (32/40/48), icon centered, no visible border at rest — a `Surface`-tinted circular/8px-radius background appears on hover only.
- **Floating Action Button (FAB):** reserved exclusively for the **AI Tutor launcher** — 56px circle, `Secondary` background, `shadow-floating`, fixed bottom-right, persists across all learner-facing screens except the assessment flow (assessments intentionally suppress the tutor to protect measurement integrity).

---

## 9. Inputs

All input types share a **40px default height**, 8px radius, 1px `Border`, 14px Body text, and a consistent state model:

| State | Border | Background | Notes |
|---|---|---|---|
| Default | `Border` | `Surface` | |
| Hover | `Border Strong` | `Surface` | |
| Focus | `Primary` 2px | `Surface` | Focus ring, no layout shift (border-box sizing) |
| Error | `Danger` 2px | `Surface` | Paired with inline error message below (Section 15) |
| Success | `Success` 2px | `Surface` | Used briefly after async validation (e.g., username availability) |
| Disabled | `Border` | `Disabled Surface` | Text at `Disabled Text` |

### 9.1 Component-specific notes

| Component | Spec |
|---|---|
| **Text Field** | Label above (Caption, `Text Secondary`), 12px horizontal padding, optional leading/trailing icon at `icon-md` |
| **Dropdown / Select** | Same shell as Text Field; chevron-down icon trailing; opens a `Surface Raised` panel below with 12px radius and `shadow-md` |
| **Search** | Pill-shaped variant available (999px radius) for global search in Top Navigation only; standard 8px radius elsewhere; leading search icon always present |
| **Checkbox** | 18×18px, 4px radius; checked state = `Primary` fill with white check icon; indeterminate = `Primary` fill with horizontal dash |
| **Radio** | 18×18px circle; checked state = `Primary` ring with 8px filled center dot |
| **Toggle** | 40×24px track; off = `Border Strong` track; on = `Primary` track; 20px thumb, `100ms` slide transition |
| **Date Picker** | Text Field trigger + `Surface Raised` calendar popover; selected day = `Primary` fill circle; today = `Primary` 1px outline (unfilled) |
| **OTP Input** | 6 individual 44×48px boxes, 8px radius, 8px gap, auto-advance focus, monospace (`JetBrains Mono`) digits at 20px |

### 9.2 Validation states

- Errors appear **inline below the field**, never as a modal or toast for form-level validation.
- Error copy is specific and actionable ("Password needs at least 8 characters," never "Invalid input").
- Success is shown subtly (border color + small check icon) — never a celebratory animation for routine form success (that vocabulary is reserved for mastery/streak moments, per §1.5).

---

## 10. Cards

All cards share the base shell: `Surface` background, 16px radius (12px for small widgets), `shadow-sm` at rest, `shadow-md` on hover (only if interactive/clickable), `Border` 1px.

| Card | Anatomy | Product-specific detail |
|---|---|---|
| **Course/Subject Card** | Thumbnail or icon, title, concept-count subtitle, Mastery Fill ring (Section 13) | Ring shows aggregate mastery across all concepts in that subject at a glance |
| **Analytics Card** | Caption label, large numeric value (Heading 1, tabular numerals), trend delta (small arrow + Success/Danger colored %) | Used for single-metric widgets (streak, study hours, retention score) |
| **Profile Card** | Avatar (999px), name, role badge, Learner Profile summary (style/speed/duration/time as small tags) | Learning Goal shown as a colored pill using `Secondary` (AI-set weighting is visible, not hidden) |
| **Video Card** | Thumbnail with segmented mini-scrubber preview overlay (colored ticks per concept segment), duration badge, "X min skipped for you" tag when applicable | The skipped-time tag is the single most important trust-building element on this card — always visible, never hidden in a tooltip |
| **Achievement/Badge Card** | Icon in a circular `Accent`-tinted background, title, earned date, subtle shine-sweep animation on first reveal only | Never animates on every view — only the moment it's newly earned |
| **Statistics Card** | Compact variant of Analytics Card, used in dense grid layouts (Admin/Instructor dashboards) | No trend delta; value + label only, to reduce visual noise at scale |
| **Empty State Card** | Centered icon (`icon-xl`, `Muted`), Heading 3 message, Body Secondary sub-copy, single primary CTA | See Section 19 for full copy guidance |

---

## 11. Navigation

| Pattern | Spec |
|---|---|
| **Top Navigation** | 64px height, `Surface` background, `Border` bottom hairline. Left: logo + current subject switcher. Center: global search (pill input). Right: notifications bell, AI Tutor quick icon, avatar menu. |
| **Sidebar** | 264px expanded / 72px collapsed (icon rail), `Surface` background, persists on desktop/laptop. Contains: subject switcher, learning path as a **vertical Mastery Fill trail** (each step is a small filled/outlined circle connected by a line — mirrors the video scrubber grammar), and secondary links (Analytics, Planner, Settings). |
| **Mobile Navigation** | Bottom tab bar, 64px height, 4–5 items max (Home, Path, Tutor, Analytics, Profile), `Surface` background with top `Border` hairline, active icon filled + `Primary` label |
| **Breadcrumb** | Caption-sized, `Text Secondary` with `Text Primary` on the current page; `/` separators using `Muted` color; truncates to last 2 levels on mobile |
| **Tabs** | Underline style (not filled pills) for content-switching within a page (e.g., "Overview / Analytics / Resources" on a subject page); active tab uses 2px `Primary` underline + `Text Primary`, inactive uses `Text Secondary` |

---

## 12. Dashboard Widgets

| Widget | Visual Spec |
|---|---|
| **Progress Widget** | Large Mastery Fill ring (Section 13), center shows overall mastery % in Heading 1 tabular numerals |
| **Learning Streak** | Calendar heatmap strip (7 or 30-day) using `Accent` gold intensity per active day, flame icon + streak count in Heading 2 |
| **AI Recommendation** | Card with `Secondary`-tinted left border (4px) or icon badge to mark it as AI-originated, headline recommendation, 1-line "why" rationale in Body Secondary — rationale is **never omitted** (Blueprint's insight-generation principle made visible) |
| **Knowledge Graph Widget** | Compact force-directed mini-graph preview (see Section 13.8), click-through to full graph view |
| **Study Time Widget** | Simple bar/area micro-chart (7-day), value + trend delta |
| **Calendar Widget** | Month grid, `Primary`-dot on days with scheduled study sessions (from Study Planner), current day outlined |
| **Recent Activity** | Vertical timeline list, small state icon per entry (quiz, video, tutor chat), relative timestamps in Caption |
| **Leaderboard Widget** | Ranked list, avatar + name + XP, current learner's row highlighted with `Primary`-tinted background at 8% opacity — competitors never shown with mastery %, only XP/streak, to keep the competitive layer separate from the personal-mastery layer |

---

## 13. Charts

**General rules across all charts:** gridlines at `Border` color and 1px only; no 3D effects, no drop shadows on chart elements, no gratuitous gradients; data-ink ratio kept high; tooltips use the `Surface Raised` shell from Section 9.

| Chart | Style Guidance |
|---|---|
| **Line Graph** | Used for trends over time (mastery growth, study hours). 2px stroke in `Primary`; light-fill area beneath at 8% opacity only when a single series is shown |
| **Bar Chart** | Used for comparative values (quiz scores per concept). Rounded top corners (4px), `Primary` for the learner's own data, `Muted` for benchmark/average comparison bars |
| **Area Chart** | Cumulative metrics (total time saved over a course). Gradient fill from `Secondary` at 20% opacity to transparent — the one place a gradient is permitted, since it represents an AI-driven cumulative benefit |
| **Pie Chart** | Avoided by default (low data-ink efficiency) — use only for simple binary/ternary splits (e.g., resource-type mix consumed); segments use semantic/neutral palette, never more than 4 slices |
| **Radar Chart** | **Primary tool for concept-mastery breakdown** across a topic (e.g., Variables/Loops/Functions/OOP/Recursion as axes) — fill uses the Mastery Fill color logic per axis point rather than one flat polygon color, so weak axes visibly pull the shape inward in red-tinted territory |
| **Heatmap** | Study-time calendar (see Learning Streak) and Instructor class-level concept heatmaps — intensity scale runs `Background → Success` (never red-to-green diverging scales, which read as alarming at a glance; low activity is simply "lighter," not "bad") |
| **Tree Graph** | Concept taxonomy view (Topic → Concept → Sub-concept hierarchy) for Instructor/Admin taxonomy management — horizontal collapsible tree, nodes colored by mastery-state only when viewed in a learner context, neutral `Surface` nodes in pure taxonomy-editing context |
| **Knowledge Graph** | The signature visualization. Force-directed node-link graph; node fill = Mastery Fill state (Section 2.3); node size = concept importance/centrality (prerequisite fan-out); edges = `Border` colored, thickening slightly for direct prerequisite relationships; hovering a node highlights its direct prerequisite/dependent edges only, dimming the rest to 30% opacity |
| **Progress Ring** | Circular Mastery Fill; 8px stroke width at large size (Progress Widget), 4px at card size; unfilled track uses `Muted` at 20% opacity, filled arc uses the state color; animates by sweeping clockwise from 12 o'clock on data load |
| **Gauge** | Used sparingly, for single "predicted mastery" or "retention score" metrics on the Analytics Dashboard — semicircular, same fill logic as Progress Ring, with a small needle/marker for "predicted" vs. filled arc for "current" |

---

## 14. Tables

| Behavior | Spec |
|---|---|
| **Sorting** | Click column header to sort; active sort column shows a small chevron in `Primary`; default sort state indicated on load (never an unsorted-feeling table) |
| **Filtering** | Filter chips/pills above the table (999px radius, `Surface` + `Border`, `Primary` when active); avoid a dense filter sidebar for learner-facing tables — reserve that pattern for Admin/Instructor bulk views |
| **Pagination** | Numbered pagination for Admin tables (large datasets); "Load more" pattern for learner-facing lists (activity history, resource lists) — infinite scroll is avoided site-wide to keep a sense of completeness/control |
| **Responsive Behavior** | Below `tablet` breakpoint, tables collapse into a **stacked card list** (one card per row, label/value pairs) rather than horizontal scroll — horizontal scroll on data tables is only acceptable for Admin power-user views on tablet+ |

---

## 15. Forms

| Aspect | Spec |
|---|---|
| **Layout** | Single-column by default (faster scanning, better mobile parity); two-column only for clearly paired short fields (e.g., City / State) on desktop, collapsing to one column below `tablet` |
| **Validation** | Inline, on blur (not on every keystroke — avoid punishing the learner mid-type); a full-form validation summary only appears on submit attempt, anchored above the form, listing each error as a link that scrolls to and focuses the field |
| **Error Messages** | `Danger` text, Caption size, directly beneath the field, paired with a small alert icon; always states what's wrong and how to fix it |
| **Success States** | Subtle: border color change + small check icon; full-form success (e.g., "Profile saved") uses a Toast (Section 17), not an in-form banner, so it doesn't compete with the next action |

---

## 16. Modals

| Type | Spec |
|---|---|
| **Confirmation** | Compact (max 400px width), Heading 3 title, one line of body copy, two buttons right-aligned (Secondary "Cancel" + Primary/Danger action) |
| **Delete** | Same shell as Confirmation but the primary button is `Danger`; requires the destructive action to be visually and verbally explicit ("Delete course," never just "Confirm") |
| **AI Loading** | Used when the AI is generating something synchronously the learner is waiting on (e.g., regenerating a quiz). Uses the **AI Thinking Animation** (Section 18.3) inside a modal or inline panel — never a generic spinner, so the learner always knows *AI* is working, not the app hanging |
| **Success** | Brief, dismissible, optional light `Accent` or `Success` icon; auto-focus the primary "Continue" action |
| **Error** | `Danger` icon, plain-language explanation, a single recovery action (retry / go back) — never exposes raw error codes to learners (Admin views may show a technical detail in a collapsed "Details" section) |

All modals: `Surface` background, 20px radius, `shadow-lg`, scrim at `rgba(11,12,16,0.4)`, closes on scrim click (except Delete, which requires explicit button choice) and `Esc` key.

---

## 17. Notifications

| Type | Spec |
|---|---|
| **Toast** | Bottom-right (desktop) / bottom-center above tab bar (mobile), `Surface Raised` shell, 12px radius, `shadow-floating`, auto-dismiss after 4s with a thin `Primary` progress bar along the bottom edge (reusing the Mastery Fill depletion metaphor — a filled bar draining is the same visual language as a concept filling) |
| **Snackbar** | Used for undoable actions ("Concept marked reviewed — Undo"), same shell as Toast but persists until action or 6s, includes an inline text action button |
| **Alerts (inline banners)** | Full-width within their container, `Info`/`Warning`/`Danger`/`Success` left-border (4px) + tinted background at 6% opacity + icon; used for page-level or section-level state, not for transient events |
| **Badges** | Two forms: **status dot** (8px circle, no label, used in lists/tables) and **count badge** (999px pill, `Danger` background for unread/urgent counts, `Muted` background for neutral counts) |

---

## 18. Loading States

| Type | Spec |
|---|---|
| **Skeletons** | Match the exact shape/size of the content they replace; `Border`-colored base with a subtle left-to-right shimmer (`1.5s` loop, respects reduced-motion — see Section 21) |
| **Progress Bars** | Linear, 4px height, 999px radius, `Primary` fill; for multi-step processes (e.g., video processing pipeline), segmented into discrete steps rather than one continuous bar, reinforcing the platform's segment-based mental model |
| **AI Thinking Animation** | Three small dots in `Secondary` (AI teal), each pulsing in a staggered wave (`0.6s` offset), OR for longer waits, a slow gradient sweep across a thin bar in `Secondary` at 40%→100% opacity. This animation is **reserved exclusively for AI-generation waits** (assessment question generation, tutor reply, video segmentation, quiz regeneration) — never reused for generic network loading, so learners learn to associate it specifically with "the AI is working on this for me" |
| **Video Loading** | Thumbnail-shaped skeleton with a centered, static (non-spinning) play-icon at 40% opacity — spinners are avoided on video surfaces to prevent implying playback has started |

---

## 19. Empty States

All empty states follow: `icon-xl` in `Muted`, Heading 3 message (plain, specific), Body Secondary sub-copy (one sentence, tells the learner what to do next), one primary CTA. No illustrations of people/mascots — line-icon only, consistent with Lucide.

| Context | Message | CTA |
|---|---|---|
| **No Courses** | "No subjects yet" | "Choose a subject to start your first assessment" → Primary button |
| **No Analytics** | "Nothing to show yet" | "Complete your first assessment to see your knowledge graph and stats" → Primary button |
| **No Videos** | "No videos in this concept yet" | "We'll recommend one as soon as it's available" (no CTA if nothing actionable — an empty state does not need to invent a button) |
| **No Search Results** | "No matches for '{query}'" | "Try a different term, or ask the AI Tutor" → AI Action button, directly offering the AI as the fallback path |

---

## 20. Animations

**Guiding rule: motion is used to explain a state change, never to decorate.** Every animation below has a maximum duration and a stated purpose.

| Context | Spec |
|---|---|
| **Hover** | `120–150ms ease-out`; color/shadow transitions only, no movement on simple hovers except cards (see below) |
| **Page Transition** | `200ms` cross-fade + `8px` upward slide on the incoming view; no full-page slide/wipe transitions (too heavy for a dashboard-frequency app) |
| **Button** | Press = `scale(0.98)` over `80ms`; release returns over `100ms` |
| **Cards** | Interactive cards lift on hover: `shadow-sm → shadow-md` + `2px` upward translate, `150ms ease-out` |
| **Graphs** | Knowledge Graph nodes/edges draw in sequentially on first load (`400–600ms` total, staggered ~30ms per node) — communicates "this graph was built for you," not just rendered; on subsequent visits (cached data) this intro animation is skipped |
| **Loading** | See Section 18 |
| **Micro-interactions** | A concept turning from Partial→Mastered triggers a single, contained animation: the fill sweeps to 100% (`400ms`) and the node/ring briefly (`600ms`) glows with a soft `Success`-colored halo, then settles — this is the platform's one "celebration" moment and is used consistently, not as confetti |

**Reduced motion:** every animation in this section has a static fallback (instant state change, no shimmer/sweep) applied automatically under `prefers-reduced-motion` (Section 21).

---

## 21. Accessibility

| Area | Standard |
|---|---|
| **Color Contrast** | WCAG 2.1 AA minimum: 4.5:1 for body text, 3:1 for large text (18px+/Heading weight) and UI component boundaries. All palette pairings in Section 2 are pre-validated against their intended Surface/Background combination. |
| **Keyboard Navigation** | Full app is operable without a mouse: logical tab order, no keyboard traps in modals (focus is trapped *within* an open modal, then returns to the trigger element on close), all interactive components reachable via `Tab`/`Shift+Tab`, activated via `Enter`/`Space` |
| **Screen Readers** | Semantic HTML/ARIA roles for all custom components (graph, charts get `aria-label` summaries of the data, not just visual rendering); AI Tutor streaming responses use `aria-live="polite"` so screen readers announce new content without interrupting |
| **Focus States** | Always visible (no `outline: none` without a replacement); consistent 2px `Primary` ring with 2px offset across every interactive element, including custom components (toggles, custom checkboxes) |
| **Reduced Motion** | `prefers-reduced-motion: reduce` disables: shimmer, graph draw-in, page slide-transitions, mastery-fill sweep animation (replaced with instant fill), AI Thinking pulsing (replaced with a static "Generating…" label) |

---

## 22. Responsive Design

| Breakpoint | Range | Layout Behavior |
|---|---|---|
| **Desktop** | ≥1440px | Full sidebar (264px) expanded by default; multi-column dashboard grids (up to 3–4 widgets per row); Knowledge Graph shown full force-directed view |
| **Laptop** | 1024–1439px | Sidebar defaults to collapsed icon rail (72px) with expand-on-hover; dashboard grids drop to 2–3 columns |
| **Tablet** | 768–1023px | Sidebar becomes an off-canvas drawer (hamburger-triggered); dashboard grids single/double column; tables switch to stacked-card layout (Section 14) |
| **Mobile** | <768px | Bottom tab bar replaces sidebar entirely; all grids single-column; Knowledge Graph switches from force-directed canvas to a scrollable, filterable **list view grouped by mastery state** (a full graph render is not usable at this width); modals become full-screen sheets rather than centered dialogs |

---

## 23. Design Tokens

Reusable token reference (naming convention: `category-property-variant`). Engineering should treat this table as the source for the platform's token file, regardless of implementation format (CSS variables, Tailwind config, JS theme object, etc. — implementation is an engineering decision, not specified here).

| Token Name | Value (Light) | Value (Dark) |
|---|---|---|
| `color-primary` | `#3B33D6` | `#7C74FF` |
| `color-primary-hover` | `#332BC2` | `#8F88FF` |
| `color-primary-pressed` | `#2A23A3` | `#9FA0FF` |
| `color-secondary` | `#0F9E93` | `#3DD9C9` |
| `color-accent` | `#D98C00` | `#F2B94A` |
| `color-success` | `#1A9450` | `#3FCE84` |
| `color-warning` | `#B87500` | `#E3A53D` |
| `color-danger` | `#C6303E` | `#F0616E` |
| `color-info` | `#2170D8` | `#5B9BFF` |
| `color-bg` | `#F6F7FB` | `#0B0C10` |
| `color-surface` | `#FFFFFF` | `#15171E` |
| `color-surface-raised` | `#FFFFFF` | `#1C1F29` |
| `color-border` | `#E3E5EC` | `#262A35` |
| `color-border-strong` | `#C7CBD6` | `#363B49` |
| `color-text-primary` | `#12141C` | `#F3F4F7` |
| `color-text-secondary` | `#565C6E` | `#A6ACBD` |
| `color-muted` | `#9AA0B0` | `#6C7284` |
| `font-display` | Geist | Geist |
| `font-body` | Inter | Inter |
| `font-mono` | JetBrains Mono | JetBrains Mono |
| `radius-sm` | 8px | 8px |
| `radius-md` | 12px | 12px |
| `radius-lg` | 16px | 16px |
| `radius-xl` | 20px | 20px |
| `radius-pill` | 999px | 999px |
| `space-1`…`space-24` | 4px–96px scale (Section 4) | same |
| `shadow-xs`…`shadow-floating` | Section 6 values | reduced-opacity variants |
| `duration-fast` | 120ms | 120ms |
| `duration-base` | 200ms | 200ms |
| `duration-slow` | 400ms | 400ms |
| `easing-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | same |

---

## 24. UI Principles

Rules every future screen must follow, regardless of who builds it:

1. **One primary action per screen.** If two things compete for the Primary button style, one of them is wrong.
2. **Mastery colors are sacred.** Success/Warning/Danger/Muted are reserved exclusively for concept-mastery state and its direct extensions (streaks of correctness, quiz results). They are never repurposed for arbitrary UI status (e.g., don't use Danger red for a generic "new" badge).
3. **AI-originated content is always visually marked** using the Secondary teal — a recommendation, an auto-generated segment, an AI tutor message, or an AI insight must never be visually indistinguishable from human/system content.
4. **Every AI decision shows its reasoning inline**, in Body Secondary text, never hidden behind a tooltip or a separate "why" click for the *first* exposure (e.g., "Skipped: you scored 92% on Loops" appears directly on the video card, not on hover-only).
5. **The knowledge graph fill grammar is universal.** If a new component needs to show partial progress of any kind, it uses the Mastery Fill pattern (Section 2.3/13) rather than inventing a new progress visualization.
6. **No feature ships without an empty state, a loading state, and an error state.** All three are part of the design, not an engineering afterthought.
7. **Assessments are visually calmer than everything else.** No score is shown live during an adaptive assessment; no color feedback (correct/incorrect) beyond a neutral "answer recorded" acknowledgment, to protect measurement integrity and reduce test anxiety.
8. **Gamification is a layer, not the foundation.** Streaks/XP/badges use the Accent color exclusively and never bleed into the mastery-color system.
9. **Every table and list has a defined empty, loading, and overflow (100+ items) behavior** before it ships.
10. **Motion always explains something.** If an animation's purpose can't be stated in one sentence, cut it (Section 20).
11. **Never make the learner re-orient.** Navigation structure (sidebar/tabs) stays constant across the entire learning loop (assessment → path → video → quiz → analytics) — only the content area changes.
12. **Dark mode is a first-class citizen, not an inverted filter.** Every token has an explicit dark value (Section 23); don't auto-invert.

---

## 25. Things to Avoid

- ❌ Reusing Success/Warning/Danger colors for anything other than mastery state and direct correctness feedback — this is the single most important rule in the system.
- ❌ Generic spinners for AI actions — always use the AI Thinking Animation (Section 18.3) so learners know *what kind* of wait they're in.
- ❌ More than one saturated accent color visible in a single viewport (Primary, Secondary, and Accent should rarely all appear at full saturation on the same screen at once).
- ❌ Mixing filled and outlined icon styles within the same component group.
- ❌ Any gradient other than the one explicitly permitted (Area Chart fill, Section 13) — no button gradients, no hero gradients, no card-background gradients.
- ❌ Confetti, mascots, or celebratory sound/visual overload on routine actions (saving a form, completing a single question) — reserve celebration for genuine mastery/streak/path-completion milestones, and even then, keep it to the single micro-interaction defined in Section 20.
- ❌ Dense, bordered, everything-boxed grid layouts reminiscent of Moodle/old LMS systems — prefer whitespace and card grouping over heavy table borders wherever the content isn't genuinely tabular.
- ❌ Infinite scroll — use "Load more" or pagination so learners retain a sense of how much content exists (Section 14).
- ❌ Showing a live numeric score during an adaptive assessment (violates Principle 7).
- ❌ Presenting a "Weak" concept with alarming iconography (red X, warning triangle) — use the Danger *color* per the mastery system, but pair it with encouraging, actionable copy ("Let's strengthen this") rather than error-style language or icons.
- ❌ Diverging red-to-green heatmap scales — use single-hue intensity scales (Section 13) so low activity reads as "quiet," not "bad."
- ❌ Disabling a button without explaining why nearby (a disabled state alone is not sufficient feedback — pair with helper text).
- ❌ Auto-playing video with sound, or auto-advancing to the next concept without an explicit learner action.
- ❌ Serif display faces, cream backgrounds, or terracotta/warm-clay accents — this reads as a templated "AI-generated demo" aesthetic, not a considered product (see Section 1 for the actual identity).
- ❌ Pure black (`#000000`) or pure white (`#FFFFFF`) as a background — always use the defined `Background`/`Surface` tokens.
- ❌ Building a new one-off progress visualization for a new feature instead of extending the existing Mastery Fill grammar (Principle 5).

---

*End of Design System. This document should evolve alongside the Project Blueprint — any new feature introduced there should be designed by first checking whether an existing pattern in this system already covers it (Section 24) before inventing something new.*
