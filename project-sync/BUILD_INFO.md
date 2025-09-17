# SignalHire Agent Production Build

**Version:** v0.1.1  
**Commit:** f5d02e02b17e8b1e15dd831fcaad0bd199446650  
**Built:** 2025-09-17T22:32:13Z  
**Build Type:** Production

## Files Included
- `src/` - Core application code
- `requirements.txt` - Production dependencies only
- `VERSION` - Version information (JSON)
- `install.sh` - Installation script
- `signalhire-agent` - CLI wrapper script
- `.env` - Production environment file (automatically created with your credentials)
- Essential documentation files only (README, QUICKSTART, etc.)
- `.github/copilot-instructions.md` - GitHub Copilot instructions
- `docs/cli-commands.md` - Complete CLI command reference for agents

## Files Excluded (Development Only)
- `tests/` - Test suite
- `specs/` - Development specifications  
- `.pytest_cache/` - Test cache
- `pyproject.toml` - Development configuration
- `TESTING_AND_RELEASE.md` - Development workflow guide
- `version.py` - Development version utility (not needed in production)
- `*.egg-info/` - Python package development metadata
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files
- Development scripts and tools

## Installation
1. Run `./install.sh`
2. Environment is already configured (.env automatically created)
3. Test: `./signalhire-agent --help`

## Version Check
Check `VERSION` file for build information (JSON format).
