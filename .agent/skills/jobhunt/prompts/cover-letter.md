# cover-letter mode

## Input
If job not in trigger: ask "Which job? (Company + Role)"

## Load
- Job note: `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
  - Extract: JD, evaluation summary, tailored resume section (if exists)
- Company note `<vault>/Job Hunt/Companies/<Company>.md` (if exists - use for culture/tone signals)
- Resume note: `<vault_root>/<resume_note>` (fallback if no tailored section)

## Generate cover letter

**Para 1 - Hook (3-4 sentences)**
Open with a specific signal about this company (product, mission, recent news if known).
State the role. Name one strongest qualification match using JD language.

**Para 2 - Evidence (4-5 sentences)**
Two concrete examples from your background that address the top JD requirements.
Use metrics/numbers where available. Mirror JD keywords exactly.

**Para 3 - Close (2-3 sentences)**
Express genuine interest in the specific mission/product.
State availability. Simple call to action - not "please consider my application".

Tone: direct, confident, human. Never open with "I am writing to apply for".

## Output (terminal)
Print full letter for review.

## Vault write
Append to job note:
```
## Cover Letter
<letter>
```
Print: `✓ Cover letter saved. Next: /jobhunt apply or /jobhunt outreach`
