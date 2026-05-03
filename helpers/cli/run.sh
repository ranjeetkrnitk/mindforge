#!/usr/bin/env bash
# run.sh — Universal entry point for all .agent skills, agents, plugins
#
# Usage:
#   ./helpers/cli/run.sh skill memorize capture "I learned X"
#   ./helpers/cli/run.sh skill memorize consolidate
#   ./helpers/cli/run.sh skill memorize remap --dry-run
#   ./helpers/cli/run.sh agent <agent-name>
#   ./helpers/cli/run.sh plugin <plugin-name>

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENT_DIR="$REPO_ROOT/.agent"

CATEGORY="${1:-}"
NAME="${2:-}"
MODE="${3:-}"
INPUT="${4:-}"

usage() {
  echo "Usage: $0 <category> <name> [mode] [input]"
  echo ""
  echo "Categories:"
  echo "  skill   — run a skill"
  echo "  agent   — load an agent"
  echo "  plugin  — inject a plugin"
  echo ""
  echo "Examples:"
  echo "  $0 skill memorize capture 'I learned that X causes Y'"
  echo "  $0 skill memorize consolidate"
  echo "  $0 skill memorize remap --dry-run"
  echo "  $0 agent researcher"
  echo "  $0 plugin concise-output"
  exit 1
}

[[ -z "$CATEGORY" || -z "$NAME" ]] && usage

case "$CATEGORY" in
  skill)
    SKILL_DIR="$AGENT_DIR/skills/$NAME"
    SKILL_MD="$SKILL_DIR/SKILL.md"

    if [[ ! -f "$SKILL_MD" ]]; then
      echo "❌ Skill '$NAME' not found at $SKILL_MD"
      exit 1
    fi

    echo "🧠 Loading skill: $NAME"
    echo "📄 Mode: ${MODE:-default}"
    [[ -n "$INPUT" ]] && echo "💬 Input: $INPUT"
    echo ""
    echo "--- SKILL.md ---"
    cat "$SKILL_MD"

    if [[ -n "$MODE" && -f "$SKILL_DIR/prompts/$MODE.md" ]]; then
      echo ""
      echo "--- prompts/$MODE.md ---"
      cat "$SKILL_DIR/prompts/$MODE.md"
    fi
    ;;

  agent)
    AGENT_DIR_PATH="$AGENT_DIR/agents/$NAME"
    if [[ ! -d "$AGENT_DIR_PATH" ]]; then
      echo "❌ Agent '$NAME' not found at $AGENT_DIR_PATH"
      exit 1
    fi
    echo "🤖 Loading agent: $NAME"
    cat "$AGENT_DIR_PATH/AGENT.md"
    ;;

  plugin)
    PLUGIN_DIR="$AGENT_DIR/plugins/$NAME"
    if [[ ! -d "$PLUGIN_DIR" ]]; then
      echo "❌ Plugin '$NAME' not found at $PLUGIN_DIR"
      exit 1
    fi
    echo "🔌 Loading plugin: $NAME"
    cat "$PLUGIN_DIR/inject.md"
    ;;

  *)
    echo "❌ Unknown category: $CATEGORY"
    usage
    ;;
esac
