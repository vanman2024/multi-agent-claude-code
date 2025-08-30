# STRICT WORKFLOW - FOLLOW EXACTLY

## THE ONLY WORKFLOW - NO EXCEPTIONS

### 🔴 BEFORE STARTING ANYTHING

```bash
git checkout main
git pull origin main
```

**IF NOT ON MAIN WITH LATEST → STOP!**

### Step 1: Create Issue

```bash
/create-issue "Clear description"
```

**Checks:**
- ✅ On main branch?
- ✅ Latest main pulled?
- ✅ Issue created with checkboxes?

### Step 2: Start Work

```bash
# ONLY after issue exists
git checkout -b feature/[issue-number]-short-name
```

**NEVER:**
- ❌ Start on old branch
- ❌ Create branch before issue
- ❌ Work without issue number

### Step 3: Make Changes

```bash
# Work on feature
# Test locally
# Commit frequently
```

### Step 4: Create PR

```bash
git push origin feature/[issue-number]-short-name
gh pr create --base main
```

**PR Must Have:**
- ✅ All checkboxes
- ✅ Links to issue
- ✅ Tests pass

### Step 5: Merge

```bash
# After all checks pass
gh pr merge --squash --delete-branch
```

### Step 6: Clean Up

```bash
git checkout main
git pull origin main
# Ready for next issue
```

## 🚨 ENFORCEMENT RULES

1. **Commands check branch first**
   - `/create-issue` → Must be on main
   - `/work` → Must be on main
   - If not → ERROR: "Switch to main first!"

2. **No work without issue**
   - Every change needs issue number
   - Branch name includes issue number
   - PR links to issue

3. **Delete branch after merge**
   - Always use `--delete-branch`
   - Never reuse old branches

## THE PROBLEM WE'RE SOLVING

- 72 branches with different versions
- Lost work from branch switching
- Hooks in wrong places
- Settings conflicts
- Total chaos

## THE SOLUTION

**SAME. EXACT. PROCESS. EVERY. TIME.**

No shortcuts. No exceptions. No "just this once."

Start from main. Every. Single. Time.