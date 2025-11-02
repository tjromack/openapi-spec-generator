# Quick Reference - OpenAPI Spec Generator

## Daily Startup (Windows)
```powershell
cd $HOME\projects\openapi-spec-generator
git pull origin main
.\.venv\Scripts\Activate.ps1
code .
```

## Daily Startup (Mac)
```bash
cd ~/projects/openapi-spec-generator
git pull origin main
source .venv/bin/activate
code .
```

## Quick Checks
```
python verify_setup.py      # Full check
python check_env.py         # API keys
python check_packages.py    # Packages
git status                  # Git status
```

## Important Files
- `MULTI_DEVICE_WORKFLOW.md` - Workflow guide
- `.dev_log.md` - Session log
- `docs/phase0_summary.md` - Setup summary
- `data/api_selection.md` - API priorities

---
*Phase 0 Complete - Ready for Phase 1*
