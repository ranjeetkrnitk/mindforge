# prune

> Detect and triage empty or stub notes.

## Definitions
| Class | Condition |
|-------|-----------|
| empty | No body (frontmatter only or 0 bytes) |
| stub | Body < `prune_min_body_words` (default 20) |
| ok | Leave untouched |

## Steps

1. **Scan** vault folders (skip _system/, _archived/)
   - Read each .md file
   - Strip YAML frontmatter → count body words
   - Classify: empty | stub | ok

2. **Flag** (non-destructive)
   - Patch YAML: `stub: true`, `tags: [..., maturity/stub]`, `stub_detected: ISO_DATE`
   - Print: `⚑ path [empty|stub, N words]`

3. **Report**
   ```
   Empty: N | Stub: N | OK: N
   Flagged N file(s)
   ```

4. **Archive** (if requested + confirmed)
   - Move to `_archived/stubs/YYYY-MM/`
   - Print: `✗ path → _archived/stubs/`

## Rules
- Never hard-delete (always archive)
- Dry-run by default if `prune_dry_run_default: true`
- Preserve existing frontmatter keys
