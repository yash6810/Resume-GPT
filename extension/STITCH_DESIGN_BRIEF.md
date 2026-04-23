# ResumeGPT Chrome Extension - UI Design Brief for Google Stitch

## Project Overview
**App Name:** ResumeGPT Scanner
**Type:** Chrome Extension Popup
**Purpose:** AI-powered resume analyzer that scans job descriptions on job boards and shows ATS score, matched/missing skills, and recommendations in real-time.

---

## Design Specifications

### Dimensions
- **Width:** 380px
- **Height:** 520px
- **Shape:** Rounded corners (16px radius)
- **Style:** Floating popup card

### Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Primary | Coral Red | #e94560 |
| Accent | Gold | #f39c12 |
| Background | Dark Navy | #1a1a2e |
| Card Background | Semi-transparent Blue | rgba(255,255,255,0.05) |
| Card Border | Subtle Red | rgba(233,69,96,0.2) |
| Text Primary | Light Gray | #e0e0e0 |
| Text Secondary | Muted Gray | #a0a0a0 |
| Success | Green | #2ecc71 |
| Error | Red | #e74c3c |
| Warning | Yellow | #f1c40f |
| Info | Blue | #3498db |

### Typography
- **Font Family:** Inter, -apple-system, sans-serif
- **Header:** Bold, 20px
- **Subheader:** Semi-bold, 14px
- **Body:** Regular, 13px
- **Small:** Regular, 11px

---

## UI Components (Top to Bottom)

### 1. Header Bar
```
┌─────────────────────────────────────────┐
│  🎯 ResumeGPT Scanner              [×]  │
└─────────────────────────────────────────┘
```
- **Left:** Logo icon (🎯) + App name "ResumeGPT Scanner"
- **Right:** Close button (×)
- **Background:** Gradient from #e94560 to #f39c12
- **Height:** 48px

### 2. Resume Status Card
```
┌─────────────────────────────────────────┐
│  📄 Your Resume                         │
│                                         │
│  ✅ John_Smith_Resume.pdf loaded        │
│                                         │
│  [📁 Upload New]    [🗑️ Remove]         │
└─────────────────────────────────────────┘
```
- **Icon:** Document icon (📄)
- **Status:** Green checkmark (✅) with filename
- **Buttons:** Upload (outline) and Remove (text only)
- **Background:** Card style with border
- **Padding:** 16px

### 3. Job Detection Card
```
┌─────────────────────────────────────────┐
│  🔍 Job Description                     │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Auto-detected from this page    │   │
│  │                                 │   │
│  │ "Senior Software Engineer at    │   │
│  │  Google - Mountain View..."     │   │
│  │                                 │   │
│  │ Source: linkedin.com            │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [🔄 Re-detect]    [📋 Paste Manual]    │
└─────────────────────────────────────────┘
```
- **Auto-detect status:** Shows detected job title
- **Text preview:** 2-line excerpt of job description
- **Source badge:** Shows website name
- **Buttons:** Re-detect (icon) and Paste Manual (outline)

### 4. ATS Score Display (Main Feature)
```
┌─────────────────────────────────────────┐
│  📊 ATS Score Analysis                  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │                                 │   │
│  │        ╭───────────╮            │   │
│  │       ╱      72     ╲           │   │
│  │      │    ━━━━━━    │           │   │
│  │       ╲   Good Match ╱          │   │
│  │        ╰───────────╯            │   │
│  │                                 │   │
│  │    ████████████████░░░░░ 72%    │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```
- **Circular progress:** Animated ring showing score
- **Score number:** Large, bold, centered
- **Status text:** "Good Match" / "Excellent" / "Needs Work"
- **Horizontal bar:** Gradient fill (coral to gold)
- **Color coding:**
  - 75+: Green (#2ecc71)
  - 50-74: Yellow (#f1c40f)
  - <50: Red (#e74c3c)

### 5. Skills Breakdown
```
┌─────────────────────────────────────────┐
│                                         │
│  ✅ Matched Skills (5)                  │
│  ┌────┐ ┌──────┐ ┌────────┐ ┌──────┐  │
│  │Python│ │React │ │JavaScript│ │Node.js│ │
│  └────┘ └──────┘ └────────┘ └──────┘  │
│                                         │
│  ❌ Missing Skills (3)                  │
│  ┌────┐ ┌────────┐ ┌──────┐           │
│  │ AWS │ │ Docker │ │Kubernetes│        │
│  └────┘ └────────┘ └──────┘           │
│                                         │
└─────────────────────────────────────────┘
```
- **Matched skills:** Green badges (#2ecc71 background)
- **Missing skills:** Red badges (#e74c3c background)
- **Badge style:** Rounded pills, small font
- **Count:** Shown in header (5), (3)

### 6. Quick Recommendations
```
┌─────────────────────────────────────────┐
│  💡 Quick Tips                          │
│                                         │
│  → Add "AWS" to your skills section    │
│  → Mention "Docker" in experience      │
│  → Include "agile" in summary          │
│                                         │
└─────────────────────────────────────────┘
```
- **Icon:** Lightbulb (💡)
- **Style:** Simple bullet points
- **Max items:** 3 tips
- **Color:** Muted gold text

### 7. Action Button
```
┌─────────────────────────────────────────┐
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      🔍 Analyze Resume          │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```
- **Style:** Full-width, gradient background
- **Gradient:** Coral (#e94560) to Gold (#f39c12)
- **Text:** White, bold, centered
- **Icon:** Search/magnifying glass (🔍)
- **Height:** 48px
- **Border radius:** 12px
- **Hover effect:** Slight lift + glow

### 8. Footer
```
┌─────────────────────────────────────────┐
│                                         │
│  ───────────────────────────────────   │
│  Powered by ResumeGPT                   │
│  ⚙️ Settings    │    ℹ️ About           │
│                                         │
└─────────────────────────────────────────┘
```
- **Divider:** Subtle line
- **Text:** "Powered by ResumeGPT" (muted)
- **Links:** Settings and About (text links)

---

## States & Animations

### Loading State
```
┌─────────────────────────────────────────┐
│                                         │
│           ⭕ Loading...                  │
│                                         │
│      Analyzing your resume...           │
│                                         │
└─────────────────────────────────────────┘
```
- **Spinner:** Rotating circle with gradient
- **Text:** "Analyzing your resume..."
- **Animation:** Smooth rotation

### Empty State (No Resume)
```
┌─────────────────────────────────────────┐
│                                         │
│              📄                         │
│                                         │
│      No resume uploaded yet             │
│                                         │
│      [📁 Upload Your Resume]            │
│                                         │
└─────────────────────────────────────────┘
```
- **Icon:** Large document icon
- **Text:** "No resume uploaded yet"
- **Button:** Prominent upload button

### Error State
```
┌─────────────────────────────────────────┐
│  ⚠️ Error                               │
│                                         │
│  Could not connect to server.           │
│  Please make sure ResumeGPT backend    │
│  is running on localhost:8000           │
│                                         │
│  [🔄 Retry]                             │
│                                         │
└─────────────────────────────────────────┘
```
- **Icon:** Warning triangle (⚠️)
- **Background:** Subtle red tint
- **Button:** Retry option

---

## Floating Badge (Injected on Job Sites)

```
    ┌──────────────────────────┐
    │  🎯 ATS Score: 72/100    │
    │  Click for full analysis │
    └──────────────────────────┘
```
- **Position:** Bottom-right corner
- **Style:** Floating card, semi-transparent
- **Size:** Auto-width, 60px height
- **Behavior:** Appears when job detected
- **Click:** Opens full popup

---

## Responsive Behavior

| Screen Size | Popup Width | Notes |
|-------------|-------------|-------|
| Desktop | 380px | Fixed width |
| Small Desktop | 380px | Same |
| Popup Height | 520px max | Scrollable if needed |

---

## Assets Needed

### Icons (PNG format)

| Size | Use | Description |
|------|-----|-------------|
| 16x16 | Toolbar favicon | Resume with checkmark |
| 32x32 | Toolbar (retina) | Same design |
| 48x48 | Extension page | Same design |
| 128x128 | Chrome Web Store | Same design |

### Icon Design
- **Shape:** Rounded square or circle
- **Main element:** Document/resume with checkmark or AI sparkle
- **Colors:** Coral red (#e94560) primary, white accent
- **Style:** Modern, flat design

---

## Interaction States

### Button States
| State | Style |
|-------|-------|
| Default | Gradient background |
| Hover | Brighter, slight lift, glow |
| Active | Slightly pressed |
| Disabled | Gray, no hover effect |

### Card States
| State | Style |
|-------|-------|
| Default | Semi-transparent background |
| Hover | Slightly brighter border |
| Expanded | More padding, shadow |

---

## Sample Content for Design

### Resume Status (Loaded)
```
✅ John_Smith_Resume.pdf
   Uploaded: Mar 31, 2026
```

### Job Detected
```
"Senior Software Engineer at Google"
Mountain View, CA - Full-time
```

### ATS Score
```
72/100 - Good Match
```

### Matched Skills
```
Python, React, JavaScript, Node.js, Git
```

### Missing Skills
```
AWS, Docker, Kubernetes
```

### Recommendations
```
→ Add "AWS" to your skills section
→ Mention "cloud" in your experience
→ Include "agile" methodology
```

---

## Design Notes for Stitch

1. **Dark theme only** - Match ResumeGPT main app
2. **Glassmorphism** - Semi-transparent cards with blur
3. **Gradient accents** - Coral to gold for CTAs
4. **Smooth animations** - Fade in, slide, progress fill
5. **Rounded corners** - 12-16px on cards, 8px on buttons
6. **Consistent spacing** - 16px padding, 12px gaps
7. **Clear hierarchy** - Headers > Subheaders > Body > Small
8. **Status indicators** - Green/Red/Yellow for quick scanning

---

**Copy this entire document and paste into Google Stitch to generate the UI design.**
