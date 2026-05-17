# reflect — Skill-Specific Procedures

> Agents: loaded via SKILL.md. Vault scan and graph metrics in `_shared/conventions.md`.

## CLS Signals (consolidation)
- **Replay**: older note linked from newer note
- **Promotion ready**: episode + 3+ links + 7+ days old
- **Maturity progression**: fleeting→developing (2+ links), developing→evergreen (consolidate revisit)

## Spaced Rep Signals
- **Dormant**: topic/domain not touched in 14+ days
- **Review due**: hub note not accessed in 7+ days

## Emotion Analysis
Emotion schema in `_shared/conventions.md`. For reflect:
- **Peaks**: arousal=high in time range
- **Trend**: positive/negative/neutral ratio
- **Clusters**: dominant mood per week

## Standard Output Sections
```
**Activity**: notes created, modified, replay events
**🔄 Consolidation**: promotion candidates, replay events  
**😴 Dormant**: untouched topics (14+ days)
**💚 Emotional Peaks**: high-arousal notes this period
**📊 Highlights**: hubs, questions, orphans
**💡 Reflection**: 2-3 prompts based on findings
```

## Rules (all modes)
- Read-only: never modify notes
- Skip _archived/, _system/
- Handle missing frontmatter gracefully
- Always include reflection prompts
