#!/bin/bash
#
# Run Real SignalHire API Tests
#
# This script runs tests against real SignalHire API endpoints to validate:
# - Data quality and structure  
# - Result counts and accuracy
# - Performance characteristics
# - Rate limiting behavior
#
# Requirements:
# - Set SIGNALHIRE_EMAIL and SIGNALHIRE_PASSWORD environment variables
# - Have real SignalHire account with available credits
# - Network connectivity to SignalHire API
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌐 SignalHire Real API Test Runner${NC}"
echo "================================================="

# Try to load .env file if it exists and credentials aren't set
if [[ -z "$SIGNALHIRE_EMAIL" || -z "$SIGNALHIRE_PASSWORD" ]]; then
    if [[ -f ".env" ]]; then
        echo -e "${YELLOW}🔄 Loading credentials from .env file${NC}"
        source .env
    fi
fi

# Check if credentials are set
if [[ -z "$SIGNALHIRE_EMAIL" || -z "$SIGNALHIRE_PASSWORD" ]]; then
    echo -e "${RED}❌ Missing Credentials${NC}"
    echo "Please set environment variables:"
    echo "  export SIGNALHIRE_EMAIL=\"your-email@example.com\""  
    echo "  export SIGNALHIRE_PASSWORD=\"your-password\""
    echo ""
    echo "Or create .env file:"
    echo "  SIGNALHIRE_EMAIL=your-email@example.com"
    echo "  SIGNALHIRE_PASSWORD=your-password"
    exit 1
fi

echo -e "${GREEN}✅ Credentials Found${NC}"
echo "  Email: ${SIGNALHIRE_EMAIL}"
echo "  Password: [REDACTED]"
echo ""

# Check Python environment
echo -e "${BLUE}🐍 Checking Python Environment${NC}"
if ! python3 -c "import pytest" 2>/dev/null; then
    echo -e "${RED}❌ pytest not found${NC}"
    echo "Install with: pip install pytest pytest-asyncio"
    exit 1
fi

if ! python3 -c "from src.lib.signalhire_client import SignalHireClient" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  SignalHire client import failed${NC}"
    echo "Make sure you're running from project root and dependencies are installed"
    exit 1
fi

echo -e "${GREEN}✅ Python environment ready${NC}"
echo ""

# Run different test categories
echo -e "${BLUE}🧪 Running Real API Tests${NC}"
echo ""

echo -e "${YELLOW}📋 Test Plan:${NC}"
echo "1. Heavy Equipment Mechanic search in Canada"
echo "2. Credits API validation"
echo "3. Contact reveal testing"  
echo "4. Rate limiting behavior"
echo "5. Location filtering accuracy"
echo "6. Job title relevance scoring"
echo ""

# Test categories with different verbosity
test_categories=(
    "test_heavy_equipment_mechanic_canada_search:Heavy Equipment Mechanic Search"
    "test_credits_check_real_api:Credits API Test"
    "test_contact_reveal_real_api:Contact Reveal Test"
    "test_api_rate_limiting_real:Rate Limiting Test"
    "test_location_filtering_accuracy:Location Filtering Test"
    "test_job_title_relevance_scoring:Job Title Relevance Test"
)

failed_tests=0
passed_tests=0

for test_info in "${test_categories[@]}"; do
    IFS=':' read -r test_name test_description <<< "$test_info"
    
    echo -e "${BLUE}🔄 Running: ${test_description}${NC}"
    
    if python3 -m pytest tests/integration/test_real_api_endpoints.py::TestRealSignalHireAPI::${test_name} -v -s --tb=short -m live; then
        echo -e "${GREEN}✅ PASSED: ${test_description}${NC}"
        ((passed_tests++))
    else
        echo -e "${RED}❌ FAILED: ${test_description}${NC}"
        ((failed_tests++))
    fi
    
    echo ""
    echo "Waiting 5 seconds between tests to respect rate limits..."
    sleep 5
done

# Data quality tests  
echo -e "${BLUE}🔍 Running Data Quality Tests${NC}"

if python3 -m pytest tests/integration/test_real_api_endpoints.py::TestAPIDataQuality -v -s --tb=short -m live; then
    echo -e "${GREEN}✅ PASSED: Data Quality Tests${NC}"
    ((passed_tests++))
else
    echo -e "${RED}❌ FAILED: Data Quality Tests${NC}"
    ((failed_tests++))
fi

# Summary
echo ""
echo -e "${BLUE}📊 Test Summary${NC}"
echo "================================================="
echo -e "${GREEN}Passed: ${passed_tests}${NC}"
echo -e "${RED}Failed: ${failed_tests}${NC}"
echo -e "Total: $((passed_tests + failed_tests))"

if [[ $failed_tests -eq 0 ]]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! SignalHire API is working correctly.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}⚠️  Some tests failed. Check output above for details.${NC}"
    echo "Common issues:"
    echo "- Insufficient credits for contact reveals"
    echo "- Rate limiting (tests run too quickly)"
    echo "- Network connectivity issues"
    echo "- API service temporarily unavailable"
    exit 1
fi