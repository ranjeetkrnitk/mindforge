# apply mode

## Input
If job not in trigger: ask "Which job? (Company + Role)"

## Load
- Job note: `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
  - Extract: JD, tailored resume section, cover letter section
- config/user.md for personal info defaults

## Pre-check
If no `## Tailored Resume` in job note:
Print: `⚠ No tailored resume found. Run /jobhunt tailor first for best results. Continue anyway? (y/n)`

## Quick-apply path (fast)
If job note has BOTH `## Tailored Resume` AND `## Cover Letter` sections:
Print everything at once for copy-paste — no round trips:
1. Personal info block (from config/user.md)
2. Tailored bullets (from job note)
3. Skills list (Strong + Partial from match table)
4. Cover letter (from job note)
5. `⚠ Export tailored resume as PDF before uploading.`
Ask once at the end: "Any custom questions to answer? (paste them)"

## Guided path (when content is missing or custom questions exist)
Work through each section one at a time. Pull from vault note where available.

**Personal info** - pull from config or ask once.
**Work experience** - present tailored bullets; ask "ok/adjust" per role.
**Education** - ask user to confirm (not stored in config).
**Skills** - extract Strong + Partial matches from job note.
**Cover letter** - print for copy-paste. If missing, offer to run cover-letter mode first.
**Resume upload** - print: `⚠ Export tailored resume as PDF before uploading.`
**Custom questions** - one at a time, draft using JD + resume context, ask approval before next.

## Completion
Ask: "Application submitted? (y/n)"
On y:
- Set frontmatter `stage: Applied`, add `applied_date: YYYY-MM-DD`
- Update `_pipeline.md` row: stage + applied_date + last_updated
- Recalculate stats block
- Print: `✓ Application logged. Next: /jobhunt outreach to reach the hiring manager`

Never auto-submit. User retains final control at every step.
