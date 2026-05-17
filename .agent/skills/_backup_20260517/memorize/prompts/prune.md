# prune

> Vault hygiene — detect and triage empty or context-poor notes.

Read: `REF.md` · `config/settings.md` (`prune_min_body_words`, `prune_dry_run_default`, `prune_requires_confirmation`)

## Goal

Find markdown notes that carry too little content to be useful, flag them
non-destructively, and optionally remove confirmed dead weight.

---

## Definitions

| class | condition |
|---|---|
| `empty` | File has no body at all — only YAML frontmatter or 0 bytes |
| `stub` | Body word count < `prune_min_body_words` (default 20) |
| `ok` | Everything else — leave untouched |

---

## Steps

### 1 — Scan
Walk every vault folder listed in `config/settings.md` (`inbox_path`, `episodes_path`,
`concepts_path`, `sources_path`, `maps_path`, `people_path`).
Collect all `.md` files. Skip files inside `_system/` and `_archived/`.

For each file:
- Read content
- Strip YAML frontmatter block (`---…---`) to get **body**
- Count words in body
- Classify: `empty` | `stub` | `ok`

### 2 — Flag (non-destructive, always runs)
For each `empty` or `stub` file, patch its YAML frontmatter:
```yaml
stub: true
tags: [...existing tags..., maturity/stub]   # add maturity/stub if not already present
stub_reason: "{{empty|stub}}"                # "empty" or "stub"
stub_detected: "{{ISO_DATE}}"
```
Do **not** alter the body. Do **not** rename or move the file.
Print: `⚑ <relative-path> [empty|stub, N words]`

### 3 — Report
After scanning, print a grouped summary:

```
Prune scan complete.
  Empty  : N file(s)
  Stub   : N file(s)  (< prune_min_body_words words)
  OK     : N file(s)

Flagged N file(s) with stub: true in frontmatter.
```

### 4 — Deletion (only if user explicitly requests it)
If `prune_requires_confirmation: true` (default), ask the user:
> "Delete the N flagged stub/empty files? This cannot be undone. (yes / no)"

On confirmation:
- Move files to `_archived/stubs/YYYY-MM/` (safer than hard delete)
- Print: `✗ <relative-path> → _archived/stubs/YYYY-MM/`
- End with: `Pruned N file(s). Archived to _archived/stubs/YYYY-MM/`

If `prune_requires_confirmation: false`, archive immediately without prompting.

---

## Rules
- **Never hard-delete** files — always archive to `_archived/stubs/` as the destructive step
- **Never touch `ok` files** — no collateral edits
- **Dry-run by default**: if `prune_dry_run_default: true`, skip step 2 and only print what *would* be flagged, prefixed with `(dry-run)`
- Frontmatter patching must preserve all existing keys; only add/update `stub`, `stub_reason`, `stub_detected`, and `tags`
- If a file has no frontmatter at all, prepend a minimal block before flagging
