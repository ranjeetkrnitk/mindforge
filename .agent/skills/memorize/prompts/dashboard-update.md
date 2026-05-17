# Dashboard Update Helper

> Regenerate `_dashboards/vault-health.html` after memorize operations.

## When to Run
- After: capture, consolidate, harvest, remap, prune
- Skip: recall, mindmap (read-only)

## Quick Metrics Collection

```bash
# All commands run from vault_root
VAULT="$vault_root"

# Counts
TOTAL=$(find "$VAULT" -name "*.md" -not -path "*/_archived/*" -not -path "*/_system/*" -not -path "*/.obsidian/*" | wc -l)
WEEK=$(find "$VAULT" -name "*.md" -not -path "*/_archived/*" -mtime -7 | wc -l)

# Domains
DOMAINS=$(find "$VAULT" -name "*.md" -exec grep -oh 'domain/[a-z]*' {} \; 2>/dev/null | sort | uniq -c | sort -rn)

# Types  
TYPES=$(find "$VAULT" -name "*.md" -exec grep -oh 'type/[a-z]*' {} \; 2>/dev/null | sort | uniq -c | sort -rn)

# Links
LINKS=$(grep -roh '\[\[' "$VAULT" --include="*.md" 2>/dev/null | wc -l)

# Orphans (files with 0 outgoing [[ links)
ORPHANS=$(find "$VAULT" -name "*.md" -not -path "*/_archived/*" -exec grep -cL '\[\[' {} \; 2>/dev/null | wc -l)
```

## HTML Update Strategy

Rather than regenerating the full HTML, update the data values in place:

1. Read existing `_dashboards/vault-health.html`
2. Replace metrics using sed/awk:
   - `<div class="metric">XXX</div>` → new total
   - `<div class="timestamp">...</div>` → new datetime
   - Chart.js data arrays → new values
3. Write back

If file doesn't exist or is malformed, regenerate from template.

## Minimal Output

```
📊 Dashboard updated (691 notes, +1 this session)
```

## Template Reference

Full HTML template lives in reflect skill: `~/.copilot/skills/reflect/templates/vault-health.html`

For memorize, only update these fields:
- Total notes count
- Notes this week count
- Timestamp
- Domain distribution bars (if changed significantly)
