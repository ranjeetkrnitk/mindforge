# dashboard

> Generate interactive HTML dashboard for vault health visualization.

## Trigger
"dashboard", "html report", "vault dashboard", "generate dashboard"

## Data Collection

Gather via shell commands:
```
1. Total notes: find vault -name "*.md" | wc -l
2. Domain dist: grep -roh 'domain/[a-z]*' | sort | uniq -c
3. Type dist: grep -roh 'type/[a-z]*' | sort | uniq -c
4. Maturity dist: grep -oh 'maturity: [a-z]*' | sort | uniq -c
5. Emotion data: grep -oh 'arousal: [a-z]*' and 'valence: [a-z]*'
6. Link stats: grep -c '\[\[' per file → orphans (0), hubs (5+)
7. Top linked: grep -roh '\[\[[^]]*' | sort | uniq -c | sort -rn
8. Recent activity: find -mtime -7 | wc -l
9. Dormant: find -mtime +14 -mtime -60
```

## Health Score Calculation

```
base = 50
+ (link_density > 1.5) ? 10 : 0
+ (orphan_rate < 0.3) ? 15 : (orphan_rate < 0.5) ? 5 : 0
+ (has_maturity_tags) ? 10 : 0
+ (emotion_coverage > 0.1) ? 5 : 0
+ (hub_count > 50) ? 10 : (hub_count > 20) ? 5 : 0
- (orphan_rate > 0.6) ? 15 : 0
- (no_recent_activity) ? 10 : 0
```

## HTML Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>/* Tokyo Night theme */</style>
</head>
<body>
    <!-- Header with timestamp -->
    <!-- Grid layout -->
    <!-- Cards: Health score, Total notes, Link density, Graph balance -->
    <!-- Domain bar chart -->
    <!-- Type pie chart (Chart.js) -->
    <!-- Activity timeline (Chart.js) -->
    <!-- Top hubs list -->
    <!-- Maturity breakdown -->
    <!-- Recommendations based on findings -->
</body>
</html>
```

## Output

1. Create `<vault>/_dashboards/` if needed
2. Write `vault-health.html`
3. Report: `✓ Dashboard saved to _dashboards/vault-health.html`
4. Show key metrics summary in chat

## Recommendations Logic

| Condition | Severity | Message |
|-----------|----------|---------|
| orphan_rate > 0.5 | high | Link orphan notes or archive |
| maturity_tags < 10 | medium | Add maturity tags |
| emotion_coverage < 0.05 | medium | Use memorize for emotion capture |
| domain_imbalance > 0.8 | low | Capture from other domains |
| hub_count < 20 | low | Create more MOCs |
