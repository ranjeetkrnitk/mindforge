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
Check `config/user.md` for `setup_complete: false`:
1. Try copying `vault_root` from `../memorize/config/user.md`
2. If empty: ask `"Where is your Obsidian vault? (absolute path)"`
3. Ask `"Which note is your resume? (path from vault root, e.g. Career/Resume.md)"`
4. Ask `"Target roles? (comma-separated)"`
5. Ask `"Preferred locations? (e.g. Remote, San Francisco)"`
6. Ask `"Minimum salary? (number, e.g. 150000)"`
7. Create `<vault>/Job Hunt/` and `<vault>/Job Hunt/Companies/`
8. Copy `templates/pipeline.md` → `<vault>/Job Hunt/_pipeline.md` (replace `{{date}}`)
9. Write answers to `config/user.md`, set `setup_complete: true`
10. Print: `💡 /add-dir ~/.copilot/skills` and `/add-dir <vault_root>`
11. Print: `✓ Pipeline initialized. Run: /jobhunt scan`

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
