#!/usr/bin/env python3
"""
vault/audit.py — Scan an Obsidian vault and extract structured metadata.

Usage:
    python helpers/vault/audit.py --vault /path/to/vault
    python helpers/vault/audit.py --vault /path/to/vault --output report.json
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Install pyyaml: pip install pyyaml")
    raise


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def extract_wikilinks(content: str) -> list[str]:
    """Extract all [[wikilinks]] from content."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def extract_tags(content: str, frontmatter: dict) -> list[str]:
    """Collect tags from frontmatter and inline #tags."""
    tags = list(frontmatter.get("tags", []))
    inline = re.findall(r"(?<!\[)#([\w/\-]+)", content)
    return list(set(tags + inline))


def detect_node_type(path: Path, frontmatter: dict, title: str) -> str:
    """Infer node type from filename, path, and frontmatter."""
    if "type" in frontmatter:
        return frontmatter["type"]
    if re.match(r"^\d{4}-\d{2}-\d{2}", title):
        return "episode"
    if title.endswith("?"):
        return "question"
    if title.endswith("MOC"):
        return "moc"
    if re.search(r"\d{4}", title) and " — " in title:
        return "source"
    if "people" in str(path):
        return "person"
    return "concept"


def detect_maturity(frontmatter: dict, link_count: int) -> str:
    """Infer maturity from frontmatter and link count."""
    if "maturity" in frontmatter:
        return frontmatter["maturity"]
    if link_count == 0:
        return "fleeting"
    if link_count <= 2:
        return "developing"
    return "evergreen"


def audit_vault(vault_path: str) -> dict:
    vault = Path(vault_path)
    if not vault.exists():
        raise FileNotFoundError(f"Vault not found: {vault_path}")

    files = []
    for md_file in vault.rglob("*.md"):
        # Skip system folders
        if any(p in str(md_file) for p in ["_system", ".obsidian", "_archived"]):
            continue

        content = md_file.read_text(encoding="utf-8", errors="ignore")
        frontmatter = extract_frontmatter(content)
        links = extract_wikilinks(content)
        tags = extract_tags(content, frontmatter)
        title = frontmatter.get("title", md_file.stem)
        node_type = detect_node_type(md_file, frontmatter, title)
        maturity = detect_maturity(frontmatter, len(links))
        word_count = len(content.split())

        files.append({
            "path": str(md_file.relative_to(vault)),
            "title": title,
            "type": node_type,
            "maturity": maturity,
            "tags": tags,
            "links": links,
            "link_count": len(links),
            "word_count": word_count,
            "has_frontmatter": bool(frontmatter),
        })

    # Summary stats
    types = {}
    maturities = {}
    for f in files:
        types[f["type"]] = types.get(f["type"], 0) + 1
        maturities[f["maturity"]] = maturities.get(f["maturity"], 0) + 1

    islands = [f["path"] for f in files if f["link_count"] == 0]

    return {
        "audited_at": datetime.now().isoformat(),
        "vault": vault_path,
        "total_files": len(files),
        "by_type": types,
        "by_maturity": maturities,
        "islands": islands,
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description="Audit an Obsidian vault")
    parser.add_argument("--vault", required=True, help="Path to vault root")
    parser.add_argument("--output", help="Output JSON file (default: stdout)")
    parser.add_argument("--islands-only", action="store_true",
                        help="Only show unlinked (island) notes")
    args = parser.parse_args()

    report = audit_vault(args.vault)

    if args.islands_only:
        output = {
            "islands": report["islands"],
            "count": len(report["islands"])
        }
    else:
        output = report

    json_out = json.dumps(output, indent=2)

    if args.output:
        Path(args.output).write_text(json_out)
        print(f"✅ Report written to {args.output}")
        print(f"   {report['total_files']} files scanned")
        print(f"   {len(report['islands'])} island notes (no links)")
    else:
        print(json_out)


if __name__ == "__main__":
    main()
