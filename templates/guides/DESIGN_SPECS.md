# Design Specifications Template

> ⚠️ **This is the SINGLE SOURCE OF TRUTH for frontend design. All agents and developers must follow this guide.**

## 🎯 Core Design Principles

### 1. Typography: Strict Size Hierarchy
**RULE: Use exactly 4 font sizes + 1 exception. No more, no less.**

#### The 4 Font Sizes + Exception:
- **Size 1**: `text-2xl` (24px) - Page titles only
- **Size 2**: `text-xl` (20px) - Section headers, card titles  
- **Size 3**: `text-base` (16px) - ALL body text, descriptions, labels
- **Size 4**: `text-sm` (14px) - Metadata, timestamps (MINIMUM SIZE)
- **Exception**: `text-xs` (12px) - ONLY for tags/badges when space is critical

#### The 2 Font Weights:
- **Primary**: `font-semibold` - Headers and emphasis
- **Secondary**: `font-normal` - Everything else

#### ❌ FORBIDDEN:
- `text-3xl`, `text-4xl`, etc. - Too big!
- `font-bold`, `font-medium`, `font-light` - Stick to two weights
- Any custom font sizes not in the system

### 2. Color System

> 📝 **CUSTOMIZE THIS SECTION** - Replace with your brand colors

#### Example Dark Theme (Gray-based):
```tsx
// CARDS - Standard card appearance
<Card className="bg-gray-900/50 border-gray-800 hover:bg-gray-900/70 transition-all duration-200">

// Backgrounds
bg-gray-950      // Page background
bg-gray-900/50   // Card backgrounds (semi-transparent)
bg-gray-900      // Header/sidebar
bg-gray-800      // Elevated elements

// Text
text-white       // Primary headings
text-gray-300    // Body text
text-gray-400    // Secondary text
text-gray-500    // Muted text

// Borders
border-gray-800  // Standard borders
```

#### Example Light Theme:
```tsx
// Replace with your light theme colors
bg-white         // Page background
bg-gray-50       // Card backgrounds
text-gray-900    // Primary text
text-gray-600    // Secondary text
border-gray-200  // Borders
```

### 3. Spacing: 8pt Grid System
**All spacing must be divisible by 4 or 8:**
- Padding: `p-2` (8px), `p-4` (16px), `p-6` (24px), `p-8` (32px)
- Margins: `m-2`, `m-4`, `m-6`, `m-8`
- Gaps: `gap-2`, `gap-4`, `gap-6`, `gap-8`

### 4. Visual Hierarchy: 60/30/10 Rule
- **60%** Background (neutral colors)
- **30%** Content (text and UI elements)
- **10%** Accent (CTAs, highlights, status indicators)

## 📋 Component Templates

### Card Component
```tsx
<Card className="[YOUR_CARD_STYLES]">
  <CardHeader className="p-6 pb-4">
    <h3 className="text-xl font-semibold [YOUR_HEADING_COLOR]">
      {/* Card title */}
    </h3>
    <p className="text-base [YOUR_SECONDARY_TEXT] mt-1">
      {/* Card description */}
    </p>
  </CardHeader>
  <CardContent className="p-6 pt-0">
    {/* Card content */}
  </CardContent>
</Card>
```

### Button Hierarchy
```tsx
// Primary Action
<Button className="[YOUR_PRIMARY_BUTTON_STYLES] text-base px-4 py-2">
  Primary Action
</Button>

// Secondary Action
<Button className="[YOUR_SECONDARY_BUTTON_STYLES] text-base px-4 py-2">
  Secondary
</Button>

// Tertiary/Ghost
<Button className="[YOUR_GHOST_BUTTON_STYLES] text-base px-3 py-1.5">
  Cancel
</Button>
```

### Status Indicators
```tsx
// Success
<Badge className="bg-green-500/20 text-green-400 border-green-500/50">
  Success
</Badge>

// Error
<Badge className="bg-red-500/20 text-red-400 border-red-500/50">
  Error
</Badge>

// Warning
<Badge className="bg-yellow-500/20 text-yellow-400 border-yellow-500/50">
  Warning
</Badge>

// Info
<Badge className="bg-blue-500/20 text-blue-400 border-blue-500/50">
  Info
</Badge>
```

### Form Elements
```tsx
// Input Field
<div className="space-y-2">
  <Label className="text-sm [YOUR_LABEL_COLOR]">Field Label</Label>
  <Input className="[YOUR_INPUT_STYLES]" />
  <p className="text-sm [YOUR_HELPER_TEXT_COLOR]">Helper text</p>
</div>

// Select Dropdown
<Select className="[YOUR_SELECT_STYLES]">
  <SelectTrigger>
    <SelectValue placeholder="Choose option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="1">Option 1</SelectItem>
  </SelectContent>
</Select>
```

## 🎨 Responsive Design

### Breakpoints
```tsx
// Mobile First Approach
sm:  // 640px  - Small tablets
md:  // 768px  - Tablets
lg:  // 1024px - Laptops
xl:  // 1280px - Desktops
2xl: // 1536px - Large screens
```

### Grid Layouts
```tsx
// Responsive card grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards */}
</div>

// Sidebar layout
<div className="flex flex-col lg:flex-row gap-6">
  <aside className="w-full lg:w-64">{/* Sidebar */}</aside>
  <main className="flex-1">{/* Content */}</main>
</div>
```

## 🔍 Design Audit Checklist

Before marking any UI task complete, verify:

### Typography
- [ ] Only using the 4 defined text sizes (+ exception)?
- [ ] Only using 2 font weights (semibold/normal)?
- [ ] Text is readable (minimum text-sm for content)?

### Colors
- [ ] Following the defined color palette?
- [ ] Consistent use of opacity/transparency?
- [ ] Proper contrast ratios for accessibility?

### Spacing
- [ ] All spacing uses 4px or 8px increments?
- [ ] Consistent padding in similar components?
- [ ] Proper breathing room between elements?

### Components
- [ ] Cards follow the standard template?
- [ ] Buttons have clear hierarchy?
- [ ] Forms are accessible with proper labels?

### Responsive
- [ ] Works on mobile (320px minimum)?
- [ ] Tablet layout optimized?
- [ ] Desktop makes use of available space?

## 📐 Layout Patterns

### Dashboard Layout
```tsx
<div className="min-h-screen [YOUR_BG_COLOR]">
  {/* Top Navigation */}
  <header className="h-16 border-b [YOUR_BORDER_COLOR]">
    {/* Logo, nav, user menu */}
  </header>
  
  {/* Main Content */}
  <div className="flex">
    {/* Sidebar (optional) */}
    <aside className="w-64 border-r [YOUR_BORDER_COLOR]">
      {/* Navigation */}
    </aside>
    
    {/* Content Area */}
    <main className="flex-1 p-6">
      {/* Page content */}
    </main>
  </div>
</div>
```

### Centered Form Layout
```tsx
<div className="min-h-screen flex items-center justify-center p-4">
  <div className="w-full max-w-md">
    <Card>
      {/* Form content */}
    </Card>
  </div>
</div>
```

## 🚨 Common Mistakes to Avoid

1. **Too many font sizes** - Stick to the system
2. **Inconsistent spacing** - Use the 8pt grid
3. **Low contrast text** - Ensure readability
4. **Cramped mobile layouts** - Test at 320px
5. **Missing hover states** - All interactive elements need feedback
6. **Inconsistent border radius** - Pick one and stick to it
7. **Too many colors** - Follow 60/30/10 rule

## 🎯 Implementation Notes

### For Frontend Agents
When implementing UI:
1. Check this document FIRST
2. Use the component templates as starting points
3. Run through the audit checklist
4. Test responsive behavior

### For Designers
When creating mockups:
1. Use only the defined typography scale
2. Stick to the color palette
3. Maintain 8pt grid spacing
4. Provide responsive variations

### For Backend Developers
When returning data for UI:
1. Consider text truncation needs
2. Provide appropriate status values
3. Include loading/error states
4. Plan for empty states

## 📝 Project-Specific Customization

### TODO: Customize these sections for your project:

#### Brand Colors
```yaml
Primary: [YOUR_PRIMARY_COLOR]    # Main brand color
Secondary: [YOUR_SECONDARY_COLOR] # Supporting color
Success: green-500
Warning: yellow-500
Error: red-500
Info: blue-500
```

#### Font Family
```css
/* Add to global CSS */
--font-sans: [YOUR_FONT], system-ui, sans-serif;
--font-mono: [YOUR_MONO_FONT], monospace;
```

#### Component Library
- [ ] Using shadcn/ui
- [ ] Using Material-UI
- [ ] Using Ant Design
- [ ] Custom components
- [ ] Other: ___________

#### Animation Preferences
- [ ] Subtle transitions (200ms)
- [ ] No animations
- [ ] Elaborate animations
- [ ] Respect prefers-reduced-motion

---

**Remember**: Consistency > Creativity. A boring but consistent UI is better than a creative mess.

*Update this document as design decisions are made. This is a living document.*