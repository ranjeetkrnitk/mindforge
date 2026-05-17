---
name: memorize
version: 0.2.0
description: >
  Second-brain skill grounded in Complementary Learning Systems (CLS) theory.
  Captures, consolidates, maps, and reorganizes knowledge. Triggers: "remember
  this", "memorize", "consolidate", "mind map", "remap", "harvest", "recall".
agent: agnostic
compatibility:
  preferred_vault: obsidian
  format: markdown + YAML frontmatter
  requires: none
---

# /memorize

## Load Order
1. `../_shared/conventions.md` — cross-skill standards
2. `config/user.md` — vault path (personal, gitignored)
3. `REF.md` — node types, link types, domains
4. `config/settings.md` — thresholds

## First-run setup (run before any mode)

Check `config/user.md`:
- If `setup_complete: false` or `vault_root` is empty → run setup:
  1. Ask: *"Where is your Obsidian vault? (absolute path)"*
  2. Write the answer to `config/user.md` as `vault_root` and set `setup_complete: true`
  3. **Permissions hint** — Tell the user:
     ```
     💡 To reduce permission prompts, run these in Copilot CLI:
        /add-dir ~/.copilot/skills
        /add-dir <vault_root>
     ```
  4. Confirm: `✓ Vault set to <path>. You're ready.`
- If `setup_complete: true` → proceed silently with `vault_root` from `config/user.md`

## Output behavior (all modes)
- **Write files directly** to `vault_root` using available file tools
- **Print one line per file written**: `✓ <relative-path-from-vault-root>`
- **No note content** in output unless the user explicitly asks to see it
- End with a **single summary line**: `Saved N note(s) to <vault_root>`
- **Update dashboard** after write operations (see Post-Action Hook below)

## Post-Action Hook: Dashboard Update

After any write operation (capture, consolidate, harvest, remap, prune), refresh the vault dashboard:

```bash
python3 ~/.copilot/skills/dashboard/scripts/refresh.py "<vault_root>"
```

Or invoke the `/dashboard` skill directly.

Skip dashboard update if:
- `_dashboards/` folder doesn't exist
- Read-only mode (recall, mindmap with no writes)
- User passes `--no-dashboard` flag

## Modes

| # | mode | trigger phrases | prompt |
|---|---|---|---|
| 1 | `capture` | "remember this", "memorize", "note this", "log this" | `prompts/capture.md` |
| 2 | `consolidate` | "consolidate", "what have I learned about X", "strengthen notes" | `prompts/consolidate.md` |
| 3 | `mindmap` | "mind map", "visualize my knowledge", "map this topic" | `prompts/mindmap.md` |
| 4 | `remap` | "remap my vault", "reorganize my notes", "apply CLS" | `prompts/remap.md` |
| 5 | `harvest` | "harvest this session", "save what we discussed", "memorize this conversation" | `prompts/harvest.md` |
| 6 | `prune` | "clean up empty notes", "prune my vault", "remove stubs", "find empty files" | `prompts/prune.md` |
| 7 | `recall` | "recall", "what do I know about", "search my vault" | `prompts/recall.md` |

## File Structure

```
.agent/skills/memorize/
├── SKILL.md
├── REF.md                  ← merged quick reference (read this, not schema/)
├── README.md
├── config/
│   ├── settings.md         ← tunable thresholds
│   └── user.md             ← local vault path (gitignored, written on first run)
├── prompts/                ← one file per mode (capture, consolidate, mindmap, remap, harvest, prune)
├── templates/              ← concept, episode, claim, source, moc
└── schema/                 ← full docs for humans; agents use REF.md
```

## Output conventions
- YAML frontmatter on all notes
- `[[wikilink]]` syntax for links
- ISO 8601 dates (`2024-01-15`)
- Mermaid diagrams as fallback outside Obsidian
