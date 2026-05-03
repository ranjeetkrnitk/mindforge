#!/usr/bin/env python3
"""
graph/link_strength.py — Compute link strength between notes in a vault.

Implements the link strength formula from .agent/skills/memorize/config/settings.md:
  strength = co_occurrence × recency_weight × annotation_bonus

Usage:
    python helpers/graph/link_strength.py --vault /path/to/vault
    python helpers/graph/link_strength.py --vault /path/to/vault --top 20
    python helpers/graph/link_strength.py --vault /path/to/vault --node "CLS Theory"
"""

import re
import json
import math
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Default weights — override with config/settings.md values
DEFAULT_WEIGHTS = {
    "co_occurrence": 1.0,
    "recency_half_life": 14,     # days
    "annotation_bonus": 1.5,
    "backlink_bonus": 1.2,
}

TYPED_LINK_PATTERN = re.compile(
    r"\[\[([^\]]+)\]\]\s*\*\(?(supports|contradicts|extends|recalls|derived-from|questions|answers)\)?\*"
)
BARE_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
DATE_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})")


def extract_date(content: str, path: Path) -> datetime | None:
    """Try to extract a date from frontmatter or filename."""
    match = DATE_PATTERN.search(path.stem)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    match = re.search(r"created:\s*(\d{4}-\d{2}-\d{2})", content)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    return None


def recency_weight(note_date: datetime | None, half_life_days: int) -> float:
    """Exponential decay — recent links count more."""
    if note_date is None:
        return 0.5  # unknown date → neutral weight
    age_days = (datetime.now() - note_date).days
    return math.exp(-math.log(2) * age_days / half_life_days)


def build_link_graph(vault_path: str, weights: dict) -> dict:
    vault = Path(vault_path)
    edges = defaultdict(lambda: {"strength": 0.0, "typed": False, "bidirectional": False})
    all_links = defaultdict(set)  # note → set of notes it links to

    for md_file in vault.rglob("*.md"):
        if any(p in str(md_file) for p in ["_system", ".obsidian", "_archived"]):
            continue

        content = md_file.read_text(encoding="utf-8", errors="ignore")
        source = md_file.stem
        note_date = extract_date(content, md_file)
        r_weight = recency_weight(note_date, weights["recency_half_life"])

        # Find typed links (annotated)
        typed_links = set()
        for match in TYPED_LINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            typed_links.add(target)
            key = tuple(sorted([source, target]))
            edges[key]["strength"] += weights["co_occurrence"] * r_weight * weights["annotation_bonus"]
            edges[key]["typed"] = True
            all_links[source].add(target)

        # Find bare links
        for match in BARE_LINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            if target in typed_links:
                continue  # already counted
            key = tuple(sorted([source, target]))
            edges[key]["strength"] += weights["co_occurrence"] * r_weight
            all_links[source].add(target)

    # Apply backlink bonus for bidirectional links
    for key in edges:
        a, b = key
        if b in all_links.get(a, set()) and a in all_links.get(b, set()):
            edges[key]["strength"] *= weights["backlink_bonus"]
            edges[key]["bidirectional"] = True

    return {
        "edges": [
            {
                "source": k[0],
                "target": k[1],
                "strength": round(v["strength"], 4),
                "typed": v["typed"],
                "bidirectional": v["bidirectional"],
            }
            for k, v in edges.items()
        ],
        "node_count": len(set(n for k in edges for n in k)),
        "edge_count": len(edges),
    }


def main():
    parser = argparse.ArgumentParser(description="Compute link strength in a vault")
    parser.add_argument("--vault", required=True, help="Path to vault root")
    parser.add_argument("--top", type=int, default=10, help="Show top N strongest links")
    parser.add_argument("--node", help="Show links for a specific note")
    parser.add_argument("--output", help="Write full graph to JSON file")
    args = parser.parse_args()

    graph = build_link_graph(args.vault, DEFAULT_WEIGHTS)
    edges = sorted(graph["edges"], key=lambda e: e["strength"], reverse=True)

    if args.node:
        edges = [e for e in edges if args.node in (e["source"], e["target"])]
        print(f"\n🔗 Links for: {args.node}\n")
    else:
        print(f"\n🔗 Top {args.top} strongest links\n")
        edges = edges[:args.top]

    for e in edges:
        badge = "↔" if e["bidirectional"] else "→"
        typed = "✦" if e["typed"] else " "
        print(f"  {typed} {e['source']} {badge} {e['target']}  [{e['strength']:.3f}]")

    print(f"\n  Nodes: {graph['node_count']}  Edges: {graph['edge_count']}")
    print(f"  ✦ = typed link   ↔ = bidirectional\n")

    if args.output:
        Path(args.output).write_text(json.dumps(graph, indent=2))
        print(f"✅ Graph written to {args.output}")


if __name__ == "__main__":
    main()
