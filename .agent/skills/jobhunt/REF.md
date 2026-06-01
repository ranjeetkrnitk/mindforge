# /jobhunt Reference

## Pipeline Stages
`Discovered → Evaluated → Tailoring → Applied → Screening → Interviewing → Offered → Closed`

- Discovered: found via scan, not yet scored
- Evaluated: scored 1-10, decision to pursue confirmed
- Tailoring: resume + cover letter customized for role
- Applied: application submitted
- Screening: recruiter or hiring manager contact initiated
- Interviewing: technical or behavioral rounds in progress
- Offered: offer received, under evaluation
- Closed: status = rejected | withdrawn | accepted

## Scoring Dimensions (evaluate mode)
| Dimension | Weight | Scoring Guide |
|---|---|---|
| role_fit | 0.30 | Match required skills vs resume. >80% match = 8-10, <50% = 1-4 |
| compensation | 0.25 | Listed salary vs salary_min. >20% above = 9-10, unknown = 6 |
| company_stage | 0.15 | Match stated preference (startup/growth/enterprise). Exact = 9-10, opposite = 3-4 |
| location | 0.15 | Remote in open_to_relocation=true → 10. Onsite in non-target city → 3 |
| growth_potential | 0.15 | Modern stack + L-levels offered + team size >20 = 8-10 |

## Job Note Frontmatter Schema
```yaml
tags: [type/episode, domain/career, jobhunt/active]
created: YYYY-MM-DD
company: ""
role: ""
score: 0
stage: Discovered
status: active
location: ""
url: ""
salary_range: ""
related: []
maturity: fleeting
```

## Pipeline Row Format
`| Company | Role | Score | Stage | Applied Date | Last Updated |`
