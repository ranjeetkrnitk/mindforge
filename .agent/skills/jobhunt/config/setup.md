# First-Run Setup

Run only when `setup_complete: false` in config/user.md.

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
