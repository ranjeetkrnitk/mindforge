# review

> Validate requirements for gaps, conflicts, and completeness.

## Steps

1. **Load** requirements from session
2. **Check coverage** per REF.md checklist
3. **Detect conflicts**: scope-time, performance-cost, security-UX, scale-timeline
4. **Find gaps**: missing personas, flows, NFRs, metrics, constraints
5. **Assess risks**: likelihood × impact → 🔴🟡🟢
6. **Validate SMART** per REF.md
7. **Present** findings, ask for resolution

## Output

- Coverage: checkmarks per domain
- Conflicts table: conflict, severity, resolution
- Gaps table: gap, domain, question to resolve
- Risk table: risk, likelihood, impact, status
- SMART table: req, S/M/A/R/T checkmarks, issues
- Status: blockers + warnings count
- Next: resolve issues, then run plan

## Rules
- Present findings, don't assume resolutions
- Use `ask_user` with choices for conflict resolution
- Blockers must resolve before plan mode
