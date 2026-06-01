---
name: jobhunt
version: 0.1.0
description: >
  AI-powered job search pipeline. Scans job boards, evaluates postings,
  tailors resumes, drafts cover letters and outreach, tracks applications.
  Triggers: "jobhunt", "job search", "find jobs", "scan jobs", "evaluate job",
  "tailor resume", "cover letter", "track applications", "draft outreach",
  "help me apply", "outreach message".
agent: agnostic
compatibility:
  preferred_vault: obsidian
  requires: none
---

# /jobhunt

## Load Order
1. `../_shared/conventions.md`
2. `config/user.md`
3. `REF.md`
4. `prompts/<mode>.md`
5. Mode extras: `config/settings.md` (evaluate only), `ref/endpoints.md` (scan only)

## First-Run Setup
If `setup_complete: false` in config/user.md: load `config/setup.md` and follow it.
Otherwise: proceed silently.

## Mode Routing

| Trigger | Mode | Extra load |
|---|---|---|
| scan, find jobs, search jobs, job openings | scan | ref/endpoints.md |
| evaluate, score this job, assess this role | evaluate | config/settings.md |
| tailor, tailor my resume, optimize resume | tailor | - |
| cover letter, write cover, draft cover | cover-letter | - |
| track, pipeline, my applications, job hunt status | track | - |
| outreach, draft message, linkedin message, cold email | outreach | - |
| apply, fill application, help me apply | apply | - |

No trigger match: list all modes with one-line descriptions.
