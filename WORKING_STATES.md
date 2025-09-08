# Known Working States

This file tracks stable commits that can be used as rollback points.

## Todo Viewer Fixes
- **6850f55** (2025-09-07) - `v1.0-todo-viewer-working` ✅ FULLY WORKING
  - All project filtering working correctly
  - Dates showing correctly (September 7th)
  - Server stability fixed
  - No more 681 task issue
  - Command: `git reset --hard 6850f55` or `git checkout v1.0-todo-viewer-working`

- **833610f** (2025-09-07) - Project path detection fixed
  - Fixed path detection for /Projects/ vs root locations
  - Stops showing 681 tasks for non-existent projects
  
- **4a7decf** (2025-09-07) - Initial complete fix attempt
  - First version with most issues resolved
  - Had timezone bug still

## Previous Stable States
- **3853dac** (2025-09-07) - Last stable before todo-viewer work
  - /work command enhancements complete
  - Before any todo-viewer modifications

## How to Use
```bash
# View this file
cat WORKING_STATES.md

# Rollback to a specific state
git reset --hard <commit-hash>

# Or use a tag
git checkout <tag-name>
```

## Naming Convention
- Production ready: `v1.0-feature-working`
- Development stable: `dev-feature-stable`
- Pre-release: `rc-feature-name`