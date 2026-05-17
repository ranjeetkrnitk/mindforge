# /dashboard

Refresh Obsidian vault health dashboard with current metrics.

## Load Order
1. `config/user.md` — vault path (shared with memorize)

## First-run setup

Check `config/user.md`:
- If `vault_root` is empty → ask user for vault path and save it
- If set → proceed silently

## Trigger Phrases

- "refresh dashboard"
- "update dashboard"
- "vault stats"
- "dashboard"

## Execution

1. **Scan vault** for metrics:
   - `total_notes`: count of .md files (excluding system folders)
   - `total_links`: count of `[[wikilink]]` patterns
   - `orphans`: notes with 0 outgoing links
   - `hubs`: notes with 5+ outgoing links
   - `domains`: count by `domain/X` tags
   - `types`: count by `type/X` tags
   - `health_score`: `100 - orphan% + (hub% * 20)`, clamped 0-100

2. **Update HTML** at `<vault_root>/_dashboards/vault-health.html`:
   - Replace JavaScript constants with fresh values
   - Update timestamp

3. **Output** (minimal):
   ```
   📊 Dashboard updated
   Notes: X | Links: Y | Orphans: Z% | Health: N%
   ```

## Script

Run `scripts/refresh.py` with vault_root as argument:

```bash
python3 ~/.copilot/skills/dashboard/scripts/refresh.py "<vault_root>"
```

## Integration with Other Skills

Add to end of any vault-modifying skill:

```markdown
## Post-Action Hook
After write operations, invoke `/dashboard` to refresh metrics.
```

The memorize skill already has this hook configured.
