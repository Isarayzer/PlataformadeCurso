# Visual Guide - CourseHub UI/UX

## 🎨 Design System Overview

### Color Palette

#### Primary Colors (Blue)
- Used for main actions, links, and primary buttons
- Range from light (#f0f9ff) to dark (#082f49)
- Main shade: #0ea5e9

#### Secondary Colors (Purple)
- Used for accent elements and secondary actions
- Range from light (#faf5ff) to dark (#3b0764)
- Main shade: #a855f7

#### Status Colors
- **Success (Green)**: #22c55e - Completed states, positive actions
- **Warning (Orange)**: #f59e0b - Warnings, pending states
- **Danger (Red)**: #ef4444 - Errors, delete actions
- **Neutral (Gray)**: Various shades for text and backgrounds

### Typography

```
Display Font (Headings): Poppins
- Font weights: 400, 500, 600, 700, 800
- Used for: Page titles, card headers, important text

Body Font (Content): Inter
- Font weights: 300, 400, 500, 600, 700, 800
- Used for: Body text, descriptions, labels

Monospace Font: Fira Code
- Used for: Code snippets (future use)
```

## 📱 Pages Overview

### 1. Login Page (`/login`)

**Layout:**
- Centered card on gradient background
- CourseHub logo and tagline
- Login form with email and password
- Remember me checkbox
- Forgot password link
- Sign in button
- Link to create account

**Features:**
- Email validation
- Password show/hide toggle
- Client-side form validation
- Loading state on submit
- Responsive design

**Visual Elements:**
- Gradient background (primary-50 → white → secondary-50)
- Card with shadow
- Icon inputs (Mail, Lock icons)
- Primary button with hover effect

---

### 2. Register Page (`/register`)

**Layout:**
- Similar to login page
- Registration form with 4 fields:
  - Full name
  - Email
  - Password
  - Confirm password
- Terms acceptance checkbox
- Create account button
- Link to sign in

**Features:**
- Full name validation (min 2 chars)
- Email validation
- Password strength check (min 6 chars)
- Password matching validation
- Show/hide toggles for both password fields
- Loading state

**Visual Elements:**
- Same gradient background as login
- User, Mail, and Lock icons
- Error messages below invalid fields
- Primary button

---

### 3. Dashboard Page (`/`)

**Layout Structure:**
```
┌─────────────────────────────────────────────┐
│ Header                                       │
├───────┬─────────────────────────────────────┤
│       │ Page Title & Description            │
│       ├─────────────────────────────────────┤
│       │ ┌───┐ ┌───┐ ┌───┐ ┌───┐           │
│ Side  │ │ 1 │ │ 2 │ │ 3 │ │ 4 │ Stats     │
│ bar   │ └───┘ └───┘ └───┘ └───┘           │
│       ├─────────────────────────────────────┤
│       │ ┌─────────┐ ┌─────────┐            │
│       │ │ Create  │ │ Upload  │ Actions   │
│       │ │ Course  │ │ Video   │            │
│       │ └─────────┘ └─────────┘            │
│       ├─────────────────────────────────────┤
│       │ Recent Courses                      │
│       │ ┌──────────────────────────────┐   │
│       │ │ Course 1                     │   │
│       │ ├──────────────────────────────┤   │
│       │ │ Course 2                     │   │
│       │ └──────────────────────────────┘   │
└───────┴─────────────────────────────────────┘
```

**Statistics Cards (4 cards in grid):**
1. Total Courses - Blue accent
2. Total Videos - Purple accent
3. Total Students - Green accent
4. Completion Rate - Orange accent

Each card shows:
- Icon in colored background
- Large number (value)
- Percentage change (with trend icon)
- Label

**Quick Action Cards (2 cards):**
- Create Course - Blue gradient background
- Upload Video - Purple gradient background
- Hover effect (lift and shadow)
- Icon + Title + Description

**Recent Courses List:**
- Card with title and "View All" button
- Course items with:
  - Thumbnail image
  - Title
  - Status badge (published/draft)
  - Lesson count
  - Duration
  - Student count
  - More actions button
- Hover effect (border color change, background tint)

---

### 4. Layout Components

#### Sidebar (`MainLayout`)
**Mobile:**
- Hidden by default
- Slides in from left
- Overlay backdrop
- Close on outside click

**Desktop:**
- Always visible
- Fixed width (256px / 16rem)
- White background
- Border on right

**Navigation Items:**
- Dashboard (LayoutDashboard icon)
- Videos (Video icon)
- Courses (BookOpen icon)
- Categories (FolderTree icon)
- Learning Paths (GitBranch icon)
- Settings (Settings icon) - Bottom section
- Logout (LogOut icon) - Bottom section

**Active State:**
- Blue background (primary-50)
- Blue text (primary-700)
- Medium font weight

**Hover State:**
- Light gray background (neutral-50)
- Dark text (neutral-900)

#### Header
**Layout:**
- Fixed height (64px / 4rem)
- White background with bottom border
- Sticky at top

**Left Section:**
- Mobile menu button (hamburger icon)
- Search bar (hidden on mobile)
  - Magnifying glass icon
  - Placeholder: "Search courses, videos..."
  - Width: 256px (mobile) → 384px (large screens)

**Right Section:**
- Notification bell (with red dot indicator)
- User profile:
  - Avatar (gradient circle with user icon)
  - Name: "John Doe"
  - Role: "Instructor"

---

## 🎨 Component Showcase

### Button Variants

```
Primary:    [Blue background, white text]
Secondary:  [Purple background, white text]
Outline:    [Transparent bg, blue border, blue text]
Ghost:      [Transparent bg, gray text, hover: light gray bg]
Danger:     [Red background, white text]
```

**Sizes:**
- Small: Less padding, smaller text
- Medium: Default size
- Large: More padding, larger text

**States:**
- Default
- Hover (darker background)
- Focus (ring around button)
- Disabled (50% opacity, not clickable)
- Loading (spinner + disabled)

### Input Field

**Structure:**
```
[Label *]          <- Optional, with red asterisk if required
┌─────────────┐
│ 🔍 Input... │    <- Icon (optional) + Input field
└─────────────┘
Error message      <- Red text if validation fails
```

**States:**
- Default: Gray border
- Focus: Blue ring + blue border
- Error: Red border + red ring
- With icon: Icon on left with padding

### Card Component

**Structure:**
```
┌─────────────────────────┐
│ Title          [Actions]│ <- Optional header
├─────────────────────────┤
│                         │
│ Content goes here       │
│                         │
└─────────────────────────┘
```

**Variants:**
- Default: White background, subtle shadow
- Hover: Lift effect + stronger shadow (if hover prop)

### Badge Component

Small pill-shaped indicators:
- Primary: Light blue background, dark blue text
- Success: Light green background, dark green text
- Warning: Light orange background, dark orange text
- Danger: Light red background, dark red text

Used for: Status indicators (published, draft, active, etc.)

### Modal Component

**Structure:**
```
┌─────────────────────────────────────┐
│ Title                           [X] │ <- Header with close
├─────────────────────────────────────┤
│                                     │
│ Modal content here                  │
│                                     │
├─────────────────────────────────────┤
│              [Cancel]  [Save]       │ <- Optional footer
└─────────────────────────────────────┘
```

**Features:**
- Backdrop overlay (dark, semi-transparent)
- Centered on screen
- Click outside or ESC to close
- Smooth scale-in animation
- Body scroll lock when open

**Sizes:**
- Small: 448px max width
- Medium: 512px max width (default)
- Large: 672px max width
- XL: 896px max width

---

## 🎭 Animations

All animations are smooth (200-300ms duration):

1. **fade-in**: Opacity 0 → 1
2. **slide-in**: Translate from left
3. **slide-up**: Translate from bottom with opacity
4. **scale-in**: Scale from 95% to 100% with opacity

Used for:
- Page transitions
- Modal appearance
- Hover effects
- Loading states

---

## 📐 Spacing & Layout

**Container Padding:**
- Page content: 24px (1.5rem / p-6)
- Cards: 24px (1.5rem / p-6)
- Sections: Gap of 24px (space-y-6)

**Grid System:**
- Statistics: 1 col (mobile) → 2 cols (tablet) → 4 cols (desktop)
- Quick actions: 1 col (mobile) → 2 cols (tablet/desktop)
- Responsive breakpoints: sm (640px), md (768px), lg (1024px)

**Border Radius:**
- Small elements: 0.5rem (8px)
- Cards: 0.75rem (12px)
- Modals: 1rem (16px)

**Shadows:**
- Soft: For cards and elevated elements
- Medium: For hover states
- Hard: For modals and important popups

---

## ✨ Visual Highlights

1. **Gradient Text**: Logo uses blue → purple gradient
2. **Gradient Backgrounds**: Quick action cards and buttons
3. **Custom Scrollbar**: Thin, rounded, gray with hover effect
4. **Icon Integration**: Lucide React icons throughout
5. **Responsive Images**: Course thumbnails with aspect ratio
6. **Status Indicators**: Color-coded badges
7. **Interactive States**: Smooth transitions on hover/focus
8. **Loading States**: Spinner animations for async operations

---

## 🎨 Theme Customization

The design system is built with TailwindCSS and can be easily customized:

**Colors**: Edit `tailwind.config.js` → `theme.extend.colors`
**Fonts**: Change Google Fonts import in `index.css`
**Spacing**: Modify TailwindCSS default spacing scale
**Animations**: Add new keyframes in `tailwind.config.js`

All components use semantic color names (primary, secondary, etc.) so theme changes propagate automatically.

---

**Current State**: Fully functional, visually polished UI/UX foundation ✅
