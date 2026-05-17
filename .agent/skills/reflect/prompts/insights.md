# insights

> Time-independent structural analysis with health score.

## Steps
1. **Full scan** per REF.md
2. **Compute all metrics**: hub, bridge, orphan risk, cluster cohesion
3. **Maturity distribution**: fleeting/developing/evergreen ratios
4. **Domain distribution**: activity per domain
5. **Health score**: weighted composite (see below)
6. **Recommendations**: top 3-5 actionable items

## Health Score (0-100)
```
30% link_density (avg links/note, target: 2.5)
20% maturity_balance (target: 60/30/10 fleeting/developing/evergreen)
20% orphan_ratio (fewer = better)
20% cross_domain (bridges exist)
10% question_answer_ratio (questions get answered)
```

## Output
```
## 🔍 Vault Insights

**Overview**
Total: {{N}} notes, {{M}} links | Avg: {{X}} links/note
Health: {{score}}/100 ⭐⭐⭐⭐

**🌟 Hubs** (anchors)
| Note | Links |
|------|-------|
| [[A]] | 15 |
| [[B]] | 12 |

**🌉 Bridges** (cross-domain)
| Note | Connects | Score |
|------|----------|-------|
| [[X]] | tech ↔ philosophy | 0.75 |

**🏝️ Orphans** (need linking)
| Note | Age | Risk |
|------|-----|------|
| [[Y]] | 30d | 0.85 |

**📊 Maturity**
Evergreen ██░░░░ 10% | Developing ████░░ 25% | Fleeting █████████ 65%
Status: ⚠️ consolidation needed if fleeting >80%

**🗂️ Domains**
technology ████████ 40% | self ████ 20% | craft ██ 12% | philosophy █ 5% ⚠️

**💚 Emotional Landscape**
High-arousal notes: 8 | Valence: 70% positive
Most emotional: [[Peak Experience]] (high/positive)

**🔓 Open Loops**
❓ Unanswered: [[Q1?]], [[Q2?]]
📝 Stale fleeting (>14d): 12 notes
🔄 Promote ready: [[Episode]] (5 links)

**🏥 Recommendations**
1. Link: 15 orphans need connections
2. Consolidate: 12 stale fleeting notes
3. Answer: 5 questions pending
4. Explore: philosophy domain neglected

**💡 Reflect**
- Which hub deserves deeper exploration?
- Can orphans be archived instead of linked?
- What question to answer this week?
```

Large vaults (500+): sample or paginate lists.
