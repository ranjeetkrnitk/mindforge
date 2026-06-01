# outreach mode

## Input
If job not in trigger: ask "Which job? (Company + Role)"
Ask in one prompt: "Type + tone — e.g. '1 warm', '2 direct', '3':
  (1) LinkedIn request  (2) Cold email  (3) Follow-up
  Tone: warm | neutral | direct (default: neutral)"

## Load
- Job note: `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
- Company note `<vault>/Job Hunt/Companies/<Company>.md` (if exists - culture/tone signals)

## Generate one targeted variant

### Type 1: LinkedIn connection request (300 char limit)
- warm: reference specific company work or shared background
- neutral: direct value prop + role mention
- direct: one-sentence hook + reason to connect

### Type 2: Cold email (to hiring manager or recruiter)
- Subject line (max 8 words, no "job application")
- Body (4 sentences max): hook → why you (one metric) → ask for 15-min call
- Sign-off: name + LinkedIn URL
Tone shapes formality and confidence level.

### Type 3: Follow-up (7+ days after applying, no response)
2-3 sentences: reference application date + role, reiterate top qualification, polite close.

## Output (terminal)
Print the single generated variant.
Ask: "Save this? (y/n)  Or regenerate with different tone? (warm/neutral/direct)"

## Vault write (on 1/2/3)
Append to job note:
```
## Outreach
**Type:** <type>  **Variant:** <N>  **Date:** <today>
<message>
```
Print: `✓ Outreach draft saved.`
