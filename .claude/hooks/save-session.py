#!/usr/bin/env python3
"""
Save a coaching session to the memory system.
This script is called by the session-end hook and can also be run manually.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Project root is the parent of .claude directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
SESSIONS_DIR = PROJECT_ROOT / "coaching-sessions" / "sessions"
INDEX_FILE = PROJECT_ROOT / "coaching-sessions" / "index.json"


def save_session(topic, conversation, insights, tags):
    """
    Save a coaching session to disk and update the index.

    Args:
        topic: Short description of the session topic
        conversation: Full conversation text
        insights: Key insights or takeaways
        tags: List of tags/keywords
    """
    # Generate filename with date and topic
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.replace(" ", "-").replace("/", "-")[:50]
    filename = f"{date_str}-{safe_topic}.md"
    filepath = SESSIONS_DIR / filename

    # Create session markdown file
    session_content = f"""# {topic}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Tags:** {", ".join(tags)}

## Key Insights
{insights}

## Conversation
{conversation}
"""

    # Write session file
    filepath.write_text(session_content)

    # Update index
    if INDEX_FILE.exists():
        index_data = json.loads(INDEX_FILE.read_text())
    else:
        index_data = {"sessions": [], "metadata": {"created": date_str, "total_sessions": 0}}

    # Add session to index
    session_entry = {
        "date": date_str,
        "topic": topic,
        "filename": filename,
        "tags": tags,
        "timestamp": datetime.now().isoformat()
    }
    index_data["sessions"].insert(0, session_entry)  # Most recent first
    index_data["metadata"]["last_updated"] = date_str
    index_data["metadata"]["total_sessions"] = len(index_data["sessions"])

    # Save updated index
    INDEX_FILE.write_text(json.dumps(index_data, indent=2))

    print(f"✅ Session saved: {filename}")
    return filepath


def interactive_save():
    """Interactive mode for manually saving a session."""
    print("\n=== Save Coaching Session ===\n")

    topic = input("Session topic: ").strip()
    if not topic:
        print("❌ Topic is required")
        return

    print("\nEnter conversation (end with Ctrl+D on macOS/Linux or Ctrl+Z on Windows):")
    conversation_lines = []
    try:
        while True:
            line = input()
            conversation_lines.append(line)
    except EOFError:
        pass

    conversation = "\n".join(conversation_lines).strip()
    if not conversation:
        print("❌ Conversation is required")
        return

    insights = input("\nKey insights (optional): ").strip() or "No specific insights recorded."

    tags_input = input("Tags (comma-separated): ").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else ["general"]

    # Save the session
    filepath = save_session(topic, conversation, insights, tags)
    print(f"\n✅ Session saved successfully!")
    print(f"📄 File: {filepath}")


if __name__ == "__main__":
    # Check if called with arguments (from hook) or interactive
    if len(sys.argv) > 1:
        # Called with arguments - parse them
        if sys.argv[1] == "--topic" and len(sys.argv) >= 3:
            topic = sys.argv[2]
            conversation = sys.argv[3] if len(sys.argv) > 3 else ""
            insights = sys.argv[4] if len(sys.argv) > 4 else "No specific insights recorded."
            tags = sys.argv[5].split(",") if len(sys.argv) > 5 else ["general"]
            save_session(topic, conversation, insights, tags)
        else:
            print("Usage: save-session.py --topic <topic> [conversation] [insights] [tags]")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_save()
