# Dashboard Skill

Refresh Obsidian vault health dashboard with current metrics.

## Installation

```bash
# Copy to your skills folder
rsync -av --exclude='config/user.md' \
  ~/repos/ranjeet/mindforge/.agent/skills/dashboard/ \
  ~/.copilot/skills/dashboard/

# Create user config
cp ~/.copilot/skills/dashboard/config/user.md.template \
   ~/.copilot/skills/dashboard/config/user.md
# Edit user.md with your vault path
```

## Usage

- `/dashboard` - refresh vault metrics
- "refresh dashboard"
- "update dashboard"
- "vault stats"

## Integration

Called automatically by `/memorize` after write operations.

## Requirements

- Python 3
- Obsidian vault with `_dashboards/vault-health.html`
