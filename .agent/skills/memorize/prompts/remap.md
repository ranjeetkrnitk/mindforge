# remap

> ⚠️ DESTRUCTIVE — first-run vault reorganization.

## Phase 0 — Safety
1. Ask: dry-run or apply directly? Default: **dry-run** (`remap_dry_run_default: true`).
2. Remind user to back up / commit vault before a live run.

## Phase 1 — Inventory
Walk all vault files. For each: filename, path, tags, links, word count, approximate maturity.
Output: `| File | Current Path | Detected Domain | Detected Type | Maturity Signal |`

## Phase 2 — Classify (use REF.md heuristics)
- date-prefixed title → `episode`
- declarative sentence → `concept`
- ends with `?` → `question`
- Author + Year → `source`
- links-only body → `moc`
- maturity: 0 links=`fleeting`, 1-2=`developing`, 3++backlinks=`evergreen`

## Phase 3 — Propose changes
```
MOVE:      "old/path.md" → "concepts/domain/Claim title.md"
ADD TAGS:  domain/X, type/concept, maturity/developing
ADD LINKS: [[MOC]] (extends)
```

## Phase 4 — Write remap report
Write `vault_root/_system/_REMAP_REPORT.md` with sections: Summary (counts) · Changes Log · Conflicts · New Structure (tree).
Print: `✓ _system/_REMAP_REPORT.md`

## Phase 5 — Apply (confirmation required)
Move files → update `[[wikilinks]]` → inject frontmatter tags → create missing MOCs → write final report.
Print one line per file touched: `✓ moved: old/path.md → new/path.md`
End: `Remapped N files. Created M MOCs. Conflicts: X (see _REMAP_REPORT.md).`

## Rules
- Never delete — only move or rename
- Unclassifiable files → `inbox/` with `#status/needs-review`
- Flag naming conflicts; do not auto-resolve
- `_system/` untouched — exception: writing `_system/_REMAP_REPORT.md`

## Post-Action
After applying changes, run dashboard update (see `prompts/dashboard-update.md`).
