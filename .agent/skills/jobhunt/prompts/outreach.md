# outreach mode

## Input
If job not in trigger: ask "Which job? (Company + Role)"
Ask: "Type: (1) LinkedIn connection request  (2) Cold email  (3) Follow-up after applying"

## Load
- Job note: `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
- Company note `<vault>/Job Hunt/Companies/<Company>.md` (if exists - culture/tone signals)

## Generate 3 variants

### Type 1: LinkedIn connection request (300 char limit)
- Warm: reference specific company work or shared background
- Neutral: direct value prop + role mention
- Direct: one-sentence hook + reason to connect

### Type 2: Cold email (to hiring manager or recruiter)
For each variant, include:
- Subject line (max 8 words, no "job application")
- Body (4 sentences max):
  - Hook: one specific signal about their product/team
  - Why you: strongest qualification match, one metric
  - Ask: 15-minute conversation, not "a job"
- Sign-off: name + LinkedIn URL

### Type 3: Follow-up (sent 7+ days after applying, no response)
2-3 sentences per variant:
- Reference application date and role title
- Reiterate top qualification in one phrase
- Polite close with available timing

## Output (terminal)
Print all 3 variants for chosen type.
Ask: "Save which variant? (1/2/3/skip)"

## Vault write (on 1/2/3)
Append to job note:
```
## Outreach
**Type:** <type>  **Variant:** <N>  **Date:** <today>
<message>
```
Print: `✓ Outreach draft saved.`
