#!/bin/bash
# Session End Hook
# This hook runs when a Claude Code session ends.
# It prompts the user to save the coaching session.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "════════════════════════════════════════════"
echo "  Coaching Session Complete"
echo "════════════════════════════════════════════"
echo ""
echo "Would you like to save this coaching session to memory? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running interactive session save..."
    python3 "$SCRIPT_DIR/save-session.py"
else
    echo "Session not saved. You can save it later by running:"
    echo "  python3 .claude/hooks/save-session.py"
fi

echo ""
