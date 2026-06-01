# scan mode

## Step 1: Search type
Ask: "Search via: (1) Direct APIs  (2) Web search  (3) Both?"

## Step 2a: Direct API search (if 1 or 3)
Load `ref/endpoints.md`.
Fetch all companies in parallel (do not fetch sequentially):
- `target_companies` from config/user.md → match slug in endpoints.md → fetch `<base_url>/<slug>/jobs`
- Also fetch top 10 endpoints.md companies not in `target_companies`
- Filter results: title matches any `target_roles` (case-insensitive), location matches `locations` OR remote

## Step 2b: Web search (if 2 or 3)
For each `target_role` + `location` combo (max 3 combos):
- Query: `"{role}" jobs {location} site:linkedin.com OR site:greenhouse.io OR site:lever.co OR site:ashbyhq.com`
- Parse: company, role, location, URL

## Step 3: Deduplication
Read `<vault>/Job Hunt/_pipeline.md`.
Skip jobs where company+role already appear in pipeline.
Print: `⚠ Already tracked: <Company> - <Role>` per skip.

## Step 4: Output
```
Company           | Role                    | Location  | Board
──────────────────┼─────────────────────────┼───────────┼──────────
Stripe            | Staff Engineer          | Remote    | Greenhouse
Anthropic         | Senior ML Engineer      | SF        | Lever
```
If N <= 5: skip confirmation, write immediately and note "Auto-writing N jobs."
If N > 5: print "Found N new jobs. Write to vault? (y/n)"

## Step 5: Vault write
For each job:
1. Fill `templates/job-entry.md` → write `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
2. If no `<vault>/Job Hunt/Companies/<Company>.md`: create minimal company concept note
3. Append row to `_pipeline.md`
4. Print: `✓ Job Hunt/Companies/<Company> - <Role>.md`

After all writes:
- Recalculate stats block in `_pipeline.md` (active count, this-week count)
- Print: `Saved N note(s). Next: /jobhunt evaluate`
