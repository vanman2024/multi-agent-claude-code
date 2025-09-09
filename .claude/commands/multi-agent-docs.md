---
allowed-tools: Task(*), WebFetch(*), Write(*), Edit(*), Read(*)
description: Load documentation from multiple sources using specialized agents
argument-hint: [urls or topics to document]
---

# Multi-Agent Documentation Loader

## Load Existing Docs
First, check what documentation already exists:
- @docs/README.md (if exists)
- @CLAUDE.md
- @README.md

## <scrape_loop_prompt>
Use @agent-docs-scraper agent to fetch and convert this URL to markdown:
- Extract main content
- Remove navigation and ads
- Format as clean markdown
- Identify key concepts and code examples
</scrape_loop_prompt>

## <synthesis_prompt>
Synthesize all gathered documentation into a cohesive guide that:
1. Avoids duplication with existing docs
2. Follows our documentation standards
3. Includes practical examples
4. References source URLs
</synthesis_prompt>

## Workflow

### Step 1: Check DELETE_OLD_DOCS Variable
```
DELETE_OLD_DOCS_AFTER_HOURS: 24
```

### Step 2: Read Existing Documentation
Read the files listed above to understand what's already documented.

### Step 3: Parse Input URLs
For each URL in $ARGUMENTS that needs documentation:
1. Check if already documented
2. If not, add to processing list

### Step 4: Parallel Documentation Fetch
For each URL in the list, use Task tool in parallel:
- Task(subagent_type="general-purpose", prompt=<scrape_loop_prompt> + URL)

### Step 5: Synthesize Results
After all agents complete:
- Task(subagent_type="general-purpose", prompt=<synthesis_prompt>)

### Step 6: Write Documentation
Based on synthesis, update or create documentation files.

## Report Format
```
📚 Documentation Update Complete
- Fetched: [X] sources
- Updated: [Y] files  
- New concepts: [list]
```