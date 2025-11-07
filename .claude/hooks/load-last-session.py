#!/usr/bin/env python3
"""
Load the most recent session notes and inject into context.
Runs on every user prompt submission via UserPromptSubmit hook.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Project root is parent of .claude directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
SESSIONS_DIR = PROJECT_ROOT / "Sessions"

def find_latest_session():
    """Find the most recent session markdown file."""
    if not SESSIONS_DIR.exists():
        return None

    session_files = sorted(
        SESSIONS_DIR.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return session_files[0] if session_files else None

def extract_session_content(filepath):
    """Extract content from the latest session."""
    content = filepath.read_text()

    # Return full content (will be trimmed by Claude if too long)
    return content

def main():
    # Read hook input (required but we don't use it for this hook)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Silently fail if input is malformed
        sys.exit(0)

    # Find latest session
    latest_session = find_latest_session()

    if not latest_session:
        # No sessions yet, silently continue
        sys.exit(0)

    # Check if session is recent (within last 7 days)
    mtime = datetime.fromtimestamp(latest_session.stat().st_mtime)
    days_old = (datetime.now() - mtime).days

    if days_old > 7:
        # Session too old, don't auto-load
        sys.exit(0)

    # Extract content
    session_content = extract_session_content(latest_session)

    # Output context via stdout
    print(f"📋 Last Session Context: {latest_session.name}")
    print("=" * 60)
    print(session_content)
    print("=" * 60)
    print()

    sys.exit(0)

if __name__ == "__main__":
    main()
