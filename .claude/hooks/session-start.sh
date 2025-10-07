#!/bin/bash
# Session Start Hook
# This hook runs when a new Claude Code session starts.
# It loads recent coaching session memories into claude.md

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python script to update claude.md with recent memories
python3 "$SCRIPT_DIR/load-memory.py"
