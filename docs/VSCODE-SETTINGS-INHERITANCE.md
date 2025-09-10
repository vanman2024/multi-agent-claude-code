# VSCode Settings Inheritance Guide

## The Problem
VSCode's `.vscode/settings.json` is project-specific and doesn't naturally inherit across projects. This creates maintenance burden when you want consistent settings everywhere.

## Quick Solution (Recommended)

**For immediate global application:**
```bash
./scripts/utilities/vscode-settings-sync.sh --user
```
This copies our template settings to your VSCode user settings, applying them globally to ALL projects.

## All Available Methods

### 1. User Settings (Global) - RECOMMENDED
**Best for:** Developers who want consistent settings everywhere

```bash
# Apply settings globally
./scripts/utilities/vscode-settings-sync.sh --user

# Location of global settings:
# Linux: ~/.config/Code/User/settings.json
# Mac: ~/Library/Application Support/Code/User/settings.json
# Windows: %APPDATA%\Code\User\settings.json
```

**Pros:**
- Applies to ALL projects automatically
- No setup needed per project
- Single source of truth

**Cons:**
- Affects all projects (may not want for some)
- Project-specific settings override these

### 2. VSCode Profiles
**Best for:** Switching between different development contexts

```bash
./scripts/utilities/vscode-settings-sync.sh --profile
```

Create different profiles:
- "Claude Development" - Our template settings
- "Python Projects" - Python-specific settings
- "Frontend" - React/Next.js focused settings

Switch profiles: `Ctrl+Shift+P` → "Profiles: Switch Profile"

### 3. Symlink Method
**Best for:** Projects that should always use template settings

```bash
cd /your/project
./scripts/utilities/vscode-settings-sync.sh --symlink
```

Creates a symbolic link to the template settings. Changes to template automatically apply.

### 4. Git Template Method
**Best for:** Automatic setup for new projects

```bash
./scripts/utilities/vscode-settings-sync.sh --git-template
```

After setup:
- New repos get settings automatically via `git init`
- Existing repos: run `git init` to apply template

### 5. Copy Method
**Best for:** Projects that need customization

```bash
cd /your/project
./scripts/utilities/vscode-settings-sync.sh --copy
```

Creates independent copy you can modify per project.

### 6. Settings Sync Extension
**Best for:** Syncing across multiple machines

```bash
./scripts/utilities/vscode-settings-sync.sh --extension
```

Uses GitHub Gist to sync settings across devices.

## Integration with Our Framework

### Add to Project Setup
Update `.claude/commands/project-setup.md` to include:
```bash
# After creating project structure
./scripts/utilities/vscode-settings-sync.sh --copy
```

### Add to Personal Config
Your personal config can reference the template:
```json
{
  "vscode_settings_template": "/home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json"
}
```

### Add to claude-init.sh
When initializing projects from spec-kit:
```bash
# In claude-init.sh, after generating CLAUDE.md
if [ ! -f ".vscode/settings.json" ]; then
    cp /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json .vscode/
fi
```

## Priority Order in VSCode

VSCode applies settings in this order (later overrides earlier):
1. Default VSCode settings
2. User settings (global)
3. Workspace settings (multi-root workspace)
4. Project settings (.vscode/settings.json)

## Recommended Workflow

1. **For most developers:** Use global user settings
   ```bash
   ./scripts/utilities/vscode-settings-sync.sh --user
   ```

2. **For this template repo:** Keep .vscode/settings.json as reference

3. **For new projects:** Let them inherit from user settings

4. **For special projects:** Add project-specific overrides only as needed

## Updating Settings

When you update the template settings:
1. User settings: Re-run `--user` to update globally
2. Symlinks: Automatically updated
3. Copies: Must manually update or re-copy
4. Git template: Re-run `--git-template` to update template

## Checking Current Settings

View active settings in VSCode:
- `Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"
- Shows merged result of all setting sources

## Troubleshooting

### Settings not applying?
1. Check VSCode settings scope (User vs Workspace)
2. Look for conflicting project settings
3. Restart VSCode after changes

### Want to revert?
```bash
# Restore backup (if created)
cp ~/.config/Code/User/settings.json.backup.* ~/.config/Code/User/settings.json
```

### Different VSCode variant?
- VSCode: `~/.config/Code/User/`
- VSCode Insiders: `~/.config/Code - Insiders/User/`
- VSCodium: `~/.config/VSCodium/User/`
- Code-OSS: `~/.config/Code - OSS/User/`