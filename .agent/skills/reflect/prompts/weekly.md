# weekly

> Comprehensive weekly productivity report with JIRA, services, ideas, and caching.

## Steps
1. **Date range**: today - 7 days (or specified week)
2. **Scan** per REF.md vault scan procedure
3. **Filter** notes modified in range; load all for link graph
4. **Extract**:
   - JIRA tickets (KIJI-XXX, CHG0XXXXXX, SNOW-XXX)
   - Services touched (storefront, cart-service, payment, checkout, cxone, rex, etc.)
   - Ideas captured (notes with idea/concept/proposal in name or content)
   - Work vs Craft vs Self breakdown by domain tags
5. **Compute** per REF.md: graph metrics, CLS signals, emotion analysis
6. **Detect** burst topics (3+ notes on same topic this week)
7. **Extract change summaries** from episode notes (## Summary sections)
8. **Generate reports** via `scripts/weekly_report.py`

## Report Generation
Always run the comprehensive report script:
```bash
python3 ~/.copilot/skills/reflect/scripts/weekly_report.py "<vault_root>"
```
This generates:
- `_dashboards/weekly-YYYY-WNN.html` - Visual dashboard
- `_dashboards/weekly-YYYY-WNN.md` - Text summary

Reports are **cached by week number**. Use `--force` to regenerate:
```bash
python3 ~/.copilot/skills/reflect/scripts/weekly_report.py "<vault_root>" --force
```

For past weeks, specify the week ID:
```bash
python3 ~/.copilot/skills/reflect/scripts/weekly_report.py "<vault_root>" --week 2026-W19
```

## Output
```
## 📅 Weekly Productivity Report: YYYY-WNN
*Month DD - Month DD, YYYY*

### Overview
- **N** notes modified
- **N** JIRA tickets referenced
- **N** services touched
- **N** ideas captured
- **N** code-related notes

### Work Breakdown
- Work: X items
- Craft/Tech: Y items
- Self: Z items

### JIRA Tickets Worked On
- **KIJI-123**: Brief context from notes
- **CHG0114968**: Change request work

### Services Touched
- **cart-service**: N notes
- **payment-service**: M notes

### Key Changes
#### Title of Change [domain]
Summary in 2-3 sentences explaining what was done and why.

#### Another Change Title [domain]
Brief summary of the work completed.

### New Ideas
- **Idea Title**: Brief description...

### Analysis & Investigations
- Investigation note 1
- Review note 2

📊 Reports saved:
- _dashboards/weekly-YYYY-WNN.html
- _dashboards/weekly-YYYY-WNN.md
```

Zero notes? Say so, suggest capture.
