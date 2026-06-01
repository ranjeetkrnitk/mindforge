# /jobhunt Skill - Design Spec

**Date:** 2026-06-01
**Status:** Approved

---

## Overview

`/jobhunt` is a single multi-mode skill for AI-powered job searching inside the mindforge skill ecosystem. It follows the same modular pattern as `memorize` and `reflect`: a lean `SKILL.md` routing table, per-mode prompt files, vault-native storage, and memorize-compatible frontmatter so job data participates in the broader personal knowledge graph.

---

## Directory Structure

```
.agent/skills/jobhunt/
├── SKILL.md                    # Routing table, load order, mode triggers (lean)
├── REF.md                      # Pipeline stages, status definitions, scoring dimensions
├── config/
│   ├── user.md                 # Vault path, resume note, preferences (gitignored)
│   └── settings.md             # Scoring weights, score threshold, pipeline stages
├── ref/
│   └── endpoints.md            # Greenhouse/Ashby/Lever endpoints (loaded only by scan)
├── prompts/
│   ├── scan.md                 # Job board + web search discovery
│   ├── evaluate.md             # 1-10 numeric scoring with summary report
│   ├── tailor.md               # ATS-optimized resume tailoring per job
│   ├── cover-letter.md         # Cover letter generation
│   ├── track.md                # Pipeline state viewer, stage mover, dashboard
│   ├── outreach.md             # LinkedIn/email message drafting
│   └── apply.md                # Application form assistance
└── templates/
    ├── job-entry.md            # Vault note template for one job (memorize-compatible)
    └── pipeline.md             # _pipeline.md dashboard template
```

**Vault structure created on first run:**
```
<vault>/Job Hunt/
├── _pipeline.md                # Master pipeline dashboard (MOC node)
└── Companies/
    └── <Company> - <Role>.md   # One episode note per job
```

---

## Token Efficiency

- `SKILL.md` is the only file always loaded - it stays under 60 lines
- Mode prompt files are loaded on demand - only the active mode's prompt is read
- `ref/endpoints.md` (large company list) is loaded only by scan mode
- `config/settings.md` (scoring weights) is loaded only by evaluate mode
- Prompt files stay under 50 lines each (per shared conventions)
- Templates are loaded only when writing new notes, not on read-only operations
- `REF.md` stays under 40 lines - pipeline stages and status definitions only

---

## Pipeline State

The pipeline lives in `<vault>/Job Hunt/_pipeline.md` as a `type/moc` node. Every mode reads it; write-modes update it atomically (read, patch, write - never overwrite from scratch).

**Stages:**
```
Discovered → Evaluated → Tailoring → Applied → Screening → Interviewing → Offered → Closed
```

`Closed` covers both rejected and withdrawn - a `status` field in the job note distinguishes them.

**Pipeline row format (one per job):**
```
| Company | Role | Score | Stage | Applied | Last Updated |
```

**Dashboard stats block** auto-updated at the top of `_pipeline.md` after every write:
```
## Stats
Active: 12  |  Applied: 5  |  Avg Score: 7.4  |  This week: 3 new, 2 moved
```

---

## Vault + Memorize Integration

Job notes use memorize-compatible frontmatter so `memorize harvest` can pick them up and `memorize recall` can surface them.

**Job entry note** (`type/episode` - timestamped personal capture):
```yaml
---
tags: [type/episode, domain/career, jobhunt/active]
created: YYYY-MM-DD
company: ""
role: ""
score: 0
stage: Discovered
status: active          # active | rejected | withdrawn | offered
location: ""
url: ""
salary_range: ""
related: []             # [[Company MOC]], [[Skill notes]]
maturity: fleeting
---
```

**Company note** (created once per company, `type/concept` - stable reference):
```yaml
---
tags: [type/concept, domain/career, jobhunt/company]
created: YYYY-MM-DD
aliases: []
related_sources: []
---
```

This means:
- `memorize harvest` surfaces job applications as episodes to consolidate
- `memorize recall "Stripe"` returns all job notes linked to Stripe
- `reflect weekly` can report job hunt activity alongside vault health
- `_pipeline.md` is a proper MOC node navigable from vault graph view

---

## Modes

### scan
- Asks at invocation: "Search via direct APIs, web search, or both?"
- Direct APIs: queries Greenhouse/Ashby/Lever endpoints from `ref/endpoints.md`
- Web search: queries job boards (LinkedIn, Indeed, levels.fyi) using target roles + location from config
- Deduplication: checks `_pipeline.md` before writing - skips jobs already tracked
- Output: compact table (company, role, location, match %) in terminal
- Writes: job stub notes to vault, appends rows to `_pipeline.md` at `Discovered`
- Company note: created lazily per company if not already present in vault

### evaluate
- Input: job URL or paste job description
- Scores 1-10 across 5 weighted dimensions (weights from `config/settings.md`):
  - Role fit (0.30) - JD vs your skills/experience
  - Compensation (0.25) - salary vs your minimum
  - Company stage (0.15) - startup/growth/enterprise preference
  - Location fit (0.15) - remote/hybrid/onsite
  - Growth potential (0.10) - tech stack, team size, trajectory
- Prints: score table + 3-sentence summary in terminal
- Writes: full report to job vault note, moves pipeline to `Evaluated`
- Cross-mode suggestion: if score >= 7, prints "Score 8.2 - run tailor mode? `/jobhunt tailor`"
- Score threshold filter: jobs below `min_score` in settings are flagged, not hidden

### tailor
- Reads: job note (JD, score report) + resume vault note from `config/user.md`
- Generates: ATS-optimized bullet points, keyword-injected summary, skills match table
- Writes: tailored content block to job note, moves pipeline to `Tailoring`
- Does NOT rewrite your full resume - outputs a job-specific addendum

### cover-letter
- Reads: job note + company note (if exists) + resume vault note
- Generates: 3-paragraph cover letter, role-specific, tone matches company culture signals
- Writes: cover letter to job note

### track
- Read-only by default: renders pipeline board in terminal
- `track move <company> <role> <stage>` moves a job to a new stage
- `track close <company> <role> rejected|withdrawn` closes a job
- Dashboard printed inline, `_pipeline.md` updated after any mutation

**Terminal dashboard output:**
```
🎯 Job Hunt Pipeline
─────────────────────────────────────────────────────
 Discovered  Evaluated  Tailoring  Applied  Screening
    3           4           2         3         1
─────────────────────────────────────────────────────
 Interviewing  Offered  Closed    Active: 13   Avg: 7.1
      1           0       2       This week: ↑4 new
```

### outreach
- Input: company + role (looks up job note automatically)
- Generates: LinkedIn connection request OR cold email, 3 variants (warm/neutral/direct)
- Reads company note for culture/tone signals if available
- Writes: chosen draft to job note

### apply
- Reads: job note (tailored resume, cover letter, JD)
- Walks through application form fields, pulling from vault note content
- Flags missing info (e.g. no salary range in config)
- Does not auto-submit - user retains final control
- Writes: application date to job note, moves pipeline to `Applied`

---

## Config Files

**`config/user.md`** (gitignored):
```yaml
setup_complete: false
vault_root: ""
resume_note: ""             # e.g. "Career/Resume.md"
target_roles: []            # e.g. ["Senior Software Engineer"]
target_companies: []        # wishlist - prioritized in scan
locations: []               # e.g. ["Remote", "San Francisco"]
salary_min: 0
open_to_relocation: false
```

**`config/settings.md`:**
```yaml
scoring_weights:
  role_fit: 0.30
  compensation: 0.25
  company_stage: 0.15
  location: 0.15
  growth_potential: 0.15

min_score: 6.0              # Jobs below this are flagged in scan results
pipeline_stages:
  - Discovered
  - Evaluated
  - Tailoring
  - Applied
  - Screening
  - Interviewing
  - Offered
  - Closed
```

---

## First-Run Setup

1. Check `config/user.md` - if `setup_complete: false`:
   - Try copying `vault_root` from `memorize/config/user.md` first
   - If not found, ask: "Where is your Obsidian vault?"
   - Ask: "Which note is your resume? (relative path from vault root)"
   - Ask for target roles, locations, salary minimum
   - Create `<vault>/Job Hunt/` and `<vault>/Job Hunt/Companies/`
   - Initialize blank `_pipeline.md` from template
   - Set `setup_complete: true`
   - Print: `💡 /add-dir ~/.copilot/skills` and `/add-dir <vault>`
2. If `setup_complete: true` - proceed silently

---

## Additional Improvements

**Deduplication:** Before writing any job note, scan `_pipeline.md` for matching company+role. Skip silently if found, print `⚠ Already tracked: Stripe - Staff Engineer`.

**reflect integration:** `reflect weekly` will naturally pick up `type/episode` job notes via the shared vault scan. No extra wiring needed - the frontmatter tags `domain/career` and `jobhunt/active` make them identifiable.

**Cross-mode prompting:** After evaluate (score >= 7) and after scan, print the next logical step. Keep it to one line - not a forced workflow.

**Score threshold:** `min_score` in settings filters scan noise. Below threshold jobs are shown with `⚠` marker and excluded from counts - never silently dropped.

---

## Load Order (every invocation)

1. `../_shared/conventions.md`
2. `config/user.md`
3. `REF.md`
4. Mode-specific: `prompts/<mode>.md`
5. Mode-specific extras: `config/settings.md` (evaluate only), `ref/endpoints.md` (scan only)

---

## Trigger Phrases

| Phrase | Mode |
|---|---|
| "scan", "find jobs", "search jobs", "job openings" | scan |
| "evaluate", "score this job", "assess this role" | evaluate |
| "tailor", "tailor my resume", "optimize resume" | tailor |
| "cover letter", "write cover", "draft cover" | cover-letter |
| "track", "pipeline", "my applications", "job hunt status" | track |
| "outreach", "draft message", "linkedin message", "cold email" | outreach |
| "apply", "fill application", "help me apply" | apply |

No match: list available modes with one-line descriptions.
