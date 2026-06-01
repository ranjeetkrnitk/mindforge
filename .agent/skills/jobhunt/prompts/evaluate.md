# evaluate mode

## Input
If job not in trigger: ask "Which job? (Company + Role, or paste URL / JD)"

## Load
- Job note: `<vault>/Job Hunt/Companies/<Company> - <Role>.md`
- Resume note: `<vault_root>/<resume_note>` — read once per session; reuse if already loaded earlier this conversation
- `config/settings.md` for scoring weights

## Score each dimension 1-10
| Dimension | Weight | Score | Weighted |
|---|---|---|---|
| Role fit | 0.30 | ? | |
| Compensation | 0.25 | ? | |
| Company stage | 0.15 | ? | |
| Location | 0.15 | ? | |
| Growth potential | 0.15 | ? | |
| **Total** | 1.00 | | **/10** |

Use scoring guide in REF.md. Round total to 1 decimal.

## Output (terminal)
1. Print score table with filled values
2. Print 3-sentence summary:
   - Overall recommendation (pursue / skip / borderline)
   - Strongest positive signal
   - Biggest risk or gap

## Vault write
- Update job note frontmatter: `score: <value>`, `stage: Evaluated`
- Append section to job note:
  ```
  ## Evaluation
  <score table>
  <3-sentence summary>
  ```
- Update `_pipeline.md` row: score + stage + today's date in Last Updated
- Recalculate stats block

## Next step suggestion
- score >= 7.0: `✓ Score <X> - strong match. Next: /jobhunt tailor`
- score 5.0-6.9: `⚠ Score <X> - borderline. Worth pursuing if role_fit >= 8.`
- score < 5.0: `✗ Score <X> - below threshold. Consider skipping.`
