# tailor mode

## Input
If job not in trigger: ask "Which job? (Company + Role)"

## Load
- Job note: `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
- Resume note: `<vault_root>/<resume_note>`
- Extract from JD: required skills, nice-to-have skills, keywords, seniority signals

## Generate three sections

### 1. Skills match table
| Required Skill | Your Match | Evidence (from resume) |
|---|---|---|
| <skill> | Strong / Partial / Gap | <brief evidence or gap note> |

List all required skills from JD. Be honest about gaps.

### 2. ATS-optimized summary (3-4 sentences)
Rewrite your resume summary to mirror this JD's exact language and keywords.
Do not fabricate experience. Use first person. Lead with years of relevant experience.

### 3. Tailored bullet points
Rewrite the 3-5 resume bullets most relevant to this role.
Lead each with an impact metric. Use JD keywords verbatim where accurate.
Format: `- [Metric/impact] by [action] using [tech/method]`

## Output (terminal)
Print all three sections for review.

## Vault write
Append to job note:
```
## Tailored Resume
### Skills Match
<table>

### Summary
<summary>

### Bullets
<bullets>
```
Set frontmatter `stage: Tailoring`.
Update `_pipeline.md` row.
Print: `✓ Tailored content saved. Next: /jobhunt cover-letter`
