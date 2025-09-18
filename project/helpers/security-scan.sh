#!/bin/bash
# Security Scanner - Simple data collector (no AI)
# Finds potential security issues and exposed secrets

echo "=== SECURITY SCAN ==="
echo "Scan Date: $(date)"
echo "Project: $(basename "$(pwd)")"
echo ""

# Check for exposed secrets
echo "🔐 Potential secrets exposure:"
grep -r "api_key\|secret\|password\|token" \
  --include="*.ts" --include="*.js" --include="*.env*" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | grep -v "example\|template\|mock\|test" | head -15

echo ""
echo "🗝️  API keys and tokens:"
grep -r "API_KEY\|SECRET_KEY\|ACCESS_TOKEN\|PRIVATE_KEY" \
  --include="*.ts" --include="*.js" --include="*.env*" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "🛡️  Authentication patterns:"
grep -r "jwt\|oauth\|auth.*token\|bearer" \
  --include="*.ts" --include="*.js" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "📦 Dependency security:"
if [ -f package.json ]; then
  echo "NPM audit summary:"
  npm audit --summary 2>/dev/null || echo "⚠️  npm audit failed"
  
  echo ""
  echo "High-risk dependencies:"
  npm list --depth=0 2>/dev/null | grep -E "(WARN|ERR)" | head -5
fi

echo ""
echo "📄 Environment files:"
find . -name ".env*" -type f | grep -v node_modules

echo ""
echo "🔒 Git security check:"
[ -f .gitignore ] && echo "✓ .gitignore exists" || echo "⚠️  No .gitignore found"

echo ""
echo "Checking if sensitive files are tracked:"
git ls-files | grep -E "\.env$|\.key$|\.pem$|\.p12$" | head -5

echo ""
echo "🚫 Hardcoded URLs and IPs:"
grep -r "http://\|https://.*\|[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" \
  --include="*.ts" --include="*.js" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | grep -v "localhost\|127.0.0.1\|example.com" | head -10

echo ""
echo "⚠️  Potential vulnerabilities:"
grep -r "eval\|innerHTML\|dangerouslySetInnerHTML" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -5

echo ""
echo "=== SECURITY SCAN COMPLETE ==="