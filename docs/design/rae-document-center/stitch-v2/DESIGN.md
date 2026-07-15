---
name: Heritage Precision
colors:
  surface: '#f9f9f7'
  surface-dim: '#dadad8'
  surface-bright: '#f9f9f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f1'
  surface-container: '#eeeeec'
  surface-container-high: '#e8e8e6'
  surface-container-highest: '#e2e3e0'
  on-surface: '#1a1c1b'
  on-surface-variant: '#3f4942'
  inverse-surface: '#2f3130'
  inverse-on-surface: '#f1f1ef'
  outline: '#6f7a72'
  outline-variant: '#bfc9c0'
  surface-tint: '#1b6b49'
  primary: '#004229'
  on-primary: '#ffffff'
  primary-container: '#005c3b'
  on-primary-container: '#86d2a8'
  inverse-primary: '#8ad6ac'
  secondary: '#5e5f5c'
  on-secondary: '#ffffff'
  secondary-container: '#e0e0dc'
  on-secondary-container: '#626360'
  tertiary: '#393934'
  on-tertiary: '#ffffff'
  tertiary-container: '#50504b'
  on-tertiary-container: '#c4c2bc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#a6f3c7'
  primary-fixed-dim: '#8ad6ac'
  on-primary-fixed: '#002112'
  on-primary-fixed-variant: '#005234'
  secondary-fixed: '#e3e2df'
  secondary-fixed-dim: '#c7c7c3'
  on-secondary-fixed: '#1b1c1a'
  on-secondary-fixed-variant: '#464744'
  tertiary-fixed: '#e4e2db'
  tertiary-fixed-dim: '#c8c6c0'
  on-tertiary-fixed: '#1b1c18'
  on-tertiary-fixed-variant: '#474742'
  background: '#f9f9f7'
  on-background: '#1a1c1b'
  surface-variant: '#e2e3e0'
typography:
  headline-xl:
    fontFamily: Sarabun
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Sarabun
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Sarabun
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Sarabun
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Sarabun
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Sarabun
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Sarabun
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Sarabun
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Sarabun
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Sarabun
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
  max-width: 1280px
---

## Brand & Style
The design system is built on a foundation of institutional trust and environmental stewardship. It balances the authoritative weight of a government entity with the approachability of a modern service provider. The aesthetic is **Corporate Modern with a Minimalist lean**, emphasizing clarity, structured information hierarchy, and a calm, professional atmosphere.

The target audience ranges from internal stakeholders to public users who require dependable, legible, and high-functioning interfaces. The emotional response should be one of "composed efficiency"—clean, stable, and purposefully organized.

## Colors
The palette is anchored by **RAE Green (#005C3B)**, a deep, professional emerald that signals growth and stability. This is supported by a warm ivory/white surface palette to avoid the sterile coldness of pure white.

- **Primary:** RAE Green (#005C3B) is used for key actions, brand moments, and active states.
- **Surface:** A warm ivory (#FDFCF8) serves as the primary background to reduce eye strain and provide a sophisticated, tactile feel.
- **Secondary Surface:** A muted bone tone (#E8E6DF) is used for grouping elements or secondary backgrounds.
- **Neutral:** A near-black (#1A1C1B) ensures high contrast for all typography and iconography.

## Typography
This design system utilizes **Sarabun** exclusively across all levels. Sarabun is a humanist sans-serif that offers excellent legibility and a clean, official appearance that bridges the gap between traditional Thai government typefaces and modern web standards.

- **Headlines:** Use Bold (700) for large displays and SemiBold (600) for smaller section headers.
- **Body Text:** Use Regular (400) for standard reading. SemiBold (600) is preferred over Bold for emphasis within body copy to maintain a sophisticated texture.
- **Labels:** Use Medium (500) or SemiBold (600) for UI labels and button text to ensure they stand out against functional backgrounds.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid** model. Content is contained within a 1280px max-width container on desktop, centered with wide margins. On smaller screens, the layout becomes fluid with a 12-column grid for tablet and a 4-column grid for mobile.

The spacing rhythm is based on a **4px baseline**, with 8px and 16px being the most common increments for internal component spacing. Use generous vertical padding (lg and xl) between major sections to emphasize the minimalist, high-end feel.

## Elevation & Depth
Depth is created through **Tonal Layers** and **Low-Contrast Outlines** rather than aggressive shadows. 

- **Level 0 (Base):** Ivory Surface (#FDFCF8).
- **Level 1 (Cards/Containers):** Flat white with a 1px border using the Tertiary color (#E8E6DF).
- **Level 2 (Hover/Active):** A very soft, diffused shadow (0px 4px 20px rgba(0, 92, 59, 0.04)) to indicate interactivity without breaking the flat aesthetic.
- **Overlays:** Use a semi-transparent backdrop blur (12px) for modals to maintain context while focusing user attention.

## Shapes
The shape language is **Soft**. Corners are slightly rounded to feel approachable and modern, but remain sharp enough to feel professional and structured. 

- **Components:** Standard buttons and input fields use a 4px (0.25rem) radius.
- **Containers:** Larger cards and modals use an 8px (0.5rem) radius.
- **Circular:** Icons and status dots maintain 100% rounding.

## Components
- **Buttons:** Primary buttons use RAE Green with white text and Medium (500) weight Sarabun. Secondary buttons use an outline style with the primary color.
- **Input Fields:** Use a subtle bone-colored background (#E8E6DF) or white with a thin border. Focus states should clearly use a 2px RAE Green border.
- **Chips/Tags:** Small, low-contrast pills using the body-sm or label-sm typography tokens. Backgrounds should be light tints of the primary color.
- **Lists:** Clean, border-bottom separated items with generous vertical padding (16px). Use SemiBold Sarabun for list titles.
- **Cards:** White backgrounds, 1px border (#E8E6DF), and 8px rounded corners. Use for grouping related data or dashboard modules.
- **Navigation:** Top-tier navigation should use Medium weight Sarabun with generous horizontal spacing. Active states are indicated by a 2px RAE Green bottom border.