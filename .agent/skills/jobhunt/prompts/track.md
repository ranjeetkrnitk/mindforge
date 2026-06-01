# track mode

## Default (no sub-command)
Read `<vault>/Job Hunt/_pipeline.md`.
Render pipeline board in terminal:

```
🎯 Job Hunt Pipeline
─────────────────────────────────────────────────────────────────
 Discovered  Evaluated  Tailoring  Applied  Screening
     N           N           N        N         N
─────────────────────────────────────────────────────────────────
 Interviewing  Offered  Closed    Active: N   Avg Score: X.X
      N           N       N       This week: ↑N new, N moved
─────────────────────────────────────────────────────────────────
```

Then list active jobs grouped by stage (skip Closed):
```
Evaluated:
  • Stripe - Staff Engineer (8.2)  last updated: 2026-05-30
Applied:
  • Anthropic - Senior ML Engineer (7.8)  applied: 2026-05-28
```

## sub-command: move
Trigger: "move <Company> <Role> to <Stage>" or "track move ..."
1. Validate stage exists in `pipeline_stages` (config/settings.md)
2. Update job note frontmatter: `stage: <Stage>`
3. Update `_pipeline.md` row: stage + last_updated = today
4. Recalculate stats block
5. Print: `→ <Company> - <Role> moved to <Stage>`

## sub-command: close
Trigger: "close <Company> <Role> as rejected|withdrawn|accepted"
1. Update job note: `stage: Closed`, `status: <reason>`, `maturity: archived`
2. Update `_pipeline.md` row: stage + last_updated
3. Recalculate stats block
4. Print: `✗ <Company> - <Role> closed (<reason>)`

## Stats recalculation
Active = all rows where stage != Closed
Applied = rows where stage in [Applied, Screening, Interviewing, Offered]
Avg Score = mean of non-zero scores
This week = rows where last_updated >= 7 days ago
