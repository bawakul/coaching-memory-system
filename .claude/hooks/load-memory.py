#!/usr/bin/env python3
"""
Load coaching session memories and update claude.md context file.
This script is called by the session-start hook.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# Project root is the parent of .claude directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
SESSIONS_DIR = PROJECT_ROOT / "coaching-sessions" / "sessions"
INDEX_FILE = PROJECT_ROOT / "coaching-sessions" / "index.json"
CLAUDE_MD = PROJECT_ROOT / ".claude" / "claude.md"


def load_recent_sessions(limit=5):
    """Load the most recent sessions from the index."""
    if not INDEX_FILE.exists():
        return []

    index_data = json.loads(INDEX_FILE.read_text())
    return index_data["sessions"][:limit]


def extract_session_summary(filepath):
    """Extract key information from a session file."""
    if not filepath.exists():
        return None

    content = filepath.read_text()
    lines = content.split("\n")

    # Extract insights section
    insights = []
    in_insights = False
    for line in lines:
        if line.startswith("## Key Insights"):
            in_insights = True
            continue
        if in_insights and line.startswith("##"):
            break
        if in_insights and line.strip():
            insights.append(line)

    return "\n".join(insights).strip() if insights else "No specific insights recorded."


def collect_all_tags():
    """Collect all unique tags from sessions to identify themes."""
    if not INDEX_FILE.exists():
        return []

    index_data = json.loads(INDEX_FILE.read_text())
    all_tags = set()
    for session in index_data["sessions"]:
        all_tags.update(session.get("tags", []))

    return sorted(list(all_tags))


def update_claude_md():
    """Update the claude.md file with recent session context."""
    recent_sessions = load_recent_sessions(limit=5)
    all_tags = collect_all_tags()

    # Build recent sessions summary
    sessions_summary = ""
    if recent_sessions:
        sessions_summary = "### Most Recent Sessions:\n\n"
        for session in recent_sessions:
            filepath = SESSIONS_DIR / session["filename"]
            insights = extract_session_summary(filepath)
            sessions_summary += f"**{session['date']}** - {session['topic']}\n"
            sessions_summary += f"*Tags: {', '.join(session['tags'])}*\n"
            if insights and insights != "No specific insights recorded.":
                sessions_summary += f"{insights}\n"
            sessions_summary += "\n"
    else:
        sessions_summary = "*No previous sessions recorded yet. This is a fresh start!*\n"

    # Build themes section
    themes_section = ""
    if all_tags:
        themes_section = f"*Active themes: {', '.join(all_tags)}*\n"
    else:
        themes_section = "*To be populated from coaching sessions*\n"

    # Create updated claude.md content
    claude_md_content = f"""# Life Coaching Context

You are acting as a life coach for this user. This file contains memories and context from previous coaching sessions to maintain continuity across conversations.

## Coaching Role
- Listen actively and ask thoughtful questions
- Help identify patterns, goals, and obstacles
- Provide support and accountability
- Remember previous discussions and progress

## Recent Sessions Summary
(This section is automatically updated at the start of each session)

{sessions_summary}

## Ongoing Goals & Themes

{themes_section}

## Key Insights & Patterns

Review the recent sessions above to identify recurring patterns, progress on goals, and areas that may need attention in today's session.

---

*Note: This context file is automatically updated at the start of each session with relevant memories from past conversations.*
*Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""

    # Write updated content
    CLAUDE_MD.write_text(claude_md_content)
    print(f"✅ Updated claude.md with context from {len(recent_sessions)} recent sessions")


if __name__ == "__main__":
    update_claude_md()
