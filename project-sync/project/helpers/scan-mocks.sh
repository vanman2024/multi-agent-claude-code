#!/bin/bash
# Mock Code Scanner - Simple data collector (no AI)
# Finds mock/placeholder code that needs to be replaced before production

echo "=== MOCK CODE SCAN ==="
echo "Scan Date: $(date)"
echo "Project: $(basename "$(pwd)")"
echo ""

# Find mock/placeholder code
echo "🎭 Mock API calls and placeholder code:"
grep -r "mock\|placeholder\|TODO\|FIXME" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__tests__ \
  . | head -20

echo ""
echo "🧪 Fake/test data in production code:"
grep -r "fake\|dummy\|test.*data\|sample.*data" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__tests__ \
  . | head -10

echo ""
echo "🐛 Development/debug code:"
grep -r "console.log\|console.warn\|console.error\|debugger\|alert(" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -15

echo ""
echo "🔧 Environment-specific code:"
grep -r "NODE_ENV.*development\|process.env.NODE_ENV\|development.*mode" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "🚧 Commented out code blocks:"
grep -r "\/\*.*TODO\|\/\/.*TODO\|\/\*.*HACK\|\/\/.*HACK" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git \
  . | head -10

echo ""
echo "📦 Mock imports and dependencies:"
grep -r "import.*mock\|from.*mock\|require.*mock" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__tests__ \
  . | head -10

echo ""
echo "=== SCAN COMPLETE ==="