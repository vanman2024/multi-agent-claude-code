# Infrastructure Document Guide

## Core Principle: BUY, DON'T BUILD

List external services used instead of building from scratch.

## Required Sections

### 1. Project Requirements
- Project Type
- Expected User Scale
- Budget Range
- Performance Requirements

### 2. Service Categories (include only what applies)

#### For API Projects:
- **API Gateway/Proxy** (Kong, Nginx)
- **Rate Limiting** (Redis, Cloudflare)
- **External API Management**
- **Webhook Processing** (Hookdeck, Svix)
- **Monitoring** (DataDog, New Relic)

#### For Full-Stack Projects:
- **Authentication** (Supabase Auth, Auth0)
- **Database** (Supabase, PlanetScale)
- **File Storage** (S3, Supabase Storage)
- **Email Service** (Resend, SendGrid)
- **Payments** (Stripe, Paddle)

#### For All Projects:
- **Error Tracking** (Sentry)
- **Analytics** (PostHog, Plausible)
- **Deployment** (Vercel, DigitalOcean)
- **CI/CD** (GitHub Actions)
- **Monitoring** (UptimeRobot)

### 3. For Each Service Document:

```markdown
### Service Used: **[Service Name]**
- **Cost**: [Free tier limits or monthly cost]
- **Implementation Time**: [Estimated hours]
- **Why Not Build**: [Time/complexity to build yourself]
- **Features We Use**:
  - [x] Feature 1
  - [x] Feature 2
  - [ ] Feature not used
- **Integration Location**: `path/to/integration/code`
```

### 4. Environment Variables Needed

List all API keys and secrets required:
```
STRIPE_API_KEY
RESEND_API_KEY
SUPABASE_URL
```

### 5. Cost Summary
- Development/Test: $X/month
- Production estimate: $Y/month at Z users

## Questions to Answer

1. What external services do we need?
2. Why use them vs building?
3. What's the total cost?
4. Where is each integrated?
5. What are the fallbacks?

## Skip These Sections for API Projects
- Database hosting (using external)
- File storage (if not needed)
- Payment processing (if not monetized)