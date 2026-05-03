---
name: memorize
version: 0.2.0
description: >
  Second-brain skill grounded in CLS theory. Captures, consolidates, maps,
  and reorganizes knowledge. Triggers: "remember this", "memorize", "consolidate
  my notes", "show me a mind map", "remap my vault", "harvest this session".
agent: agnostic
compatibility:
  preferred_vault: obsidian
  format: markdown + YAML frontmatter
  requires: none
---

# /memorize

## Always load first
1. `config/user.md` — vault path (personal, gitignored)
2. `REF.md` — node types, link types, domains, naming conventions
3. `config/settings.md` — thresholds

## First-run setup (run before any mode)

Check `config/user.md`:
- If `setup_complete: false` or `vault_root` is empty → run setup:
  1. Ask: *"Where is your Obsidian vault? (absolute path)"*
  2. Write the answer to `config/user.md` as `vault_root` and set `setup_complete: true`
  3. Confirm: `✓ Vault set to <path>. You're ready.`
- If `setup_complete: true` → proceed silently with `vault_root` from `config/user.md`

## Output behavior (all modes)
- **Write files directly** to `vault_root` using available file tools
- **Print one line per file written**: `✓ <relative-path-from-vault-root>`
- **No note content** in output unless the user explicitly asks to see it
- End with a **single summary line**: `Saved N note(s) to <vault_root>`

## Modes

| # | mode | trigger phrases | prompt |
|---|---|---|---|
| 1 | `capture` | "remember this", "memorize", "note this", "log this" | `prompts/capture.md` |
| 2 | `consolidate` | "consolidate", "what have I learned about X", "strengthen notes" | `prompts/consolidate.md` |
| 3 | `mindmap` | "mind map", "visualize my knowledge", "map this topic" | `prompts/mindmap.md` |
| 4 | `remap` | "remap my vault", "reorganize my notes", "apply CLS" | `prompts/remap.md` |
| 5 | `harvest` | "harvest this session", "save what we discussed", "memorize this conversation" | `prompts/harvest.md` |

## File Structure

```
.agent/skills/memorize/
├── SKILL.md
├── REF.md                  ← merged quick reference (read this, not schema/)
├── README.md
├── config/
│   ├── settings.md         ← tunable thresholds
│   └── user.md             ← local vault path (gitignored, written on first run)
├── prompts/                ← one file per mode
├── templates/              ← concept, episode, claim, source, moc
└── schema/                 ← full docs for humans; agents use REF.md
```

## Output conventions
- YAML frontmatter on all notes
- `[[wikilink]]` syntax for links
- ISO 8601 dates (`2024-01-15`)
- Mermaid diagrams as fallback outside Obsidian
