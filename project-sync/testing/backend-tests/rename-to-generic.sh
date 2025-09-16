#!/bin/bash
# Rename Signal Hire-specific test files to generic names

set -e

echo "Renaming Signal Hire-specific test files to generic names..."

# Contract tests
if [ -f "contract/test_person_api.py" ]; then
    git mv contract/test_person_api.py contract/test_resource_api.py
    echo "✓ Renamed test_person_api.py → test_resource_api.py"
fi

if [ -f "contract/test_credits_api.py" ]; then
    git mv contract/test_credits_api.py contract/test_usage_api.py
    echo "✓ Renamed test_credits_api.py → test_usage_api.py"
fi

if [ -f "contract/test_scroll_search_api.py" ]; then
    git mv contract/test_scroll_search_api.py contract/test_pagination_api.py
    echo "✓ Renamed test_scroll_search_api.py → test_pagination_api.py"
fi

# Integration tests
if [ -f "integration/test_quickstart_workflow.py" ]; then
    git mv integration/test_quickstart_workflow.py integration/test_basic_workflow.py
    echo "✓ Renamed test_quickstart_workflow.py → test_basic_workflow.py"
fi

if [ -f "integration/test_resume.py" ]; then
    git mv integration/test_resume.py integration/test_document_processing.py
    echo "✓ Renamed test_resume.py → test_document_processing.py"
fi

if [ -f "integration/test_search_to_export_workflow.py" ]; then
    git mv integration/test_search_to_export_workflow.py integration/test_data_export_workflow.py
    echo "✓ Renamed test_search_to_export_workflow.py → test_data_export_workflow.py"
fi

# Unit tests
if [ -f "unit/test_export_comprehensive.py" ]; then
    git mv unit/test_export_comprehensive.py unit/test_data_export.py
    echo "✓ Renamed test_export_comprehensive.py → test_data_export.py"
fi

# Performance tests
if [ -f "performance/test_csv_export_enhanced.py" ]; then
    git mv performance/test_csv_export_enhanced.py performance/test_bulk_export.py
    echo "✓ Renamed test_csv_export_enhanced.py → test_bulk_export.py"
fi

echo ""
echo "Now updating imports and references in the renamed files..."

# Update imports and class names
FILES_TO_UPDATE=$(find . -name "*.py" -type f)

for file in $FILES_TO_UPDATE; do
    if [ -f "$file" ]; then
        # Replace specific Signal Hire terms with generic ones
        sed -i 's/PersonAPI/ResourceAPI/g' "$file"
        sed -i 's/person_api/resource_api/g' "$file"
        sed -i 's/CreditsAPI/UsageAPI/g' "$file"
        sed -i 's/credits_api/usage_api/g' "$file"
        sed -i 's/ScrollSearchAPI/PaginationAPI/g' "$file"
        sed -i 's/scroll_search_api/pagination_api/g' "$file"
        sed -i 's/QuickstartWorkflow/BasicWorkflow/g' "$file"
        sed -i 's/quickstart_workflow/basic_workflow/g' "$file"
        sed -i 's/ResumeParser/DocumentProcessor/g' "$file"
        sed -i 's/resume_parser/document_processor/g' "$file"
        sed -i 's/SearchToExport/DataExport/g' "$file"
        sed -i 's/search_to_export/data_export/g' "$file"
        
        # Update test class names
        sed -i 's/TestPerson/TestResource/g' "$file"
        sed -i 's/TestCredits/TestUsage/g' "$file"
        sed -i 's/TestScrollSearch/TestPagination/g' "$file"
        sed -i 's/TestQuickstart/TestBasic/g' "$file"
        sed -i 's/TestResume/TestDocument/g' "$file"
        
        # Update docstrings
        sed -i 's/SignalHire/Generic API/g' "$file"
        sed -i 's/Signal Hire/Generic API/g' "$file"
        sed -i 's/signalhire/generic_api/g' "$file"
    fi
done

echo "✅ Renaming complete! All Signal Hire-specific names have been genericized."
echo ""
echo "Next steps:"
echo "1. Review the changes with: git status"
echo "2. Run tests to ensure nothing broke: pytest backend-tests/"
echo "3. Commit the changes"