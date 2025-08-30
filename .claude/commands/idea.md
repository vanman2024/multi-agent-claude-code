---
allowed-tools: Read(*), Write(*), Bash(gh *, ls), TodoWrite(*), Glob(*)
description: Create new ideas or analyze existing scratchpad discussions
argument-hint: "[optional: topic or existing file name]"
---

# Idea - Create or Analyze Discussion Framework

## Purpose
Either start a new idea discussion OR analyze an existing scratchpad idea to determine next steps (feature, bug fix, etc.)

## Initial Flow

When user runs `/idea $ARGUMENTS`:

```
What would you like to do?

1. 💡 Create - Start a new idea discussion
2. 🔍 Analyze - Review existing scratchpad idea for next steps
3. 📋 List - Show all existing idea discussions

Choose [1/2/3]:
```

## Path 1: Create New Idea

If user chooses Create:

1. **Get the topic**:
   - If provided in $ARGUMENTS, use it
   - Otherwise: "What idea would you like to explore?"

2. **Create scratchpad file**:
   ```bash
   DATE=$(date +%Y%m%d)
   TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
   FILEPATH="/home/gotime2022/Projects/multi-agent-claude-code/scratchpad/ideas/${DATE}-${TOPIC_SLUG}.md"
   ```

3. **Use template** from `@/home/gotime2022/Projects/multi-agent-claude-code/templates/idea-template.md`

4. **Start collaborative discussion**:
   ```
   📝 Created: scratchpad/ideas/[filename]
   
   Let's explore this idea. What problem are we trying to solve?
   ```

5. **Build the document through conversation**

## Path 2: Analyze Existing Idea

If user chooses Analyze:

1. **Find existing ideas**:
   ```bash
   ls -la /home/gotime2022/Projects/multi-agent-claude-code/scratchpad/ideas/*.md
   ```

2. **Let user select**:
   ```
   Which idea would you like to analyze?
   
   1. 20250829-automatic-pr-review.md
   2. 20250830-branch-strategy.md
   3. 20250830-testing-framework.md
   
   Or provide filename directly:
   ```

3. **Read and analyze the idea**:
   - Load the scratchpad file
   - Assess completeness of sections
   - Identify what type of work this should become

4. **Provide analysis**:
   ```
   📊 Analysis of: [idea title]
   
   Completeness:
   ✅ Problem clearly defined
   ✅ Solution approach documented
   ⚠️ Technical details need refinement
   ❌ Resource requirements not specified
   
   This appears to be a: [Feature/Bug Fix/Enhancement/Refactor]
   
   Recommended next step:
   → Create Feature Issue (requirements are clear enough)
   
   What would you like to do?
   1. 📝 Create issue from this idea
   2. 💬 Create GitHub discussion for feedback
   3. ✏️ Continue refining in scratchpad
   4. 🗂️ Archive (not pursuing now)
   ```

5. **Execute next step**:

   **If Create Issue**:
   ```
   What type of issue should this become?
   1. 🚀 Feature - New functionality
   2. 🐛 Bug - Something to fix  
   3. 🔧 Enhancement - Improve existing feature
   4. 🏗️ Refactor - Code improvement
   
   I'll help structure it properly for implementation.
   ```
   
   Then create issue with:
   - Proper issue template based on type
   - Reference to original scratchpad discussion
   - Extracted requirements and acceptance criteria
   - Implementation checkboxes

   **If Create Discussion**:
   - Push to GitHub for broader feedback
   - Link back to scratchpad origins

   **If Continue Refining**:
   - Resume collaborative editing
   - Focus on gaps identified in analysis

## Path 3: List Ideas

If user chooses List:

```bash
# List all idea files with preview
for file in /home/gotime2022/Projects/multi-agent-claude-code/scratchpad/ideas/*.md; do
  echo "📄 $(basename $file)"
  head -n 3 "$file" | grep -E "^##|^###" | head -1
  echo ""
done
```

Output:
```
Current idea discussions:

📄 20250829-automatic-pr-review.md
   💡 Idea: Automatic PR Review System

📄 20250830-branch-strategy.md
   💡 Idea: Smart Branch Creation Strategy

📄 20250830-testing-framework.md
   💡 Idea: Comprehensive Testing Framework

Use '/idea analyze' to review any of these.
```

## Smart Detection

If $ARGUMENTS contains a filename that exists:
- Skip the menu, go straight to analyzing that file

If $ARGUMENTS is a new topic:
- Skip the menu, go straight to creating new idea

Only show menu when:
- No arguments provided
- Arguments are ambiguous

## Example Usage

### Quick create:
```
/idea "automatic code review system"
→ Skips menu, creates new idea discussion
```

### Quick analyze:
```
/idea 20250830-branch-strategy.md
→ Skips menu, analyzes existing file
```

### Interactive:
```
/idea
→ Shows menu for create/analyze/list
```

## Transition Workflows

### Idea → Feature Issue
- Extract requirements from scratchpad
- Create implementation checkboxes
- Add acceptance criteria
- Reference: "Based on discussion: scratchpad/ideas/[file]"

### Idea → Bug Report
- Extract problem description
- Create reproduction steps
- Add fix checkboxes
- Reference original discussion

### Idea → GitHub Discussion
- Push for community feedback
- Keep scratchpad as internal notes
- Link between them

## Key Principles

1. **Single entry point** - `/idea` handles both create and analyze
2. **Smart routing** - Detects intent from arguments
3. **Clear progression** - Idea → Analysis → Issue/Feature
4. **Maintains history** - Scratchpad files track evolution
5. **Type-aware** - Knows if idea should become feature, bug, etc.