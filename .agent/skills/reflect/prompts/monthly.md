# monthly

> Current calendar month with trends and progression.

## Steps
1. **Date range**: first of month to today (or past N days if configured)
2. **Scan** per REF.md; group by week within month
3. **Compute**: graph metrics, CLS signals, emotion trends
4. **Analyze trends**: week-over-week velocity, domain shifts, burst/decline detection

## Output
```
## 📅 Monthly ({{month}} {{year}})

**Overview**: N created, M modified, X maturity progressions
Velocity: Y notes/week (↑↓ vs last month)

**Week-by-Week**
- W1: ████░░ 8 notes (technology)
- W2: ██████ 12 notes 🔥 burst: "topic"
- W3: ██░░░░ 4 notes (light)

**🔄 Maturity Progression**
- [[Episode A]] → developing (+3 links)
- [[Concept B]] → evergreen (consolidated)
Velocity: 0.8/week (↑ from 0.5)

**📈 Trends**
🔥 Burst: "topic" (6 notes W2)
📉 Declining: "docker" (3→1→0)
🌱 Emerging: #new-tag (first W2)

**💚 Emotional Summary**
High-arousal: 4 notes | Valence trend: increasingly positive
Peak moment: [[Exciting discovery]] (May 12)

**😴 Dormant All Month**: domain/philosophy, domain/people

**🗂️ Domain Distribution**
technology ████████ 60% | self ███░ 20% | craft ██░ 13% | philosophy ░ 0% ⚠️

**💡 Reflect**
- What theme dominated? Intentional?
- Which burst topic needs deeper exploration?
- Neglected domains to revive?
```
