# custom

> User-specified date range with period comparison.

## Steps
1. **Parse range**: "May 1-15", "last 3 days", "Q1", etc.
   - Ambiguous? Ask user.
2. **Comparison period**: prior equivalent duration
3. **Scan** per REF.md; compute metrics for both periods
4. **Delta analysis**: notes, links, domains, velocity

## Date Parsing
| Input | Range |
|-------|-------|
| "May 1-15" | 2026-05-01 to 2026-05-15 |
| "last 3 days" | today-3 to today |
| "Q1" | Jan 1 - Mar 31 |
| "January" | full month |

## Output
```
## 📅 Custom ({{start}} - {{end}})

**Period**: {{N}} days | {{X}} notes (↑↓ {{delta}} vs prior)
Velocity: {{Y}} notes/day

**Comparison**
| Metric | This | Prior | Δ |
|--------|------|-------|---|
| Notes | 23 | 15 | +8 ↑ |
| Links | 45 | 32 | +13 |
| Questions | 5 | 3 | +2 |

**Domain Shifts**
technology: +50% 📈 | self: -62% 📉

**🔄 Consolidation**: 3 promoted, 8 replays

**💚 Emotional Peaks**: [[Note]] (high arousal, positive)

**📈 Timeline** (if >7 days)
- Week 1: ████████ 14 notes
- Week 2: █████░░░ 9 notes

**🔗 Cross-Period Influence**
Notes from this period linked later: 12
Most influential: [[Note]] (6 later links)

**💡 Reflect**
- What drove the activity change?
- Focus areas intentional?
```

For ranges >90 days, offer monthly breakdown.
