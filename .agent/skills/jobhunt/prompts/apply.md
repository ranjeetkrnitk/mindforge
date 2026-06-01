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

## Application walkthrough
Work through each section one at a time. Pull from vault note where available.

**Personal info**
Name, email, location, LinkedIn, GitHub/portfolio - pull from config or ask once.

**Work experience**
Present tailored bullets from job note, one role at a time.
Ask: "Does this look good, or adjust? (ok/adjust)"

**Education**
Ask user to confirm - not stored in config.

**Skills**
Extract from skills match table in job note (Strong + Partial matches only).

**Cover letter**
Print saved cover letter for copy-paste. If none, offer to run cover-letter mode first.

**Resume upload reminder**
Print: `⚠ Remember to export your tailored resume as PDF before uploading.`

**Custom questions**
Tackle one at a time. Use JD context + resume note to draft answers.
Ask for approval before moving to next question.

## Completion
Ask: "Application submitted? (y/n)"
On y:
- Set frontmatter `stage: Applied`, add `applied_date: YYYY-MM-DD`
- Update `_pipeline.md` row: stage + applied_date + last_updated
- Recalculate stats block
- Print: `✓ Application logged. Next: /jobhunt outreach to reach the hiring manager`

Never auto-submit. User retains final control at every step.
