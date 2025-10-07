#!/usr/bin/env python3
"""
Search through coaching session memories.
Find sessions by keyword, date, or tag.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SESSIONS_DIR = PROJECT_ROOT / "coaching-sessions" / "sessions"
INDEX_FILE = PROJECT_ROOT / "coaching-sessions" / "index.json"


def load_index():
    """Load the session index."""
    if not INDEX_FILE.exists():
        print("❌ No sessions found. Index file does not exist.")
        return None
    return json.loads(INDEX_FILE.read_text())


def search_by_keyword(keyword, sessions):
    """Search sessions by keyword in topic or content."""
    results = []
    keyword_lower = keyword.lower()

    for session in sessions:
        # Check if keyword is in topic
        if keyword_lower in session["topic"].lower():
            results.append(session)
            continue

        # Check if keyword is in session content
        filepath = SESSIONS_DIR / session["filename"]
        if filepath.exists():
            content = filepath.read_text().lower()
            if keyword_lower in content:
                results.append(session)

    return results


def search_by_tag(tag, sessions):
    """Search sessions by tag."""
    tag_lower = tag.lower()
    return [s for s in sessions if tag_lower in [t.lower() for t in s.get("tags", [])]]


def search_by_date(date_str, sessions):
    """Search sessions by date (YYYY-MM-DD)."""
    return [s for s in sessions if s["date"] == date_str]


def display_results(results):
    """Display search results."""
    if not results:
        print("\n❌ No sessions found matching your criteria.\n")
        return

    print(f"\n📚 Found {len(results)} session(s):\n")
    print("=" * 80)

    for i, session in enumerate(results, 1):
        print(f"\n{i}. {session['topic']}")
        print(f"   Date: {session['date']}")
        print(f"   Tags: {', '.join(session['tags'])}")
        print(f"   File: coaching-sessions/sessions/{session['filename']}")

    print("\n" + "=" * 80)
    print("\nTo read a full session, use: cat coaching-sessions/sessions/<filename>\n")


def list_all_tags(sessions):
    """List all unique tags."""
    all_tags = set()
    for session in sessions:
        all_tags.update(session.get("tags", []))

    if not all_tags:
        print("\n❌ No tags found.\n")
        return

    print("\n📋 All tags:")
    for tag in sorted(all_tags):
        count = sum(1 for s in sessions if tag in s.get("tags", []))
        print(f"  • {tag} ({count} session{'s' if count != 1 else ''})")
    print()


def interactive_search():
    """Interactive search mode."""
    index_data = load_index()
    if not index_data:
        return

    sessions = index_data["sessions"]
    total = len(sessions)

    print("\n" + "=" * 80)
    print("  COACHING SESSION SEARCH")
    print("=" * 80)
    print(f"\nTotal sessions: {total}")

    if total == 0:
        print("\n❌ No sessions recorded yet.\n")
        return

    print("\nSearch options:")
    print("  1. Search by keyword")
    print("  2. Search by tag")
    print("  3. Search by date (YYYY-MM-DD)")
    print("  4. List all tags")
    print("  5. Show all sessions")
    print("  6. Exit")

    choice = input("\nEnter your choice (1-6): ").strip()

    if choice == "1":
        keyword = input("Enter keyword: ").strip()
        results = search_by_keyword(keyword, sessions)
        display_results(results)

    elif choice == "2":
        keyword = input("Enter tag: ").strip()
        results = search_by_tag(keyword, sessions)
        display_results(results)

    elif choice == "3":
        date = input("Enter date (YYYY-MM-DD): ").strip()
        results = search_by_date(date, sessions)
        display_results(results)

    elif choice == "4":
        list_all_tags(sessions)

    elif choice == "5":
        display_results(sessions)

    elif choice == "6":
        print("\n👋 Goodbye!\n")
        return

    else:
        print("\n❌ Invalid choice.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command-line mode
        index_data = load_index()
        if not index_data:
            sys.exit(1)

        sessions = index_data["sessions"]

        if sys.argv[1] == "--keyword" and len(sys.argv) > 2:
            results = search_by_keyword(sys.argv[2], sessions)
            display_results(results)
        elif sys.argv[1] == "--tag" and len(sys.argv) > 2:
            results = search_by_tag(sys.argv[2], sessions)
            display_results(results)
        elif sys.argv[1] == "--date" and len(sys.argv) > 2:
            results = search_by_date(sys.argv[2], sessions)
            display_results(results)
        elif sys.argv[1] == "--tags":
            list_all_tags(sessions)
        elif sys.argv[1] == "--all":
            display_results(sessions)
        else:
            print("Usage:")
            print("  search-sessions.py --keyword <word>")
            print("  search-sessions.py --tag <tag>")
            print("  search-sessions.py --date <YYYY-MM-DD>")
            print("  search-sessions.py --tags")
            print("  search-sessions.py --all")
            print("  search-sessions.py  (interactive mode)")
    else:
        # Interactive mode
        interactive_search()
