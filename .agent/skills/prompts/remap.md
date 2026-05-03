# Prompt: remap mode

> First-run vault reorganization. Apply CLS taxonomy to existing notes.
> ⚠️ DESTRUCTIVE — always dry-run first and confirm with user before applying.

---

## Your job in this mode

Audit an existing Obsidian vault and reorganize it to match the CLS-based
taxonomy defined in `schema/taxonomy.md`. This is a one-time (or periodic)
deep restructuring pass.

---

## Phase 0 — Safety check

Before anything:
1. Confirm with the user: *"This will propose moving and renaming files. Should I dry-run first or do you want to apply changes directly?"*
2. Default to **dry-run**. Never apply changes without explicit confirmation.
3. Remind the user to commit or back up the vault before a live run.

---

## Phase 1 — Inventory

Walk all files in the vault. For each file, extract:
- Current filename and path
- Existing tags (from frontmatter or inline `#tags`)
- Existing links (`[[wikilinks]]`)
- Word count and approximate maturity

Build a flat inventory list:
```
| File | Current Path | Detected Domain | Detected Type | Maturity Signal |
```

---

## Phase 2 — Classification

Using `schema/taxonomy.md` and `schema/node-types.md`, classify each file:

**Domain detection heuristics:**
- Keywords in title and body → map to `#domain/*` tags
- Existing folder → use as weak prior
- Backlink context → infer domain from what links to this note

**Type detection heuristics:**
- Date-prefixed title → `episode`
- Declarative sentence title → `concept`
- Title ending in `?` → `question`
- Author + Year in title → `source`
- Multiple `[[links]]` with no body → `moc`

**Maturity detection heuristics:**
- 0 outbound links → `fleeting`
- 1-2 links → `developing`
- 3+ links + multiple backlinks → `evergreen`

---

## Phase 3 — Propose changes

For each file, propose:
1. New folder path (based on taxonomy)
2. New filename (based on naming conventions)
3. Tags to add to frontmatter
4. Links to add or correct

Format:
```
MOVE:   "Old Path/file.md"
     →  "concepts/technology/Attention mechanisms scale better than RNNs.md"
ADD TAGS: #domain/technology, #type/concept, #maturity/developing
ADD LINKS: [[Transformers MOC]] (extends)
```

---

## Phase 4 — Generate remap report

Write a `_system/_REMAP_REPORT.md` file containing:

```markdown
# Remap Report — YYYY-MM-DD

## Summary
- Total files scanned: N
- Files moved: M
- Files renamed: X
- Tags added: Y
- New MOCs created: Z
- Conflicts (manual review needed): [list]

## Changes Log
[full list of MOVE / RENAME / TAG operations]

## Conflicts
[files that could not be auto-classified — needs user decision]

## New Structure
[tree view of vault after remap]
```

---

## Phase 5 — Apply (only after confirmation)

If user confirms:
1. Move files to new paths
2. Update all `[[wikilinks]]` to reflect new filenames
3. Inject frontmatter tags
4. Create missing MOC notes
5. Write the final `_REMAP_REPORT.md`

---

## Rules for remap mode

- Never delete files — only move or rename
- Preserve all existing `[[wikilinks]]` — update targets, not remove
- If a file cannot be classified confidently, put it in `inbox/` with `#status/needs-review`
- Flag but do not auto-resolve naming conflicts
- Leave `_system/` folder untouched
