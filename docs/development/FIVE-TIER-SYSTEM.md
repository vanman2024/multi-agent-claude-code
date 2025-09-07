# The Five-Tier Development System

## Overview

The Five-Tier Development System provides a structured approach to building applications by categorizing work into five distinct layers. This system clarifies what should be GitHub issues versus local tasks, and ensures dependencies are handled in the correct order.

## The Five Tiers

### ⚙️ Tier 1: Infrastructure Tasks (DevOps & Setup)
**Local work only - NO GitHub issues**

These are one-time setup tasks that configure your development and deployment environment. They're like setting up your workshop before building.

**Examples:**
- Configure CI/CD pipelines
- Set up deployment to Vercel
- Configure monitoring (Sentry, LogRocket)
- Set up development environment
- Configure secrets and environment variables
- Database migrations and seeding
- SSL certificates and domain setup

**Why no issues?** These are implementation details that don't need tracking. They're done once and rarely revisited.

### 🏗️ Tier 2: Architecture Decisions (System Design)
**Documentation only - NO GitHub issues**

High-level technical decisions that shape the entire system. These are documented in ARCHITECTURE.md but aren't "built" - they're decided.

**Examples:**
- Choosing REST vs GraphQL
- Monolithic vs microservices
- Database selection (PostgreSQL vs MongoDB)
- Authentication strategy (JWT vs sessions)
- State management approach
- Caching strategy
- API versioning approach

**Why no issues?** These are decisions, not tasks. Document them, don't track them.

### 🎨 Tier 3: Design System & UI Foundation
**Local work mostly - Maybe 1-2 setup issues**

The visual foundation of your application. This establishes the look and feel before building features.

**Examples:**
- Color palette and typography
- Component library setup (shadcn/ui, MUI)
- Layout grids and spacing system
- Icon system
- Loading states and animations
- Error state designs
- Responsive breakpoints

**Why few issues?** Most of this is configuration and setup work. Maybe one issue for "Implement design system" if it's complex.

### 📱 Tier 4: Standard Features (Universal Functionality)
**Group into 5-8 GitHub issues**

Features that almost every application needs. These are well-understood patterns that can be grouped together.

**Examples grouped as single issues:**
- **"User Management System"** includes:
  - Registration, login, logout
  - Password reset, email verification
  - Profile management, account settings
  
- **"Admin Dashboard"** includes:
  - User management interface
  - System settings
  - Analytics overview
  - Activity logs

- **"Notification System"** includes:
  - Email notifications
  - In-app notifications
  - Notification preferences
  - Unsubscribe handling

**Why group them?** These are commodity features. One issue can cover the entire authentication flow rather than 10 micro-issues.

### 🎯 Tier 5: Custom Business Features (Unique Value)
**Individual GitHub issues - 5-10 features**

The features that make your application unique. These deliver your core business value and differentiate you from competitors.

**Examples (each gets its own issue):**
- AI-powered resume matching (for job platform)
- Real-time collaborative editing (for docs app)
- Advanced scheduling algorithm (for booking system)
- Custom analytics dashboard (for B2B SaaS)
- Specialized workflow automation (for industry tool)
- Unique gamification system (for education app)

**Why individual issues?** These are complex, unique, and need careful tracking. They're your competitive advantage.

## The House Building Metaphor 🏠

Think of building an application like building a house:

```
Foundation (Tier 1: Infrastructure)
    ↓ Must be solid before building
Framing (Tier 2: Architecture)
    ↓ Defines structure
Plumbing & Electrical (Tier 3: Design System)
    ↓ Hidden but essential
Rooms & Features (Tier 4: Standard Features)
    ↓ What everyone expects
Custom Finishes (Tier 5: Custom Features)
    ↓ What makes it special
```

You can't install custom marble countertops (Tier 5) before you have plumbing (Tier 3)!

## Issue Creation Strategy

### Total Issues: 10-20 Maximum

**Breakdown:**
- 0 issues for Tier 1 (Infrastructure)
- 0 issues for Tier 2 (Architecture)
- 0-2 issues for Tier 3 (Design System)
- 5-8 issues for Tier 4 (Standard Features)
- 5-10 issues for Tier 5 (Custom Features)

### Issue Sizing Guide

| Tier | Typical Size | Complexity | Agent |
|------|-------------|------------|-------|
| Infrastructure | N/A (local) | N/A | Claude locally |
| Architecture | N/A (docs) | N/A | N/A |
| Design System | M-L | 2-3 | Claude locally |
| Standard Features | M-L | 2-3 | Copilot or Claude |
| Custom Features | L-XL | 3-5 | Claude (complex) |

## Implementation Order

### Phase 1: Foundation (Week 1)
**All local work - no issues**
```bash
# Set up locally without issues
- Configure repository
- Set up CI/CD
- Configure deployment
- Set up monitoring
- Database setup
```

### Phase 2: Architecture & Design (Week 1-2)
**Documentation and setup**
```bash
/project-setup  # Create vision
/plan:generate  # Create technical docs
/test:generate  # Create test suites

# Maybe 1 issue:
/create-issue "Implement design system"
```

### Phase 3: Standard Features (Weeks 2-4)
**5-8 grouped issues**
```bash
/create-issue "User authentication system"
/create-issue "Admin dashboard"
/create-issue "Notification system"
/create-issue "Payment processing"
/create-issue "API documentation"
```

### Phase 4: Custom Features (Weeks 3-6)
**5-10 individual issues**
```bash
/create-issue "AI recommendation engine"
/create-issue "Real-time collaboration"
/create-issue "Advanced analytics dashboard"
/create-issue "Custom workflow builder"
```

## Common Mistakes to Avoid

### ❌ Creating Too Many Issues
**Wrong:** 70 issues for every small task
**Right:** 10-20 issues for major features only

### ❌ Issues for Infrastructure
**Wrong:** "Configure GitHub Actions CI/CD" as issue #1
**Right:** Do it locally, no issue needed

### ❌ Splitting Standard Features
**Wrong:** Separate issues for login, logout, password reset
**Right:** One issue: "User authentication system"

### ❌ Starting with Custom Features
**Wrong:** Building unique features before foundation
**Right:** Infrastructure → Standard → Custom

## Quick Decision Guide

**Should this be a GitHub issue?**

Ask yourself:
1. Is it infrastructure setup? → **No issue** (do locally)
2. Is it an architecture decision? → **No issue** (document it)
3. Is it design system setup? → **Maybe 1 issue** if complex
4. Is it a standard feature? → **Yes, but group** related features
5. Is it a custom feature? → **Yes, individual issue**

## Example: E-Commerce Platform

### What's NOT an Issue (Local Work):
- Set up PostgreSQL database
- Configure Stripe webhooks
- Set up Redis caching
- Configure CDN
- Set up error tracking

### What IS an Issue (Tracked Work):

**Standard Features (5 issues):**
1. User authentication system
2. Product catalog management
3. Shopping cart and checkout
4. Order management system
5. Admin dashboard

**Custom Features (5 issues):**
1. AI-powered product recommendations
2. Virtual try-on feature
3. Subscription box builder
4. Influencer marketplace
5. Dynamic pricing engine

**Total:** 10 GitHub issues (not 70!)

## Commands for Each Tier

| Tier | Commands | Output |
|------|----------|--------|
| Planning | `/project-setup`<br>`/plan:generate`<br>`/test:generate` | Documentation & tests |
| Infrastructure | Work locally | No issues |
| Architecture | Edit ARCHITECTURE.md | Documentation |
| Design System | Work locally or<br>`/create-issue` (if complex) | 0-2 issues |
| Standard Features | `/create-issue` (grouped) | 5-8 issues |
| Custom Features | `/create-issue` (individual) | 5-10 issues |

## Remember

- **Plan before building** - Use the planning commands first
- **Infrastructure is invisible** - No issues for setup work
- **Group commodity features** - One issue for related standard features
- **Focus on unique value** - Individual issues for what makes you special
- **10-20 issues total** - If you have more, you're too granular

This system ensures you focus on what matters: delivering unique value to users, not tracking every configuration file change.