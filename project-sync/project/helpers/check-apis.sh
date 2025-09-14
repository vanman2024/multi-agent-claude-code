#!/bin/bash
# API Status Checker - Simple data collector (no AI)
# Analyzes API endpoints and external service integrations

echo "=== API ENDPOINT ANALYSIS ==="
echo "Scan Date: $(date)"
echo "Project: $(basename "$(pwd)")"
echo ""

# Find API routes
echo "🛣️  API Routes found:"
echo "Next.js API routes:"
find . -path "*/api/*" -name "*.ts" -o -name "*.js" | grep -v node_modules | head -20

echo ""
echo "Express/FastAPI routes:"
grep -r "app\.\(get\|post\|put\|delete\|patch\)" \
  --include="*.ts" --include="*.js" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "🌐 External API calls:"
grep -r "fetch\|axios\|http\." \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | grep -E "(http://|https://)" | head -15

echo ""
echo "🔗 API base URLs and endpoints:"
grep -r "baseURL\|apiUrl\|API_URL\|endpoint" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "🗄️  Database connections:"
echo "MongoDB connections:"
grep -r "mongodb\|mongoose\|MongoClient" \
  --include="*.ts" --include="*.js" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -5

echo ""
echo "PostgreSQL connections:"
grep -r "postgresql\|postgres\|pg\|psycopg" \
  --include="*.ts" --include="*.js" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -5

echo ""
echo "SQLite connections:"
grep -r "sqlite\|\.db" \
  --include="*.ts" --include="*.js" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -5

echo ""
echo "📚 API documentation files:"
find . -name "*api*" -name "*.md" -o -name "swagger*" -o -name "openapi*" | grep -v node_modules

echo ""
echo "🔐 Authentication endpoints:"
grep -r "auth\|login\|register\|token" \
  --include="*.ts" --include="*.js" \
  . | grep -E "(route|endpoint|api)" | head -10

echo ""
echo "💳 Payment/billing endpoints:"
grep -r "payment\|billing\|stripe\|paypal" \
  --include="*.ts" --include="*.js" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "📧 Email/notification services:"
grep -r "sendgrid\|mailgun\|nodemailer\|ses\|notification" \
  --include="*.ts" --include="*.js" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -5

echo ""
echo "=== API SCAN COMPLETE ==="